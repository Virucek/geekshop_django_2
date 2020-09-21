from datetime import timedelta

from django.core.management import BaseCommand
from django.db.models import Q, F, When, Case, IntegerField, DecimalField

from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1_time_delta = timedelta(hours=12)
        action_2_time_delta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_expired_discount = 0.05

        action_1_condition = Q(order__updated_at__lte=F('order__created_at') + action_1_time_delta)
        action_2_condition = Q(order__updated_at__gt=F('order__created_at') + action_1_time_delta) &\
                               Q(order__updated_at__lte=F('order__created_at') + action_2_time_delta)
        action_expired_condition = Q(order__updated_at__gt=F('order__created_at') + action_2_time_delta)

        action_1__order = When(action_1_condition, then=ACTION_1)
        action_2__order = When(action_2_condition, then=ACTION_2)
        action_expired__order = When(action_expired_condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2__price = When(action_2_condition, then=F('product__price') * F('quantity') * action_2_discount)
        action_expired_price = When(action_expired_condition, then=F('product__price') * F('quantity') *\
                                                                   action_expired_discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired_price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        for item in test_orders:
            print(f'{item.action_order}: заказ № {item.pk}: \
                {item.product.name}: скидка\
                {abs(item.total_price): 6.3f} руб. | \
                {item.order.updated_at - item.order.created_at}'
                  )
