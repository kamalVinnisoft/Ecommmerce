from django.db import models
from django.utils import timezone

class ActiveManager(models.Manager):
    def get_queryset(self):
        # Filter out objects where is_deleted is True
        return super().get_queryset().filter(is_deleted=False)

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveManager()  # Active objects manager
    all_objects = models.Manager()  # Default manager to include all objects

    def soft_delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
        
       
    def restore(self, *args, **kwargs):
        self.is_deleted = False
        self.save()
        
    class Meta:
        abstract = True