from django.db import models
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator



class CustomUser(AbstractUser, models.Model):
    account_balance = models.FloatField(null=True)
	
class Deposit(models.Model):
	amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD',
	validators=[
            MinMoneyValidator(10),
            MaxMoneyValidator(100000),
        ]
	)
	
class Withdraw(models.Model):
	amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD',
	validators=[
            MinMoneyValidator(20),
            MaxMoneyValidator(100000),
        ]
	)