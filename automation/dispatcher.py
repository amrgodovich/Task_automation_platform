from automation.models import AutomationRule, MessageTemplate
from .tasks import process_automation_logic

def notify(event_code, trigger_object):
    app_label = trigger_object._meta.app_label
    model_name = trigger_object._meta.model_name
    # object_id = trigger_object.pk

    # print(f"📨 Dispatcher: Queuing logic for {event_code} on {model_name} #{object_id}")

    # process_automation_logic.delay(
    #     event_code=event_code,
    #     app_label=app_label,
    #     model_name=model_name,
    #     object_id=object_id
    # )