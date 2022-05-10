# Generated by Django 4.0.4 on 2022-05-02 21:34

from django.db import migrations
import djmoney.models.fields
import djmoney.models.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0004_deposit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='USD', max_digits=10, validators=[djmoney.models.validators.MinMoneyValidator(10), djmoney.models.validators.MaxMoneyValidator(10000)]),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('BRL', 'Brazilian Real'), ('GBP', 'British Pound'), ('CAD', 'Canadian Dollar'), ('CNY', 'Chinese Yuan'), ('CZK', 'Czech Koruna'), ('DKK', 'Danish Krone'), ('EUR', 'Euro'), ('HKD', 'Hong Kong Dollar'), ('HUF', 'Hungarian Forint'), ('ILS', 'Israeli New Shekel'), ('JPY', 'Japanese Yen'), ('MYR', 'Malaysian Ringgit'), ('MXN', 'Mexican Peso'), ('TWD', 'New Taiwan Dollar'), ('NZD', 'New Zealand Dollar'), ('NOK', 'Norwegian Krone'), ('PHP', 'Philippine Peso'), ('PLN', 'Polish Zloty'), ('RUB', 'Russian Ruble'), ('SGD', 'Singapore Dollar'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('THB', 'Thai Baht'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3),
        ),
    ]
