"""urlconf for the base application"""

from django.conf.urls import url, patterns

urlpatterns = patterns('base.views',
    url(r'^$', 'frontpage'),
    url(r'^login/$', 'login_view'),
    url(r'^logout/$', 'logout_view'),
    url(r'^registration/$', 'registration_view'),
    url(r'^home/$', 'home_view'),
    url(r'^home/newaccount/$', 'create_money_account_view'),
    url(r'^home/newaccountpost/$', 'create_money_account_post'),
    url(r'^home/createBalance/$', 'create_balance_post'),
    url(r'^home/createTransaction/$', 'create_transaction_post'),
    url(r'^sms_update/$', 'sms_update'),
)
