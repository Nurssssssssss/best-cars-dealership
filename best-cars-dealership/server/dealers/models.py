from django.db import models
from django.conf import settings
class Dealer(models.Model):
 name=models.CharField(max_length=160)
 city=models.CharField(max_length=100)
 state=models.CharField(max_length=100)
 address=models.CharField(max_length=240)
 zip_code=models.CharField(max_length=20,blank=True)
 phone=models.CharField(max_length=40,blank=True)
 description=models.TextField(blank=True)
 def __str__(self):return self.name
class CarMake(models.Model):
 name=models.CharField(max_length=80,unique=True)
 def __str__(self):return self.name
class CarModel(models.Model):
 make=models.ForeignKey(CarMake,on_delete=models.CASCADE,related_name='models')
 name=models.CharField(max_length=80)
 class Meta:unique_together=[('make','name')]
 def __str__(self):return f'{self.make} {self.name}'
class Review(models.Model):
 dealer=models.ForeignKey(Dealer,on_delete=models.CASCADE,related_name='reviews')
 author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
 text=models.TextField()
 rating=models.PositiveSmallIntegerField()
 purchase_date=models.DateField()
 car_make=models.CharField(max_length=80)
 car_model=models.CharField(max_length=80)
 car_year=models.PositiveSmallIntegerField()
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:ordering=['-created_at']
