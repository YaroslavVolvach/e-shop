from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.forms.widgets import EmailInput
from .models import CustomUser, image
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .form_mixins import ChangeWigetsMixins
from django.utils import timezone

attrs_ = {'class': 'form-control'}


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=EmailInput(attrs=attrs_))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_))


class CustomUserCreationForm(ChangeWigetsMixins, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('user_name', 'email')


default_image = {
    "Male": "account_image/default_account_image/Man default_image.jpg",
    "Female": "account_image/default_account_image/Woman_default_image.jpg",
    "Not specified": image}


class ChangeProfileForm(ChangeWigetsMixins, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_name', 'country', 'city', 'birth_date', 'gender']

    def age_valid(self):
        today = timezone.now()
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date is None:
            return True
        return (today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))) >= 1

    def is_valid(self):
        if super().is_valid():
            if not self.age_valid():
                self.errors['age'] = '     Your age must be over 0 years old'
                self.errors.as_text()

        return bool(not self.errors)

    @staticmethod
    def image(image_, gender_):
        if image_ in default_image.values():
            return default_image[gender_]
        return image_

    def save(self):
        user = super().save(commit=False)
        user.main_image = self.image(user.main_image, user.gender)
        user.save()
        return user


class ImageForm(forms.Form):
    main_image = forms.ImageField(required=False)

    def save(self, user):
        main_image = self.cleaned_data['main_image']
        if main_image is not None:
            user.main_image = main_image
            user.save()


class ChangePasswordForm(ChangeWigetsMixins, PasswordChangeForm):
    pass


class CustomPasswordResetForm(ChangeWigetsMixins, PasswordResetForm):
    pass


class CustomSetPasswordForm(ChangeWigetsMixins, SetPasswordForm):
    pass


class ChangeEmailForm(ChangeWigetsMixins, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    new_email = forms.CharField(widget=EmailInput)
    repeat_new_email = forms.CharField(widget=EmailInput)

    class Meta:
        model = CustomUser
        fields = ['email']

    def is_valid(self):
        if super().is_valid():
            new_email = self.cleaned_data['new_email']
            repeat_new_email = self.cleaned_data['repeat_new_email']

            return new_email == repeat_new_email
        return False

    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data['new_email']
        user.save()
        return user
