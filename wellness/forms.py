from django import forms
from django.utils import timezone
from .models import WellnessLog, StressTrigger


class WellnessLogForm(forms.ModelForm):
    triggers = forms.ModelMultipleChoiceField(
        queryset=StressTrigger.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = WellnessLog
        fields = [
            'log_date',
            'sleep_hours',
            'mood',
            'stress_level',
            'academic_workload',
            'triggers',
            'notes',
        ]
        widgets = {
            'log_date': forms.DateInput(attrs={'type': 'date'}),
            'sleep_hours': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '24'}),
            'stress_level': forms.NumberInput(attrs={'min': '1', 'max': '10'}),
            'academic_workload': forms.NumberInput(attrs={'min': '1', 'max': '10'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional reflection on today...'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_log_date(self):
        log_date = self.cleaned_data['log_date']
        if log_date > timezone.localdate():
            raise forms.ValidationError("You cannot log a future date.")
        if self.user:
            qs = WellnessLog.objects.filter(user=self.user, log_date=log_date)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("You already have a wellness log for this date.")
        return log_date