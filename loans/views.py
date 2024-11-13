from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LoanApplication
from .utils import extract_text_from_image
from .serializers import LoanApplicationSerializer
from math import pow
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoanApplicationView(APIView):
    def post(self, request):
        serializer = LoanApplicationSerializer(data=request.data)
        if serializer.is_valid():
            loan_application = serializer.save()
            logger.info("Loan application saved. Starting OCR processing...")

            user_entered_name = loan_application.applicant_name
            user_entered_income = int(loan_application.monthly_income)

            if user_entered_income < 50000:
                approx_loan_amount = user_entered_income * 1.5
                interest_rate = 10 
            elif user_entered_income < 100000:
                approx_loan_amount = user_entered_income * 2
                interest_rate = 8 
            else:
                approx_loan_amount = min(user_entered_income * 3, 300000)  
                interest_rate = 6 

            loan_term_years = 5 

            monthly_rate = interest_rate / 100 / 12
            loan_term_months = loan_term_years * 12
            if monthly_rate > 0:
                monthly_payment = approx_loan_amount * (monthly_rate * pow(1 + monthly_rate, loan_term_months)) / (pow(1 + monthly_rate, loan_term_months) - 1)
            else:
                monthly_payment = approx_loan_amount / loan_term_months

            logger.info(f"Approximate Loan Amount: {approx_loan_amount}")
            logger.info(f"Interest Rate: {interest_rate}%")
            logger.info(f"Monthly Payment: {monthly_payment}")

            extracted_text = extract_text_from_image(loan_application.document_image.path)
            if extracted_text:
                logger.info("Text successfully extracted from the main document image.")
                loan_application.extracted_text = extracted_text
                name_match_in_document = user_entered_name.lower() in extracted_text.lower()
            else:
                logger.warning("No text was extracted from the main document image.")
                name_match_in_document = False

            if loan_application.w2_image:
                w2_extracted_text = extract_text_from_image(loan_application.w2_image.path)
                if w2_extracted_text:
                    logger.info("Text successfully extracted from the W2 image.")
                    loan_application.w2_extracted_text = w2_extracted_text
                    name_match_in_w2 = user_entered_name.lower() in w2_extracted_text.lower()
                    income_match_in_w2 = str(user_entered_income) in w2_extracted_text
                else:
                    logger.warning("No text was extracted from the W2 image.")
                    name_match_in_w2 = False
                    income_match_in_w2 = False
            else:
                logger.info("No W2 image provided.")
                name_match_in_w2 = False
                income_match_in_w2 = False

            response_data = serializer.data
            response_data["name_match_in_document"] = name_match_in_document
            response_data["name_match_in_w2"] = name_match_in_w2
            response_data["income_match_in_w2"] = income_match_in_w2
            response_data["approx_loan_amount"] = approx_loan_amount
            response_data["interest_rate"] = interest_rate
            response_data["loan_term_years"] = loan_term_years
            response_data["monthly_payment"] = monthly_payment

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Loan application submission failed due to invalid data.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoanApplicationListView(APIView):
    def get(self, request):
        applications = LoanApplication.objects.all()
        serializer = LoanApplicationSerializer(applications, many=True)
        return Response(serializer.data)
