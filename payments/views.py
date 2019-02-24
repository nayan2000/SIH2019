# from django.contrib.auth.models import User
# from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework.reverse import reverse

# import json
# import requests

# from instamojo_wrapper import Instamojo

# class Transfer(APIView):
# 	"""
# 		The API endpoint that will be called when money is to be transferred
# 		from one user's wallet to another. This view may even be called by other
# 		views such as the PlaceOrder view to abstract the process of
# 		transferring money.
# 	"""

# 	permission_classes = (IsAuthenticated, TokenVerification,)

# 	def post(self, request, format=None):
#         data = request.data
#         amount = 0
#         try:
#             amount = data["amount"]
#             target_user = User.objects.get(id=data["target_user"])
#         except KeyError as missing:
#             msg = {"message": "missing the following field: {}".format(missing)}
#             return Response(msg, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             try:
#                 # target_user = decString(data["target_user"])[0]
#                 # target_user = User.objects.get(id=target_user)
#                 target_user = Wallet.objects.get(uuid=data["target_user"]).user
#             except:
#                 msg = {"message" : "Invalid request!"}
#                 return Response(msg, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             source = request.user.wallet
#             target = Wallet.objects.get(user=target_user)
#         except Wallet.DoesNotExist:
#             msg = {"message": "Wallet does not exist"}
#             return Response(msg, status=status.HTTP_404_NOT_FOUND)

#         if not source.profile == target.profile:
#             msg = {"message" : "Invalid action. You can only transfer money to a {}".format(source.get_profile_display().title())}
#             return Response(msg, status = status.HTTP_403_FORBIDDEN)

#         if source == target:
#             return Response({"message": "You can't transfer money to yourself."}, status=status.HTTP_403_FORBIDDEN)

#         if amount < 0:
#             return Response({"message": "transfered amount cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)

#         if amount > source.getTotalBalance():
#             return Response({"message": "Insufficient funds."}, status=status.HTTP_200_OK) # status 200 for the iOS app.

#         source.transferTo(target, amount, transfertype="transfer")

#         msg = {"message": "Request successful!"}
#         return Response(msg, status=status.HTTP_200_OK)

# class AddMoney(APIView):
# 	"""
# 		The API endpoint that will handle funding requests from
#         the app, The user can use Credit/Debit Cards or UPIs via Instamojo.
# 	"""

# 	permission_classes= (IsAuthenticated, TokenVerification,)

# 	def post(self, request, format=None):
# 		data = request.data

# 		try:
# 			origin = request.META["HTTP_X_ORIGIN"]
# 			if origin not in ["iOS", "Web", "Android"]:
# 				return Response({"message": "invalid x-origin"}, status=status.HTTP_400_BAD_REQUEST)
# 		except KeyError:
# 			return Response({"message": "x-origin missing from headers."}, status=status.HTTP_400_BAD_REQUEST)

# 		try:
# 			try:
# 				amount=data['amount']
# 			except KeyError as missing_data:
# 				return Response({"message": "Missing the following field: {}".format(missing_data)}, status=status.HTTP_400_BAD_REQUEST)
# 			if amount<0:
# 				return Response({"message": "Amount to be added cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
# 			if is_swd:
# 				try:
# 					bitsian_profile = Bitsian.objects.get(user=request.user)
# 				except:
# 					return Response({"message": "The user has not been identified as a bitsian."}, status=status.HTTP_403_FORBIDDEN)
# 				try:
# 					bitsian_wallet = bitsian_profile.user.wallet
# 				except:
# 					return Response({"message": "The bitsian has no wallet. Cannot add money as of yet. Please contact the administrators."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

# 				teller = Teller.objects.get(user__username="SWD")
# 				teller_wallet = Teller.objects.get(user__username="SWD").user.wallet

# 				Transaction.objects.create(
# 					amount=amount,
# 					transfer_from=teller_wallet,
# 					transfer_to=bitsian_wallet,
# 					transfer_type="add"
# 				)

# 				teller.cash_collected += amount
# 				teller.save()
# 				bitsian_wallet.balance.add(amount,0,0,0)


# 				return Response({"message": "Money added successfully!"})
# 			if amount not in range(10,200000):
# 				return Response({"message": "Amount to be added has to be between Rs. 10 and Rs. 2,00,000."})
# 			try:
# 				profile = Participant.objects.get(user=request.user)
# 			except:
# 				try:
# 					profile = Bitsian.objects.get(user=request.user)
# 				except:
# 					return Response({"message": "The user has not been identified as a bitsian nor as participant."}, status=status.HTTP_403_FORBIDDEN)
# 			user_email = profile.email
# 			user_mobile = profile.phone
# 			user_name = profile.name

# 			# just check if the wallet exists before continuing
# 			try:
# 				wallet = profile.user.wallet
# 			except:
# 				return Response({"message": "The user has no wallet. Cannot add money as of yet."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

# 			if origin == "iOS":
# 				redirect_url = reverse("shop:AddMoneyResponseIOS",request=request)
# 			elif origin == "Web":
# 				redirect_url = reverse("shop:AddMoneyResponseWeb",request=request)
# 			elif origin == "Android":
# 				redirect_url = reverse("shop:AddMoneyResponseAndroid",request=request)

# 			response = api.payment_request_create(
# 				amount=str(amount),
# 				purpose='Add Money to wallet',
# 				send_email=False,
# 				email=user_email,
# 				buyer_name=user_name,
# 				phone=user_mobile,
# 				redirect_url=redirect_url
# 			)

# 			return Response({'url': response['payment_request']['longurl']})

# 		except Exception as e:
# 			return Response({'message': 'Add Money Failed! '})



# def AddMoneyResponse(request):
# 	'''
# 		A function called by the AddMoneyResponse____ views
# 	'''

# 	data = request.GET

# 	payid = data['payment_request_id']

# 	try:
# 		headers = {'X-Api-Key': INSTA_API_KEY, 'X-Auth-Token': AUTH_TOKEN}
# 		r = requests.get('https://www.instamojo.com/api/1.1/payment-requests/'+str(payid),headers=headers)
# 	except:
# 		headers = {'X-Api-Key': INSTA_API_KEY_test, 'X-Auth-Token': AUTH_TOKEN_test}
# 		r = requests.get('https://test.instamojo.com/api/1.1/payment-requests/'+str(payid), headers=headers)

# 	json_ob=r.json()
# 	payment_status = json_ob['success']

# 	if not payment_status:
# 		return 'Payment not successful/cancelled.'

# 	else:
# 		try:
# 			profile = Participant.objects.get(email=json_ob['payment_request']['email'])
# 		except:
# 			try:
# 				profile = Bitsian.objects.get(email=json_ob['payment_request']['email'])
# 			except:
# 				return "The user has not been identified as a bitsian nor as participant."

# 		wallet = Wallet.objects.get(user=profile.user)
# 		amount = int(float(json_ob['payment_request']['amount']))
# 		payment_id=json_ob['payment_request']['payments'][0]['payment_id']

# 		transaction, created = Transaction.objects.get_or_create(amount=amount, transfer_from=wallet, transfer_to=wallet,transfer_type="add", payment_id=payment_id)
# 		if not created:
# 			return "You have encashed this money."

# 		wallet.balance.add(0,0,amount,0)

# 		return "Money Added Successfully."


# class AddMoneyResponseWeb(APIView):

# 	def get(self, request, format=None):
# 		message = AddMoneyResponse(request)
# 		# response = redirect( url_provided_by_frontend_team )
# 		# reponse["X-Message"] = message
# 		# return response
# 		return HttpResponse(message) # temporary stub, until we have url_provided_by_frontend_team



# class AddMoneyResponseIOS(APIView):

# 	# renderer_classes = [TemplateHTMLRenderer]
# 	# template_name = 'shop/base.html'

# 	def get(self, request, format=None):
# 		message = AddMoneyResponse(request)
# 		return render(request, "shop/base.html", {"message": message}) # get a better page from frontend team?


# class AddMoneyResponseAndroid(APIView):

# 	def get(self, request, format=None):
# 		message = AddMoneyResponse(request)
# 		return render(request, "shop/templates", {"message": message}) # get a better page from frontend team?

