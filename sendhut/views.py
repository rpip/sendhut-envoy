from django.shortcuts import render


def home(request):
    context = {
        'page_title': 'Home',
    }
    return render(request, 'home.html', context)


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
