import decimal
from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ( 'receiver_email', 'amount', 'transaction_date')
class AccountSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('sender_email', 'receiver_email', 'amount', 'transaction_date')
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    @action(detail=False, methods=['post'])
    def make_payment(self, request):
        sender = request.user
        receiver= request.data.get('receiver_email')
        #amount = request.data.get('amount')
        print(receiver)
        amount = decimal.Decimal(request.data.get('amount'))
        #receiver_email = request.data.get('receiver')
        print(receiver)
        if sender.balance < amount:
            return Response({'error': 'Bakiye yetersiz.'}, status=400)

        try:
            receiver = User.objects.get(email=receiver)
        except User.DoesNotExist:
            print(receiver)
            return Response({'error': 'Alıcı bulunamadı.'}, status=400)

        transaction = Transaction.objects.create(sender=sender, receiver_email=receiver, amount=amount)

        # Bakiyeleri güncelle
        sender.balance -= amount
        sender.save()

        receiver.balance += amount
        receiver.save()

        return Response(TransactionSerializer(transaction).data)
    

    @action(detail=False, methods=['get'], serializer_class=AccountSummarySerializer)
    def list_transactions(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'])
    def account_summary(self, request):
        user = request.user
        
        sent_transactions = Transaction.objects.filter(sender=user)
        received_transactions = Transaction.objects.filter(receiver=user)
        
        serializer = AccountSummarySerializer(sent_transactions, many=True)
        sent_data = serializer.data
        
        serializer = AccountSummarySerializer(received_transactions, many=True)
        received_data = serializer.data
        sent_summary = [{'amount': transaction['amount'], 'receiver_email': transaction['receiver_email'],'transaction_date': transaction['transaction_date']} for transaction in sent_data]
        received_summary = [{'amount': transaction['amount'], 'sender_email': transaction['sender_email'],'transaction_date': transaction['transaction_date']} for transaction in received_data]
        summary = {
            'sent_transactions': sent_summary,
            'received_transactions': received_summary,
        }
        
        return Response(summary)