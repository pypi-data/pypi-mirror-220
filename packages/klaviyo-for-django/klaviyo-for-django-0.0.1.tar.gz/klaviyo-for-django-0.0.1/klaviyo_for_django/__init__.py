from django.conf import settings


def send_event(email: str, event_name: str, properties={}):
    """
    Sends an event to Klaviyo.
    :param event_name: The name of the event.
    :param customer_properties: A dictionary with the customer properties.
    :param properties: A dictionary with the event properties.
    """
    # api = KlaviyoAPI()
    # api.track(event_name, customer_properties, properties)

    print(settings.DEBUG)
    print(f"Email: {email}")
    print(f"Event: {event_name}")


def profile_update():
    print("Profile update")
