from django.core.management.base import BaseCommand

from catalog.models import AdditionalOption, Product, ProductColorOption
from catalog.seed_data import DEFAULT_ADDITIONAL_OPTIONS, DEFAULT_PRODUCTS


class Command(BaseCommand):
    help = 'Carga adicionales y productos base para el catálogo.'

    def handle(self, *args, **options):
        additional_objects = []
        for item in DEFAULT_ADDITIONAL_OPTIONS:
            option, _ = AdditionalOption.objects.update_or_create(
                name=item['name'],
                defaults=item,
            )
            additional_objects.append(option)

        for product_item in DEFAULT_PRODUCTS:
            colors = product_item['colors']
            defaults = {key: value for key, value in product_item.items() if key != 'colors'}
            defaults.setdefault('category', 'limpiapipas')
            product, _ = Product.objects.update_or_create(
                name=product_item['name'],
                defaults=defaults,
            )
            product.additional_options.set(additional_objects)
            product.color_options.all().delete()
            ProductColorOption.objects.bulk_create(
                [
                    ProductColorOption(product=product, name=color, display_order=index)
                    for index, color in enumerate(colors)
                ]
            )

        self.stdout.write(self.style.SUCCESS('Catálogo base cargado correctamente.'))
