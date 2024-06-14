from django.contrib import admin
from django.urls import path, include
from App1.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("App1.urls")),
    path('login/', include("App1.urls")),
    path('register/', include("App1.urls")),
    path('user/', include("App1.urls")),
]
