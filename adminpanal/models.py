# models.py

from django.db import models

class ParentModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("full_access_parent_admin", "Full access to parent admin"),
        ]

class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)
    child_name = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("limited_access_child_admin", "Limited access to child admin"),
        ]

