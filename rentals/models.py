import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Amenity(models.Model):
    CATEGORY_CHOICES = (
        ('essentials', 'Essentials'),
        ('comfort', 'Comfort & Luxury'),
        ('safety', 'Safety & Security'),
        ('convenience', 'Convenience & Services'),
    )

    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(max_length=50, default='fa-check', help_text="FontAwesome icon class e.g. fa-wifi")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='essentials')

    class Meta:
        verbose_name_plural = 'Amenities'
        ordering = ['name']

    def __str__(self):
        return self.name


class PropertyListing(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('single_room', 'Single Private Room'),
        ('shared_room', 'Shared Room / PG Bed'),
        ('1bhk', '1 BHK Apartment'),
        ('2bhk', '2 BHK Apartment'),
        ('3bhk', '3 BHK Apartment'),
        ('studio', 'Studio Apartment'),
        ('house', 'Independent House / Villa'),
    )

    FURNISHING_CHOICES = (
        ('fully_furnished', 'Fully Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    )

    TENANT_PREFERENCE_CHOICES = (
        ('anyone', 'Anyone (Bachelors / Family)'),
        ('bachelors_male', 'Male Bachelors Only'),
        ('bachelors_female', 'Female Bachelors Only'),
        ('family', 'Family Only'),
        ('company_lease', 'Company Lease / Working Execs'),
    )

    BATHROOM_TYPE_CHOICES = (
        ('attached', 'Attached Washroom'),
        ('shared', 'Shared Washroom'),
    )

    FOOD_CHOICES = (
        ('none', 'Self-Cooking / No Food'),
        ('included', 'Meals Included (Breakfast & Dinner)'),
        ('available', 'Meal Subscription Available'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPE_CHOICES, default='single_room')
    furnishing = models.CharField(max_length=30, choices=FURNISHING_CHOICES, default='fully_furnished')
    tenant_preference = models.CharField(max_length=30, choices=TENANT_PREFERENCE_CHOICES, default='anyone')
    bathroom_type = models.CharField(max_length=20, choices=BATHROOM_TYPE_CHOICES, default='attached')
    food_availability = models.CharField(max_length=20, choices=FOOD_CHOICES, default='none')

    rent_monthly = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monthly Rent in ₹")
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, help_text="Security Deposit in ₹")
    maintenance_monthly = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Maintenance in ₹ (0 if included)")
    available_from = models.DateField(help_text="Available from date")
    minimum_lease_months = models.PositiveIntegerField(default=3, help_text="Lock-in / Minimum stay period in months")
    notice_period_days = models.PositiveIntegerField(default=30)

    floor = models.IntegerField(default=1)
    total_floors = models.IntegerField(default=3)
    area_sqft = models.PositiveIntegerField(default=250, help_text="Carpet Area in Sq.Ft.")

    city = models.CharField(max_length=100, default='Bangalore')
    locality = models.CharField(max_length=150, help_text="e.g. Koramangala 4th Block, Indiranagar, etc.")
    address = models.TextField(help_text="Complete building and street address")
    landmark = models.CharField(max_length=200, blank=True, help_text="Nearby metro, mall, or landmark")

    description = models.TextField()
    house_rules = models.TextField(blank=True, help_text="e.g. Gate closes at 11 PM, smoking prohibited inside, guests allowed on weekends")

    primary_image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    primary_image_url = models.URLField(blank=True, help_text="Fallback or direct image URL")

    is_verified = models.BooleanField(default=True, help_text="Direct Owner Listing / Zero Brokerage Verified")
    is_active = models.BooleanField(default=True, help_text="Listing is visible and available for booking")
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name='listings')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.locality}, {self.city} (₹{int(self.rent_monthly)}/mo)"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.locality}-{self.city}")
            slug = base_slug
            counter = 1
            while PropertyListing.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'slug': self.slug})

    @property
    def display_image(self):
        if self.primary_image:
            return self.primary_image.url
        if self.primary_image_url:
            return self.primary_image_url
        return 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80'

    @property
    def total_monthly_cost(self):
        return self.rent_monthly + self.maintenance_monthly

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 4.8  # Default positive score for new listings


class PropertyGalleryImage(models.Model):
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='property_gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    caption = models.CharField(max_length=100, blank=True)

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url


class VisitSchedule(models.Model):
    TIME_SLOT_CHOICES = (
        ('morning', 'Morning (09:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:00 PM - 04:00 PM)'),
        ('evening', 'Evening (04:00 PM - 08:00 PM)'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('confirmed', 'Confirmed by Owner'),
        ('completed', 'Visit Completed'),
        ('cancelled', 'Cancelled'),
    )

    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='visit_schedules')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_visits')
    visitor_name = models.CharField(max_length=100)
    visitor_phone = models.CharField(max_length=20)
    visitor_email = models.EmailField(blank=True)
    visit_date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES, default='morning')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tenant_note = models.TextField(blank=True)
    owner_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_date', '-created_at']

    def __str__(self):
        return f"Visit for {self.listing.title} on {self.visit_date} by {self.visitor_name}"


class BookingRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Under Owner Review'),
        ('approved', 'Approved & Reserved'),
        ('rejected', 'Declined by Owner'),
        ('cancelled', 'Cancelled by Tenant'),
    )

    PAYMENT_CHOICES = (
        ('pay_on_movein', 'Pay Token Upon Visit / Agreement'),
        ('prepaid_token', 'Simulated Token Paid (₹1,000)'),
    )

    booking_id = models.CharField(max_length=20, unique=True, blank=True)
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='booking_requests')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_room_bookings')
    applicant_name = models.CharField(max_length=100)
    applicant_phone = models.CharField(max_length=20)
    expected_move_in = models.DateField()
    duration_months = models.PositiveIntegerField(default=6)
    occupants_count = models.PositiveIntegerField(default=1)
    token_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    payment_status = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='pay_on_movein')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"NB-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.booking_id} for {self.listing.title} by {self.applicant_name}"


class ContactInquiry(models.Model):
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='contact_inquiries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_requests')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact request for {self.listing.title} from {self.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.listing.title}"


class Review(models.Model):
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.listing.title} ({self.rating}★)"
