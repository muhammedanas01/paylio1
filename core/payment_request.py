from account.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account, KYC
from django.contrib import messages
from django.db.models import Q
from core.models import Transaction
from decimal import Decimal

@login_required
def search_user_request(request):
    account = Account.objects.all()
    user_input = request.POST.get("account_number")

    if user_input:
        search_account = Account.objects.filter(
            Q(account_number = user_input)|
            Q(account_id = user_input)
        ).distinct()

        context = {
            "accounts": search_account,
            "search_query": user_input
            }
        
        return render(request, "payment-request/search-user.html", context)
    
    return render(request, "payment-request/search-user.html")

def request_amount_transfer(request, account_number):# requesting for amount
    try:
         requested_account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, "Account does not exist.")
        return redirect("core:search-requested-account")
    
    context = {
        'account':requested_account
    }
    return render(request, "payment-request/request-amount-transfer.html", context )

def request_amount_transfer_process(request, account_number): # process of requesting
    request_reciever_account = Account.objects.get(account_number=account_number)# account of person where user is requesting for money
    request_reciever_account_number = request_reciever_account.account_number
    request_reciever = request_reciever_account.user

    request_sender = request.user # user who is requesting money
    request_sender_account = request_sender.account

    if request.method=="POST":
        amount = request.POST.get("request_amount")
        description = request.POST.get("request_description")

        new_request = Transaction.objects.create(
            user = request.user,
            amount = amount,
            description = description,

            sender =request_sender, # person who sent the request
            sender_account = request_sender_account,

            receiver = request_reciever,# person who receive's the request
            receiver_account = request_reciever_account,

            transaction_status = "request_processing",
            transaction_type = "request"
        )
        new_request.save()
        transaction_id = new_request.transaction_id 
        return redirect("core:request_confirmation", request_reciever_account_number, transaction_id)
    else:
        messages.warning(request, "error occured try again later")
        return redirect("account:dashboard")
    
def request_confirmation(request, request_reciever_account_number, transaction_id):
    request_reciever_account = Account.objects.get(account_number=request_reciever_account_number)# account of person where user is requesting for money
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "account": request_reciever_account,
        "transaction": transaction
    }
    return render(request, "payment-request/request-amount-confirmation.html", context)

def amount_request_final_process(request, request_reciever_account_number, transaction_id ):
    request_reciever_account = Account.objects.get(account_number=request_reciever_account_number)# account of person where user is requesting for money
    request_reciever_account_number = request_reciever_account.account_number
    request_reciever = request_reciever_account.user

    request_sender = request.user # user who is requesting money
    request_sender_account = request_sender.account

    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.method=="POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            transaction.transaction_status = "request_sent"
            transaction.save()
            messages.success(request, "your payment request have been sent successfully")
            return redirect("core:request-completed", request_reciever_account_number, transaction_id)
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect("account:dashboard")
    else:
        messages.warning(request, "An error occured")
        return redirect("account:dashboard")
    
def request_completed(request, request_reciever_account_number, transaction_id):
    request_reciever_account = Account.objects.get(account_number=request_reciever_account_number)# account of person where user is requesting for money
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "account": request_reciever_account,
        "transaction": transaction
    }
    print(request.user)
    print(request_reciever_account.user.kyc.full_name)
    return render(request, "payment-request/request-completed.html", context)

########################## request settlement ###########################################

def settlement_confirmation(request,request_sender_account_number,transaction_id):

    account = Account.objects.get(account_number=request_sender_account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "account": account,
        "transaction": transaction,
    }

    return render(request, "payment-request/settlement-confirmation.html", context)


def settlement_process(request, request_sender_account_number, transaction_id):

    request_sender_account = Account.objects.get(account_number=request_sender_account_number)# person who sent the request
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    request_settler = request.user # person who  settle money to a request  
    request_settler_account = request.user.account

    if request.method =="POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request_settler_account.pin_number:
            if request_settler_account.account_balance < transaction.amount or request_settler_account.account_balance <= 0:
                messages.warning(request, "Insufficinet Fund")
            else:
                request_settler_account.account_balance -= transaction.amount
                request_settler_account.save()

                request_sender_account.account_balance += transaction.amount
                request_sender_account.save()

                transaction.transaction_status = "request settled"
                transaction.save()

                messages.success(request, f"settlement to {request_sender_account.user.kyc.full_name} was sucessfully done.")
                return redirect("core:settlement_completed",request_sender_account_number, transaction_id)
        else:
            messages.warning(request, "Incorrect Pin Number")
            return redirect("core:settlement_confirmation", request_sender_account_number, transaction_id)
    else:
        messages.warning(request, "error occured")
        return redirect("account:dashboard")
        
 
def settlement_completed(request, request_sender_account_number, transaction_id):
    request_reciever_account = Account.objects.get(account_number=request_sender_account_number)# account of person where user is requesting for money
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "account": request_reciever_account,
        "transaction": transaction
    }
    print(request.user)
    print(request_reciever_account.user.kyc.full_name)
    return render(request, "payment-request/settlement-completed.html", context)

def delete_request(request,  account_number, transaction_id ):
    
    account = Account.objects.get(account_number=account_number)# account of person where user is requesting for money
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.user == transaction.user: 
        transaction.delete()
        messages.success(request, "payment request was deleted successfully")
        return redirect("core:transaction-list")
    else:
        return redirect("core:transaction-list")
    
   





            




    

        
        






    