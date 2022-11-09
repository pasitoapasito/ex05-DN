from django.contrib import admin
from django.urls    import path

from config.api     import api


"""
Django app url patterns
"""
urlpatterns = [
    path("api/", api.urls),
    path('admin/', admin.site.urls),
]