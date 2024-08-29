from account.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account, KYC
from django.contrib import messages
from django.db.models import Q
from core.models import Transaction
from decimal import Decimal
# 1302327510470
@login_required
def search_user_by_account_number(request):
    #account = Account.objects.filter(account_status = 'active')
    accounts = Account.objects.all()

    search_query = request.POST.get("account_number") # gets the profile of the intended recipient, corresponding to the account number entered by the current user.
    
    if search_query:
        accounts = accounts.filter( # Successfully retrieves  the accurate account information of the intended recipient, ensuring a precise match based on the entered account number.
            Q(account_number=search_query)|  # Q is used when you need to filter a queryset based on multiple conditions, or when you need to use logical operators
            Q(account_id = search_query)
        ).distinct # .distinct() is used to eliminate duplicate results that might occur when filtering


    context = {
        'accounts': accounts, # this shows the infomation(only basic basic info like profilepic, name and account.no are displyed to user) of the indended recipient based on the entered account number.
        'search_query': search_query
    }
    return render(request, 'transfer/search-user-by-account-number.html', context)

# if user clicks on choose button in search-user-by-account-number.html it will go to url adress given in form action. in this case in addition to url it passes  payee's account number also {% url 'core:amount-transfer' account.account_number %}.

def amount_transfer(request, account_number):
    try: 
        account = Account.objects.get(account_number=account_number) # get's the payee's account number
        
    except:
        messages.warning(request, "Account does not exist.")# if enterd a wrong account number
        return redirect('core:search-account') # if account does not exist we will ask user again search for user

    context = {
        'account':account  # if account exist on amount_transfer.html we will display the basic info of payee. # also we ask user to enter the amount and description in amount_transfer.html
    }
    return render(request, "transfer/amount_transfer.html", context) 

# after enetering amount and description in amount_transfer.html and if user clicks the next button in the current template it will go to url adress given in the form action. in this case in addition to url it passes  payee's account number also. {% url 'core:amount-transfer-process' account.account_number %}. which is def AmountTransferProcess

def AmountTransferProcess(request, account_number):
    #note: for this function there is no html template because this process runing behind and redirects to another url adress after exicuting function.
    receiver_account = Account.objects.get(account_number=account_number) # we can retrieve an Account object using any of the unique fields in the model
    sender_account = request.user.account 

    sender = request.user 
    receiver = receiver_account.user 

    if request.method == "POST":
        amount = request.POST.get("amount_sent") # we get this info from amount_tranfer.html
        description = request.POST.get("description") # we get's this info from amount_tranfer.html
        
        # amount and description are getting through a form from amount-transfer.html. #when form is submitted from amount-transfer.html we tells django to go to next page which is : <form action="{% url 'core:amount-transfer-process' account.account_number %} so that's how we reach in this view function"  # path("amount-transfer-process/<account_number>/", transfer.AmountTransferProcess, name="amount-transfer-process")
        # also when the form is submitted from amount_transfer.html trasaction obj will be created. note: here money won't be reduced from sender account only a transaction obj is created 

        # after submiting form from amount-transfer.html below line of code will executed next:
        if sender_account.account_balance >= Decimal(amount):  # creates and keep track of the current new transaction which user wish to complete.
            new_transaction = Transaction.objects.create(
            user = request.user,
            amount = amount,
            description = description,
            
            sender = sender,
            sender_account = sender_account,

            receiver = receiver,
            receiver_account = receiver_account,

            transaction_status = "processing",
            transaction_type = "transfer"
        )
            new_transaction.save()
            transaction_id = new_transaction.transaction_id #"The transaction ID will be generated automatically, as specified in the models.py file. #Shortuuidfield
            return redirect("core:transfer-confirmation", receiver_account.account_number, transaction_id)# here after creating transaction obj we will redirect the page to  this url adress.  #adress: #path("transfer-confirmation/<account_number>/<transaction_id>/", transfer.TransferConfirmation, name="transfer-confirmation"),

        else:
             messages.warning(request,"Insufficient Fund")
             return redirect("core:amount-transfer", receiver_account.account_number)
    else:
         messages.warning(request,"error occured try again")
         return redirect("account:account")

# from def AmountTransferProcess if (if sender_account.account_balance > 0 and amount:) is True it redirects to def TranferConfirmation (refer core/urls.py line.no 12)

def TransferConfirmation(request, account_number, transaction_id):

    # in this function we show's the amount and some other basic details of the trasaction in transfer-confirmation.html to get the confirmation from the user to transfer the money.

    try:
        account = Account.objects.get(account_number=account_number) # gets receiver's account number
        transaction = Transaction.objects.get(transaction_id=transaction_id)# gets transaction obj of the currect transaction(refer line.no between 60 and 74)  
    except:
        messages.warning(request, "transaction does not exist")
        return redirect('core:search-account')

    context = {
        'account': account,
        'transaction': transaction
    }
    return render(request, "transfer/transfer-confirmation.html", context)

# in transfer-confirmation.html if user clicks on the PAY button then it will ask for PIN_NUMBER. its pop up page using javascript on that after entering pin number and we clicks on confirm button it goes to the urls given in form action which is {% url "core:transfer-process" account.account_number transaction.transaction_id %}
    
def transfer_process(request,account_number, transaction_id):
    # note: for this function there is no html template because this function run's behind and redirects to another page after exicuting function.
    receiver_account = Account.objects.get(account_number=account_number) 
    sender_account = request.user.account 
    
    sender = request.user 
    receiver = receiver_account.user 

    transaction = Transaction.objects.get(transaction_id=transaction_id)
    print(transaction)
    transaction_completed = False
    if request.method == "POST":
        pin_number = request.POST.get("pin-number") # gets the pin number enterd by user
        print(pin_number)
        if pin_number == sender_account.pin_number: # verifies pin number with pin number saved in user's database
            transaction.transaction_status == "completed" # in db it changes the staus from default to completed
            transaction.save()

            sender_account.account_balance -= transaction.amount # removes the amount from the sender account and updated sender's account
            sender_account.save()

            receiver_account.account_balance += transaction.amount # add's the amount sent by sender to reciever account.
            receiver_account.save()

            transaction.transaction_status = "completed"
            transaction.save()
            #transaction.transaction_status = "completed"


            messages.success(request, "Transfer is sucessfull.")
            #return redirect("account:account") 
            return redirect("core:transfer-completed", receiver_account.account_number, transaction_id) 
        else:
            messages.warning(request, "incorrect pin")
            return redirect("core:transfer-confirmation", receiver_account.account_number, transaction_id)
        
    messages.warning(request, "An error occured try again later")
    return redirect("core:transfer-confirmation", receiver_account.account_number, transaction_id)

# after verifying pin and transfer is sucsessfull it redirects to def transfer_completed

def transfer_completed(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "transfer does not exist")
        return redirect('core:search-account')

    context = {
        'account': account,
        'transaction': transaction
    }

    return render(request, "transfer/transfer-completed.html", context)

