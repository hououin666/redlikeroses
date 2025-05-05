

from django import forms

from main.models import Color, Size, MetalType, ProductVariation

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    color = forms.ModelChoiceField(queryset = Color.objects.none(),required=False)
    size = forms.ModelChoiceField(queryset=Size.objects.none(), required=False)
    metal_type = forms.ModelChoiceField(queryset=MetalType.objects.none(), required=False)


    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        if product:
            variations = ProductVariation.objects.filter(product=product)

            if variations.exists():
                self.fields['color'].queryset = Color.objects.filter(
                    id__in=variations.exclude(color=None).values_list('color', flat=True).distinct()
                )
                self.fields['size'].queryset = Size.objects.filter(
                    id__in=variations.exclude(size=None).values_list('size',flat=True).distinct()
                )
                self.fields['metal_type'].queryset = MetalType.objects.filter(
                    id__in=variations.exclude(metal_type=None).values_list('metal_type', flat=True).distinct()
                )



