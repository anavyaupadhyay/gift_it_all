from django.urls import path, include

from website.views import HomePageView, ProductListView
from oscar.apps.basket import views as basket_views

app_name = 'website'
urlpatterns = [
  path("", HomePageView.as_view(), name='homepage'),
  path("products/",ProductListView.as_view(), name='product_list'),
  path("products/<slug:slug>",ProductListView.as_view(), name='product_list_category'),
  path("products/<slug:slug>/detail",ProductListView.as_view(), name='product_detail'),
  path('basket/add/<int:product_id>/', basket_views.BasketAddView.as_view(), name='basket-add'),
  # path('basket/remove/<int:line_id>/', basket_views.BasketRe, name='basket-remove'),
  path('basket/summary/', basket_views.BasketView.as_view(), name='basket-summary'),
  path("api/", include("website.api.urls")),
]