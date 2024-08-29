from account.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account, KYC
from django.contrib import messages
from django.db.models import Q
from core.models import CreditCard
from decimal import Decimal
from core.forms import CreditCardForm



def credit_card_detail(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = Account.objects.get(user=request.user)
    
    form = CreditCardForm
    context = {
        "account":account,
        "card":credit_card,
        "form":form,    

    }
    return render(request, "credit_card/card-detail.html", context)

def fund_credit_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = Account.objects.get(user=request.user)
    
    if request.method == "POST":
        amount = request.POST.get("amount")
        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount)
            account.save()

            credit_card.amount += Decimal(amount)
            credit_card.save()
            messages.success(request, "Amount Added Successfully")
            return redirect("core:card_detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Fund")
            return redirect("core:card_detail", credit_card.card_id)    
    else:
        messages.warning(request, "Error Occured")
        return redirect("core:card_detail", credit_card.card_id)   
    
def withdraw_fund(request,  card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = Account.objects.get(user=request.user)
    if request.method == "POST":
        withdrawal_amount = request.POST.get("amount")
        
        if credit_card.amount >= Decimal( withdrawal_amount):
            account.account_balance += Decimal(withdrawal_amount)
            account.save()

            credit_card.amount -= Decimal(withdrawal_amount)
            credit_card.save()

            messages.success(request, "withdrawal successfull")
            return redirect("core:card_detail",  credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Fund")
            return redirect("core:card_detail", credit_card.card_id) 
    else:
        messages.warning(request, "Error Occured")
        return redirect("core:card_detail", credit_card.card_id)   
    
def delete_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = Account.objects.get(user=request.user)
    delete = "delete"

    if request.method == "POST":
        delete_confirmation = request.POST.get("delete")
        if delete_confirmation == delete:
            if credit_card.amount > 0 :
                account.account_balance += credit_card.amount
                account.save()
            
                credit_card.delete()
                messages.success(request, "Card deleted successfully, your remaining card balance is transferd to your paylio account.")
                return redirect("account:dashboard")
            else:
                credit_card.delete()
                messages.success(request, "Card deleted successfully.")
                return redirect("account:dashboard")
        else:
            messages.warning(request, "your input does'nt match.")
            return redirect("core:card_detail", credit_card.card_id)
    else:
        messages.warning(request, "Error Occured")
        return redirect("core:card_detail", credit_card.card_id)   
    

    
  

       

        




