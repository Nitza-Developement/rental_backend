from rental.forms.models import *
from settings.utils.exceptions import NotFound404APIException


def rename_form(form_id, name, tenant):
    form = get_form(form_id, tenant)
    if form:
        form.name = name
        form.save()
    raise NotFound404APIException(f"Form with ID {form_id} doesnt exists")


def get_forms(tenant):
    forms = Form.objects.filter(tenant=tenant)
    return forms


def get_form(form_id, tenant):
    try:
        return Form.objects.get(id=form_id, tenant=tenant)
    except Form.DoesNotExist:
        raise NotFound404APIException(f"Form with ID {form_id} doesnt exists")


def create_form(tenant, data):

    form = Form.objects.create(
        tenant=tenant,
        name=data.get("name"),
    )

    cards = data.get("cards", [])

    for _card in cards:
        create_card(form, _card.get("name"), _card.get("fields", []))

    return form


def update_form(form_id, name, is_active):
    try:
        form = Form.objects.get(id=form_id)
        form.name = name
        form.is_active = is_active
        form.save()
        return form
    except form.DoesNotExist:
        raise NotFound404APIException(f"Form with ID {form_id} doesnt exists")


def create_card(form, name, fields):
    card = Card.objects.create(name=name, form=form)
    for _field in fields:
        field = Field.objects.create(
            name=_field["labelName"],
            type=_field["type"],
            required=_field["required"],
            card=card,
        )
        if field.type == Field.SINGLE_CHECK:
            CheckOption.objects.create(name=_field["pointPass"], field=field)
            CheckOption.objects.create(name=_field["pointFail"], field=field)
    return card


def import_forms(tenant, forms: list):

    created_forms = []

    for _form in forms:
        form = Form.objects.create(name=_form.get("name"), tenant=tenant)

        cards = _form.get("cards", [])
        for card in cards:
            create_card(form, card.get("name"), card.get("fields", []))

        created_forms.append(form)

    return created_forms


def delete_form(form_id , tenant):
    form = get_form(form_id , tenant)
    if form:
        form.delete()
        return True
    raise NotFound404APIException(f"Form with ID {form_id} doesnt exists")
