from django.urls import path
from apps.settings.views import HelloAPIView

urlpatterns = [
    path("", HelloAPIView.as_view(), name="hello")
]