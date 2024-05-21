from django.db.models import Q
from rental.rentalPlan.models import RentalPlan
from settings.utils.exceptions import NotFound404APIException


def get_rental_plans(search_text: str = None, order_by: str = None, asc: bool = True):
    rental_plans = RentalPlan.objects.all()

    if search_text:
        rental_plans = rental_plans.filter(
            Q(name__icontains=search_text)
            | Q(periodicity__icontains=search_text)
            | Q(amount__icontains=search_text)
        )

    if order_by:
        if not asc:
            order_by = "-" + order_by
        rental_plans = rental_plans.order_by(order_by)

    return rental_plans


def get_rental_plan(rental_plan_id: int):
    try:
        rental_plan = RentalPlan.objects.get(id=rental_plan_id)
    except RentalPlan.DoesNotExist:
        raise NotFound404APIException(f"Rental Plan with id {rental_plan_id} not found")

    return rental_plan


def create_rental_plan(
    name: str, 
    amount: int, 
    periodicity: str, 
    tenant
):
    new_rental_plan = RentalPlan.objects.create(
        name=name, 
        amount=amount, 
        periodicity=periodicity, 
        tenant=tenant
    )
    new_rental_plan.save()
    return new_rental_plan


def update_rental_plan(
    rental_plan_id: int, 
    name: str = None, 
    amount: int = None, 
    periodicity: str = None
):
    rental_plan = RentalPlan.objects.get(id=rental_plan_id)
    if rental_plan:
        if name:
            rental_plan.name = name

        if amount:
            rental_plan.amount = amount

        if periodicity:
            rental_plan.periodicity = periodicity

        rental_plan.full_clean()
        rental_plan.save()
    else:
        raise NotFound404APIException(f"Rental Plan with id {rental_plan_id} not found")
    return rental_plan


def delete_rental_plan(rental_plan_id: int):
    try:
        rental_plan = RentalPlan.objects.get(id=rental_plan_id)
        rental_plan.delete()

    except RentalPlan.DoesNotExist:
        raise NotFound404APIException(f"Rental Plan with id {rental_plan_id} not found")
