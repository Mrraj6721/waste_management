# 🌍 Community Waste Reporting Platform

A comprehensive Django-based platform for citizens to report illegal waste dumping and help keep communities clean.

## 🎯 Project Goal

**Community Waste Reporting** - A citizen-driven initiative to combat illegal waste dumping:

1. **📸 Citizen Uploads Photo** - Users upload photos of illegal dumping
2. **🤖 AI Detects Waste** - Advanced AI analyzes photos for waste detection
3. **📍 Location Auto-Tagged** - GPS coordinates automatically captured and reverse-geocoded
4. **📧 Report Sent to Authorities** - Automated notifications sent to relevant authorities

## ✨ Features

### For Citizens
- 📱 **Easy Photo Upload** - Simple drag-and-drop interface
- 🗺️ **Automatic Location Detection** - GPS coordinates captured automatically
- 📝 **Optional Description** - Add details about the waste issue
- ⚠️ **Severity Classification** - Mark issues as Low/Medium/High/Critical
- 🎯 **Real-time Feedback** - Immediate confirmation and status updates

### For Authorities
- 📊 **Comprehensive Dashboard** - View all reports with filtering options
- 🖼️ **Image Preview** - High-quality image display in admin interface
- 📍 **Location Mapping** - Interactive map showing all reported locations
- 📧 **Automated Notifications** - Email alerts for high-priority reports
- 📈 **Status Tracking** - Track cleanup progress from pending to resolved

### AI-Powered Detection
- 🤖 **Google Cloud Vision API** - Advanced image analysis
- 🗂️ **Waste Type Classification** - Categorizes waste as:
  - Plastic Waste
  - Organic Waste
  - Construction Debris
  - Electronic Waste
  - Medical Waste
  - Other
- 📊 **Confidence Scoring** - AI confidence level for each detection
- 🔄 **Automatic Authority Notification** - High-confidence detections trigger alerts

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Google Cloud Vision API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd waste_platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud Vision API**
   - Create a Google Cloud project
   - Enable the Cloud Vision API
   - Create a service account and download JSON key
   - Set environment variable:
     ```bash
     # Windows
     set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
     
     # Linux/Mac
     export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
     ```

4. **Configure database**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
waste_platform/
├── backend/                 # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── reports/                # Main app
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin interface
│   ├── urls.py            # App URL routing
│   └── templates/         # HTML templates
├── media/                  # Uploaded files
├── static/                 # Static assets
└── requirements.txt        # Python dependencies
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google Cloud service account key
- `AUTHORITY_EMAIL` - Email address for authority notifications

### Database Settings
The project uses PostgreSQL. Update `backend/settings.py` with your database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'waste_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Email Configuration
Configure email settings in `backend/settings.py` for authority notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'
AUTHORITY_EMAIL = 'authorities@yourdomain.com'
```

## 🎨 User Interface

### Modern Design
- 🌈 **Gradient Backgrounds** - Beautiful visual appeal
- 📱 **Responsive Layout** - Works on all device sizes
- 🎯 **Intuitive Navigation** - Easy-to-use interface
- 📊 **Interactive Maps** - Real-time waste report visualization
- 📈 **Statistics Dashboard** - Report counts and metrics

### Key Components
- **Report Form** - Photo upload with location and description
- **Interactive Map** - Shows all reported waste locations
- **Statistics Cards** - Total reports and confirmed cases
- **Status Indicators** - Visual feedback for report processing

## 🔒 Security Features

- 🔐 **CSRF Protection** - Built-in Django security
- 👤 **User Authentication** - Optional user registration
- 📍 **Location Privacy** - Secure GPS coordinate handling
- 🖼️ **File Upload Security** - Image validation and sanitization

## 📊 Admin Features

### Report Management
- 📋 **List View** - All reports with filtering and search
- 🖼️ **Image Preview** - High-quality image display
- 📍 **Location Display** - Address and coordinates
- 📊 **AI Results** - Detection confidence and waste type
- 📧 **Notification Status** - Authority notification tracking

### Bulk Actions
- ✅ **Mark as Confirmed** - Bulk status updates
- 🧹 **Mark as Resolved** - Track cleanup completion
- 📧 **Notify Authorities** - Manual notification triggers

## 🤖 AI Integration

### Google Cloud Vision API
- **Image Analysis** - Advanced object detection
- **Waste Classification** - Categorizes different waste types
- **Confidence Scoring** - Reliability metrics for detections
- **Error Handling** - Graceful fallback when API is unavailable

### Detection Categories
- **Plastic Waste** - Bottles, bags, containers
- **Organic Waste** - Food, compost, vegetables
- **Construction Debris** - Bricks, concrete, wood
- **Electronic Waste** - Devices, computers, batteries
- **Medical Waste** - Syringes, medicine, hospital waste
- **Other** - General waste and litter

## 📈 Reporting and Analytics

### Real-time Statistics
- 📊 **Total Reports** - Count of all submitted reports
- ✅ **Confirmed Cases** - High-confidence AI detections
- 📍 **Geographic Distribution** - Reports by location
- ⏰ **Time-based Analysis** - Reports over time

### Authority Dashboard
- 📧 **Email Notifications** - Automated alerts for high-priority reports
- 📊 **Status Tracking** - Monitor cleanup progress
- 📈 **Trend Analysis** - Identify problem areas
- 📋 **Response Management** - Track authority responses

## 🚀 Deployment

### Production Setup
1. **Configure production database**
2. **Set up static file serving**
3. **Configure email backend**
4. **Set up Google Cloud Vision API**
5. **Configure environment variables**
6. **Set up SSL certificates**

### Recommended Hosting
- **Heroku** - Easy deployment with PostgreSQL add-on
- **DigitalOcean** - VPS with full control
- **AWS** - Scalable cloud infrastructure
- **Google Cloud** - Integrated with Vision API

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Cloud Vision API** - For advanced image analysis
- **OpenStreetMap** - For reverse geocoding services
- **Django Community** - For the excellent web framework
- **Leaflet.js** - For interactive mapping

## 📞 Support

For support and questions:
- 📧 Email: support@wasteplatform.com
- 📱 Phone: +1-800-WASTE-REPORT
- 🌐 Website: https://wasteplatform.com

---

**Together, let's keep our communities clean! 🌍♻️**
