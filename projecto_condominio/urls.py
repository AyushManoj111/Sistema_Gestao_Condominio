from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from gerente_condominio.views import login_view

urlpatterns = [
    path('', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('gerente/', include('gerente_condominio.urls')),
]