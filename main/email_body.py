
def register():
	body = '''<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
			<pre style="font-family:Roboto,sans-serif">
Hello %s!

Thank you for registering.

Please verify your email by clicking on the link below.

<a href='%s'>Click Here</a> to verify your email.

</pre>
		'''	
	return body

def login_creds():
	body='''<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
			<pre style="font-family:Roboto,sans-serif">
Hello %s!

Your email has been verified successfully.
You can now login into the app using the following credentials:
Username : '%s'
Password : '%s'
</pre>
'''
	return body	