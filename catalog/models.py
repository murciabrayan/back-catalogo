from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AdditionalOption(TimestampedModel):
    class Category(models.TextChoices):
        BOUQUET = 'bouquet', 'Ramo'
        FLOWER = 'flower', 'Flor individual'

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.BOUQUET)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self) -> str:
        return self.name


class Product(TimestampedModel):
    class Category(models.TextChoices):
        LIMPIAPIPAS = 'limpiapipas', 'Limpiapipas'
        DETAILS = 'details', 'Detalles'

    class Accent(models.TextChoices):
        LILA = 'lila', 'Lila'
        GOLD = 'gold', 'Dorado'
        PINK = 'pink', 'Rosa'
        BERRY = 'berry', 'Carmesí'
        BLUE = 'blue', 'Azul'
        MINT = 'mint', 'Menta'

    name = models.CharField(max_length=180)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.LIMPIAPIPAS,
    )
    description = models.TextField(blank=True)
    includes = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    accent = models.CharField(max_length=20, choices=Accent.choices, default=Accent.LILA)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    additional_options = models.ManyToManyField(
        AdditionalOption,
        blank=True,
        related_name='products',
    )

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self) -> str:
        return self.name


class ProductColorOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='color_options')
    name = models.CharField(max_length=80)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        unique_together = ('product', 'name')

    def __str__(self) -> str:
        return f'{self.product.name} - {self.name}'
