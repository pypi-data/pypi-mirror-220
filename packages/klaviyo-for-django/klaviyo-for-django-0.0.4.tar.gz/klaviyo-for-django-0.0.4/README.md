# klaviyo-for-django

Add your Klaviyo api key to your Django project's settings.py file.

settings.py

```plain
KLAVIYO_PRIVATE_API_KEY='YOUR_PRIVATE_API_KEY_HERE'
```

## Usage

```python
from klaviyo_for_django import send_event

send_event(
    'event_name',
    profile_find={'email':'profile_email@email.com'},
    event_properties={'property_name': 'property_value'},
    profile_properties={'other_property_name': 'other_property_value'}
)
```
