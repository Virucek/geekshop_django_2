from django.urls import path, re_path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/', adminapp.UsersListView.as_view(), name='users'),
    # path('users/', adminapp.users, name='users'),
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/edit/<int:pk>/', adminapp.UserEditView.as_view(), name='user_edit'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('categories/', adminapp.CategoriesListView.as_view(), name='categories'),
    path('categories/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('categories/edit/<int:pk>/', adminapp.CategoryEditView.as_view(), name='category_edit'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/category/<int:pk>/', adminapp.ProductsListView.as_view(), name='products'),
    path('products/category/<int:pk>/page/<int:page>/', adminapp.ProductsListView.as_view(), name='products_page'),
    path('products/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product'),
    path('products/create/category/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/edit/<int:pk>/', adminapp.ProductEditView.as_view(), name='product_edit'),
    path('products/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),

    path('merchtypes/', adminapp.MerchTypesListView.as_view(), name='merch_types'),
    path('merchtypes/create/', adminapp.MerchTypeCreateView.as_view(), name='merch_type_create'),
    path('merchtypes/edit/<int:pk>/', adminapp.MerchTypeEditView.as_view(), name='merch_type_edit'),
    path('merchtypes/delete/<int:pk>/', adminapp.MerchTypeDeleteView.as_view(), name='merch_type_delete'),

    path('orders/', adminapp.OrdersListView.as_view(), name='orders'),
    path('orders/create/', adminapp.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', adminapp.OrderDetailView.as_view(), name='order_detail'),
    path('orders/edit/<int:pk>/', adminapp.OrderUpdateView.as_view(), name='order_update'),
    path('orders/delete/<int:pk>/', adminapp.OrderDeleteView.as_view(), name='order_delete'),
    re_path(r'^orders/(?P<pk>\d+)/status/next/$', adminapp.order_status_next, name='order_status_next'),
    re_path(r'^orders/(?P<pk>\d+)/cancel/$', adminapp.order_cancel_customer, name='order_cancel_customer'),

    path('discounts/', adminapp.DiscountsListView.as_view(), name='discounts'),
    path('discounts/create/', adminapp.DiscountCreateView.as_view(), name='discount_create'),
    path('discounts/<int:pk>/', adminapp.DiscountDetailView.as_view(), name='discount_detail'),
    path('discounts/edit/<int:pk>/', adminapp.DiscountUpdateView.as_view(), name='discount_update'),
    path('discounts/delete/<int:pk>/', adminapp.DiscountDeleteView.as_view(), name='discount_delete'),
]
