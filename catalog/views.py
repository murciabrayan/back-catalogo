from rest_framework import generics, parsers, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import AdditionalOption, Product
from .permissions import IsAdminPanelUser
from .serializers import (
    AdditionalOptionSerializer,
    AdminLoginSerializer,
    AdminPasswordChangeSerializer,
    AdminProductSerializer,
    PublicProductSerializer,
)


class PublicProductListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicProductSerializer

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .prefetch_related('color_options', 'additional_options')
            .order_by('display_order', 'name')
        )


class AdminLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = AdminLoginSerializer


class AdminMeView(APIView):
    permission_classes = [IsAdminPanelUser]

    def get(self, request):
        return Response(
            {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'is_staff': request.user.is_staff,
            }
        )


class AdminPasswordChangeView(APIView):
    permission_classes = [IsAdminPanelUser]

    def post(self, request):
        serializer = AdminPasswordChangeSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        return Response({'detail': 'Contraseña actualizada correctamente.'})


class AdditionalOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminPanelUser]
    serializer_class = AdditionalOptionSerializer
    queryset = AdditionalOption.objects.all().order_by('display_order', 'name')


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminPanelUser]
    serializer_class = AdminProductSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_queryset(self):
        return Product.objects.prefetch_related('color_options', 'additional_options').order_by(
            'display_order',
            'name',
        )


class AdminDashboardView(APIView):
    permission_classes = [IsAdminPanelUser]

    def get(self, request):
        products = Product.objects.prefetch_related('color_options', 'additional_options').all()
        additional_options = AdditionalOption.objects.all()

        return Response(
            {
                'products': AdminProductSerializer(
                    products,
                    many=True,
                    context={'request': request},
                ).data,
                'additional_options': AdditionalOptionSerializer(
                    additional_options,
                    many=True,
                ).data,
            },
            status=status.HTTP_200_OK,
        )
