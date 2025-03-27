from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.text import slugify
from .models import Story, GalleryItem
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    context = {
        'profile_image': '/media/profile.jpg',  # Updated to use the image from media folder
    }
    return render(request, 'portfolio_app/home.html', context)

def stories(request):
    stories = Story.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    gallery_items = GalleryItem.objects.all()[:8]  # Limit to 8 items
    
    context = {
        'stories': stories,
        'gallery_items': gallery_items,
    }
    return render(request, 'portfolio_app/stories.html', context)

def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug, published_date__lte=timezone.now())
    context = {
        'story': story,
    }
    return render(request, 'portfolio_app/story_detail.html', context)

@login_required
def story_new(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        read_time = request.POST.get('read_time', 5)
        image = request.FILES.get('image')
        
        if title and content and image:
            slug = slugify(title)
            
            # Check if slug already exists and modify if needed
            base_slug = slug
            counter = 1
            while Story.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            story = Story(
                title=title,
                slug=slug,
                content=content,
                read_time=read_time,
                image=image,
                published_date=timezone.now()
            )
            story.save()
            return redirect('story_detail', slug=story.slug)
    
    return render(request, 'portfolio_app/story_edit.html')

@login_required
def story_edit(request, slug):
    story = get_object_or_404(Story, slug=slug)
    
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        read_time = request.POST.get('read_time', story.read_time)
        image = request.FILES.get('image')
        
        if title and content:
            story.title = title
            story.content = content
            story.read_time = read_time
            
            if image:
                story.image = image
            
            story.save()
            return redirect('story_detail', slug=story.slug)
    
    context = {
        'story': story,
    }
    return render(request, 'portfolio_app/story_edit.html', context)

@login_required
def gallery_new(request):
    if request.method == "POST":
        title = request.POST.get('title')
        image = request.FILES.get('image')
        
        if title and image:
            gallery_item = GalleryItem(
                title=title,
                image=image
            )
            gallery_item.save()
            return redirect('stories')
    
    return render(request, 'portfolio_app/gallery_edit.html')

def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validate inputs
        if not all([name, email, subject, message]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required'})
        
        # Email content
        email_subject = f'Portfolio Contact: {subject}'
        email_message = f"""
From: {name} <{email}>
Subject: {subject}

Message:
{message}

---
This message was sent from your portfolio website contact form.
"""
        
        recipient_email = 'rahul.edu.ranjan98153@gmail.com'
        
        try:
            # Send email
            send_mail(
                email_subject,
                email_message,
                email,  # Use sender's email as from_email
                [recipient_email],
                fail_silently=False,
                reply_to=[email],  # Set reply-to as the sender's email
            )
            
            # Log successful email
            logger.info(f"Contact form email sent from {email}")
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Thank you for your message! I will get back to you soon.'
            })
        
        except BadHeaderError:
            logger.error("Invalid header found in email")
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid email headers detected. Please try again with a different message.'
            })
            
        except Exception as e:
            # Log the error
            logger.error(f"Email sending failed: {str(e)}")
            
            # Check if we're using console backend (development)
            if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
                # In development, we'll simulate success
                logger.info(f"Development mode: Email would have been sent to {recipient_email}")
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Thank you for your message! I will get back to you soon. (Development mode)'
                })
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Sorry, there was a problem sending your message. Please try again later or contact me directly at rahul.edu.ranjan98153@gmail.com'
                })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def test_email(request):
    """A simple view to test email functionality"""
    try:
        send_mail(
            'Test Email from Portfolio',
            'This is a test email from your portfolio website.',
            'test@example.com',
            ['rahul.edu.ranjan98153@gmail.com'],
            fail_silently=False,
        )
        return JsonResponse({
            'status': 'success',
            'message': 'Test email sent successfully! Check your console if in development mode.'
        })
    except Exception as e:
        logger.error(f"Test email failed: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to send test email: {str(e)}'
        })
