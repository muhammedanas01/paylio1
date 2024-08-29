from django.urls import path 
from core import views, transfer, transaction, payment_request, credit_card

app_name = "core"

urlpatterns = [
    path("", views.sample, name="index"),

    #transfers
    path("search-account/", transfer.search_user_by_account_number, name="search-account"),
    path("amount-transfer/<account_number>/", transfer.amount_transfer, name="amount-transfer"),
    path("amount-transfer-process/<account_number>/", transfer.AmountTransferProcess, name="amount-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>/", transfer.TransferConfirmation, name="transfer-confirmation"),
    path("transfer-process/<account_number>/<transaction_id>/", transfer.transfer_process, name="transfer-process"),
    path("transfer-completed/<account_number>/<transaction_id>/", transfer.transfer_completed, name="transfer-completed"),

    #transactions(list)
    path("transaction-list/", transaction.transaction_list, name="transaction-list"),   
    path("transaction-details/<transaction_id>", transaction.transaction_details, name="transaction-details"),   

    #payment-request
    path("search-requested-account/", payment_request.search_user_request, name="search-requested-account"),
    path("request_amount_transfer/<account_number>/", payment_request.request_amount_transfer, name="request_amount_transfer"),
    path("request_amount_transfer_process/<account_number>/", payment_request.request_amount_transfer_process, name="request_amount_transfer_process"),
    path("request_confirmation/<request_reciever_account_number>/<transaction_id>", payment_request.request_confirmation, name="request_confirmation"),
    path("amount_request_final_process/<request_reciever_account_number>/<transaction_id>", payment_request.amount_request_final_process, name="amount_request_final_process"),
    path("request-completed/<request_reciever_account_number>/<transaction_id>", payment_request.request_completed, name="request-completed"),

    # request settlement confirmation
    path("settlement_confirmation/<request_sender_account_number>/<transaction_id>", payment_request.settlement_confirmation, name="settlement_confirmation"),
    path("settlement_process/<request_sender_account_number>/<transaction_id>", payment_request.settlement_process, name="settlement_process"),
    path("settlement_completed/<request_sender_account_number>/<transaction_id>", payment_request.settlement_completed, name="settlement_completed"),
    path("delete_request/<account_number>/<transaction_id>", payment_request.delete_request, name="delete_request"),

    # credit card
    path("card_detail/<card_id>", credit_card.credit_card_detail, name="card_detail"),
    path("fund_credit_card/<card_id>", credit_card.fund_credit_card, name="fund_credit_card"),
    path("withdraw_fund/<card_id>", credit_card.withdraw_fund, name="withdraw_fund"),
    path("delete_card/<card_id>", credit_card.delete_card, name="delete_card"),


]