from typing import Any
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from crispy_forms.bootstrap import FormActions
from jobapp.models import Education, Resume, Experience
from users.models import User


class EmployeeRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "Имя :"
        self.fields['last_name'].label = "Фамилия :"
        self.fields['password1'].label = "Пароль :"
        self.fields['password2'].label = "Подтвердите пароль :"
        self.fields['email'].label = "Email :"
        self.fields['gender'].label = "Пол :"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Введите ваше имя',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Введите вашу фамилию',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Укажите Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Введите пароль',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Подтвердите пароль',
            }
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'gender']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "Company Name"
        self.fields['last_name'].label = "Company Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Address',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', ]

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', })
    )
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={

        'placeholder': 'Пароль'
    }))
    password.label = 'Пароль'
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, field_order=None, use_required_attribute=None, renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)
        self.user = None

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("User Does Not Exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")

            if not user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean()

    def get_user(self):
        return self.user


class EmployeeProfileEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender"]


class ResumeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Название резюме :"
        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Например: Python-разработчик',
            }
        )
        self.fields['title'].required=True
        self.fields['photo'].label = "Ваше фото :"
        self.fields['photo'].widget.attrs.update(
            {
                'placeholder': 'Файл не выбран',
            }
        )
        self.fields['name'].label = "Имя :"
        self.fields['surname'].label = "Фамилия :"
        self.fields['date_birth'].label = "Дата рождения :"
        self.fields['date_birth'].required=False
        self.fields['home_town'].label = "Город, в котором вы живёте :"
        self.fields['home_town'].required=False
        self.fields['phone_num'].label = "Номер телефона :"
        self.fields['job_position'].label = "Желаемая должность :"
        self.fields['salary'].label = "Желаемая зарплата :"
        self.fields['skills'].label = "Профессиональные навыки :"
        self.fields['about_me'].label = "О себе :"

    class Meta:
        model = Resume

        fields = [
            "title",
            'photo',
            "name",
            "surname",
            "date_birth",
            "home_town",
            "phone_num",
            "job_position",
            "salary",
            "skills",
            "about_me"
        ]
        widgets = {
            'date_birth': forms.DateInput(format='%m/%d/%Y',
                                          attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                 'type': 'date'}),
            'photo': forms.FileInput(attrs={'accept': 'image/*', 'style':"height: 200px ; width : 200px ;"})
        }

    def save(self, commit=True):
        resume =  super(ResumeForm, self).save(commit=False)
        if commit:
            resume.save()
        return resume


class ExperienceForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['start_date'].label = "Начало работы"
        self.fields['start_date'].required=False
        self.fields['end_date'].label = "Окончание"
        self.fields['end_date'].required=False
        self.fields['company'].label = "Организация"
        self.fields['company'].required=False
        self.fields['position'].label = "Должность"
        self.fields['position'].required=False
        self.fields['responsibilities'].label = "Обязанности на рабочем месте"
        self.fields['responsibilities'].required=False
        

    class Meta:
        model = Experience

        fields = [
            'start_date', 'end_date', 'company', 'position', 'responsibilities'
        ]
        widgets = {
            'start_date': forms.DateInput(format='%m/%d/%Y',
                                          attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                 'type': 'date'}),
            'end_date': forms.DateInput(format='%m/%d/%Y',
                                          attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                 'type': 'date'}),
        }

    def save(self, commit=True):
        experience = super(ExperienceForm, self).save(commit=False)
        if commit:
            experience.save()
        return experience
    


       
class EducationForm(forms.ModelForm):     
       class Meta:
            model = Education
            fields = ['university',  'faculty', 'specialization', 'graduation_year']
            widgets = {'graduation_year': forms.DateInput(format='%m/%d/%Y',
                                          attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                 'type': 'date'})}
        

class EmployeeResumeEditForm(forms.ModelForm):   
   
          
    
    class Meta:
        model = Resume
        fields =   ["title",
            'photo',
            "name",
            "surname",           
            "home_town",
            "phone_num",
            "job_position",
            "salary",
            "skills",
            "about_me"]
            
    
    def save(self, commit=True):       
        resume = self.instance
        resume.title = self.cleaned_data['title']       
        resume.photo = self.cleaned_data['photo']
        resume.name = self.cleaned_data['name']
        resume.surname = self.cleaned_data['surname']       
        resume.home_town = self.cleaned_data['home_town']
        resume.phone_num = self.cleaned_data['phone_num']
        resume.job_position = self.cleaned_data['job_position']
        resume.salary = self.cleaned_data['salary']
        resume.skills = self.cleaned_data['skills']
        resume.about_me = self.cleaned_data['about_me']        
       
        if commit:
            resume.save()
        return resume
