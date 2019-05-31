from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Insurance API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login),
    path('detaildata', detaildata),
    path('detailagencydata', detailagencydata),
    path('vendorpremium', vendorpremium),
    path('stateproductionlinepremium', stateproductionlinepremium),
    path('csvreportexport', csvreportexport),
    path(r'swagger-docs/', schema_view),
]