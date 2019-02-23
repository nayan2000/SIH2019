from main.models import UserProfile

def generate_email_token(user_profile):
	'''
	To generate a unique email token for a registering user
	'''
	import uuid
	token = uuid.uuid4().hex
	registered_tokens = [profile.email_token for profile in UserProfile.objects.all()]

	while token in registered_tokens:
		token = uuid.uuid4().hex

	user_profile.email_token = token
	user_profile.save()

	return token

def authenticate_email_token(token):
	'''
	To authenticate the token sent to a user while verifying email
	'''
	try:
		user_profile = UserProfile.objects.get(email_token=token)
		user_profile.email_verified = True
		user_profile.save()
		return user_profile
	except :
		return False