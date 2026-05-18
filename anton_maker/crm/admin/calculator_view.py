from django.views.generic import TemplateView
from django.contrib.admin.sites import site
from crm.models import Material

class CalculatorView(TemplateView):
    template_name = "admin/custom_calculator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materials'] = Material.objects.filter(is_active=True)
        context['title'] = "Калькулятор стоимости"
        context['site_title'] = site.site_title
        return context
