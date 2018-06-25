from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import PartnerForm

# Create your views here.

# /calculate earnings


class PartnerApplication(FormView):
    template_name = 'partners/apply.html'
    form_class = PartnerForm
    success_url = '/partners'

    def form_valid(self, form):
        # TODO(yao): send email/sms
        messages.info(self.request, "Thank you. We'll contact you shortly")
        return super().form_valid(form)
