from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Deposit, Withdraw


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ("username", "first_name","last_name", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.account_balance = 0
		if commit:
			user.save()
		return user
		
class DepositForm(forms.ModelForm):

	class Meta:
		model = Deposit
		fields = ("amount",)

class WithdrawForm(forms.ModelForm):

	class Meta:
		model = Withdraw
		fields = ("amount",)
		
class PayPalPaymentsForm(forms.Form):
    """ A dummy hidden form for PayPal Checkout with just order_id field """
    order_id = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # assign HiddenInput widget      
        self.fields['order_id'].widget = forms.HiddenInput()