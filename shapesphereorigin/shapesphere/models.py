from django.db import models
from django.contrib.auth.models import User

class KullaniciBilgileri(models.Model):
    isim = models.CharField(max_length=100)
    soyisim = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    telefon = models.CharField(max_length=15)
    kredi_karti_numarasi = models.CharField(max_length=16)
    son_kullanma_tarihi = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3, default='000')
    def __str__(self):
        return f"{self.isim} {self.soyisim}"

class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'contact'    

    def __str__(self):
        return f"{self.name} {self.email}"
        


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prompt[:30]}"
        
        


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Kullanıcıyla ilişkilendirme
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    

    def __str__(self):
        return self.name     

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Sepet bir kullanıcıya ait olacak
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Ürün ile ilişkilendirme
    # quantity alanı kaldırıldı

    def __str__(self):
        return f"{self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    order_notes = models.TextField(blank=True, null=True)

# # Class Booking System
# class Class(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     instructor = models.CharField(max_length=100)
#     schedule = models.DateTimeField()
#     # ...

# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     booked_class = models.ForeignKey(Class, on_delete=models.CASCADE)
#     booking_date = models.DateTimeField(auto_now_add=True)
#     # ...

# # Notification and Reminder
# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#     # ...

# class Reminder(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     reminder_date = models.DateTimeField()
#     reminder_message = models.TextField()
#     # ...

# class ClassSchedule(models.Model):
#     class_item = models.ForeignKey(Class, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_schedules')
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     # ...
