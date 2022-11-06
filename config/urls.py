from django.contrib import admin
from django.urls    import path


"""
Django app url patterns
"""
urlpatterns = [
    path('admin/', admin.site.urls),
]