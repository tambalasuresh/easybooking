from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('tenant', 'Tenant / Room Seeker (Looking to rent)'),
        ('owner', 'Property Owner / Landlord (Posting rooms/houses)'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'peer hidden'}),
        initial='tenant'
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 10-digit mobile number',
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
        })
    )
    city = forms.CharField(
        max_length=100,
        initial='Bangalore',
        widget=forms.TextInput(attrs={
            'placeholder': 'City (e.g. Bangalore, Mumbai)',
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create strong password',
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Re-enter password',
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose unique username',
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name',
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name',
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'name@example.com',
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100 transition'
            }),
        }

    def clean_confirm_password(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match!")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = user.profile
            profile.role = self.cleaned_data.get('role', 'tenant')
            profile.phone = self.cleaned_data.get('phone', '')
            profile.city = self.cleaned_data.get('city', 'Bangalore')
            profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'
    }))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'
    }))

    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'city', 'bio', 'avatar']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell owners or tenants about yourself...',
                'class': 'w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:border-red-500 focus:ring-2 focus:ring-red-100'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
