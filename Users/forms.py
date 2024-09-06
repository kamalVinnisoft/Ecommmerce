from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirm Password'
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'username','phone_number', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        if CustomUser.objects.filter(username=cleaned_data.get("username")).exists():
            self.add_error('username', "Email already exists")
        
        if CustomUser.objects.filter(email=cleaned_data.get("email")).exists():
            self.add_error('email', "Email already exists")

        if CustomUser.objects.filter(phone_number=cleaned_data.get("phone_number")).exists():
            self.add_error('phone_number', "Phone number already exists")

        return cleaned_data
    

        if self.instance and self.instance.pk:
            # Exclude the current instance for uniqueness check
            if CustomUser.objects.filter(email=cleaned_data.get("email")).exclude(pk=self.instance.pk).exists():
                self.add_error('email', "Email already exists")

            if CustomUser.objects.filter(phone_number=cleaned_data.get("phone_number")).exclude(pk=self.instance.pk).exists():
                self.add_error('phone_number', "Phone number already exists")
        else:
            # For new instances
            if CustomUser.objects.filter(email=cleaned_data.get("email")).exists():
                self.add_error('email', "Email already exists")

            if CustomUser.objects.filter(phone_number=cleaned_data.get("phone_number")).exists():
                self.add_error('phone_number', "Phone number already exists")

        return cleaned_data