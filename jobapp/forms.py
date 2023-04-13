from django import forms

from jobapp.models import Job


class JobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Наименование вакансии :"
        self.fields['location'].label = "Локация вакансии :"
        self.fields['salary'].label = "Зарплата :"
        self.fields['description'].label = "Описание вакансии :"
        self.fields['tags'].label = "Теги :"
        self.fields['company_name'].label = "Наименование компании :"
        self.fields['url'].label = "Адрес сайта :"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'например: Программист',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'например: Москва',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '$800 - $1200',
            }
        )
        self.fields['tags'].widget.attrs.update(
            {
                'placeholder': 'Пишите через запятую, например: Python, JavaScript ',
            }
        )

        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'например: ООО Тритон',
            }
        )
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )

    class Meta:
        model = Job

        fields = [
            "title",
            "location",
            "job_type",
            "category",
            "salary",
            "description",
            "tags",
            "company_name",
            "company_description",
            "url"
        ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category

    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        if commit:
            job.save()
        return job
