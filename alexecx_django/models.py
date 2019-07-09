from itertools import chain

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

#Utilities

def model_dict(model, fields=None, exclude=None) -> dict: 
    """Fait une copie en surface d'un Model sous forme de dict.
    
    Args:
        model (django.db.models.Model): [description]
        fields (list, optional): liste de nom des champs à inclure
        exclude (list, optional): liste de nom de champs à exclure
    
    Returns:
        dict: Model sous forme de dict
    """
    opts = model._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(model)
    return data


def deep_model_dict(model, fields=None, exclude=None) -> dict:
    """Fait une copie en profondeur d'un Model sous forme de dict.

    Ex:
        models.ForeignKey => un dict
        models.ManyToManyField => une liste de dict
        Autres  => str(champ)
    
    Args:
        model (django.db.models.Model): [description]
        fields (list, optional): liste de nom des champs à inclure
        exclude (list, optional): liste de nom de champs à exclure
    
    Returns:
        dict: Model sous forme de dict
    """
    opts = model._meta
    data = {}
    for field in chain(opts.concrete_fields, opts.private_fields):
        if fields and field.name not in fields:
            continue
        if exclude and field.name in exclude:
            continue
        attr = getattr(model, field.name)
        if isinstance(attr, models.Model):
            data[field.name] = deep_model_dict(attr) #<-- recursive call
        else:
            data[field.name] = str(attr)

    for field in opts.many_to_many:
        if fields and field.name not in fields:
            continue
        if exclude and field.name in exclude:
            continue
        attr = field.value_from_object(model)
        data[field.name] = [deep_model_dict(i) for i in attr] #<-- recursive call
    return data


# Models

class User:
    address = models.CharField(max_length=200, )
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=10, blank=True) # validators should be a list
    # For unique emails
    class Meta(object):
        unique_together = ('email',)