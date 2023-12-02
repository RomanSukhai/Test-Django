from django import forms
from .models import User, Product


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Підтвердження паролю')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        labels = {
            'email': 'Електронна пошта',
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Пошта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class OrderForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Продукт")
    quantity = forms.IntegerField(min_value=1, label="Кількість")
