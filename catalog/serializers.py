import json

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import AdditionalOption, Product, ProductColorOption


class FlexibleListField(serializers.ListField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = data.strip()
            if not data:
                data = []
            else:
                data = json.loads(data)
        return super().to_internal_value(data)


class AdditionalOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalOption
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'is_active',
            'display_order',
        ]


class ProductColorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColorOption
        fields = ['id', 'name', 'display_order']


class PublicProductSerializer(serializers.ModelSerializer):
    color_options = serializers.SerializerMethodField()
    additional_options = AdditionalOptionSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'includes',
            'price',
            'accent',
            'image_url',
            'color_options',
            'additional_options',
        ]

    def get_color_options(self, obj):
        return [option.name for option in obj.color_options.all()]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None


class AdminProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    color_options = ProductColorOptionSerializer(many=True, read_only=True)
    color_option_names = FlexibleListField(
        child=serializers.CharField(max_length=80),
        write_only=True,
        required=False,
    )
    additional_option_ids = FlexibleListField(
        child=serializers.IntegerField(min_value=1),
        write_only=True,
        required=False,
    )
    additional_options = AdditionalOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'includes',
            'price',
            'accent',
            'image',
            'image_url',
            'is_active',
            'display_order',
            'color_options',
            'color_option_names',
            'additional_options',
            'additional_option_ids',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def create(self, validated_data):
        color_option_names = validated_data.pop('color_option_names', [])
        additional_option_ids = validated_data.pop('additional_option_ids', [])
        product = Product.objects.create(**validated_data)
        if additional_option_ids:
            product.additional_options.set(
                AdditionalOption.objects.filter(id__in=additional_option_ids)
            )
        self._replace_colors(product, color_option_names)
        return product

    def update(self, instance, validated_data):
        color_option_names = validated_data.pop('color_option_names', None)
        additional_option_ids = validated_data.pop('additional_option_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if additional_option_ids is not None:
            instance.additional_options.set(
                AdditionalOption.objects.filter(id__in=additional_option_ids)
            )

        if color_option_names is not None:
            self._replace_colors(instance, color_option_names)

        return instance

    def _replace_colors(self, product: Product, color_option_names: list[str]):
        product.color_options.all().delete()
        cleaned_names = [name.strip() for name in color_option_names if name.strip()]
        ProductColorOption.objects.bulk_create(
            [
                ProductColorOption(product=product, name=name, display_order=index)
                for index, name in enumerate(cleaned_names)
            ]
        )


class AdminLoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs.get('username'),
            password=attrs.get('password'),
        )

        if not user:
            raise serializers.ValidationError('Usuario o contraseña inválidos.')

        if not user.is_staff:
            raise serializers.ValidationError('Esta cuenta no tiene acceso administrativo.')

        data = super().validate(attrs)
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        }
        return data


class AdminPasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError(
                {'current_password': 'La contraseña actual no es correcta.'}
            )

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': 'Las contraseñas nuevas no coinciden.'}
            )

        return attrs
