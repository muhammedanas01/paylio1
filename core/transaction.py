from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account, KYC
from django.contrib import messages
from django.db.models import Q
from core.models import Transaction
from decimal import Decimal
from django.shortcuts import render, redirect

def transaction_list(request):
    sent_transactions = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by("-id")
    received_transactions = Transaction.objects.filter(receiver=request.user, transaction_type="transfer").order_by("-id")

    request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")
    request_reciever_transaction = Transaction.objects.filter( receiver=request.user, transaction_type="request")

    context = {
        "sent_transactions":sent_transactions,
        "received_transactions":received_transactions,

        "request_sender_transaction": request_sender_transaction,
        "request_reciever_transaction": request_reciever_transaction,
     }
    
    return render(request, "transaction/transaction-list.html", context)

def transaction_details(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "transaction":transaction
    }

    return render(request, "transaction/transaction-detail.html", context)
