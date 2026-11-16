from .models import Wishlist, VisitSchedule, BookingRequest, PropertyListing

def global_context(request):
    context = {
        'POPULAR_CITIES': [
            'Bangalore', 'Mumbai', 'Pune', 'Delhi NCR', 'Hyderabad', 'Chennai'
        ],
        'PROPERTY_TYPES': PropertyListing.PROPERTY_TYPE_CHOICES,
        'saved_count': 0,
        'pending_visits_count': 0,
        'pending_bookings_count': 0,
    }

    if request.user.is_authenticated:
        context['saved_count'] = Wishlist.objects.filter(user=request.user).count()
        
        # If user is owner, count pending visits & bookings on their properties
        if hasattr(request.user, 'profile') and request.user.profile.role == 'owner':
            context['pending_visits_count'] = VisitSchedule.objects.filter(
                listing__owner=request.user, status='pending'
            ).count()
            context['pending_bookings_count'] = BookingRequest.objects.filter(
                listing__owner=request.user, status='pending'
            ).count()
        else:
            # Tenant's active visits and bookings
            context['my_visits_count'] = VisitSchedule.objects.filter(tenant=request.user).count()
            context['my_bookings_count'] = BookingRequest.objects.filter(tenant=request.user).count()

    return context
