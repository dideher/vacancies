from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Χρήστης', max_length=50)
    password = forms.CharField(label='Κωδικός πρόσβασης', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Λανθασμένα στοιχεία εισόδου. Παρακαλώ προσπαθήστε ξανά.'
        super().__init__(*args, **kwargs)


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Χρήστης', max_length=50, error_messages=
    {
        'invalid': "Ένα έγκυρο όνομα χρήστη μπορεί να περιέχει μόνο γράμματα, αριθμούς και τους χαρακτήρες @ . + - _ .",
        'unique': "Υπάρχει ήδη αυτός ο χρήστης."
    })
    password1 = forms.CharField(label='Κωδικός πρόσβασης', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Επιβεβαίωση κωδικού πρόσβασης', widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError("Το συγκεκριμένο mail χρησιμοποιείται ήδη.")

        return email
