from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page),
    path('product/<int:pk>', views.get_exact_pr),
    path('category/<int:pk>', views.get_exact_category),
    path('add-to-cart/<int:pk>', views.to_cart),
    path('del-from-cart/<int:pk>', views.del_from_cart),
    path('cart', views.get_user_cart),
    path('search', views.search_product),
    path('register', views.Register.as_view()),
    path('logout', views.logout_view),
]
