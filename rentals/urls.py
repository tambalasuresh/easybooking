from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('listings/', views.listing_list_view, name='listing_list'),
    path('listings/<slug:slug>/', views.listing_detail_view, name='listing_detail'),
    path('listings/<slug:slug>/schedule-visit/', views.schedule_visit_view, name='schedule_visit'),
    path('listings/<slug:slug>/book-room/', views.book_room_view, name='book_room'),
    path('listings/<slug:slug>/contact-owner/', views.contact_owner_view, name='contact_owner'),
    path('listings/<slug:slug>/add-review/', views.add_review_view, name='add_review'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:listing_id>/', views.toggle_wishlist_view, name='toggle_wishlist'),

    # Dashboards
    path('dashboard/tenant/', views.tenant_dashboard_view, name='tenant_dashboard'),
    path('dashboard/owner/', views.owner_dashboard_view, name='owner_dashboard'),

    # Property Owner Operations
    path('property/post-new/', views.property_create_view, name='property_create'),
    path('property/<slug:slug>/edit/', views.property_edit_view, name='property_edit'),
    path('property/<slug:slug>/delete/', views.property_delete_view, name='property_delete'),
    path('property/<slug:slug>/toggle-status/', views.property_toggle_status_view, name='property_toggle_status'),

    # Status updates
    path('visits/<int:visit_id>/status/<str:new_status>/', views.update_visit_status_view, name='update_visit_status'),
    path('bookings/<int:booking_id>/status/<str:new_status>/', views.update_booking_status_view, name='update_booking_status'),
]
