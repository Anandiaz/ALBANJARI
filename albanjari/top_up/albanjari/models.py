from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

# User Profile Model
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('AGENT', 'Agent'),
        ('PLAYER', 'Player'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PLAYER')
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField()

    def _str(self):  # Fixed the method name from _str to _str_
        return f"{self.user.username} - {self.role}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Ensure user is in the correct group
            group_name = self.role.capitalize()
            group, _ = Group.objects.get_or_create(name=group_name)
            self.user.groups.clear()  # Remove from other groups
            self.user.groups.add(group)

# Category Model
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def str(self):
        return self.category_name

# Product Model
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def str(self):
        return self.product_name

# Top-Up Package Model
class TopUpPackage(models.Model):
    package_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    agent_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def str(self):
        return f"{self.product.product_name} - {self.package_name}"

# Transaction Model
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed')
    ]

    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TopUpPackage, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_proof = models.ImageField(upload_to='transaction_proofs/', null=True, blank=True)

    def str(self):
        return f"Transaction {self.transaction_id} - {self.user.username}"

# Payment Model
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    ]

    payment_id = models.AutoField(primary_key=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    def str(self):
        return f"Payment {self.payment_id} - Transaction {self.transaction.transaction_id}"

# Signal untuk handle user creation dan role assignment
@receiver(post_save, sender=UserProfile)
def create_user_for_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.user_id:
            user = User.objects.create_user(
                username=instance.email,
                email=instance.email,
                password=instance.phone_number
            )
            instance.user = user
            instance.save()

        # Menambahkan user ke grup berdasarkan role
        group_name = instance.role.capitalize()
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.user.groups.add(group)