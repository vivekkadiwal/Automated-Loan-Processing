from django.db import models

class LoanApplication(models.Model):
    applicant_name = models.CharField(max_length=100)
    document_image = models.ImageField(upload_to='documents/')
    w2_image = models.ImageField(upload_to='w2_forms/', blank=True, null=True)
    extracted_text = models.TextField(blank=True, null=True)
    w2_extracted_text = models.TextField(blank=True, null=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.applicant_name}'s Loan Application"
