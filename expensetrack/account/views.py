from django.shortcuts import render,redirect
# from .models import User
from django.contrib import messages
from django.contrib.auth.models import User,auth

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail


# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        pswd = request.POST.get('password')
        print(email, pswd)
        user = auth.authenticate(username=email, password=pswd)
        print(user)
        if user is not None:
            request.session['email'] = email
            print("not none")
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid email or password')
            return redirect('login')
    return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Add validation logic here
        if not first_name or not last_name or not username or not email or not password:
            messages.warning(request, 'Please fill in all the fields.')
            return redirect('register')

        if password != password_confirm:
            messages.warning(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists.')
            return redirect('register')

        # You can add more specific validation logic here, such as checking the email format or password complexity.

        # Create a new user if data is valid
        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.is_active = False
        user.save()
        # You can add additional logic here, such as sending a confirmation email.
        current_site = get_current_site(request)
        message = render_to_string('account_verification_email.html', {
                        'user': user,
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })

        send_mail(
                        'Please activate your account',
                        message,
                        'onlinefirststep1@gmail.com',
                        [email],
                        fail_silently=False,
                    )
        messages.info(request, 'Please verify your email for login !!!')
     
        return redirect('login')  # Redirect to the login page after successful registration

    return render(request, "register.html")


def base(request):
    return render(request,"base.html")

def forgotpwd(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email, is_active=True).first() 
        if user:
            user = User.objects.get(email__exact=email)

            # Reset password email


            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'onlinefirststep1@gmail.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.warning(request, 'Account does not exist!')
            return redirect('forgotpwd')
    return render(request,"forgotpassword.html")



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')    




def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')


def dashboard(request):
    return render(request,"dashboard.html")



def logout(request):
    auth.logout(request)
    return redirect('login')