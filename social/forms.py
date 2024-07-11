from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, label='username or password', required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'bio', 'photo', 'job', 'phone')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone.isdigit():
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError("this phone number is already taken")
            return phone
        else:
            raise forms.ValidationError("Please enter a valid phone number")

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'date_of_birth', 'bio', 'photo', 'job', 'email']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("this phone number is already taken")
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("this username is already taken")
        return username

class TicketForm(forms.Form):
    # چون توی تمپلیت وارد کردیم اینجا دیگه بی معنیه و میتوانیم وارد نکنیم و در سابچکت بجای چوز فیلد باید از چر فیلد استفاده کنیم  و پرانتز روبروش رو خالی کنیم
    # SUBJECT_CHOICES = (
    #     ('پیشنهاد', 'پیشنهاد'),
    #     ('انتقاد', 'انتقاد'),
    #     ('گزارش', 'گزارش'),
    # )

    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250 ,required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11,required=True)
    subject = forms.CharField()#choices=SUBJECT_CHOICES

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.startswith('09') or len(phone) != 11:
            raise forms.ValidationError("Phone number must be 11 digits and start with  09")
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("The number is invalid")
            else:
                return phone