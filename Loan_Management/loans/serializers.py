from rest_framework import serializers
from .models import Loan, Transaction



class LoanSerializer(serializers.ModelSerializer):
    payment_schedule = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'user', 'amount', 'tenure', 'interest_rate',
                  'total_interest', 'total_amount', 'monthly_installment',
                  'status', 'created_at', 'payment_schedule']
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate_amount(self, value):
        """ Ensure loan amount is within the valid range """
        if value < 1000 or value > 100000:
            raise serializers.ValidationError("Loan amount must be between ₹1,000 and ₹100,000.")
        return value

    def validate_tenure(self, value):
        """ Ensure tenure is within the valid range """
        if value < 3 or value > 24:
            raise serializers.ValidationError("Tenure must be between 3 and 24 months.")
        return value

    def get_payment_schedule(self, obj):
        return obj.generate_payment_schedule()


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
