import json
import uuid

from crequest.middleware import CrequestMiddleware
from django.contrib.auth.models import User
from django.db import models, transaction

from utils.clock import Clock


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    timestamp = models.BigIntegerField(editable=False, default=0, db_index=True)
    is_active = models.BooleanField(default=True, editable=False)
    is_deleted = models.BooleanField(default=False, editable=False)
    is_locked = models.BooleanField(default=False, editable=False)
    created_by = models.ForeignKey(
        User,
        related_name="+",
        null=True,
        on_delete=models.SET_NULL,
    )
    last_updated_by = models.ForeignKey(
        User,
        related_name="+",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        request = CrequestMiddleware.get_request()
        with transaction.atomic():
            self.clean()
            current_timestamp = Clock.timestamp()
            if self.date_created is None or self.date_created == 0:
                if self.created_by is None:
                    try:
                        self.created_by = request.c_user
                    except:
                        pass
                self.timestamp = current_timestamp
                try:
                    self.last_updated_by = request.c_user
                except:
                    pass
            super(BaseModel, self).save()
