from django.http import QueryDict


def qdict_to_dict(qdict:QueryDict):
    """Convert a Django QueryDict to a Python dict.

    Single-value fields are put in directly, and for multi-value fields, a list
    of all values is stored at the field's key.

    """
    return {
        str(k).replace("[]", ""): v[0] if len(v) == 1 else v
        for k, v in qdict.lists()
    }