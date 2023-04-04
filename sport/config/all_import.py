import json
from datetime import datetime
from django.db.models import *
from django.db.transaction import *
from django.apps import apps

classes = apps.get_models()
for _class in classes:
    globals()[_class.__name__] = _class
