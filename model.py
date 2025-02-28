from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
import uuid
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField
from phone_field import PhoneField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    street_address = models.CharField(max_length=100, default="")
    postal_code = models.CharField(max_length=10, default="00000")
    city = models.CharField(max_length=50, default="")
    country = CountryField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=10, default="")
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    preferences = models.ManyToManyField(Category, blank=True)
    
    def __str__(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, default="")
    units_available = models.PositiveIntegerField(null=True)
    price = models.FloatField(null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images', default='images/none/no-image.png')
    added_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default="", editable=False, max_length=100, unique=True)
    categories = models.ManyToManyField(Category)
    rating = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ["-added_on"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("ecommerce_platform:product_detail", kwargs={"slug": self.slug})


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
    
    def __str__(self):
        return f"{self.user.username} -> {self.product.name} ({self.score})"


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique Order Number')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True)
    delivered = models.BooleanField(default=False)
    order_item_total = models.FloatField(null=True)
    
    def get_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    order_items = models.ManyToManyField(OrderItem)
    
    def get_total(self):
        return sum(item.get_total() for item in self.order_items.all())
    
    def __str__(self):
        return f"Cart of {self.user.username}"
