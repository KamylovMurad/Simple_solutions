from django.urls import path
from django.views.generic import TemplateView

from apps.stripe_api.views import (
    get_checkout_session_id,
    item_detail,
    create_checkout_session,
    create_order,
    order_detail
)

urlpatterns = [
    path(f'buy/<int:item_id>/', get_checkout_session_id, name='get_checkout_session_id'),
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('buy_order/<int:order_id>/', create_checkout_session, name='create_checkout_session'),
    path('create_order/', create_order, name='create_order'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('cancel/', TemplateView.as_view(template_name='cancel_template.html'), name='payment_cancel'),
    path('success/', TemplateView.as_view(template_name='payment_success.html'), name='payment_success'),
]
