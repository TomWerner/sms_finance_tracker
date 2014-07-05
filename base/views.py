""" Views for the base application """
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from base.models import *

import datetime

def frontpage(request):
    """ Default view for the root """
    if request.user.is_authenticated():
        return redirect("/home")
    else:
        return render(request, 'base/frontpage.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST.has_key('remember_me'):
                    request.session.set_expiry(1209600) # 2 weeks
                # Redirect to a success page.
                print "success"
            else:
                # Return a 'disabled account' error message
                print "disabled account"
        else:
            # Return an 'invalid login' error message.
            print "invalid login"
    #endif
    return redirect("/")
    
def logout_view(request):
    logout(request)
    
    return redirect("/")
    
def username_ok(username):
    if len(username) < 5 or len(username) > 15:
        return False
    if User.objects.filter(username = username).exists():
        return False
    
    return True
    
def passwords_ok(password1, password2):
    if password1 != password2:
        return False
    if len(password1) < 8:
        return False
    return True
    
def registration_view(request):
    if request.method == 'POST':
        print request.POST
        username = request.POST.get('username', "")
        password1 = request.POST.get('password1', "")
        password2 = request.POST.get('password2', "")
        phone_number = request.POST.get('phonenumber', '')
        if username_ok(username) and passwords_ok(password1, password2):
            user = User.objects.create_user(username, password=password1)
            user.save()
            
            holder = AccountHolder(user = user, phone_number = phone_number)
            holder.save()
            
    #endif
    return redirect("/home")
    
@login_required(redirect_field_name="/")
def home_view(request):

    #get the current account
    ah = AccountHolder.objects.filter(user__username=request.user.username)
    
    if len(ah) > 0:
        ah = ah[0]
        ac = MoneyAccount.objects.filter(user=ah)
        account_name = ""
        account_tag = ""
        records = []
        
        if len(ac) > 0:
            ac = ac[0]
            records = AccountEntry.objects.filter(account=ac)
            account_name = ac.account_name
            account_tag = ac.account_tag
            
    else:
        print "make an account model"
        #TODO: if not ah create ah
    #endif
    
    return render(request, 'base/loggedInHome.html', 
        {'account_count' : len(ah.moneyaccount_set.all()),
         'account_list' : MoneyAccount.objects.filter(user=ah),
         #FIX THIS
         'selected_account' : account_name,
         'selected_account_tag' : account_tag,
         'records' : records,
         'no_records' : len(records) == 0,
         })

@login_required(redirect_field_name="/")
def create_money_account_view(request):
    
    return render(request, 'base/createMoneyAccount.html')
    
def create_money_account_post(request):
    print request.POST
    #get the current account
    ah = AccountHolder.objects.filter(user__username=request.user.username)[0]
    account_name = request.POST.get("accountName", "")
    account_tag = request.POST.get("accountTag", "")
    account_description = request.POST.get("accountDescription", "")
    
    if (account_name == ""):
        return redirect("/home") #error
    
    m_acc = MoneyAccount(user = ah, account_name = account_name, account_tag = account_tag, account_description = account_description)
    m_acc.balance = 0
    m_acc.save()
    
    
    
    return redirect("/home")
    
    
def create_balance_post(request):
    print request.POST
    
    #get the current account
    ah = AccountHolder.objects.filter(user__username=request.user.username)[0]
    account = MoneyAccount.objects.filter(account_tag=request.POST['account'])[0]
    account.balance = 0
    amount = float(request.POST['amount'])
    
    transaction = AccountEntry(account = account, date = str(datetime.datetime.now()),
                               tag='START', comment='Initial balance', amount = amount,
                               balance=float(account.balance) + amount)
    account.balance = amount
    
    transaction.save()
    account.save()
    return redirect("/home")
    
def create_transaction_post(request):
    print request.POST
    
    #get the current account
    ah = AccountHolder.objects.filter(user__username=request.user.username)[0]
    account = MoneyAccount.objects.filter(account_tag=request.POST['account'])[0]
    amount = float(request.POST['amount']) * float(request.POST["sign"])
    tag = request.POST.get("tag", "")
    comment = request.POST['comment']
    
    
    transaction = AccountEntry(account = account, date = str(datetime.datetime.now()),
                               tag=tag, comment=comment, amount = amount,
                               balance=float(account.balance) + amount)
    account.balance = float(account.balance) + amount
    
    transaction.save()
    account.save()
    
    
    
    
    
    
    return redirect("/home")
    
@csrf_exempt
def sms_update(request):
    print request.POST
    print request.POST['phone_number']
    ah = AccountHolder.objects.filter(phone_number=request.POST["phone_number"])
    
    if len(ah) == 0:
        return HttpResponse("{'result' : 'no_matching_phone'}")
    ah = ah[0]
    
    account = MoneyAccount.objects.filter(account_tag=request.POST['account_tag'])
    
    if len(account) == 0:
        return HttpResponse("{'result' : 'no_matching_account'}")
    account = account[0]
    
    amount = float(request.POST['amount'])
    comment = request.POST['comment']
    
    
    transaction = AccountEntry(account = account, date = str(datetime.datetime.now()),
                               comment=comment, amount = amount,
                               balance=float(account.balance) + amount)
    account.balance = float(account.balance) + amount
    
    transaction.save()
    account.save()
    
    return HttpResponse("{'result' : 'ok'}")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    