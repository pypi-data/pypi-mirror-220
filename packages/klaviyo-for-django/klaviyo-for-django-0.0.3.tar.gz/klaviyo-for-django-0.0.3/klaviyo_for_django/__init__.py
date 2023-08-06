from klaviyo_api import KlaviyoAPI

from django.conf import settings

klaviyo = KlaviyoAPI(
    settings.KLAVIYO_PRIVATE_API_KEY, max_delay=60, max_retries=3, test_host=None
)


def send_event(
    email: str,
    event_name: str,
    event_properties: dict = {},
    profile_properties: dict = {},
):
    payload = {
        "data": {
            "type": "event",
            "attributes": {
                "properties": event_properties,
                "metric": {
                    "data": {"type": "metric", "attributes": {"name": event_name}}
                },
                "profile": {
                    "data": {
                        "type": "profile",
                        "attributes": {"properties": {"email": email}},
                        "meta": {"patch_properties": {"append": profile_properties}},
                    }
                },
            },
        }
    }
    klaviyo.Events.create_event(payload)
