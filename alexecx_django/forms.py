from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
#from django.utils.translation import ugettext_lazy as _u

from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(
    #     label=_u('Prénom'), 
    #     max_length=30, 
    #     required=True,
    #     )
    # last_name = forms.CharField(
    #     label=_u('Nom'), 
    #     max_length=30, 
    #     required=True, 
    #     )
    # email = forms.EmailField(
    #     label=_u('Email'), 
    #     max_length=254, 
    #     help_text=_u(
    #         'Utiliser une adresse email valide (something@exemple.com).'
    #         )
    #     )
    # address = forms.CharField(
    #     label=_u('Adresse'),
    #     max_length=200, 
    #     required=False,
    #     )
    # phone = forms.CharField(
    #     label=_u('Téléphone'), 
    #     max_length=10, 
    #     required=False, 
    #     )

    class Meta:
        model = get_user_model()
        exclude = ('password', 'is_superuser', 'is_staff', 'groups', 
        'user_permissions', 'last_login', 'is_active', 'date_joined')
        # fields = ('username', 'first_name', 'last_name', 'email', 
        #           'password1', 'password2', 
        #           'address', 'phone', )

    def __init__(self, request=None, **kwargs):
        super().__init__(**kwargs)


class ChangeListForm(forms.Form):
    ACTIONS = (
        (None, '--------'),
    )
    action = forms.ChoiceField(choices=ACTIONS)
    selection = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=True,
        #error_messages=default_error_messages
    )

    def __init__(self, *args, **kwargs):
        items = kwargs.pop("selection", None)
        super().__init__(*args, **kwargs)
        if items:
            self.set_selection(items)
        self.fields["selection"].error_messages.update({
            "invalid_choice": _('Choix checkbox invalide.'),
            'required': _('Sélectionnez au moins 1 item.')
        })

    def set_selection(self, items):
        self.fields["selection"].choices = [ (i, str(x)) \
                                            for i,x in enumerate(items)]

    def clean_selection(self):
        selection = self.cleaned_data.get('selection')
        if not selection:
            raise forms.ValidationError(_('Vous devez choisir au moins 1 item'))
        return selection


class ChangeListModelForm(ChangeListForm):
    
    def set_selection(self, items):
        self.fields["selection"].choices = [ (x.id, str(x)) for x in items]
