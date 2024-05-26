# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from users.models.library_user import LibraryUser
from library.models.reserve_book import ReserveBook
from library.models.issued_book import IssuedBook
from library.models.book import Book


class LibraryUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    library_card_number = forms.CharField(max_length=20, required=True)
    personal_identification_number = forms.CharField(max_length=20, required=True,
                                                     label='Personal Identification Number')
    date_of_birth = forms.DateField(required=True, label='Date of Birth')
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone_number = forms.CharField(max_length=20, required=True, label='Phone Number')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'library_card_number',
                  'personal_identification_number', 'date_of_birth', 'address', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            library_user = LibraryUser(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                library_card_number=self.cleaned_data['library_card_number'],
                personal_identification_number=self.cleaned_data['personal_identification_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
            )
            library_user.save()
        return user


class LibraryUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return username


class ReserveBookForm(forms.ModelForm):
    class Meta:
        model = ReserveBook
        fields = ['book', 'take_date', 'due_date']
        widgets = {
            'take_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class IssueBookForm(forms.ModelForm):
    class Meta:
        model = IssuedBook
        fields = ['book', 'user', 'issued_date', 'due_date']
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publisher', 'published_date', 'tags', 'stock_quantity',
                  'borrowed_quantity', 'current_borrowed_quantity']


class UpdateIsTakenForm(forms.ModelForm):
    class Meta:
        model = ReserveBook
        fields = ['is_taken']


