from django.shortcuts import  render, redirect
from .forms import NewUserForm, DepositForm, WithdrawForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import redis, json
from paypalcheckoutsdk.core import LiveEnvironment, SandboxEnvironment, PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersGetRequest
from django.forms.models import model_to_dict
from django.views.generic import FormView, TemplateView, View
from django.http import JsonResponse, HttpResponse
from .forms import PayPalPaymentsForm
from currency_converter import CurrencyConverter
from django.core import serializers
from .game import *


class PayPalCheckOutView(FormView):	
	"""Handle a PayPal payments"""
	form_class = PayPalPaymentsForm
	template_name = 'checkout.html'
	success_url = '/'

	PAYPAL_CLIENT_ID = 'AT-T_G9c4b5ONFenoD6TI9Ll3__bKC7vG2lXFh1RVs0WaevO-YQGI7lV4PoehzER654_yO1Z-43nUzZk'

	PAYPAL_CLIENT_SECRET = 'ENtJlN8ZvA8M5ti_uGvsy99pItA30AJUuWiGleub9zJBLPTaXMocC3OK-6BVRRf8kTtwAQjJkCPWG2Ju'


	def get_converted_amount(self, amount, currency):
		return CurrencyConverter().convert(amount, currency, 'USD')
		
	def check_payment_status(self, order_id=None):
		""" Checks payment status and return True if it paid or False if it not """
		
		environment_case = SandboxEnvironment
		
		environment = environment_case(client_id=self.PAYPAL_CLIENT_ID, client_secret=self.PAYPAL_CLIENT_SECRET)
		client = PayPalHttpClient(environment)
		request = OrdersGetRequest(order_id)

		response = client.execute(request)

		result = response.result['status'].lower()


		return result == 'completed'
	
	def get_context_data(self, *args, **kwargs):
		context = super(PayPalCheckOutView, self).get_context_data(*args, **kwargs)

		context['client_id'] = self.PAYPAL_CLIENT_ID

		context['amount'] = self.kwargs['amount']

		context['currency'] = self.kwargs['currency']

		context['description'] = 'Some payment description to the user'
		return context
		
	
	def form_valid(self, form):
		order_id = form.cleaned_data['order_id']
		
		result_status = self.check_payment_status(order_id)
		if result_status:
			self.request.user.account_balance += round(float(self.get_context_data()['amount']), 2)
			self.request.user.save()
		return super().form_valid(form)

# Create your views here.

class HomeView(TemplateView):
	template_name = 'homepage.html'
	
class DepositView(View):
	def post(self, request):
		form = DepositForm(request.POST)
		if form.is_valid():
			amount = form.cleaned_data.get('amount').amount
			currency = form.cleaned_data.get('amount').currency
			request.session['deposit'] = True
			return redirect("deposit_checkout", currency=currency, amount=amount)
	def get(self, request):
		form = DepositForm()
		return render (request=request, template_name="deposit.html", context={"deposit_form": form})

class WithdrawView(View):
	def post(self, request):
		form = DepositForm(request.POST)
		if form.is_valid():
			amount = form.cleaned_data.get('amount').amount
			currency = form.cleaned_data.get('amount').currency
			request.session['withdraw'] = True
			return redirect("withdraw_checkout", currency=currency, amount=amount)
	def get(self, request):
		form = DepositForm()
		return render (request=request, template_name="withdraw.html", context={"withdraw_form": form})

class RegisterView(View):
	def post(self, request):
		if request.user.is_anonymous:
			form = NewUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				login(request, user)
				messages.success(request, "Registration successful." )
				return redirect("/")
			messages.error(request, "Unsuccessful registration. Invalid information.")
		return redirect(request.META.get('HTTP_REFERER'))
	
	def get(self, request):
		if request.user.is_anonymous:
			form = NewUserForm()
			return render (request=request, template_name="register.html", context={"register_form":form})
		return redirect(request.META.get('HTTP_REFERER'))

class LoginView(View):
	def post(self, request):
		if request.user.is_anonymous:
			form = AuthenticationForm(request, data=request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=password)
				if user is not None:
					login(request, user)
					messages.info(request, f"You are now logged in as {username}.")
					return redirect("/")
				else:
					messages.error(request,"Invalid username or password.")
			else:
				messages.error(request,"Invalid username or password.")
		return redirect(request.META.get('HTTP_REFERER'))
	def get(self, request):
		if request.user.is_anonymous:
			form = AuthenticationForm()
			return render(request=request, template_name="login.html", context={"login_form":form})
		return redirect(request.META.get('HTTP_REFERER'))	

class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect("login")

class LowTableView(TemplateView):
	template_name = 'table.html'
	
class GetUserBalance(View):
	def get(self, request):
		return HttpResponse(request.user.account_balance)
		
class GetGameBalance(View):
	def post(self, request):
		redis_db = redis.Redis(
		 host= '192.168.56.1',
		 port= '6379', 
		 password = "rootkotka",
		 db = 1
		)
		redis_db.set(request.user.id, request.POST['game_bal'])
		return HttpResponse(request.POST['game_bal'])

class LowTableSitView(View):
	def get(self, request):
		redis_db_0 = redis.Redis(
		 host= '192.168.56.1',
		 port= '6379', 
		 password = "rootkotka",
		 db = 0
		)
		redis_db_1 = redis.Redis(
		 host= '192.168.56.1',
		 port= '6379', 
		 password = "rootkotka",
		 db = 1
		)
		redis_dict = {}
		redis_dict['id'] = request.user.id
		redis_dict['username'] = request.user.username
		redis_dict['first_name'] = request.user.first_name
		redis_dict['last_name'] = request.user.last_name
		redis_dict['table'] = 'low'
		game_bal = float(redis_db_1.get(request.user.id))
		redis_dict['game_balance'] = game_bal
		redis_db_0.hmset(request.user.id, redis_dict)
		json_object = json.dumps(redis_dict, indent = 4) 
		request.user.account_balance -= game_bal
		request.user.save()
		redis_db_1.delete(request.user.id)
		return JsonResponse(json_object, safe = False)

class LowTableHitView(View):
	def get(self, request):
		tmp = get_card()
		msg = f'{tmp.card_name}-{tmp.suit}.png'
		return HttpResponse(msg, content_type='text/plain')

@login_required()
def table_medium(request):
	return render(request=request, template_name="table.html")
@login_required()
def table_high(request):
	return render(request=request, template_name="table.html")
@login_required()
def table_vip(request):
	return render(request=request, template_name="table.html")