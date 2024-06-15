from rental.inspections.models import Inspection


def get_inspections(tenant):
    inspections = Inspection.objects.filter(tenant=tenant).all()
    return inspections
