import os
from decimal import Decimal

import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from dotenv import load_dotenv
from apps.items.models import Item
from apps.orders.models import Order, Discount, Tax

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def get_checkout_session_id(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/item/{item.id}/'),
        cancel_url=request.build_absolute_uri(f'/item/{item.id}/'),
    )

    return JsonResponse({'session_id': session.id})


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    return render(
        request,
        'item_detail.html',
        {
            'item': item,
            'stripe_publishable_key': stripe_publishable_key
        }
    )


def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    line_items = []
    for item in order.items.all():
        final_price = item.price

        if order.discount:
            discount_amount = (Decimal(order.discount.amount) / 100) * final_price
            final_price -= discount_amount
        if order.tax:
            final_price *= (1 + Decimal(order.tax.rate) / 100)

        line_items.append({
            'price_data': {
                'currency': 'USD',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(final_price * 100),
            },
            'quantity': 1,
        })

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
    )

    return JsonResponse({'session_id': checkout_session.id})


def create_order(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('item_ids')
        discount_id = request.POST.get('discount_id')
        tax_id = request.POST.get('tax_id')

        items = Item.objects.filter(id__in=item_ids)
        discount = Discount.objects.get(id=discount_id) if discount_id else None
        tax = Tax.objects.get(id=tax_id) if tax_id else None

        order = Order.objects.create(
            discount=discount,
            tax=tax,
        )
        order.items.set(items)
        total_price = sum(item.price for item in order.items.all())
        if order.discount:
            discount_amount = (Decimal(order.discount.amount) / 100) * total_price
            total_price -= discount_amount
        if order.tax:
            total_price *= (1 + Decimal(order.tax.rate) / 100)
        order.total_price = total_price
        order.save()
        return redirect('order_detail', order_id=order.id)
    else:
        items = Item.objects.all()
        discounts = Discount.objects.all()
        taxes = Tax.objects.all()
        return render(request, 'create_order.html', {'items': items, 'discounts': discounts, 'taxes': taxes})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    return render(request, 'order_detail.html', {'order': order, 'stripe_publishable_key': stripe_publishable_key})