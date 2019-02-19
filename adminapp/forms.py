from django import forms
from accounts.models import Account
from accounts.forms import AccountEditForm
from mainapp.models import Category, Product


class AccountAdminEditForm(AccountEditForm):
    class Meta:
        model = Account
        fields = '__all__'


class CategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='скидка', required=False,
                                  min_value=0, max_value=90, initial=0)

    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(CategoryEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
