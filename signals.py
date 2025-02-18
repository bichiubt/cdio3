from django.shortcuts import get_object_or_404
from .models import Cart, Address, User_Profile, Coupon, OrderItem
from django.contrib.auth.models import User
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.db.models.signals import post_save
from ecommerce_platform.recommender import Recommender

@receiver(post_save, sender=User)
def create_user_cart_and_address_and_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create cart, address, and user profile for new users
        Cart.objects.create(user=instance)    
        Address.objects.create(user=instance)
        User_Profile.objects.create(user=instance)

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    coupon_id = ipn.custom
    gross = (ipn.mc_gross * 100)  # Convert to cent (if needed for currency compatibility)

    if ipn.payment_status == 'Completed':
        # Retrieve the cart using the invoice code
        cart = Cart.objects.get(invoice_code=ipn.invoice)

        # Adding the bought products into the recommendation system
        recommender = Recommender()
        orders = cart.order_items.filter(ordered=False)
        bought_products = [order.product for order in orders]
        recommender.products_bought(bought_products)  # Update the recommender with bought products

        if coupon_id is not None and coupon_id != "":  # Check if a coupon was used
            coupon = Coupon.objects.get(id=coupon_id)
            if cart.get_total_after_discount(coupon.discount) == gross:  # Validate the total amount with the discount
                # Process the orders if the payment matches the expected total
                orders = cart.order_items.filter(ordered=False)
                for order in orders:
                    order.ordered = True
                    order.order_invoice_code = ipn.invoice
                    order.save()
                    cart.order_items.remove(order)
                    cart.save()
        else:
            # If no coupon was used, verify if the total matches the expected amount
            if cart.get_total() == gross:
                orders = cart.order_items.filter(ordered=False)
                for order in orders:
                    order.ordered = True
                    order.order_invoice_code = ipn.invoice
                    order.save()
                    cart.order_items.remove(order)
                    cart.save()

        # You could also add some more logic to update the user's profile or other related processes if needed.
