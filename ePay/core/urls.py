from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('payapp.urls')),
    path('account/' , include('account.urls')),
    path('pay/' , include('payapp.urls')),
    
]
