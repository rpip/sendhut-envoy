from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(page_title='Home', **context)


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(page_title='About', **context)


class FAQView(TemplateView):
    template_name = 'faqs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(page_title='FAQs', **context)


class PrivacyView(TemplateView):
    template_name = 'privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(page_title='Privacy Policy', **context)


class TermsView(TemplateView):
    template_name = 'terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(page_title='Terms and Conditions', **context)
