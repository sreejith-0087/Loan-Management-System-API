from django.db import models
from users.models import User
from datetime import timedelta, date
from decimal import Decimal, InvalidOperation
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError


class Loan(models.Model):
    LOAN_STATUS = [
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField(help_text="Tenure in months")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Yearly interest rate in %")
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=LOAN_STATUS, default='ACTIVE')

    def clean(self):
        """ Validate loan amount and tenure before saving. """
        try:
            amount = Decimal(self.amount)
        except (TypeError, ValueError, InvalidOperation):
            raise ValidationError({"amount": "Invalid loan amount."})

        if amount < Decimal(1000) or amount > Decimal(100000):
            raise ValidationError({"amount": "Loan amount must be between ₹1,000 and ₹100,000."})

        if not isinstance(self.tenure, int) or self.tenure < 3 or self.tenure > 24:
            raise ValidationError({"tenure": "Tenure must be between 3 and 24 months."})

    def calculate_loan_details(self):
        """Calculates total payable amount, total interest, and monthly installment using compound interest formula."""
        P = Decimal(self.amount)
        r = Decimal(self.interest_rate) / Decimal(100) / Decimal(12)  # Convert yearly rate to monthly decimal
        n = self.tenure

        if r > 0:
            A = P * ((Decimal(1) + r) ** n)  # Compound Interest Formula
        else:
            A = P  # No interest case

        self.total_interest = A - P
        self.total_amount = A
        self.monthly_installment = A / n

    def save(self, *args, **kwargs):
        self.clean()  # Run validation before saving
        self.calculate_loan_details()  # Auto-calculate before saving
        super().save(*args, **kwargs)

    def generate_payment_schedule(self):
        """Generate payment schedule only if the loan is active."""
        if self.status == "CLOSED":
            return None  # Exclude payment schedule for closed loans

        schedule = []
        for i in range(1, self.tenure + 1):
            due_date = (self.created_at + timedelta(days=30 * i)).strftime("%Y-%m-%d")
            schedule.append({
                "installment_no": i,
                "due_date": due_date,
                "amount": round(self.monthly_installment, 2)
            })
        return schedule

    def foreclose(self):
        """ Foreclose the loan before tenure completion. Adjust interest accordingly. """
        if self.status == 'CLOSED':
            raise ValidationError("This loan is already closed.")

        remaining_principal = self.total_amount - self.amount_paid
        early_payment_interest = remaining_principal * Decimal(0.02)  # 2% foreclosure fee
        self.total_interest += early_payment_interest  # Adjust total interest
        self.amount_paid = self.total_amount  # Mark loan as fully paid
        self.status = 'CLOSED'
        self.save()



class Transaction(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='transactions')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(
        max_length=50, choices=[('EMI', 'EMI Payment'), ('FORECLOSURE', 'Foreclosure')]
    )
