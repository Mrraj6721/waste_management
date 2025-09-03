from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Report(models.Model):
    WASTE_TYPES = [
        ('plastic', 'Plastic Waste'),
        ('organic', 'Organic Waste'),
        ('construction', 'Construction Debris'),
        ('electronic', 'Electronic Waste'),
        ('medical', 'Medical Waste'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'Cleanup In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic report information
    image = models.ImageField(upload_to='reports/')
    location_lat = models.FloatField()
    location_lng = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    
    # AI Detection results
    detected = models.BooleanField(default=False)
    confidence = models.FloatField(default=0.0)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES, default='other')
    
    # Report details
    description = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], default='medium')
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reported_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    # Authority notification
    notified_authorities = models.BooleanField(default=False)
    authority_response = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-reported_at']
    
    def __str__(self):
        return f"Waste Report #{self.id} - {self.get_waste_type_display()} at {self.address or f'{self.location_lat}, {self.location_lng}'}"