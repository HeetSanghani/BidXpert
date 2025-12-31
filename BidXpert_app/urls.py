from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import (
    index,
    register_view, login_view, logout_view,
    profile, dashboard, contact_view, about_us,
    category_products, product_list,
    product, product_view, productdelete, productupdate, delete_product_image,
    bids, users,
    categories_view, category, categoriesdelete, categoriesupdate,
    admin_messages_view, delete_message,
    bid_view, place_bid_ajax
)

urlpatterns = [
    # Home Page
    path('', index, name="index"),
    path('dashboard/', dashboard, name="dashboard"),
    
    
    # User Profile
    path('profile/', profile, name='profile'),

    # _______________________________ USER SIDE _________________________________
    path('register/', register_view, name='register'),
    path('register/admin/', views.register_admin, name='register_admin'),
    
    path('login/', login_view, name='login'),
    
    path('logout/', logout_view, name='logout'),

    # _____________________________ END USER SIDE ________________________________
    
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('categories/', views.browse_categories, name='browse_categories'),


    # Static Pages
    path('contact/', contact_view, name='contact'),
    path('about_us/', about_us, name="about_us"),

    # Product Listings and Bidding
    path('products/', product_list, name='product_list'),
    path('bid/<int:product_id>/', bid_view, name='bid_view'), # Shows the bidding page
    path('bid/<int:product_id>/ajax/', place_bid_ajax, name='place_bid_ajax'),  # Handles AJAX POST
    path('my-bids/', views.user_bids_view, name='user_bids'),
    
    #payment
    path('pay/', views.initiate_payment, name='initiate_payment'),


    # _____________________________ ADMIN SIDE _________________________________
    path('category/', category, name="category"),
    path('categories_view/', categories_view, name="categories_view"),
    path('categoriesdelete/<int:id>/', categoriesdelete, name='categoriesdelete'),
    path('categoriesupdate/<int:id>/', categoriesupdate, name='categoriesupdate'),

    path('product/', product, name="product"),
    path('product_view/', product_view, name="product_view"),
    path('productdelete/<int:id>/', productdelete, name='productdelete'),
    path('productupdate/<int:id>/', productupdate, name='productupdate'),
    path('delete-product-image/<int:id>/', delete_product_image, name='delete_product_image'),

    path('bids/', views.bids, name="bids"),
    path('users/', users, name="users"),
    path('ended-auctions/', views.ended_auctions_view, name='ended_auctions'),


    # Admin Messages
    path('admin_messages/', admin_messages_view, name='admin_messages'),
    path('admin_messages/delete/<int:pk>/', delete_message, name='delete_message'),


]
# Development media/static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
