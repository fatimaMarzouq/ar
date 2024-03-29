from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from .models import Event, Location, Asset


class EventCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(EventCreationForm, self).__init__(*args, **kwargs)

        self.fields['Locations'].queryset = Location.objects.filter(
            user=self.request.user)

        self.fields['Assets'].queryset = Asset.objects.filter(
            user=self.request.user)

    class Meta:
        model = Event
        fields = ['Name', 'Photo', 'Locations', 'Assets', 'starting_date', 'ending_date']
        widgets = {
            'starting_date': forms.DateInput(format=('%Y-%m-%d'),
                                             attrs={'class': 'datepicker1', 'placeholder': 'Select Date', 'type': 'date'}),
            'ending_date': forms.DateInput(format=('%Y-%m-%d'),
                                             attrs={'class': 'datepicker2', 'placeholder': 'Select Date',
                                                    'type': 'date'})
        }

    Photo = forms.ImageField()

    Locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    # Locations = forms.ModelMultipleChoiceField(
    #     queryset=Location.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    Assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class AssetCreationForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = ['Asset_File', 'featured_image', 'Google_maps_link', 'ASSETS_TYPE', 'Expiry_date', 'Expiry_time']
        widgets = {
            'Expiry_date': forms.DateInput(format=('%Y-%m-%d'),
                                             attrs={'class': 'datepicker1', 'placeholder': 'Select Date', 'type': 'date'}),
            'Expiry_time': forms.TimeInput(format='%H:%M',attrs={'type': 'time'}),
        }

    Google_maps_link = forms.CharField()

    featured_image = forms.ImageField()

    ASSETS_TYPE = forms.Select()
    Asset_File = forms.FileField(widget=forms.FileInput(attrs={'onchange': 'handleContentUpload(self)'}))


class LocationCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(LocationCreationForm, self).__init__(*args, **kwargs)

        self.fields['Assets'].queryset = Asset.objects.filter(
            user=self.request.user)


    class Meta:
        model = Location
        fields = ['Name', 'Longitude', 'Latitude', 'Google_maps_link', 'Plus_code', 'Radius', 'Assets']
        widgets = {
            'Expiry_date': forms.DateInput(format=('%Y-%m-%d'),
                                             attrs={'class': 'datepicker1', 'placeholder': 'Select Date', 'type': 'date'}),
            'Expiry_time': forms.TimeInput(format='%H:%M',attrs={'type': 'time'}),
        }

    Longitude = forms.NumberInput()
    Latitude = forms.NumberInput()
    Radius = forms.NumberInput()
    Google_maps_link = forms.CharField()
    Plus_code = forms.CharField()



    Assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
