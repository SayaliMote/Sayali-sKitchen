from django.urls import path
from . import views  # Import views

app_name = 'shop'  # Ensure your app has a namespace

urlpatterns = [
    path('', views.prod_list, name='all_products'),
    path('filtered-products/', views.filtered_products, name='filtered_products'),  # ADD THIS LINE
    path('<uuid:type_id>/', views.prod_list, name='products_by_type'),
    path('<uuid:type_id>/<uuid:product_id>/', views.product_detail, name='product_detail'),
]
