from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task, Milestone, Comments
from projects.models import Project
from .dispatcher import notify 

# =======================================================
# 1. THE REGISTRY (Configuration)
# Map Models to their Event Logic here.
# =======================================================
AUTOMATION_REGISTRY = {
    Task: {
        'event_code': 'TASK_DONE',
        # Logic: Only trigger if task is marked completed
        'condition': lambda instance, created: instance.is_completed, 
    },
    Milestone: {
        'event_code': 'MILESTONE_DONE',
        'condition': lambda instance, created: instance.is_completed,
    },
    Comments: {
        'event_code': 'COMMENT_ADDED',
        # Logic: Trigger only on creation (not edits)
        'condition': lambda instance, created: created,
    },
    Project: {
        'event_code': 'PROJECT_CREATED',
        'condition': lambda instance, created: created,
    }
}

# =======================================================
# 2. THE GENERIC HANDLER
# This function handles ALL models defined above.
# =======================================================
def generic_automation_handler(sender, instance, created, **kwargs):
    # 1. Get config for this model
    config = AUTOMATION_REGISTRY.get(sender)
    if not config:
        return

    # 2. Check if condition is met (e.g., is_completed == True)
    # We pass 'created' because some events only happen on creation
    if config['condition'](instance, created):
        
        event_code = config['event_code']
        print(f"⚡ Signal Fired: {event_code} for {instance}")

        # 3. CALL THE DISPATCHER
        # We pass the 'instance' (trigger_object) so the dispatcher
        # can extract {{ name }}, {{ id }}, etc.
        notify(event_code=event_code, trigger_object=instance)

# =======================================================
# 3. CONNECT SIGNALS DYNAMICALLY
# This binds the generic handler to the models in the registry.
# =======================================================
for model_class in AUTOMATION_REGISTRY.keys():
    post_save.connect(generic_automation_handler, sender=model_class)