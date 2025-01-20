from django import forms
from trainer.models import Category, Service, TraineSchedule, TraineDescription
from django.contrib.auth.models import User, Group

# Form per gestire gli orari del trainer
class TrainerScheduleForm(forms.ModelForm):    
    class Meta:
        model = TraineSchedule
        fields = ['datatime_start', 'datatime_end', 'trainer']
        widgets = {
            'datatime_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'datatime_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# Form per creare o modificare un trainer
class TrainerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        trainer_group = Group.objects.get(name="Trainer")
        # Filtra gli utenti che appartengono al gruppo "Trainer"
        self.fields['username'].queryset = trainer_group.user_set.all()

# Form per impostare il programma di lavoro settimanale
class WeeklyWorkScheduleForm(forms.Form):
    DAYS_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    days = forms.MultipleChoiceField(
        choices=DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Days of the Week"
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True,
        label="Start Time"
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True,
        label="End Time"
    )

# Form per creare una categoria
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category name'}),
        }

# Form per creare o modificare un servizio
class ServiceForm(forms.ModelForm):
    DURATION_CHOICES = [
        (30, '30 minutes'),
        (60, '60 minutes'),
        (120, '120 minutes'),
    ]
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'),  # Ordina le categorie per nome
        label="Category",
        empty_label="Select a category",
        required=True,
    )

    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        label="Duration (minutes)",
        required=True,
    )

    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        label="Level",
        required=True,
    )

    class Meta:
        model = Service
        fields = ['category', 'price', 'level', 'duration']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Price'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizza la rappresentazione delle categorie nel menu a discesa
        self.fields['category'].label_from_instance = lambda obj: obj.name
