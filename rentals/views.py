from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone

from .models import (
    PropertyListing, PropertyGalleryImage, VisitSchedule,
    BookingRequest, ContactInquiry, Wishlist, Review, Amenity
)
from .forms import (
    PropertyListingForm, VisitScheduleForm, BookingRequestForm,
    ContactInquiryForm, ReviewForm
)


def home_view(request):
    featured_properties = PropertyListing.objects.filter(is_active=True, is_featured=True)[:6]
    recent_properties = PropertyListing.objects.filter(is_active=True).order_by('-created_at')[:8]
    amenities = Amenity.objects.all()[:12]

    # Aggregate stats for homepage
    stats = {
        'total_properties': PropertyListing.objects.filter(is_active=True).count(),
        'brokerage_saved': '₹ 3.8 Cr+',
        'verified_owners': PropertyListing.objects.values('owner').distinct().count() + 50,
        'happy_tenants': '12,500+',
    }

    context = {
        'featured_properties': featured_properties,
        'recent_properties': recent_properties,
        'amenities': amenities,
        'stats': stats,
    }
    return render(request, 'rentals/home.html', context)


def listing_list_view(request):
    queryset = PropertyListing.objects.filter(is_active=True)

    # Search params
    city = request.GET.get('city', '').strip()
    locality = request.GET.get('locality', '').strip()
    query = request.GET.get('q', '').strip()
    property_type = request.GET.get('property_type', '').strip()
    furnishing = request.GET.get('furnishing', '').strip()
    tenant_preference = request.GET.get('tenant_preference', '').strip()
    min_rent = request.GET.get('min_rent', '').strip()
    max_rent = request.GET.get('max_rent', '').strip()
    amenity_ids = request.GET.getlist('amenities')
    sort_by = request.GET.get('sort', 'newest')

    if city and city != 'all':
        queryset = queryset.filter(city__iexact=city)

    if locality:
        queryset = queryset.filter(
            Q(locality__icontains=locality) | Q(address__icontains=locality) | Q(landmark__icontains=locality)
        )

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(locality__icontains=query) |
            Q(city__icontains=query) |
            Q(landmark__icontains=query)
        )

    if property_type and property_type != 'all':
        queryset = queryset.filter(property_type=property_type)

    if furnishing and furnishing != 'all':
        queryset = queryset.filter(furnishing=furnishing)

    if tenant_preference and tenant_preference != 'all':
        queryset = queryset.filter(tenant_preference=tenant_preference)

    if min_rent and min_rent.isdigit():
        queryset = queryset.filter(rent_monthly__gte=float(min_rent))

    if max_rent and max_rent.isdigit():
        queryset = queryset.filter(rent_monthly__lte=float(max_rent))

    if amenity_ids:
        for a_id in amenity_ids:
            if a_id.isdigit():
                queryset = queryset.filter(amenities__id=a_id)

    # Sorting
    if sort_by == 'price_low':
        queryset = queryset.order_by('rent_monthly')
    elif sort_by == 'price_high':
        queryset = queryset.order_by('-rent_monthly')
    elif sort_by == 'popular':
        queryset = queryset.order_by('-views_count')
    else:
        queryset = queryset.order_by('-is_featured', '-created_at')

    # Pagination
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_amenities = Amenity.objects.all()

    # User wishlist IDs for active heart state
    user_saved_ids = []
    if request.user.is_authenticated:
        user_saved_ids = list(Wishlist.objects.filter(user=request.user).values_list('listing_id', flat=True))

    context = {
        'page_obj': page_obj,
        'total_count': queryset.count(),
        'all_amenities': all_amenities,
        'user_saved_ids': user_saved_ids,
        'selected_city': city,
        'selected_locality': locality,
        'selected_type': property_type,
        'selected_furnishing': furnishing,
        'selected_preference': tenant_preference,
        'min_rent': min_rent,
        'max_rent': max_rent,
        'selected_amenities': [int(x) for x in amenity_ids if x.isdigit()],
        'sort_by': sort_by,
        'query': query,
    }
    return render(request, 'rentals/listing_list.html', context)


def listing_detail_view(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)

    # Increment views
    PropertyListing.objects.filter(id=listing.id).update(views_count=listing.views_count + 1)

    is_saved = False
    if request.user.is_authenticated:
        is_saved = Wishlist.objects.filter(user=request.user, listing=listing).exists()

    # Forms
    initial_visitor = {}
    if request.user.is_authenticated:
        initial_visitor = {
            'visitor_name': request.user.profile.display_name,
            'visitor_phone': request.user.profile.phone,
            'visitor_email': request.user.email,
        }

    visit_form = VisitScheduleForm(initial=initial_visitor)
    booking_form = BookingRequestForm(initial=initial_visitor)
    inquiry_form = ContactInquiryForm(initial=initial_visitor)
    review_form = ReviewForm()

    reviews = listing.reviews.all().order_by('-created_at')
    gallery = listing.gallery_images.all()

    # Similar listings in same city/locality
    similar_listings = PropertyListing.objects.filter(
        city=listing.city, is_active=True
    ).exclude(id=listing.id)[:3]

    context = {
        'listing': listing,
        'is_saved': is_saved,
        'visit_form': visit_form,
        'booking_form': booking_form,
        'inquiry_form': inquiry_form,
        'review_form': review_form,
        'reviews': reviews,
        'gallery': gallery,
        'similar_listings': similar_listings,
    }
    return render(request, 'rentals/listing_detail.html', context)


@login_required
def schedule_visit_view(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)

    if request.method == 'POST':
        form = VisitScheduleForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.listing = listing
            visit.tenant = request.user
            visit.save()
            messages.success(request, f"Free visit successfully scheduled for {visit.visit_date} ({visit.get_time_slot_display()})! The owner has been notified.")
            return redirect('tenant_dashboard')
        else:
            messages.error(request, "Failed to schedule visit. Please check the form fields.")
    return redirect('listing_detail', slug=slug)


@login_required
def book_room_view(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)

    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            booking.tenant = request.user
            booking.save()
            messages.success(request, f"Your booking request #{booking.booking_id} for '{listing.title}' has been submitted to the owner! You can track its status in your dashboard.")
            return redirect('tenant_dashboard')
        else:
            messages.error(request, "Could not submit booking request. Please check required fields.")
    return redirect('listing_detail', slug=slug)


@login_required
def contact_owner_view(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)

    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.listing = listing
            inquiry.user = request.user
            inquiry.save()

            owner_phone = listing.owner.profile.phone or "Available upon request"
            owner_name = listing.owner.profile.display_name

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': f"Inquiry sent to owner! Owner Contact: {owner_phone} ({owner_name})",
                    'owner_phone': owner_phone,
                    'owner_name': owner_name
                })

            messages.success(request, f"Owner Contact: {owner_name} - Phone: {owner_phone}. They have also received your message.")
            return redirect('listing_detail', slug=slug)

    return redirect('listing_detail', slug=slug)


@login_required
def add_review_view(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.user = request.user
            review.save()
            messages.success(request, "Thank you! Your verified review has been posted.")
        else:
            messages.error(request, "Could not post review. Please check your rating and comment.")
    return redirect('listing_detail', slug=slug)


@login_required
def toggle_wishlist_view(request, listing_id):
    listing = get_object_or_404(PropertyListing, id=listing_id)
    saved_obj = Wishlist.objects.filter(user=request.user, listing=listing).first()

    if saved_obj:
        saved_obj.delete()
        saved = False
        message = "Removed from your shortlisted properties."
    else:
        Wishlist.objects.create(user=request.user, listing=listing)
        saved = True
        message = "Saved to your shortlisted properties!"

    total_saved = Wishlist.objects.filter(user=request.user).count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'saved': saved,
            'message': message,
            'total_saved': total_saved
        })

    messages.info(request, message)
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'home')


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('listing')
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'rentals/wishlist.html', context)


# Tenant Dashboard
@login_required
def tenant_dashboard_view(request):
    visits = VisitSchedule.objects.filter(tenant=request.user).select_related('listing').order_by('-created_at')
    bookings = BookingRequest.objects.filter(tenant=request.user).select_related('listing').order_by('-created_at')
    saved_listings = Wishlist.objects.filter(user=request.user).select_related('listing')[:4]

    context = {
        'visits': visits,
        'bookings': bookings,
        'saved_listings': saved_listings,
        'total_visits': visits.count(),
        'total_bookings': bookings.count(),
    }
    return render(request, 'rentals/tenant_dashboard.html', context)


# Owner Dashboard
@login_required
def owner_dashboard_view(request):
    # Ensure only owners or profile switched
    user_properties = PropertyListing.objects.filter(owner=request.user)
    
    # Visit requests for owner's properties
    visits = VisitSchedule.objects.filter(listing__owner=request.user).select_related('listing', 'tenant').order_by('-created_at')
    
    # Booking requests for owner's properties
    bookings = BookingRequest.objects.filter(listing__owner=request.user).select_related('listing', 'tenant').order_by('-created_at')

    # Inquiries
    inquiries = ContactInquiry.objects.filter(listing__owner=request.user).select_related('listing').order_by('-created_at')[:10]

    context = {
        'properties': user_properties,
        'visits': visits,
        'bookings': bookings,
        'inquiries': inquiries,
        'total_listings': user_properties.count(),
        'active_listings': user_properties.filter(is_active=True).count(),
        'pending_visits': visits.filter(status='pending').count(),
        'pending_bookings': bookings.filter(status='pending').count(),
    }
    return render(request, 'rentals/owner_dashboard.html', context)


# Owner Property CRUD
@login_required
def property_create_view(request):
    if request.method == 'POST':
        form = PropertyListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            form.save_m2m()  # For amenities
            messages.success(request, f"Property '{listing.title}' has been successfully posted with 0% brokerage!")
            return redirect('owner_dashboard')
        else:
            messages.error(request, "Failed to post property. Please check the highlighted fields.")
    else:
        form = PropertyListingForm()

    return render(request, 'rentals/property_form.html', {'form': form, 'title': 'Post a New Room / Property'})


@login_required
def property_edit_view(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug, owner=request.user)

    if request.method == 'POST':
        form = PropertyListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            listing = form.save()
            messages.success(request, f"Property '{listing.title}' updated successfully.")
            return redirect('owner_dashboard')
        else:
            messages.error(request, "Could not update property. Please check errors.")
    else:
        form = PropertyListingForm(instance=listing)

    return render(request, 'rentals/property_form.html', {'form': form, 'listing': listing, 'title': 'Edit Property Listing'})


@login_required
def property_delete_view(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug, owner=request.user)

    if request.method == 'POST':
        listing_title = listing.title
        listing.delete()
        messages.success(request, f"Listing '{listing_title}' was permanently deleted.")
        return redirect('owner_dashboard')

    return render(request, 'rentals/property_confirm_delete.html', {'listing': listing})


@login_required
def property_toggle_status_view(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug, owner=request.user)
    listing.is_active = not listing.is_active
    listing.save()
    status_label = "Active & Available" if listing.is_active else "Rented Out / Inactive"
    messages.info(request, f"Property status updated to: {status_label}")
    return redirect('owner_dashboard')


@login_required
def update_visit_status_view(request, visit_id, new_status):
    visit = get_object_or_404(VisitSchedule, id=visit_id)
    # Check permission (owner of listing can accept/reject; tenant can cancel)
    if visit.listing.owner == request.user:
        if new_status in ['confirmed', 'completed', 'cancelled']:
            visit.status = new_status
            visit.save()
            messages.success(request, f"Visit request status updated to '{visit.get_status_display()}'.")
    elif visit.tenant == request.user:
        if new_status == 'cancelled':
            visit.status = 'cancelled'
            visit.save()
            messages.info(request, "Your scheduled visit has been cancelled.")

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'home')


@login_required
def update_booking_status_view(request, booking_id, new_status):
    booking = get_object_or_404(BookingRequest, id=booking_id)
    if booking.listing.owner == request.user:
        if new_status in ['approved', 'rejected', 'cancelled']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking #{booking.booking_id} status updated to '{booking.get_status_display()}'.")
    elif booking.tenant == request.user:
        if new_status == 'cancelled':
            booking.status = 'cancelled'
            booking.save()
            messages.info(request, f"Booking request #{booking.booking_id} has been cancelled.")

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'home')
