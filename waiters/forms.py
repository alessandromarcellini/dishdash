from django import forms
from api.models import Dish

class OrderItemForm(forms.Form):
    dish = forms.IntegerField()
    quantity = forms.IntegerField()


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(OrderItemForm, self).clean()

        if not self.user:
            raise forms.ValidationError("User isn't specified.")
        if not Dish.objects.filter(menu_section__restaurant=self.user.restaurant):
            raise forms.ValidationError("Dish id doesn't correspond to an existing dish")

        return cleaned_data
