from .forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login, logout
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required

def index(request):
    messages_to_dispaly=messages.get_messages(request)
    return render(request, "registration/index.html", {"messages":messages_to_dispaly})

def register_user(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active= False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activează-ți contul!"
            message=render_to_string("registration/account_activation_email.html", {
                "user": user, 
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user)
            })
            to_email=form.cleaned_data.get("email")
            email=EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, "Te rog să îți verifici e-mailul pentru a finaliza înregistrarea.")
            return redirect("index")
    return render(request, "registration/register.html", {"form":form})
        
def activate(request, uidb64, token):
    User =get_user_model()

    try: 
        uid=force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()

        login(request, user)

        messages.success(request, "Contul tău a fost activat cu succes!")
        return redirect(reverse("login"))
    else:
        messages.error(request, "Link-ul de activare a contului este invalid sau a expirat!")
        return redirect("index")


@login_required(login_url='accounts/register/')    
def homepage(request):
    messages_to_dispaly=messages.get_messages(request)
    return render(request, "homepage.html", {"messages":messages_to_dispaly})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')