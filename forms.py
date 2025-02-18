from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form
from phone_field.forms import PhoneFormField

COUNTRIES = (
    ("USA", "United States"),
    ("UK", "United Kingdom"),
    ("CANADA", "Canada"),
    ("AUSTRALIA", "Australia"),
)

class SignUpForm(UserCreationForm):
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other")
    )
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    phone_number = PhoneFormField(required=True, help_text="Phone number including country code.")
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")
    gender = forms.ChoiceField(choices=GENDER, required=True)
    street_address = forms.CharField(max_length=50, required=True, help_text="Required.")
    postal_code = forms.CharField(max_length=10, required=True, help_text="Postal Code (numbers only).")
    city = forms.CharField(max_length=30, required=True, help_text="Required.")
    country = forms.ChoiceField(choices=COUNTRIES, required=True)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "gender", "street_address", "postal_code", "city", "country", "phone_number", "email", "password1", "password2")

class UpdateQuantityForm(Form):
    PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label="Quantity"
    )

class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"})
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Leave a comment!"})
    )

class CheckOutForm(Form):
    DELIVERY_METHODS = (
        ("Home Delivery", "Delivery to Home or Office"),
        ("Pick Up Station", "Pick Up Station")
    )
    PICK_UP_STATIONS = (
        ("Central Warehouse, New York", "Central Warehouse, New York"),
        ("Mall Pickup, Los Angeles", "Mall Pickup, Los Angeles")
    )
    SHIPPING_ADDRESSES = (
        ("Use Default Shipping Address", "Use Default Shipping Address"),
        ("Set New Shipping Address", "Set New Shipping Address")
    )
    
    delivery_method = forms.ChoiceField(choices=DELIVERY_METHODS, required=True)
    pick_up_station = forms.ChoiceField(choices=PICK_UP_STATIONS, required=False)
    shipping_address = forms.ChoiceField(choices=SHIPPING_ADDRESSES, required=True)
    street_address = forms.CharField(max_length=50, required=False)
    postal_code = forms.CharField(max_length=10, required=False, help_text="Postal Code (numbers only).")
    city = forms.CharField(max_length=30, required=False)
    country = forms.ChoiceField(choices=COUNTRIES, required=False)
    
    PAYMENT_CHOICES = (
        ("PayPal", "PayPal"),
        ("Stripe", "Stripe"),
        ("Credit Card", "Credit Card")
    )
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES, required=True)

class CouponForm(Form):
    code = forms.CharField(label="Enter a valid discount code", max_length=10)

class AccountDetailsChangeForm(Form):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    phone_number = PhoneFormField(required=True, help_text="Phone number including country code.")
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")

class AddressChangeForm(Form):
    street_address = forms.CharField(max_length=50, required=True, help_text="Required.")
    postal_code = forms.CharField(max_length=10, required=True, help_text="Postal Code (numbers only).")
    city = forms.CharField(max_length=30, required=True, help_text="Required.")
    country = forms.ChoiceField(choices=COUNTRIES, required=True)
