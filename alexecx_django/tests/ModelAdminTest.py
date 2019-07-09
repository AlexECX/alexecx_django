import inspect
import random
import re
import string
from abc import ABC
from datetime import timedelta
from itertools import chain
from uuid import uuid4

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import (AutoField, BinaryField, BooleanField,
                                     CharField, DateField, DateTimeField,
                                     DecimalField, DurationField, EmailField,
                                     FilePathField, FloatField,
                                     GenericIPAddressField, IntegerField,
                                     TextField, TimeField, UUIDField)
from django.db.models.fields.related import ForeignKey
from django.db.utils import IntegrityError
from django.test import RequestFactory, TestCase
from django.utils import timezone

from .AccessTest import AccessHelper


class AbstractModelAdminTest(ABC):
    admin_module = None
    models_module = None
    models_exludes = []
    app_name = ""

    def setUp(self):
        self.site = AdminSite()
        self.helper = AccessHelper()
        self.excludes = []
        classes = []
        for c in self.models_module.__dict__.values():
            if inspect.isclass(c) and issubclass(c, models.Model):
                classes.append(c)
        
        self.model_admins = []
        for c in classes:
            if c in self.models_exludes:
                continue
            if not self.admin_module.__dict__.get(c.__name__):
                continue
            self.model_admins.append([
                    c,
                    self.admin_module.__dict__.get(c.__name__+"Admin", ModelAdmin)(c, self.site)
                ])
        
        self.user = get_user_model().objects.create_superuser(username='super', email='super@email.com',
                    password='super')
        self.factory = RequestFactory()
        self.client.login(username="super", password="super")
            
    def test_model_admin(self):
        for i,entry in enumerate(self.model_admins):
            ##print(f"{entry[1].__class__.__name__.lower()}\n")
            with self.subTest(f"save {entry[1].__class__.__name__.lower()}"):
                obj = fill_model(entry[0])
                entry[1].save_model(request=None, obj=obj, form=None, change=None)
                
            with self.subTest(f"admin view {entry[1].__class__.__name__.lower()}"):
                self.helper.assert_has_access(
                    self.client, 
                    f"/admin/{self.app_name}/{obj.__class__.__name__.lower()}/"
                )   
            
            with self.subTest(f"admin change {entry[1].__class__.__name__.lower()}"):
                self.helper.assert_has_access(
                    self.client, 
                    f"/admin/{self.app_name}/{obj.__class__.__name__.lower()}/{obj.id}/change/"
                )   
                
                # try:
                    
                # except IntegrityError as e:
                #     raise Exception(str(obj.id)+"::\n"+str(entry)+"::\n"+str(e))


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def random_str(length=6):
    return "".join(random.choice(string.ascii_letters) for i in range(length))

TIMEZONE_NOW = timezone.now()

def fill_model(model):
    def get_defaults(cls):
        opts = cls._meta
        field_names = {}
        for field in chain(opts.concrete_fields, opts.private_fields):
            if issubclass(field.__class__, ForeignKey):
                other = field.remote_field.model
                defaults = get_defaults(other)
                field_names[field.name] = other.objects.filter(**defaults).first()
                if field_names[field.name] is None:
                    field_names[field.name] = other.objects.first()
                if field_names[field.name] is None:
                    try:
                        field_names[field.name] = other.objects.create(**defaults)
                    except IntegrityError as e:
                        raise IntegrityError(str(defaults)+"::"+str(other)+"::"+str(e))
            elif field.null is True:
                continue
            elif issubclass(field.__class__, AutoField):
                continue
            elif issubclass(field.__class__, BooleanField):
                field_names[field.name] = True
            elif issubclass(field.__class__, FloatField):
                field_names[field.name] = 1.0
            elif issubclass(field.__class__, DecimalField):
                field_names[field.name] = 0.1
            elif issubclass(field.__class__, BinaryField):
                field_names[field.name] = b''
            elif issubclass(field.__class__, EmailField):
                field_names[field.name] = "al@g.com"
            elif issubclass(field.__class__, TextField):
                field_names[field.name] = "True"
            elif issubclass(field.__class__, FilePathField):
                field_names[field.name] = "zxcvd"
            elif issubclass(field.__class__, DateTimeField):
                field_names[field.name] = TIMEZONE_NOW
            elif issubclass(field.__class__, TimeField):
                field_names[field.name] = TIMEZONE_NOW
            elif issubclass(field.__class__, DurationField):
                field_names[field.name] = timedelta()
            elif issubclass(field.__class__, DateField):
                field_names[field.name] = TIMEZONE_NOW
            elif issubclass(field.__class__, GenericIPAddressField):
                field_names[field.name] = "127.0.0.1"
            elif issubclass(field.__class__, UUIDField):
                field_names[field.name] = uuid4()
            elif issubclass(field.__class__, CharField):
                field_names[field.name] = "True"
            elif issubclass(field.__class__, IntegerField):
                field_names[field.name] = 1
        return field_names

    defaults = get_defaults(model)
    m = model.objects.filter(**defaults).first()
    return model(**defaults) if m is None else m
