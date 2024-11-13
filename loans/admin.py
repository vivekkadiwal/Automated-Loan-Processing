from django.contrib import admin
from .models import LoanApplication

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name','monthly_income','status', 'extracted_text', 'w2_extracted_text')
    readonly_fields = ('extracted_text', 'w2_extracted_text')
