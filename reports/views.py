from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReportForm, UserLoginForm, UserRegistrationForm
from .models import Report
import json
import requests
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Google Cloud Vision API configuration
GOOGLE_CLOUD_VISION_API_KEY = "GOOGLE_CLOUD_VISION_API_KEY"
GOOGLE_CLOUD_VISION_URL = "https://vision.googleapis.com/v1/images:annotate"

def home(request):
    """Main landing page with report form and map"""
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            
            # Set the user if authenticated
            if request.user.is_authenticated:
                report.reported_by = request.user
            
            # Get address from coordinates
            address = get_address_from_coordinates(report.location_lat, report.location_lng)
            report.address = address
            
            # Save the report first
            report.save()
            
            # AI waste detection
            try:
                detected, confidence, waste_type = detect_waste_with_api(report.image.path)
                report.detected = detected
                report.confidence = confidence
                report.waste_type = waste_type
                report.save()
                
                # Notify authorities if waste is detected with high confidence
                if detected and confidence > 0.7:
                    notify_authorities(report)
                    report.notified_authorities = True
                    report.save()
                    
            except Exception as e:
                print(f"Waste detection failed: {str(e)}")
                report.detected = False
                report.confidence = 0.0
                report.save()
            
            # Return success response
            reports = Report.objects.filter(detected=True).values(
                'id', 'location_lat', 'location_lng', 'confidence', 'waste_type', 'severity'
            )
            reports_json = json.dumps(list(reports)) if reports else json.dumps([])
            
            return JsonResponse({
                'status': 'success', 
                'reports': reports_json,
                'message': 'Report submitted successfully! Authorities have been notified.' if report.notified_authorities else 'Report submitted successfully!'
            })
        return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
    else:
        form = ReportForm()
        reports = Report.objects.filter(detected=True).values(
            'id', 'location_lat', 'location_lng', 'confidence', 'waste_type', 'severity'
        )
        reports_json = json.dumps(list(reports)) if reports else json.dumps([])
        return render(request, 'reports/index.html', {'form': form, 'reports_json': reports_json})

def get_address_from_coordinates(lat, lng):
    """Reverse geocode coordinates to get address"""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lng}&format=json"
        response = requests.get(url, headers={'User-Agent': 'WasteReportingApp/1.0'})
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', '')
    except Exception as e:
        print(f"Geocoding failed: {str(e)}")
    return ''

def detect_waste_with_api(image_path):
    """Detect waste using Google Cloud Vision API with API key"""
    try:
        # Read image file
        with open(image_path, 'rb') as image_file:
            import base64
            image_content = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Prepare request payload
        payload = {
            "requests": [
                {
                    "image": {
                        "content": image_content
                    },
                    "features": [
                        {
                            "type": "LABEL_DETECTION",
                            "maxResults": 10
                        }
                    ]
                }
            ]
        }
        
        # Make API request
        headers = {
            'Content-Type': 'application/json',
        }
        
        url = f"{GOOGLE_CLOUD_VISION_URL}?key={GOOGLE_CLOUD_VISION_API_KEY}"
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            labels = data.get('responses', [{}])[0].get('labelAnnotations', [])
            
            # Enhanced waste detection keywords
            waste_keywords = {
                'plastic': ['plastic', 'bottle', 'bag', 'container', 'packaging', 'trash', 'garbage'],
                'organic': ['food', 'organic', 'compost', 'vegetable', 'fruit', 'waste'],
                'construction': ['construction', 'debris', 'brick', 'concrete', 'wood', 'building'],
                'electronic': ['electronic', 'device', 'computer', 'phone', 'battery', 'technology'],
                'medical': ['medical', 'syringe', 'medicine', 'hospital', 'healthcare'],
                'other': ['waste', 'trash', 'garbage', 'litter', 'rubbish', 'pollution']
            }
            
            max_confidence = 0.0
            detected_waste_type = 'other'
            
            for label in labels:
                label_text = label.get('description', '').lower()
                score = label.get('score', 0.0)
                
                for waste_type, keywords in waste_keywords.items():
                    for keyword in keywords:
                        if keyword in label_text and score > max_confidence:
                            max_confidence = score
                            detected_waste_type = waste_type
            
            return max_confidence > 0.3, max_confidence, detected_waste_type
        else:
            print(f"API request failed: {response.status_code} - {response.text}")
            return False, 0.0, 'other'
            
    except Exception as e:
        print(f"Error in waste detection: {str(e)}")
        return False, 0.0, 'other'

def notify_authorities(report):
    """Send notification to authorities about the waste report"""
    try:
        subject = f"New Waste Report - {report.get_severity_display()} Priority"
        message = f"""
New waste report submitted:

Location: {report.address or f'{report.location_lat}, {report.location_lng}'}
Waste Type: {report.get_waste_type_display()}
Severity: {report.get_severity_display()}
Confidence: {report.confidence:.2f}
Description: {report.description or 'No description provided'}

View report: http://localhost:8000/admin/reports/report/{report.id}/
        """
        
        # Send email to authorities (configure in settings)
        if hasattr(settings, 'AUTHORITY_EMAIL'):
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.AUTHORITY_EMAIL],
                fail_silently=True,
            )
            
    except Exception as e:
        print(f"Failed to notify authorities: {str(e)}")

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'reports/login.html', {'form': form})

def user_register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'reports/register.html', {'form': form})

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')

@login_required
def dashboard(request):
    """Admin dashboard for authenticated users"""
    reports = Report.objects.all().order_by('-reported_at')
    total_reports = reports.count()
    pending_reports = reports.filter(status='pending').count()
    confirmed_reports = reports.filter(status='confirmed').count()
    resolved_reports = reports.filter(status='resolved').count()
    
    context = {
        'reports': reports,
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'confirmed_reports': confirmed_reports,
        'resolved_reports': resolved_reports,
    }
    
    return render(request, 'reports/dashboard.html', context)

@login_required
def report_detail(request, report_id):
    """Detailed view of a specific report"""
    try:
        report = Report.objects.get(id=report_id)
        return render(request, 'reports/report_detail.html', {'report': report})
    except Report.DoesNotExist:
        messages.error(request, 'Report not found.')
        return redirect('dashboard')

@login_required
def update_report_status(request, report_id):
    """Update report status"""
    if request.method == 'POST':
        try:
            report = Report.objects.get(id=report_id)
            new_status = request.POST.get('status')
            if new_status in dict(Report.STATUS_CHOICES):
                report.status = new_status
                report.save()
                messages.success(request, 'Report status updated successfully!')
            else:
                messages.error(request, 'Invalid status.')
        except Report.DoesNotExist:
            messages.error(request, 'Report not found.')
    
    return redirect('dashboard')