from django.urls import path
from .views import LoanApplicationView, LoanApplicationListView

urlpatterns = [
    path('loan-application/', LoanApplicationView.as_view(), name='loan-application'),
    path('loan-applications/', LoanApplicationListView.as_view(), name='loan-applications'),
]
