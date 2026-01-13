from celery import shared_task
from .models import AutomationRule, MessageTemplate
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def process_automation_logic(event_code, app_label, model_name, object_id):
    """
    This runs in the background.
    """
    try:
        # 1. RE-HYDRATE THE OBJECT (Fetch from DB)
        # We use apps.get_model to turn string 'tasks.Task' into the actual Class
        ModelClass = apps.get_model(app_label=app_label, model_name=model_name)
        trigger_object = ModelClass.objects.get(id=object_id)
        
        print(f"⚙️ Worker: Processing {event_code} for {trigger_object}")

        # 2. FIND RULES (The logic we discussed earlier)
        # Find rules matching this event code
        rules = AutomationRule.objects.filter(event__code=event_code)
        
        # 3. EXECUTE EACH RULE
        for rule in rules:
            # A. Resolve Recipients (This can be a complex function)
            # We pass the trigger_object so we can find the project owner, etc.
            recipients = resolve_recipients(rule.recipients, trigger_object)
            
            # B. Loop through channels
            for channel in rule.channels:
                # C. Find/Render Template
                subject, body = render_template(event_code, channel, trigger_object)
                
                # D. Send (Delivery)
                deliver_message(channel, recipients, subject, body)

    except ModelClass.DoesNotExist:
        print(f"❌ Error: Object {model_name} #{object_id} was deleted before we could process it.")
    except Exception as e:
        print(f"❌ Automation Error: {e}")

# ==========================================
# HELPER FUNCTIONS (Keep task clean)
# ==========================================

def resolve_recipients(roles_list, trigger_object):
    """
    Converts ['ADMIN', 'SUPERVISOR','MEMBER'] into actual email addresses.
    """
    emails = set() # to avoid duplicates
    
    # # Example logic:
    # if 'OWNER' in roles_list and hasattr(trigger_object, 'owner'):
    #     emails.add(trigger_object.owner.email)
        
    # if 'PROJECT_MANAGER' in roles_list:
    #     # Assuming trigger_object has a way to get to project
    #     # e.g. Task -> Project -> Manager
    #     if hasattr(trigger_object, 'project'):
    #         emails.add(trigger_object.project.manager.email)
            
    return list(emails)

def render_template(event_code, channel, trigger_object):
    # 1. Fetch Template from DB
    try:
        tpl = MessageTemplate.objects.get(event__code=event_code, channel=channel)
    except MessageTemplate.DoesNotExist:
        # Fallback to 'ALL'
        tpl = MessageTemplate.objects.get(event__code=event_code, channel='ALL')

    # 2. Create Context (The data available for {{ placeholders }})
    context = {
        'id': trigger_object.id,
        'name': getattr(trigger_object, 'name', str(trigger_object)),
        # Add more context variables here...
    }

    # 3. Simple Replace (Or use Jinja2/Django Templates)
    subject = tpl.subject_template
    body = tpl.body_template
    
    for key, val in context.items():
        placeholder = f"{{{{ {key} }}}}" # {{ name }}
        subject = subject.replace(placeholder, str(val))
        body = body.replace(placeholder, str(val))
        
    return subject, body

def deliver_message(channel, recipients, subject, body):
    if not recipients:
        return

    if channel == 'EMAIL':
        print(f"📧 Sending Email to {recipients}: {subject}")
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
    elif channel == 'SLACK':
        print(f"💬 Sending Slack: {body}")
        # Slack logic here...