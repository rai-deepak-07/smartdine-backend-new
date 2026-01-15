from rest_framework import serializers

class MockPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockPayment
        fields = '__all__'
