import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easybooking_core.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from rentals.models import Amenity, PropertyListing, PropertyGalleryImage, Review, VisitSchedule, BookingRequest

def run_seed():
    print("🌱 Starting EasyBooking database seeding...")

    # 1. Create Superuser / Admin
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@easybooking.com', 'first_name': 'Admin', 'last_name': 'Super'})
    if created:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        admin_user.profile.role = 'owner'
        admin_user.profile.phone = '+91 98765 43210'
        admin_user.profile.is_verified_owner = True
        admin_user.profile.save()
        print("✅ Superuser created: admin / admin123")
    else:
        print("ℹ️ Superuser already exists.")

    # 2. Create Amenities
    amenities_data = [
        ("High-speed Wi-Fi", "fa-wifi", "essentials"),
        ("Air Conditioning", "fa-snowflake", "comfort"),
        ("Attached Bathroom", "fa-bath", "essentials"),
        ("Power Backup / Inverter", "fa-bolt", "essentials"),
        ("Washing Machine", "fa-shirt", "essentials"),
        ("Geyser / Hot Water", "fa-shower", "essentials"),
        ("RO Water Purifier", "fa-faucet-drip", "essentials"),
        ("Refrigerator", "fa-box-archive", "essentials"),
        ("Smart LED TV", "fa-tv", "comfort"),
        ("Reserved Parking", "fa-square-parking", "convenience"),
        ("24x7 CCTV & Security", "fa-shield-halved", "safety"),
        ("Daily Housekeeping", "fa-broom", "convenience"),
        ("Private Balcony", "fa-mountain-sun", "comfort"),
        ("Elevator / Lift", "fa-elevator", "convenience"),
        ("Wardrobe & Study Table", "fa-door-closed", "essentials"),
        ("Nutritious Meals Included", "fa-utensils", "convenience"),
        ("Fitness Gym Access", "fa-dumbbell", "comfort"),
    ]

    amenity_objs = {}
    for name, icon, cat in amenities_data:
        obj, _ = Amenity.objects.get_or_create(name=name, defaults={'icon': icon, 'category': cat})
        amenity_objs[name] = obj
    print(f"✅ {len(amenity_objs)} Amenities created.")

    # 3. Create Sample Owners & Tenants
    def get_or_create_user(uname, fname, lname, email, role, phone, city, is_verified=False):
        u, was_created = User.objects.get_or_create(username=uname, defaults={
            'first_name': fname,
            'last_name': lname,
            'email': email
        })
        if was_created:
            u.set_password('demo1234')
            u.save()
            u.profile.role = role
            u.profile.phone = phone
            u.profile.city = city
            u.profile.is_verified_owner = is_verified
            u.profile.bio = f"{role.title()} on EasyBooking directly connecting without intermediaries."
            u.profile.save()
        return u

    owner1 = get_or_create_user('rajesh_sharma', 'Rajesh', 'Sharma', 'rajesh@example.com', 'owner', '+91 98450 11223', 'Bangalore', True)
    owner2 = get_or_create_user('priya_menon', 'Priya', 'Menon', 'priya@example.com', 'owner', '+91 97410 44556', 'Bangalore', True)
    owner3 = get_or_create_user('vikram_patel', 'Vikram', 'Patel', 'vikram@example.com', 'owner', '+91 98200 77889', 'Mumbai', True)
    owner4 = get_or_create_user('suresh_kumar', 'Suresh', 'Kumar', 'suresh@example.com', 'owner', '+91 98840 99001', 'Pune', True)

    tenant1 = get_or_create_user('arjun_verma', 'Arjun', 'Verma', 'arjun@example.com', 'tenant', '+91 99112 33445', 'Bangalore', False)
    tenant2 = get_or_create_user('sneha_rao', 'Sneha', 'Rao', 'sneha@example.com', 'tenant', '+91 99887 66554', 'Bangalore', False)

    print("✅ Demo users created (all passwords: demo1234).")

    # 4. Property Listings
    listings_data = [
        {
            'owner': owner1,
            'title': "Luxury Furnished Private Room with Balcony & AC in Koramangala",
            'property_type': 'single_room',
            'furnishing': 'fully_furnished',
            'tenant_preference': 'anyone',
            'bathroom_type': 'attached',
            'food_availability': 'available',
            'rent_monthly': 14500,
            'security_deposit': 25000,
            'maintenance_monthly': 500,
            'available_from': date.today(),
            'minimum_lease_months': 3,
            'notice_period_days': 30,
            'area_sqft': 280,
            'floor': 2,
            'total_floors': 4,
            'city': 'Bangalore',
            'locality': 'Koramangala 4th Block',
            'address': '#42, 7th Main, 4th Block, Near Sony World Signal',
            'landmark': '5 mins from Sony World Junction & Forum Mall',
            'description': "Zero brokerage direct owner room! Premium independent spacious private room with wooden flooring, split AC, attached bathroom with geyser, private balcony with green views, and king-size bed with mattress. Shared modern modular kitchen and high-speed fiber internet.",
            'house_rules': "Quiet hours 11:00 PM onwards. Smoking strictly restricted to balcony. Visitors allowed during daytime.",
            'primary_image_url': 'https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
            'amenities_list': ["High-speed Wi-Fi", "Air Conditioning", "Attached Bathroom", "Power Backup / Inverter", "Washing Machine", "Geyser / Hot Water", "RO Water Purifier", "Refrigerator", "Private Balcony", "24x7 CCTV & Security", "Daily Housekeeping"]
        },
        {
            'owner': owner2,
            'title': "Spacious Modern 1 BHK Flat near Metro Station in Indiranagar",
            'property_type': '1bhk',
            'furnishing': 'fully_furnished',
            'tenant_preference': 'anyone',
            'bathroom_type': 'attached',
            'food_availability': 'none',
            'rent_monthly': 26000,
            'security_deposit': 50000,
            'maintenance_monthly': 1200,
            'available_from': date.today() + timedelta(days=5),
            'minimum_lease_months': 6,
            'notice_period_days': 30,
            'area_sqft': 650,
            'floor': 3,
            'total_floors': 5,
            'city': 'Bangalore',
            'locality': 'Indiranagar 100ft Road',
            'address': 'Plot 18, 12th Cross, Behind Toit, Indiranagar',
            'landmark': 'Walking distance from Indiranagar Metro Station',
            'description': "Beautifully architected 1 BHK full apartment for rent directly by owner. Features modern open kitchen, brand new sofa set, 43-inch 4K Smart TV, washing machine, double-door fridge, covered bike and car parking, and 24-hr Cauvery water supply.",
            'house_rules': "Family or working professionals preferred. Pets welcome with prior intimation.",
            'primary_image_url': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
            'amenities_list': ["High-speed Wi-Fi", "Air Conditioning", "Smart LED TV", "Attached Bathroom", "Power Backup / Inverter", "Washing Machine", "Refrigerator", "Reserved Parking", "Elevator / Lift", "24x7 CCTV & Security"]
        },
        {
            'owner': owner1,
            'title': "Co-Living Single Room with Homely Food & Housekeeping in HSR",
            'property_type': 'single_room',
            'furnishing': 'fully_furnished',
            'tenant_preference': 'bachelors_female',
            'bathroom_type': 'attached',
            'food_availability': 'included',
            'rent_monthly': 16000,
            'security_deposit': 16000,
            'maintenance_monthly': 0,
            'available_from': date.today(),
            'minimum_lease_months': 2,
            'notice_period_days': 15,
            'area_sqft': 220,
            'floor': 1,
            'total_floors': 3,
            'city': 'Bangalore',
            'locality': 'HSR Layout Sector 2',
            'address': 'Building 88, 27th Main Road, HSR Sector 2',
            'landmark': 'Near NIFT Campus & BDA Complex',
            'description': "Safe and comfortable premium co-living room for girls. Daily home-cooked North & South Indian breakfast and dinner included in rent! High-speed 300 Mbps Wi-Fi, biometric entry, CCTV surveillance, and regular professional housekeeping.",
            'house_rules': "Girls only. Biometric gate closes at 11:30 PM. No drinking or smoking inside premises.",
            'primary_image_url': 'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
            'amenities_list': ["Nutritious Meals Included", "High-speed Wi-Fi", "Attached Bathroom", "Daily Housekeeping", "Power Backup / Inverter", "RO Water Purifier", "Washing Machine", "24x7 CCTV & Security", "Wardrobe & Study Table"]
        },
        {
            'owner': owner3,
            'title': "Stunning Sea-Breeze 2 BHK Flat in Powai with Lake View",
            'property_type': '2bhk',
            'furnishing': 'semi_furnished',
            'tenant_preference': 'family',
            'bathroom_type': 'attached',
            'food_availability': 'none',
            'rent_monthly': 48000,
            'security_deposit': 100000,
            'maintenance_monthly': 3000,
            'available_from': date.today() + timedelta(days=10),
            'minimum_lease_months': 11,
            'notice_period_days': 45,
            'area_sqft': 950,
            'floor': 8,
            'total_floors': 16,
            'city': 'Mumbai',
            'locality': 'Powai Hiranandani',
            'address': 'Tower B, Glen Heights, Hiranandani Gardens, Powai',
            'landmark': 'Next to Powai Lake & Galleria Shopping Mall',
            'description': "Expansive 2 BHK apartment with scenic lake view directly available from owner. Equipped with modular kitchen with piped gas, wardrobes in both bedrooms, premium bathroom fittings, clubhouse and swimming pool access, and reserved stilt parking.",
            'house_rules': "Registered agreement for 11 months. Society norms apply.",
            'primary_image_url': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
            'amenities_list': ["Reserved Parking", "Elevator / Lift", "Fitness Gym Access", "24x7 CCTV & Security", "Power Backup / Inverter", "Private Balcony"]
        },
        {
            'owner': owner3,
            'title': "Budget Single Room in 3 BHK Shared Apartment in Andheri West",
            'property_type': 'single_room',
            'furnishing': 'fully_furnished',
            'tenant_preference': 'bachelors_male',
            'bathroom_type': 'shared',
            'food_availability': 'available',
            'rent_monthly': 17500,
            'security_deposit': 30000,
            'maintenance_monthly': 800,
            'available_from': date.today(),
            'minimum_lease_months': 3,
            'notice_period_days': 30,
            'area_sqft': 190,
            'floor': 4,
            'total_floors': 7,
            'city': 'Mumbai',
            'locality': 'Andheri West Lokhandwala',
            'address': 'Gulmohar Enclave, Near Lokhandwala Complex',
            'landmark': '3 mins from DN Nagar Metro Station',
            'description': "Zero brokerage private room in a vibrant 3BHK flat shared with 2 IT professionals. Comes with AC, single bed, orthopaedic mattress, large closet, and shared washing machine and kitchen.",
            'house_rules': "Working professionals only. Chill flatmates, neat and clean living expected.",
            'primary_image_url': 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=80',
            'is_featured': False,
            'amenities_list': ["Air Conditioning", "High-speed Wi-Fi", "Washing Machine", "Refrigerator", "Elevator / Lift", "Wardrobe & Study Table"]
        },
        {
            'owner': owner4,
            'title': "Cozy Studio Apartment for Techies near Hinjewadi Phase 1",
            'property_type': 'studio',
            'furnishing': 'fully_furnished',
            'tenant_preference': 'anyone',
            'bathroom_type': 'attached',
            'food_availability': 'none',
            'rent_monthly': 13000,
            'security_deposit': 25000,
            'maintenance_monthly': 600,
            'available_from': date.today(),
            'minimum_lease_months': 3,
            'notice_period_days': 30,
            'area_sqft': 350,
            'floor': 2,
            'total_floors': 4,
            'city': 'Pune',
            'locality': 'Hinjewadi Phase 1',
            'address': 'Silver Oaks Residency, Near Infosys Circle, Hinjewadi',
            'landmark': '5 mins drive from Wipro & Infosys Campus',
            'description': "Ideal studio apartment for IT executives working in Hinjewadi. Self-contained kitchenette with induction stove and mini fridge, dedicated work desk with ergonomic chair, high-speed fiber internet, and inverter backup.",
            'house_rules': "Comfortable living for singles or young couples. 24x7 gate security.",
            'primary_image_url': 'https://images.unsplash.com/photo-1502005229762-ee1b4038a8e3?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
            'amenities_list': ["High-speed Wi-Fi", "Air Conditioning", "Attached Bathroom", "Power Backup / Inverter", "Refrigerator", "Wardrobe & Study Table", "24x7 CCTV & Security", "Reserved Parking"]
        },
        {
            'owner': owner2,
            'title': "Economical Shared Bed in 2-Sharing Room in BTM Layout",
            'property_type': 'shared_room',
            'furnishing': 'fully_furnished',
            'tenant_preference': 'bachelors_male',
            'bathroom_type': 'attached',
            'food_availability': 'included',
            'rent_monthly': 8500,
            'security_deposit': 8500,
            'maintenance_monthly': 0,
            'available_from': date.today(),
            'minimum_lease_months': 1,
            'notice_period_days': 15,
            'area_sqft': 200,
            'floor': 1,
            'total_floors': 3,
            'city': 'Bangalore',
            'locality': 'BTM 2nd Stage',
            'address': 'Plot 45, 16th Main, Near Udupi Garden',
            'landmark': 'Near BTM Lake & Udupi Garden Signal',
            'description': "Affordable twin sharing room for students and young job seekers. Rent covers delicious 3 times food, Wi-Fi, electricity, water, and daily room cleaning. No brokerage, direct admission.",
            'house_rules': "No smoking in room. ID card verification required.",
            'primary_image_url': 'https://images.unsplash.com/photo-1540518614846-7ede433c4ef4?auto=format&fit=crop&w=1200&q=80',
            'is_featured': False,
            'amenities_list': ["Nutritious Meals Included", "High-speed Wi-Fi", "Daily Housekeeping", "RO Water Purifier", "Geyser / Hot Water", "Wardrobe & Study Table"]
        },
        {
            'owner': owner4,
            'title': "Premium Independent 1 BHK in Viman Nagar near Airport",
            'property_type': '1bhk',
            'furnishing': 'fully_furnished',
            'tenant_preference': 'anyone',
            'bathroom_type': 'attached',
            'food_availability': 'none',
            'rent_monthly': 22000,
            'security_deposit': 40000,
            'maintenance_monthly': 1000,
            'available_from': date.today() + timedelta(days=2),
            'minimum_lease_months': 6,
            'notice_period_days': 30,
            'area_sqft': 580,
            'floor': 3,
            'total_floors': 6,
            'city': 'Pune',
            'locality': 'Viman Nagar',
            'address': 'Rosewood Apartments, Near Phoenix Marketcity',
            'landmark': '5 mins from Phoenix Marketcity & Pune Airport',
            'description': "Sunlit and airy 1 BHK with modular kitchen, double bed, smart TV, 3-seater sofa, washing machine, and spacious balcony facing landscaped gardens. High security gated community with lift and covered parking.",
            'house_rules': "Direct owner deal. No brokers please. Long term tenants preferred.",
            'primary_image_url': 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=1200&q=80',
            'is_featured': True,
            'amenities_list': ["High-speed Wi-Fi", "Smart LED TV", "Washing Machine", "Air Conditioning", "Refrigerator", "Elevator / Lift", "Reserved Parking", "Private Balcony", "24x7 CCTV & Security"]
        }
    ]

    for item in listings_data:
        amenities_list = item.pop('amenities_list')
        listing, was_created = PropertyListing.objects.get_or_create(
            title=item['title'],
            defaults=item
        )
        if was_created:
            for aname in amenities_list:
                if aname in amenity_objs:
                    listing.amenities.add(amenity_objs[aname])
            
            # Add gallery images
            gallery_urls = [
                'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80',
            ]
            for gurl in gallery_urls:
                PropertyGalleryImage.objects.create(listing=listing, image_url=gurl, caption="Interior view")

            # Add sample review
            Review.objects.create(
                listing=listing,
                user=tenant1,
                rating=5,
                comment="Visited this room last week directly through EasyBooking. Owner Rajesh was very transparent, exactly as shown in photos with zero brokerage!"
            )

    print("✅ Sample listings created.")

    # 5. Create a sample Scheduled Visit and Booking
    first_listing = PropertyListing.objects.first()
    if first_listing:
        VisitSchedule.objects.get_or_create(
            listing=first_listing,
            tenant=tenant1,
            defaults={
                'visitor_name': 'Arjun Verma',
                'visitor_phone': '+91 99112 33445',
                'visitor_email': 'arjun@example.com',
                'visit_date': date.today() + timedelta(days=2),
                'time_slot': 'evening',
                'status': 'confirmed',
                'tenant_note': 'Interested in moving in next month. Would love to inspect the room.'
            }
        )

        BookingRequest.objects.get_or_create(
            listing=first_listing,
            tenant=tenant2,
            defaults={
                'applicant_name': 'Sneha Rao',
                'applicant_phone': '+91 99887 66554',
                'expected_move_in': date.today() + timedelta(days=7),
                'duration_months': 6,
                'occupants_count': 1,
                'token_amount': 1000.00,
                'payment_status': 'prepaid_token',
                'status': 'pending',
                'message': 'Working in an IT firm in Koramangala. Ready to sign agreement.'
            }
        )
        print("✅ Demo visit and booking created.")

    print("🎉 Seeding completed successfully!")

if __name__ == '__main__':
    run_seed()
