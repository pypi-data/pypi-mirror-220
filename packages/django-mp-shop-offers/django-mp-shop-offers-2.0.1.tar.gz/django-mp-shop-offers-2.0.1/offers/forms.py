
from django import forms
from django.utils.translation import gettext_lazy as _

from captcha.fields import ReCaptchaField

from offers.models import ProductPriceOffer


class ProductPriceOfferForm(forms.ModelForm):

    captcha = ReCaptchaField()

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if mobile.startswith('+3800'):
            raise forms.ValidationError(
                _('Phone number could not start with `+3800`'))
        return mobile

    class Meta:
        model = ProductPriceOffer
        fields = ('name', 'mobile', 'email', 'text', )
