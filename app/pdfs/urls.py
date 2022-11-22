from django.urls import path
from .views import (
    PdfUserEntries,
    PdfEntries,
    PdfHistory,
    PdfUserHistory
)


app_name = 'pdfs'

urlpatterns = [
    path('pdf_user_entries/', PdfUserEntries.as_view(), name='pdf_user_entries'),
    path('pdf_entries/', PdfEntries.as_view(), name='pdf_entries'),
    path('pdf_history/', PdfHistory.as_view(), name='pdf_history'),
    path('pdf_user_history/', PdfUserHistory.as_view(), name='pdf_user_history'),
]
