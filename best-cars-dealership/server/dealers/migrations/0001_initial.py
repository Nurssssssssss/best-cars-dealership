from django.conf import settings
from django.db import migrations,models
import django.db.models.deletion
class Migration(migrations.Migration):
 initial=True
 dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
 operations=[
 migrations.CreateModel(name='Dealer',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=160)),('city',models.CharField(max_length=100)),('state',models.CharField(max_length=100)),('address',models.CharField(max_length=240)),('zip_code',models.CharField(blank=True,max_length=20)),('phone',models.CharField(blank=True,max_length=40)),('description',models.TextField(blank=True))]),
 migrations.CreateModel(name='CarMake',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=80,unique=True))]),
 migrations.CreateModel(name='CarModel',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=80)),('make',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='models',to='dealers.carmake'))],options={'unique_together':{('make','name')}}),
 migrations.CreateModel(name='Review',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('text',models.TextField()),('rating',models.PositiveSmallIntegerField()),('purchase_date',models.DateField()),('car_make',models.CharField(max_length=80)),('car_model',models.CharField(max_length=80)),('car_year',models.PositiveSmallIntegerField()),('created_at',models.DateTimeField(auto_now_add=True)),('author',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to=settings.AUTH_USER_MODEL)),('dealer',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='reviews',to='dealers.dealer'))],options={'ordering':['-created_at']})
 ]
