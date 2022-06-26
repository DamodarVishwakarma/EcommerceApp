from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from accounts.forms import RegistrationForm
from accounts.models import Account


# Create your views here.
def register(request):
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phone_number = form.cleaned_data.get("phone_number")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name, last_name, username, email, password
            )
            user.phone_number = phone_number
            user.save()
            messages.success(request, "Registration Successful !")

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "SSI Ecomm | Please Activate Account"
            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank You for registering with us. We have sent you the verification email to your email address. Please verify if for login.')
            return redirect("/accounts/login/?command=verification&email=" + email)

            # return redirect("registration")
        form = RegistrationForm()

    context_data = {"form": form}
    return render(request, "accounts/register.html", context_data)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your Account has been successfully activated!")
        return redirect("login")
    else:
        messages.error(request, "Invalid Activation Link")
        return redirect("registration")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(email=email, password=password)

        if user:
            auth.login(request, user)
            return redirect("ssi-home")
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect("login")

    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out successfully!")
    return redirect("login")