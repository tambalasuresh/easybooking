from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import PropertyListing, Amenity, VisitSchedule, BookingRequest, Wishlist, Review


class EasyBookingFlowTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Owner
        self.owner = User.objects.create_user(username='test_owner', password='password123', email='owner@test.com')
        self.owner.profile.role = 'owner'
        self.owner.profile.phone = '9876543210'
        self.owner.profile.city = 'Bangalore'
        self.owner.profile.save()

        # Create Tenant
        self.tenant = User.objects.create_user(username='test_tenant', password='password123', email='tenant@test.com')
        self.tenant.profile.role = 'tenant'
        self.tenant.profile.phone = '9812345678'
        self.tenant.profile.save()

        # Amenities
        self.wifi = Amenity.objects.create(name='High-speed Wi-Fi', icon='fa-wifi', category='essentials')
        self.ac = Amenity.objects.create(name='Air Conditioning', icon='fa-snowflake', category='comfort')

        # Property Listing
        self.property = PropertyListing.objects.create(
            owner=self.owner,
            title='Spacious Single Room in Koramangala',
            property_type='single_room',
            furnishing='fully_furnished',
            tenant_preference='anyone',
            bathroom_type='attached',
            food_availability='none',
            rent_monthly=12000,
            security_deposit=24000,
            maintenance_monthly=500,
            available_from=date.today(),
            area_sqft=250,
            city='Bangalore',
            locality='Koramangala 4th Block',
            address='123, 4th Cross, Koramangala',
            landmark='Near Sony Signal',
            description='Direct owner spacious room with zero brokerage.',
            is_active=True
        )
        self.property.amenities.add(self.wifi, self.ac)

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EasyBooking')
        self.assertContains(response, 'Zero Brokerage')
        self.assertContains(response, 'Spacious Single Room in Koramangala')

    def test_listing_search_and_filter(self):
        # Search by city
        response = self.client.get(reverse('listing_list'), {'city': 'Bangalore'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spacious Single Room')

        # Search with mismatch
        response2 = self.client.get(reverse('listing_list'), {'city': 'Delhi'})
        self.assertNotContains(response2, 'Spacious Single Room')

    def test_listing_detail_view(self):
        response = self.client.get(self.property.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spacious Single Room in Koramangala')
        self.assertContains(response, 'Schedule Free Visit')
        self.assertContains(response, 'Book Room / Token Lock')

    def test_schedule_visit_workflow(self):
        self.client.login(username='test_tenant', password='password123')
        post_data = {
            'visitor_name': 'Test Tenant',
            'visitor_phone': '9812345678',
            'visitor_email': 'tenant@test.com',
            'visit_date': (date.today() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'time_slot': 'morning',
            'tenant_note': 'Looking forward to visiting.'
        }
        response = self.client.post(
            reverse('schedule_visit', kwargs={'slug': self.property.slug}),
            data=post_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(VisitSchedule.objects.filter(tenant=self.tenant, listing=self.property).exists())

    def test_booking_request_workflow(self):
        self.client.login(username='test_tenant', password='password123')
        post_data = {
            'applicant_name': 'Test Tenant',
            'applicant_phone': '9812345678',
            'expected_move_in': (date.today() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'duration_months': 6,
            'occupants_count': 1,
            'payment_status': 'prepaid_token',
            'message': 'Software engineer relocating.'
        }
        response = self.client.post(
            reverse('book_room', kwargs={'slug': self.property.slug}),
            data=post_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(BookingRequest.objects.filter(tenant=self.tenant, listing=self.property).exists())

    def test_wishlist_toggle(self):
        self.client.login(username='test_tenant', password='password123')
        response = self.client.get(reverse('toggle_wishlist', kwargs={'listing_id': self.property.id}))
        self.assertTrue(Wishlist.objects.filter(user=self.tenant, listing=self.property).exists())

        # Toggle again to remove
        response2 = self.client.get(reverse('toggle_wishlist', kwargs={'listing_id': self.property.id}))
        self.assertFalse(Wishlist.objects.filter(user=self.tenant, listing=self.property).exists())

    def test_owner_dashboard(self):
        self.client.login(username='test_owner', password='password123')
        response = self.client.get(reverse('owner_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Property Owner Dashboard')
        self.assertContains(response, self.property.title)
