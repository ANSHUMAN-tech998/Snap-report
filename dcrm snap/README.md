# 🏢 Snap and Report - Issue Management System

A modern, professional Django-based issue tracking and management system with GPS location integration, analytics dashboard, and comprehensive admin features.

![Django](https://img.shields.io/badge/Django-5.2.6-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Navigation](#navigation)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🎯 Core Functionality
- **Issue Reporting** - Submit issues with GPS location detection
- **Admin Dashboard** - Comprehensive overview with statistics
- **Issues Management** - Filter, search, and manage all issues
- **Analytics Dashboard** - Interactive charts and data insights
- **User Management** - Role-based access control
- **GPS Integration** - Automatic location detection and mapping

### 🎨 User Experience
- **Modern UI** - Beautiful glass morphism design
- **Responsive Design** - Works on all devices
- **Interactive Charts** - Chart.js integration for data visualization
- **Real-time Updates** - Dynamic content updates
- **Professional Styling** - Bootstrap 5 with custom CSS

### 🔧 Technical Features
- **Geolocation API** - Automatic GPS coordinate detection
- **Reverse Geocoding** - Convert coordinates to addresses
- **Database Analytics** - Dynamic chart generation from data
- **Form Validation** - Comprehensive input validation
- **Error Handling** - User-friendly error messages

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (for cloning repository)
- **Web browser** (Chrome, Firefox, Safari, Edge)

### System Requirements
- **Operating System:** Windows 10/11, macOS, or Linux
- **RAM:** 512MB minimum, 1GB recommended
- **Storage:** 500MB free space
- **Internet:** Required for geolocation services

## 🚀 Installation

### Method 1: Clone from Git Repository

```bash
# Clone the repository
git clone https://github.com/your-username/snap-and-report.git

# Navigate to project directory
cd snap-and-report
```

### Method 2: Download ZIP File

1. Download the project ZIP file
2. Extract to your desired location
3. Navigate to the extracted folder

## ⚙️ Setup

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv dcrm_env

# Activate virtual environment
# Windows
dcrm_env\Scripts\activate

# macOS/Linux
source dcrm_env/bin/activate
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install Django
pip install django

# Install additional packages (if needed)
pip install requests
```

### Step 3: Database Setup

```bash
# Run migrations
python manage.py migrate
```

### Step 4: Create Admin User

```bash
# Interactive method
python manage.py createsuperuser

# Or create with predefined credentials
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@test.com', 'admin123')"
```

### Step 5: Start the Server

```bash
# Start development server
python manage.py runserver

# For network access
python manage.py runserver 0.0.0.0:8000
```

## 🌐 Usage

### Accessing the Application

Once the server is running, open your web browser and navigate to:

- **Main Application:** http://127.0.0.1:8000/
- **Alternative:** http://localhost:8000/

### Login Credentials

#### Admin Access
- **Username:** `admin`
- **Password:** `admin123`

#### Staff Access
- **Username:** `admin_user` (if created)
- **Password:** `admin123`

## 🗺️ Navigation

### Public URLs (No Login Required)

| URL | Description |
|-----|-------------|
| `/` | Home page with login form |
| `/register/` | User registration |
| `/report/` | Report new issues (requires login) |

### Admin URLs (Login Required)

| URL | Description |
|-----|-------------|
| `/management/dashboard/` | Admin dashboard with statistics |
| `/management/issues/` | Issues management and filtering |
| `/management/analytics/` | Analytics dashboard with charts |
| `/management/issues/{id}/` | Individual issue management |

### Django Admin

| URL | Description |
|-----|-------------|
| `/admin/` | Django built-in admin interface |
| `/admin/website/record/` | Manage customer records |
| `/admin/auth/user/` | Manage users |

## 📱 Mobile Access

The application is fully responsive and works perfectly on mobile devices:

- **Touch-friendly** interface
- **GPS integration** for location detection
- **Responsive charts** that adapt to screen size
- **Mobile-optimized** navigation

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. **Port Already in Use**
```bash
# Kill existing processes
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### 2. **Database Migration Errors**
```bash
# Reset migrations (if needed)
python manage.py migrate --fake-initial
```

#### 3. **Virtual Environment Issues**
```bash
# Recreate virtual environment
rm -rf dcrm_env
python -m venv dcrm_env
dcrm_env\Scripts\activate  # Windows
```

#### 4. **Geolocation Not Working**
- Ensure HTTPS is used in production
- Check browser permissions
- Verify GPS is enabled on device

#### 5. **Charts Not Displaying**
- Check browser JavaScript is enabled
- Ensure internet connection for CDN resources
- Verify Chart.js is loading properly

### Error Messages and Solutions

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'django'` | Install Django: `pip install django` |
| `OperationalError: no such table` | Run migrations: `python manage.py migrate` |
| `Permission denied: geolocation` | Allow location access in browser |
| `Connection refused` | Start server: `python manage.py runserver` |

## 📊 Analytics Dashboard

The analytics dashboard provides real-time insights:

### Data Sources
- **Location Analytics:** Geographic distribution of issues
- **Contact Analytics:** Email/phone/address availability
- **Temporal Analytics:** Monthly trends and patterns
- **Statistical Insights:** Count-based data analysis

### Chart Types
- **Doughnut Charts:** Location distribution
- **Bar Charts:** Contact method preferences
- **Line Charts:** Monthly trends
- **Interactive Legends:** Click to show/hide data

## 🔐 Security Features

- **CSRF Protection:** Built-in Django security
- **Password Hashing:** Secure password storage
- **Session Management:** Automatic session handling
- **SQL Injection Protection:** ORM-based queries
- **XSS Protection:** Template auto-escaping

## 🚀 Deployment

### Production Deployment

For production deployment, consider:

1. **Web Server:** Use Nginx or Apache
2. **Database:** PostgreSQL or MySQL
3. **HTTPS:** Enable SSL certificates
4. **Static Files:** Configure static file serving
5. **Environment Variables:** Use `.env` files
6. **Security:** Enable production settings

### Docker Deployment

```dockerfile
# Create Dockerfile for containerization
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch
3. **Commit** your changes
4. **Push** to the branch
5. **Submit** a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages
- Test on multiple browsers/devices

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django** - Web framework
- **Bootstrap 5** - CSS framework
- **Chart.js** - Chart library
- **Font Awesome** - Icons
- **OpenStreetMap** - Geocoding services

## 📞 Support

For support and questions:

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** support@snapandreport.com

## 🔄 Updates

- **Version 1.0.0** - Initial release
- **Features:** Issue tracking, GPS integration, Analytics
- **Compatibility:** Django 5.2+, Python 3.8+

---

**⭐ If you found this helpful, please give it a star!**

[Back to Top](#-snap-and-report---issue-management-system)
