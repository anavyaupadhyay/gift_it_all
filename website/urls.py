from django.urls import path

from website.views import HomePageView

app_name = 'website'
urlpatterns = [
  path("", HomePageView.as_view(), name='homepage'),
]