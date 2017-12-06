from django import forms
from localflavor.us.us_states import STATE_CHOICES
from .shortcuts import Shortcuts

class PatientSignInForm(forms.Form):
    firstname = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name'
        }))
    lastname = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name'
        }))

class PatientDemographicsForm(forms.Form):
    first_name = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)
    gender = forms.ChoiceField(required=False, choices=(
        ('', 'Select gender'),
        (Shortcuts.Gender.MALE, 'Male'),
        (Shortcuts.Gender.FEMALE, 'Female'),
        (Shortcuts.Gender.OTHER, 'Other')
    ))
    social_security_number = forms.CharField(required=False)

    home_phone = forms.CharField(required=False)
    cell_phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.ChoiceField(required=False, choices=STATE_CHOICES)
    zip_code = forms.CharField(required=False)
    email_address = forms.CharField(required=False)

    ethnicity = forms.ChoiceField(required=False, choices=(
        ('', 'Select ethicity'),
        (Shortcuts.Ethnicity.HISPANIC, 'Hispanic'),
        (Shortcuts.Ethnicity.NOT_HISPANIC, 'Not Hispanic'),
        (Shortcuts.Ethnicity.DECLINED, 'Decline to answer')
    ))
    race = forms.ChoiceField(required=False, choices=(
        ('', 'Select race'),
        (Shortcuts.Race.ASIAN, 'Asian (NOT including India)'),
        (Shortcuts.Race.INDIAN, 'Indian'),
        (Shortcuts.Race.WHITE, 'White (including Middle-Eastern)'),
        (Shortcuts.Race.BLACK, 'Black or African-American'),
        (Shortcuts.Race.HAWAIIAN, 'Native Hawaiian or other Pacific Islander (Original Peoples)'),
        (Shortcuts.Race.DECLINED, 'Decline to answer')
    ))

    emergency_contact_name = forms.CharField(required=False)
    emergency_contact_phone = forms.CharField(required=False)
    emergency_contact_relation = forms.CharField(required=False) # Maybe make this a drop-down?

    employer = forms.CharField(required=False)
    employer_address = forms.CharField(required=False)
    employer_city = forms.CharField(required=False)
    employer_state = forms.ChoiceField(required=False, choices=STATE_CHOICES)
    employer_zip_code = forms.CharField(required=False)

    responsible_party_name = forms.CharField(required=True)
    responsible_party_relation = forms.CharField(required=True) # Make this a drop-down too?
    responsible_party_phone = forms.CharField(required=True)
    responsible_party_email = forms.CharField(required=True)




