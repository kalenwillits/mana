from django.contrib import admin
from django.contrib.auth.models import Group


from .models import Organization
from .models import Project
from .models import State
from .models import Role
from .models import Sprint
from .models import Tag
from .models import Task
from .models import Thread
from .models import User

admin.site.unregister(Group)

admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(State)
admin.site.register(Role)
admin.site.register(Sprint)
admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(Thread)
admin.site.register(User)
