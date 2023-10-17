from django.urls import path

from website.views import HomePageView, ProductListView

app_name = 'website'
urlpatterns = [
  path("", HomePageView.as_view(), name='homepage'),
  path("products/",ProductListView.as_view(), name='product_list'),
  path("products/<slug:slug>",ProductListView.as_view(), name='product_list_category'),
  path("products/<slug:slug>/detail",ProductListView.as_view(), name='product_detail'),
]