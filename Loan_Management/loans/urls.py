from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanListCreateView, LoanDetailView, TransactionViewSet, foreclose_loan



# Create a router for the Transaction API
router = DefaultRouter()
router.register(r"transactions", TransactionViewSet, basename="transaction")


urlpatterns = [
    # Loan Endpoints
    path("loans/", LoanListCreateView.as_view(), name="loan-list-create"),
    path("loans/<int:pk>/", LoanDetailView.as_view(), name="loan-detail"),
    path("loans/<int:loan_id>/foreclose/", foreclose_loan, name="loan-foreclose"),

    # Include Transaction API
    path("", include(router.urls)),
]
