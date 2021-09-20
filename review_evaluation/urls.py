from django.urls import include, path, re_path

urlpatterns = [
    path('', include('app.urls')),
]
