from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.password_validation import validate_password
from .models import CustomUserModel

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, label='Email', help_text='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(max_length=255, label='Password', help_text='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_qs = User.objects.filter(email=email)
        if not user_qs.exists():
            raise forms.ValidationError("Invalid credentials - user does not exists")
        user = user_qs.first()
        if not user.is_active:
            raise forms.ValidationError("Invalid credentials - user does not exists")
        if not user.check_password(password):
            raise forms.ValidationError("Credentials not correct")
        return super(LoginForm, self).clean(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               validators=[validate_password])
    class Meta:
        model = CustomUserModel
        fields = ('username', 'email', 'password',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUserModel.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2