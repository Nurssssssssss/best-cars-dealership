from django.core.management.base import BaseCommand
from dealers.models import Dealer,CarMake,CarModel
class Command(BaseCommand):
 help='Create demo dealers and car makes'
 def handle(self,*args,**kwargs):
  rows=[('Sunflower Auto Center','Wichita','Kansas','1200 East Douglas Ave','67202'),('Prairie Motors','Topeka','Kansas','415 Kansas Ave','66603'),('Heartland Cars','Overland Park','Kansas','7900 Metcalf Ave','66204'),('Metro Auto Gallery','Denver','Colorado','2100 Market St','80205'),('Lakeside Motors','Chicago','Illinois','900 Lake St','60601')]
  for name,city,state,address,zip_code in rows:Dealer.objects.get_or_create(name=name,defaults={'city':city,'state':state,'address':address,'zip_code':zip_code,'phone':'555-0100','description':f'Independent dealer serving {city}.'})
  for make,models in {'Toyota':['Camry','Corolla','RAV4'],'Honda':['Civic','Accord','CR-V'],'Ford':['Focus','Mustang','Escape'],'Hyundai':['Elantra','Tucson']}.items():
   m,_=CarMake.objects.get_or_create(name=make)
   for model in models:CarModel.objects.get_or_create(make=m,name=model)
  self.stdout.write(self.style.SUCCESS('Demo dealers and car makes ready'))
