from rental.forms.models import Card, Form, Field, CheckOption
from settings.utils.exceptions import NotFound404APIException


def rename_form(form_id, name, tenant):
    form = get_form(form_id, tenant)

    if form:
        form.name = name
        form.save()
        return True

    raise NotFound404APIException(f"Form with ID {form_id} doesnt exists")


def get_forms(tenant):
    forms = Form.objects.filter(tenant=tenant, is_active=True)
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


def import_forms(tenant, forms: list):

    created_forms = []

    for _form in forms:
        form = Form.objects.create(name=_form.get("name"), tenant=tenant)

        cards = _form.get("cards", [])
        for card in cards:
            create_card(form, card.get("name"), card.get("fields", []))

        created_forms.append(form)

    return created_forms


def delete_form(form_id, tenant):
    form = get_form(form_id, tenant)
    if form:
        form.is_active = False
        form.save()
        return True
    raise NotFound404APIException(f"Form with ID {form_id} doesnt exists")


def create_card(form, name, fields):
    card = Card.objects.create(name=name, form=form)

    for _field in fields:

        field = Field.objects.create(
            name=_field["name"],
            type=_field["type"],
            required=_field["required"],
            card=card,
        )

        if field.type == "SINGLE_CHECK":

            for option in _field.get("check_options"):

                CheckOption.objects.create(
                    name=option.get("name"), type=option.get("type"), field=field
                )
    return card


def delete_card(card_id):

    try:
        card = Card.objects.get(id=card_id)
        card.delete()
        return True
    except Card.DoesNotExist:
        raise NotFound404APIException(f"Card with ID {card_id} doesnt exists")


def update_card(card_id, name, fields):
    try:
        card = Card.objects.get(id=card_id)
        card.name = name
        card.save()

        filtered_fields_id = [field.get("id") for field in fields if field.get("id")]

        Field.objects.filter(card=card).exclude(id__in=filtered_fields_id).delete()

        for _field in fields:

            field_id = _field.get("id")
            field_name = _field.get("name")
            field_type = _field.get("type")
            field_required = _field.get("required", True)

            if field_id:  # update
                field = Field.objects.get(id=field_id)
                field.name = field_name
                field.type = field_type
                field.required = field_required
                field.save()
            else:  # create
                field = Field.objects.create(
                    name=field_name,
                    type=field_type,
                    required=field_required,
                    card=card,
                )

            if field.type == "SINGLE_CHECK":

                _options = _field.get("check_options")

                filtered_options_id = [
                    option.get("id") for option in _options if option.get("id")
                ]

                CheckOption.objects.filter(field=field).exclude(
                    id__in=filtered_options_id
                ).delete()

                for opt in _options:

                    option_id = opt.get("id")

                    if option_id:

                        CheckOption.objects.filter(id=option_id).update(
                            name=opt.get("name")
                        )

                    else:
                        CheckOption.objects.create(
                            name=opt.get("name"), type=opt.get("type"), field=field
                        )

            else:
                CheckOption.objects.filter(field=field).delete()

        return card
    except Card.DoesNotExist:
        raise NotFound404APIException(f"Card with ID {card_id} doesnt exists")
