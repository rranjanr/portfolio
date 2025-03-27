# Deployment Guide for Portfolio Website

This guide outlines the steps to deploy your portfolio website to a production environment with proper security measures.

## Pre-Deployment Checklist

1. Set `DEBUG = False` in settings.py
2. Add your domain to `ALLOWED_HOSTS` in settings.py
3. Secure your `SECRET_KEY` by setting it as an environment variable
4. Configure HTTPS and ensure all security settings are enabled

## Environment Setup

### Secret Key

In production, NEVER use the development secret key. Generate a new one:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Store this as an environment variable and update settings.py:

```python
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

### Static and Media Files

Configure your web server to serve static and media files directly:

1. Run `python manage.py collectstatic` to collect all static files
2. Configure your web server (Nginx, Apache) to serve files from STATIC_ROOT and MEDIA_ROOT

## Production Deployment Options

### Option 1: Traditional Hosting (Recommended for beginners)

1. **Server Setup:**
   - Set up a VPS (DigitalOcean, Linode, AWS EC2)
   - Install required dependencies (Python, pip, etc.)
   - Set up a database (PostgreSQL recommended over SQLite for production)

2. **Web Server:**
   - Install and configure Nginx or Apache
   - Set up Gunicorn or uWSGI as the WSGI server

3. **SSL Certificate:**
   - Obtain an SSL certificate (Let's Encrypt offers free certificates)
   - Configure HTTPS in your web server

4. **Database Migration:**
   - Run `python manage.py migrate` to set up the database

### Option 2: Platform as a Service (PaaS)

1. **Heroku:**
   - Create a `Procfile`: `web: gunicorn portfolio_project.wsgi --log-file -`
   - Configure environment variables in Heroku dashboard
   - Connect a PostgreSQL database

2. **PythonAnywhere:**
   - Upload your code
   - Configure WSGI file
   - Set up environment variables

## Security Best Practices

1. **Database:**
   - Use PostgreSQL instead of SQLite for production
   - Keep database credentials secure

2. **HTTPS:**
   - Force HTTPS by setting `SECURE_SSL_REDIRECT = True`
   - Ensure `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are enabled

3. **Headers:**
   - Enable security headers:
     - `SECURE_CONTENT_TYPE_NOSNIFF = True`
     - `SECURE_BROWSER_XSS_FILTER = True`
     - `X_FRAME_OPTIONS = 'DENY'`

4. **HSTS:**
   - Enable HTTP Strict Transport Security:
     - `SECURE_HSTS_SECONDS = 31536000`  # 1 year
     - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
     - `SECURE_HSTS_PRELOAD = True`

5. **Admin Interface:**
   - Change the default admin URL by modifying urls.py
   - Implement strong password policies
   - Consider implementing IP restrictions for admin access

6. **Regular Updates:**
   - Keep Django and all dependencies updated
   - Subscribe to Django security announcements

## Maintenance

1. **Backups:**
   - Regularly backup your database and media files
   - Test restoring from backups periodically

2. **Monitoring:**
   - Set up monitoring for your application (Sentry, New Relic)
   - Configure error logging

3. **Updates:**
   - Establish a routine for applying security updates

## Going Live Checklist

Before opening your site to the public:

1. Verify all security settings are enabled
2. Test your site thoroughly on different devices and browsers
3. Ensure proper error handling for 404 and 500 pages
4. Validate CSS and HTML
5. Test site performance and optimize as needed
6. Implement analytics tracking 