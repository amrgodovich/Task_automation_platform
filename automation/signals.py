from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task, Milestone, Comments
from projects.models import Project
from .dispatcher import notify 

AUTOMATION_REGISTRY = {
    Task: [
        {
            'event_code': 'TASK_CREATED',
            'condition': lambda instance, created: created,
        },
        {
            'event_code': 'TASK_DONE',
            'condition': lambda instance, created: instance.status == 'SUCCESS', 
        },
        {
            'event_code': 'TASK_FAILED',
            'condition': lambda instance, created: instance.status == 'FAILED',
        },
    ],
    Milestone: [{
        'event_code': 'MILESTONE_DONE',
        'condition': lambda instance, created: instance.is_completed,
    }],
    Comments: [{
        'event_code': 'COMMENT_ADDED',
        'condition': lambda instance, created: created,
    }],
    Project: [{
        'event_code': 'PROJECT_CREATED',
        'condition': lambda instance, created: created,
    }]
}

def generic_automation_handler(sender, instance, created, **kwargs):
    event_configs = AUTOMATION_REGISTRY.get(sender)
    if not event_configs:
        return

    for config in event_configs:
        if config['condition'](instance, created):
            event_code = config['event_code']
        
            print(f"⚡ Signal Fired: {event_code} for {instance}")

            # 3. CALL THE DISPATCHER
            # We pass the 'instance' (trigger_object) so the dispatcher
            # can extract {{ name }}, {{ id }}, etc.
            notify(event_code=event_code, trigger_object=instance)


for model_class in AUTOMATION_REGISTRY.keys():
    print(f"🔗 Connecting signal for {model_class.__name__}")
    post_save.connect(generic_automation_handler, sender=model_class)