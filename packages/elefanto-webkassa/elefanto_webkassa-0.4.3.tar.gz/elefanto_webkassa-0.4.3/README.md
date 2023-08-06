about
=====
# [Home page](https://github.com/elefanto-organization/elefanto-webkassa)
integration with [webkassa.kz](https://webkassa.kz)

This package developed for Elefantoteam, for using in future projects

# For contributors

**NOTE:** After clone this repository you should run command:

   ```bash
   chmod ug+x.githooks/pre-commit
   ```

   ```bash
   git config core.hooksPath .githooks
   ````

# For users

setup
=====
install via pip:

  ```bash
  pip install elefanto-webkassa
  ```

install via poetry:

  ```bash
  poetry add elefanto-webkassa
  ```

Configs
===
add it to installed apps in django settings.py:

```python
INSTALLED_APPS = (
    ...,
    'webkassa',
)
```

now add this to your settings.py:

```python
WEBKASSA_CONFIG = {
    'api_key': 'YOUR_WEBKASSA_API_KEY',
    'encryption_key': 'SOME_ECRYPTION_KEY',
    'url': 'WEBKASSA_API_URL',
}
```

***Note***
you can generate `encryption_key` by this command in python shell

```python
import base64
import os

base64.urlsafe_b64encode(os.urandom(32))
```

Usage
===
after configure project, you should run `migrate`

```python
python manage.py migrate
```

then go to admin page, find `Webkassa accounts` in `WEBKASSA` app and add new account
![img.png](https://dl.dropboxusercontent.com/s/fdrkqpvk73sf6m4/Screenshot%20from%202023-07-20%2014-18-17.png?dl=0)

now you can use package

```python
from webkassa.services.manager import WebKassaManager

...

data = {
    'OperationType': int,
    'Positions': [
        {
            'Count': int,
            'Price': float,
            'TaxPercent': int,
            'TaxType': int,
            'PositionName': str,
            'PositionCode': str,
            'Discount': int,
            'Markup': int,
            'SectionCode': str,
            'UnitCode': int,
            ...    
        }
    ],
    'Payments': [
        {
            'Sum': float,
            'PaymentType': int
        }
    ],
    'TicketModifiers': [
        {
            'Sum': int,
            'Text': str,
            'Type': int,
            'TaxType': int,
            'TaxPercent': int,
            'Tax': float
        }
    ],
    'Change': int,
    'RoundType': int,
    'CustomerEmail': str,
    'ExternalOrderNumber': str,
    'ExternalCheckNumber': str,
    ...
}

manager = WebKassaManager(email='<Account email>', cashbox_unique_number='<Cashbox number>')
ticket = manager.get_check(data)
```
`ticket` is instance of `webkassa.models.Check`, you can add it as `OneToOneField` on your payment model

**Note** 
`ExternalOrderNumber` should be pk of your payment instance, and will be unique to avoid ticket duplicates


You can find list of tickets from admin page `Checks` in `WEBKASSA`
![img.png](https://dl.dropboxusercontent.com/s/klsng5wb6sm14qb/Screenshot%20from%202023-07-20%2014-34-39.png?dl=0)


Also you can find error logs for integration. If for some reason error depends on package functionality please tell Джони ага 😜 or give him solution.
