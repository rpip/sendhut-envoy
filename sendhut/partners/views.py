from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse
from .forms import PartnerForm

# Create your views here.

# /calculate earnings


class PartnerApplication(FormView):
    template_name = 'partners/apply.html'
    form_class = PartnerForm
    success_url = '/partners/feedback'

    def form_valid(self, form):
        # TODO(yao): send email/sms
        messages.success(self.request, "Thank you. We'll contact you shortly")
        return super().form_valid(form)


class PartnerApplicationSuccess(TemplateView):

    template_name = "partners/application_feedback.html"
