from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class StressTrigger(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WellnessLog(models.Model):
    MOOD_CHOICES = [
        ('great', 'Great'),
        ('good', 'Good'),
        ('neutral', 'Neutral'),
        ('stressed', 'Stressed'),
        ('overwhelmed', 'Overwhelmed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wellness_logs',
    )
    log_date = models.DateField(default=timezone.localdate)
    sleep_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(24.0)],
    )
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    stress_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='1 (Low) to 10 (Extreme)',
    )
    academic_workload = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='1 (Light) to 10 (Heavy)',
    )
    triggers = models.ManyToManyField(StressTrigger, blank=True, related_name='logs')
    notes = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-log_date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'log_date'],
                name='unique_user_daily_wellness_log',
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.log_date} (Stress: {self.stress_level}/10)"