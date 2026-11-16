from django.contrib import admin
from .models import Amenity, PropertyListing, PropertyGalleryImage, VisitSchedule, BookingRequest, ContactInquiry, Wishlist, Review


class PropertyGalleryImageInline(admin.TabularInline):
    model = PropertyGalleryImage
    extra = 2


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(PropertyListing)
class PropertyListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'property_type', 'city', 'locality', 'rent_monthly', 'is_active', 'is_verified', 'is_featured', 'created_at')
    list_filter = ('property_type', 'furnishing', 'city', 'is_active', 'is_verified', 'is_featured')
    search_fields = ('title', 'locality', 'city', 'address', 'owner__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyGalleryImageInline]


@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ('listing', 'tenant', 'visitor_name', 'visitor_phone', 'visit_date', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'time_slot', 'visit_date')
    search_fields = ('listing__title', 'visitor_name', 'visitor_phone')


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'listing', 'tenant', 'applicant_name', 'expected_move_in', 'duration_months', 'status', 'payment_status')
    list_filter = ('status', 'payment_status')
    search_fields = ('booking_id', 'listing__title', 'applicant_name', 'applicant_phone')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'name', 'phone', 'created_at')
    search_fields = ('listing__title', 'name', 'phone', 'email')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'created_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
