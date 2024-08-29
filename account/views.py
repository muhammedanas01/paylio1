from django.shortcuts import render, redirect
from account.models import Account, KYC
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard

# Create your views here.
@login_required
def account(request):
    if request.user.is_authenticated: 
        try:
            user = request.user
            kyc = KYC.objects.get(user=user) # here in account the kyc info will be showing so without submiting kyc user wont able to view their account.
        except:
            messages.warning(request, "you need to submit your kyc.")
            return redirect('account:kyc-reg') # here it redirect to kyc registration page for submiting kyc.
        
        account = Account.objects.get(user = request.user)

    else:
        messages.warning(request, "you need to submit your kyc.")
    # form = KYCForm(instance=kyc)
    context = {
        'account':account,
        'kyc':kyc,
        'user':user
    }
    return render(request, "account/account.html", context)# here in account.html page the kyc info are shown thats why user can't go to account page without submitting kyc.


@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user = user)

    try:
        kyc = KYC.objects.get(user = user) # if user has already submitted kyc instead of creating new kyc user can update the existing kyc so this line is to check for already existing kyc.
    except KYC.DoesNotExist:
        kyc = None # if there there is no existing kyc for user will create new one.
    

    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        form = KYCForm(request.POST, request.FILES, instance=kyc)# here we use django's inbuild form to get user's kyc details.(refer account.forms.py) here kyc will new or updated one refer line.no 37
        if form.is_valid(): # validates if the form is filled correctly according to instruction.(#placeholder)
            new_form = form.save(commit=False) # here form will be saved but will not commit database.
            new_form.user = user # it sets the relation ship  to identify kyc and its user.(there is a user field in class KYC (account.models.py) )
            new_form.account = account
            new_form.save()
            messages.success(request, 'KYC form submitted successfully, In review now')
            return redirect("account:account")
    
    form = KYCForm(instance=kyc) # here the kyc is none it means it's a new form(refer line.no 39)
    
    context = {
            'account': account,
            'form': form,
            'kyc':kyc
        }
    return render(request, 'account/kyc-form.html', context)

def dashboard(request):
    if request.user.is_authenticated:
        try:
            user = request.user
            account = Account.objects.get(user=user)
            kyc = KYC.objects.get(user=user)
        except:
            messages.warning(request, "account not found")
            return redirect("userauths:login")
        
        credit_card = CreditCard.objects.filter(user = request.user)
  
        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()

                card_id = new_form.card_id
                messages.success(request,"Card added successfully")
                return redirect("core:card_detail", card_id)
        else:
            form = CreditCardForm

    else:
        messages.warning(request, "you need to login to access the dashboard")
        return redirect("userauths:login")
    context = {
        "account": account,
        "kyc": kyc,
        "user": user,
        "form":form,
        "credit_card":credit_card
    }

    return render(request, 'account/dashboard.html', context)


# *1. def kyc_registration(request):*
# - Defines a view function named kyc_registration that takes a request object as an argument.

# *2. user = request.user*
# - Retrieves the currently logged-in user from the request object.

# *3. account = Account.objects.get(user=user)*
# - Retrieves the user's account instance from the database using the Account model.

# *4. try: kyc = KYC.objects.get(user=user)*
# - Tries to retrieve an existing KYC (Know Your Customer) instance for the user from the database using the KYC model.

# *5. except KYC.DoesNotExist: kyc = None*
# - If no KYC instance exists for the user, sets kyc to None.

# *6. if request.method == 'POST':*
# - Checks if the request method is POST (i.e., the form has been submitted).

# *7. print(request.POST)*
# - Prints the POST data (form data) for debugging purposes.

# *8. print(request.FILES)*
# - Prints the uploaded files (if any) for debugging purposes.

# *9. form = KYCForm(request.POST, request.FILES, instance=kyc)*
# - Creates a new KYCForm instance with the submitted data and files, and associates it with the existing KYC instance (if any).

# *10. if form.is_valid():*
# - Checks if the form data is valid.

# *11. new_form = form.save(commit=False)*
# - Saves the form data to a new KYC instance without committing it to the database yet.

# *12. new_form.user = user*
# - Sets the user attribute of the new KYC instance to the current user.

# *13. new_form.account = account*
# - Sets the account attribute of the new KYC instance to the user's account.

# *14. new_form.save()*
# - Saves the new KYC instance to the database.

# *15. messages.success(request, 'KYC form submitted successfully, In review now')*
# - Displays a success message to the user.

# *16. return redirect("core:index")*
# - Redirects the user to the core:index URL.

# *17. form = KYCForm(instance=kyc)*
# - Creates a new KYCForm instance with the existing KYC data (if any).

# *18. context = {'account': account, 'form': form, 'kyc': kyc}*
# - Creates a context dictionary with the account, form, and KYC data.

# *19. return render(request, 'account/kyc-form.html', context)*

# - Renders the kyc-form.html template with the context data.
