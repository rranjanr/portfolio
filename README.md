# Modern Portfolio Website

A beautiful and modern portfolio website built with Django and Tailwind CSS. Features a stunning UI with animations, snow effects, and a fully functional contact form.

## Features

- 🎨 Modern and responsive design
- ❄️ Beautiful snow effect animation
- 🌓 Dark/Light mode support
- 📱 Mobile-friendly navigation
- 🎯 Smooth scroll animations
- 📬 Working contact form
- 🖼️ Project showcase section
- 📊 Skills visualization
- 💼 About me section
- 🔗 Social media integration

## Technologies Used

- Django 5.1.4
- Tailwind CSS
- Font Awesome Icons
- AOS (Animate On Scroll)
- Django Compressor
- Django Browser Reload

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd portfolio-website
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file in the project root and add your settings:
```
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST=your-email-host
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@example.com
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ in your browser

## Customization

1. Replace the profile image:
   - Add your profile image to `static/images/profile.jpg`

2. Update personal information:
   - Edit `portfolio_app/templates/portfolio_app/home.html`
   - Update your name, title, and description
   - Add your social media links

3. Add your projects:
   - Add project images to `static/images/`
   - Update the projects section in `home.html`
   - Add your project details and links

4. Customize skills:
   - Update the skills section in `home.html`
   - Adjust skill percentages and icons

5. Modify the color scheme:
   - Edit the Tailwind configuration in `base.html`
   - Update primary and secondary colors

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 