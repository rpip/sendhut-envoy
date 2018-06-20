from django.conf import settings
from django.contrib import messages
from django.shortcuts import render


def home(request):
    context = {
        'page_title': 'Home',
    }
    template = 'app.html' if request.user.is_authenticated() else 'home.html'
    return render(request, template, context)


def about(request):
    return render(request, 'about.html', {'page_title': 'About Us'})


def faqs(request):
    return render(request, 'faqs.html', {'page_title': 'FAQs'})


def privacy(request):
    return render(request, 'privacy.html', {
        'page_title': 'Privacy Policy'
    })


def terms(request):
    return render(request, 'terms.html', {
        'page_title': 'Terms and Conditions'
    })
