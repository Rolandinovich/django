from django import forms
from cartapp.models import Cart
from django import forms


# Форма для получение количества товара для добавления в корзину
class CartQuantityForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('quantity',)

    def __init__(self, *args, **kwargs):
        super(CartQuantityForm, self).__init__(*args, **kwargs)
        field = self.fields['quantity']
        field.widget.attrs['class'] = 'form-control'
        field.widget.attrs['type'] = 'number'
        field.widget.attrs['min'] = 1
        field.help_text = ''


