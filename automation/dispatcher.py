from automation.models import AutomationRule, MessageTemplate
# from automation.utils import get_users_by_role, render, send_to_channel

def notify(event_code, trigger_object):
    # 1. Find the Rule
    # (Simplified: logic to find generic rules or project-specific rules)
    rule = AutomationRule.objects.get(event__code=event_code)

    # 2. Resolve Recipients (The "Admin/PM/Member" logic)
    # users_to_notify = get_users_by_role(rule.recipients, trigger_object.project)

    for channel in rule.channels:
        # 3. Find the Best Template
        # Try to find a specific Email template, fallback to 'ALL'
        try:
            tpl = MessageTemplate.objects.get(event__code=event_code, channel=channel)
        except MessageTemplate.DoesNotExist:
            tpl = MessageTemplate.objects.get(event__code=event_code, channel='ALL')

        # 4. Render & Send using functoin inside tasks.py of celery
        # message = render(tpl.body_template, trigger_object)
        # send_to_channel(channel, users_to_notify, message)
        # send_notification_task.delay(
        #         channel=channel, 
        #         recipients=recipients, 
        #         subject=subject, 
        #         body=body
        #     )