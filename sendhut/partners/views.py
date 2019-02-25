from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages

from .forms import PartnerForm, MerchantForm

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


class SMEPackageView(FormView):
    template_name = 'business.html'
    form_class = MerchantForm
    success_url = '/business'
    success_message = "Thank you. We'll contact you shortly"

    def form_valid(self, form):
        # TODO(yao): send email/sms
        messages.success(self.request, "Thank you. We'll contact you shortly")
        form.save()
        return super().form_valid(form)
