from django import forms
from .models import PropertyListing, VisitSchedule, BookingRequest, ContactInquiry, Review, Amenity


class PropertyListingForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'amenity-checkbox'}),
        required=False
    )

    class Meta:
        model = PropertyListing
        fields = [
            'title', 'property_type', 'furnishing', 'tenant_preference',
            'bathroom_type', 'food_availability',
            'rent_monthly', 'security_deposit', 'maintenance_monthly',
            'available_from', 'minimum_lease_months', 'notice_period_days',
            'area_sqft', 'floor', 'total_floors',
            'city', 'locality', 'address', 'landmark',
            'description', 'house_rules',
            'primary_image', 'primary_image_url',
            'amenities', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Spacious 1 BHK / Private Room with Attached Balcony & AC',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'property_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'furnishing': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'tenant_preference': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'bathroom_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'food_availability': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'rent_monthly': forms.NumberInput(attrs={
                'placeholder': 'Monthly rent (₹)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'security_deposit': forms.NumberInput(attrs={
                'placeholder': 'Security deposit (₹)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'maintenance_monthly': forms.NumberInput(attrs={
                'placeholder': '0 if included in rent',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'available_from': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'minimum_lease_months': forms.NumberInput(attrs={
                'placeholder': 'e.g. 3',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'notice_period_days': forms.NumberInput(attrs={
                'placeholder': 'e.g. 30',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'area_sqft': forms.NumberInput(attrs={
                'placeholder': 'Sq.Ft.',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'floor': forms.NumberInput(attrs={
                'placeholder': 'Floor (e.g. 2)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'total_floors': forms.NumberInput(attrs={
                'placeholder': 'Total floors (e.g. 4)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'City (e.g. Bangalore, Mumbai)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'locality': forms.TextInput(attrs={
                'placeholder': 'Locality / Area (e.g. Koramangala 5th Block)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'address': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Building name, flat number, street name',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'landmark': forms.TextInput(attrs={
                'placeholder': 'Nearby landmark (e.g. Opposite Forum Mall / Metro)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your room / property, special features, ventilation, nearby transport...',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'house_rules': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Any specific house rules (e.g. quiet hours after 10 PM, visitors allowed, etc.)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'primary_image': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'
            }),
            'primary_image_url': forms.URLInput(attrs={
                'placeholder': 'Or paste image URL (Unsplash, CDN, etc.)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 rounded border-slate-300 focus:ring-red-500'
            }),
        }


class VisitScheduleForm(forms.ModelForm):
    class Meta:
        model = VisitSchedule
        fields = ['visitor_name', 'visitor_phone', 'visitor_email', 'visit_date', 'time_slot', 'tenant_note']
        widgets = {
            'visitor_name': forms.TextInput(attrs={
                'placeholder': 'Your Full Name',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'visitor_phone': forms.TextInput(attrs={
                'placeholder': '10-digit Mobile Number',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'visitor_email': forms.EmailInput(attrs={
                'placeholder': 'Email Address (Optional)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'visit_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'time_slot': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'tenant_note': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Any question or message for the owner before the visit...',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
        }


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['applicant_name', 'applicant_phone', 'expected_move_in', 'duration_months', 'occupants_count', 'payment_status', 'message']
        widgets = {
            'applicant_name': forms.TextInput(attrs={
                'placeholder': 'Your Full Name',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'applicant_phone': forms.TextInput(attrs={
                'placeholder': 'Mobile Number',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'expected_move_in': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'duration_months': forms.NumberInput(attrs={
                'min': 1, 'max': 36,
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'occupants_count': forms.NumberInput(attrs={
                'min': 1, 'max': 10,
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Briefly describe your occupation, company/college, or special requirements...',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
        }


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Mobile Number',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address (Optional)',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Hi, I am interested in your property listed on EasyBooking. Please let me know when we can connect.',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(5, '5 Stars - Outstanding'), (4, '4 Stars - Very Good'), (3, '3 Stars - Average'), (2, '2 Stars - Poor'), (1, '1 Star - Terrible')],
                attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'}
            ),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your feedback regarding the room, amenities, and interaction with the owner...',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'
            }),
        }
