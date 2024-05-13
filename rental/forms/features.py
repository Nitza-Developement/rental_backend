from rental.forms.models import *
from settings.utils.exceptions import NotFound404APIException

def get_forms(tenant):
    forms = Form.objects.filter(tenant=tenant)
    return forms

def get_form(form_id):
    try:
        return Form.objects.get(id=form_id)
    except Form.DoesNotExist:
        raise NotFound404APIException(f'Form with ID {form_id} doesnt exists')
    
def create_form(tenant, name, is_active=None):
    form = Form.objects.create(
        tenant = tenant,
        name = name,
        is_active = is_active,
    )
    return form

def update_form(form_id, name, is_active):
    try:
        form = Form.objects.get(id=form_id)
        form.name = name
        form.is_active = is_active
        form.save()
        return form
    except form.DoesNotExist:
        raise NotFound404APIException(f'Form with ID {form_id} doesnt exists')
    
def create_card(form, name, fields):
    card = Card.objects.create(name=name, form=form)
    for _field in fields:
        field = Field.objects.create(
            name=_field['labelName'],
            type=_field['type'],
            required=_field['required'],
            card=card
        )
        if field.type == Field.SINGLE_CHECK:
            CheckOption.objects.create(name=_field['pointPass'], field=field)
            CheckOption.objects.create(name=_field['pointFail'], field=field)
    return card