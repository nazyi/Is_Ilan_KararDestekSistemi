"""
URL configuration for proje_adi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'), 
    path('about/', views.about,name='about'),
    path('company/<str:company_name>/', views.company_homepage, name='company_homepage'),
    path('add-job/', views.add_job, name='add_job'),
    path('company/<str:company_name>/job/<str:job_id>/edit/', views.edit_job, name='edit_job'),
    path('personel_uye_ol/', views.personel_uye_ol, name='personel_uye_ol'),
    path('personel-homepage/<str:personel_email>/', views.personel_homepage, name='personel_homepage'),
    path('job-application/', views.job_application, name='job_application'),
    path('add-cv/', views.add_cv, name='add_cv'),
    path('job-detail/<str:ilan_id>/', views.job_detail, name='job_detail'),
    path('job-apply/<str:ilan_id>/', views.job_apply, name='job_apply'),
    path('company/<str:company_name>/job/<str:job_id>/', views.sirket_job_detail, name='sirket_job_detail'),
    path('ilan-ekle/', views.yeni_ilan_ekle_anlamli, name='yeni_ilan_ekle_anlamli'),
    path('eslestirme/', views.eslestirme, name='eslestirme'),
    path('SkorHesaplama/', views.SkorHesapla, name='SkorHesaplama'),
    path('ozgecmis/', views.Ozgecmis, name='ozgecmis'),
]
