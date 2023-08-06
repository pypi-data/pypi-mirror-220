from posthog import Posthog
import os

posthog = Posthog('phc_YpKoFD7smPe4SXRtVyMW766uP9AjUwnuRJ8hh2EJcVv',
                  host='https://app.posthog.com')


def capture_event(event_name, event_properties):
    print("inside function", os.environ.get('EVENT_CAPTURE'))
    print(os.environ.get('EVENT_CAPTURE') == "disable")
    if not os.environ.get('EVENT_CAPTURE') == "disable":
        posthog.capture("not_distinct", event_name, event_properties)