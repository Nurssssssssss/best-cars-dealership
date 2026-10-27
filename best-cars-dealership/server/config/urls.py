from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.views.static import serve
from dealers import course_compat as course
urlpatterns=[
 path('admin/',admin.site.urls),
 path('api/',include('dealers.urls')),
 path('fetchDealers',course.fetch_dealers),
 path('fetchDealer/<int:dealer_id>',course.fetch_dealer),
 path('fetchDealers/<str:state>',course.fetch_dealers_by_state),
 path('fetchReviews/dealer/<int:dealer_id>',course.fetch_reviews),
 path('djangoapp/get_cars',course.get_cars),
 path('djangoapp/login',course.course_login),
 path('djangoapp/logout',course.course_logout),
 path('analyze/<path:review_text>',course.analyze_text),
]
if __import__('os').environ.get('DJANGO_SERVE_REACT')=='1':
 from django.views.generic import View
 from django.http import FileResponse
 from pathlib import Path
 class ReactIndex(View):
  def get(self,request,*args,**kwargs):
   p=settings.BASE_DIR/'frontend'/'dist'/'index.html'
   if not p.exists():raise Http404('Build frontend first')
   return FileResponse(open(p,'rb'),content_type='text/html')
 urlpatterns += [re_path(r'^(?!api/|admin/|static/|assets/).*$',ReactIndex.as_view())]
