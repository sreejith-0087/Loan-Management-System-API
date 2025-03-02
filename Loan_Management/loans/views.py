from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Loan, Transaction
from .serializers import LoanSerializer, TransactionSerializer
from decimal import Decimal

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Users can create loans for themselves.
    Admins can view all loans but cannot create loans.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == "POST" and request.user.role != "user":
            return False  # Only users can create loans

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow all users to read
        return obj.user == request.user


class LoanListCreateView(generics.ListCreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsUserOrReadOnly]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Loan.objects.all()
        return Loan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Users create their own loans


class IsAdminOrLoanOwner(permissions.BasePermission):
    """
    Admins can delete any loan.
    Users can only view and foreclose their own loans.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.role == "admin"  # Admins can delete any loan
        return obj.user == request.user  # Users can only access their own loans



class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrLoanOwner]


class IsLoanOwnerForTransaction(permissions.BasePermission):
    """
    Only the loan owner can create transactions for their loan.
    """
    def has_permission(self, request, view):
        if request.method == "POST":
            loan_id = request.data.get("loan")
            loan = Loan.objects.filter(id=loan_id).first()
            return loan and loan.user == request.user
        return request.user.is_authenticated  # Allow viewing for logged-in users

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin" or obj.loan.user == request.user


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsLoanOwnerForTransaction]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Transaction.objects.all()
        return Transaction.objects.filter(loan__user=self.request.user)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def foreclose_loan(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)

        # Ensure only loan owner or admin can foreclose
        if loan.user != request.user and request.user.role != "admin":
            return Response({"error": "Unauthorized"}, status=403)

        if loan.status == "CLOSED":
            return Response({"message": "Loan is already closed."}, status=400)

        # Calculate total amount, discount, and final settlement
        total_amount = loan.total_amount  # FIXED
        discount = total_amount * Decimal("0.05")  # 5% foreclosure discount
        final_amount = total_amount - discount

        # Close the loan
        loan.status = "CLOSED"
        loan.save()

        # Log foreclosure transaction
        Transaction.objects.create(
            loan=loan,
            amount_paid=final_amount,
            transaction_type="FORECLOSURE"
        )

        return Response({
            "status": "success",
            "message": "Loan foreclosed successfully.",
            "data": {
                "loan_id": loan.id,
                "amount_paid": float(final_amount),  # Convert Decimal to float
                "foreclosure_discount": float(discount),
                "final_settlement_amount": float(final_amount),
                "status": "CLOSED"
            }
        })
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found."}, status=404)

