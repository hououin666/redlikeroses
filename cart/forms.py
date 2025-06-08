

from django import forms
from django.template.context_processors import request

from main.models import Color, Size, MetalType, ProductVariation

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        if product:
            variations = ProductVariation.objects.filter(product=product)

            if variations.exists():
                # Цвета
                colors = Color.objects.filter(
                    id__in=variations.exclude(color=None).values_list('color', flat=True).distinct()
                )
                if colors.exists():  # Проверяем, есть ли результаты
                    self.fields['color'] = forms.ModelChoiceField(
                        queryset=colors,
                        required=False,
                        label='Цвет'
                    )

                # Размеры
                sizes = Size.objects.filter(
                    id__in=variations.exclude(size=None).values_list('size', flat=True).distinct()
                )
                if sizes.exists():  # Проверяем, есть ли результаты
                    self.fields['size'] = forms.ModelChoiceField(
                        queryset=sizes,
                        required=False,
                    )

                # Типы металлов
                metals = MetalType.objects.filter(
                    id__in=variations.values_list('metal_type', flat=True).distinct()
                )
                if metals.exists():  # Проверяем, есть ли результаты
                    self.fields['metal_type'] = forms.ModelChoiceField(
                        queryset=metals,
                        required=True,
                        label='Metal Type'
                    )

                # self.fields['size'].queryset = Size.objects.filter(
                #     id__in=variations.exclude(size=None).values_list('size',flat=True).distinct()
                # )
                # self.fields['metal_type'].queryset = MetalType.objects.filter(
                #     id__in=variations.exclude(metal_type=None).values_list('metal_type', flat=True).distinct()
                # )



