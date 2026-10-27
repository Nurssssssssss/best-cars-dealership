import json
from datetime import date
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Dealer,Review,CarMake

def err(msg,status=400):return JsonResponse({'error':msg},status=status)
def body(request):
 try:return json.loads(request.body.decode('utf-8'))
 except (ValueError,UnicodeDecodeError):return None

def dealer_dict(d):return {'id':d.id,'name':d.name,'city':d.city,'state':d.state,'address':d.address,'zip_code':d.zip_code,'phone':d.phone,'description':d.description}
def review_dict(r):return {'id':r.id,'dealer_id':r.dealer_id,'username':r.author.username,'text':r.text,'rating':r.rating,'purchase_date':r.purchase_date.isoformat(),'car_make':r.car_make,'car_model':r.car_model,'car_year':r.car_year,'sentiment':sentiment(r.text)}
def sentiment(t):
 s=t.lower();pos=['fantastic','excellent','great','good','friendly','helpful','amazing','love','quick'];neg=['bad','poor','terrible','awful','slow','rude','horrible','hate']
 score=sum(x in s for x in pos)-sum(x in s for x in neg)
 return 'positive' if score>0 else 'negative' if score<0 else 'neutral'
@ensure_csrf_cookie
@require_http_methods(['GET'])
def csrf(request):return JsonResponse({'ok':True,'authenticated':request.user.is_authenticated,'username':request.user.username if request.user.is_authenticated else None})
@require_http_methods(['GET'])
def dealers(request):
 q=Dealer.objects.all().order_by('id');state=request.GET.get('state')
 if state:q=q.filter(state__iexact=state)
 return JsonResponse({'dealers':[dealer_dict(d) for d in q]})
@require_http_methods(['GET'])
def dealer(request,pk):
 d=Dealer.objects.filter(pk=pk).first()
 return JsonResponse(dealer_dict(d)) if d else err('Dealer not found',404)
@require_http_methods(['GET','POST'])
def reviews(request,pk):
 d=Dealer.objects.filter(pk=pk).first()
 if not d:return err('Dealer not found',404)
 if request.method=='GET':return JsonResponse({'reviews':[review_dict(r) for r in d.reviews.select_related('author')]})
 if not request.user.is_authenticated:return err('Login required',401)
 data=body(request)
 if not isinstance(data,dict):return err('Invalid JSON')
 try:
  rating=int(data.get('rating',0));year=int(data.get('car_year',0));purchase=date.fromisoformat(str(data.get('purchase_date','')))
  if not 1<=rating<=5 or not 1900<=year<=date.today().year+1:raise ValueError()
 except (ValueError,TypeError):return err('Invalid rating, year or date')
 text=str(data.get('text','')).strip();make=str(data.get('car_make','')).strip();model=str(data.get('car_model','')).strip()
 if not text or not make or not model:return err('Review text, car make and model required')
 r=Review.objects.create(dealer=d,author=request.user,text=text[:5000],rating=rating,purchase_date=purchase,car_make=make[:80],car_model=model[:80],car_year=year)
 return JsonResponse(review_dict(r),status=201)
@require_http_methods(['GET'])
def carmakes(request):return JsonResponse({'car_makes':[{'id':m.id,'name':m.name,'models':[x.name for x in m.models.all()]} for m in CarMake.objects.prefetch_related('models')]})
@require_http_methods(['GET'])
def analyze(request):
 t=request.GET.get('text','')
 return JsonResponse({'text':t,'sentiment':sentiment(t),'method':'keyword-baseline'})
@require_http_methods(['POST'])
def register(request):
 data=body(request)
 if not isinstance(data,dict):return err('Invalid JSON')
 required=['username','first_name','last_name','email','password']
 if any(not str(data.get(k,'')).strip() for k in required):return err('All five fields are required')
 try:validate_password(data['password'])
 except ValidationError as e:return err('; '.join(e.messages))
 if User.objects.filter(username=data['username']).exists():return err('Username already exists')
 try:u=User.objects.create_user(username=data['username'],email=data['email'],password=data['password'],first_name=data['first_name'],last_name=data['last_name'])
 except (IntegrityError,ValueError):return err('Invalid user data')
 return JsonResponse({'username':u.username,'registered':True},status=201)
@require_http_methods(['POST'])
def login_view(request):
 data=body(request)
 if not isinstance(data,dict):return err('Invalid JSON')
 u=authenticate(request,username=data.get('username',''),password=data.get('password',''))
 if u is None:return err('Invalid credentials',401)
 login(request,u);return JsonResponse({'authenticated':True,'username':u.username})
@require_http_methods(['POST'])
def logout_view(request):
 logout(request);return JsonResponse({'authenticated':False})
