from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import RegisterForm, LoginForm, CustomUserChangeForm, CustomPasswordChangeForm, CustomPasswordResetForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize

# Create your views here.

# Send email Token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from .models import User as UserModel
from product.models import Cart, Category, ProductInCart, ProductInPayment, Payment


def login(request):
    categories = Category.objects.all()
    # if (request.user.is_authenticated):
    #     return redirect("index")
    if request.method == "GET":
        next = ''
        if 'next' in request.GET:
            next = request.GET['next']
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form, 'next': next})

    form = LoginForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        next_url = request.GET.get('next')
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, total=0)

        count = 0
        total = 0

        productsInCart = ProductInCart.objects.filter(cart=cart)
        print(1)
        for p in productsInCart:
            count = count + p.quantity
            total = total + p.product.price * p.quantity

        print(2)
        request.session['productsInCart'] = serialize('json', productsInCart)
        request.session['count'] = count

        print(3)
        if next_url:
            print(4)
            return HttpResponseRedirect(next_url)
        else:
            print(5)
            return redirect('/')

    return render(request, 'accounts/login.html', {'form': form, 'title': 'Login', 'categories': categories})


def logout(request):
    auth_logout(request)
    try:
        del request.session['productsInCart']
        del request.session['count']
    except KeyError:
        pass
    return redirect('/accounts/login')


def register(request):
    if (request.user.is_authenticated):
        return redirect("index")

    categories = Category.objects.all()

    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
    #    user.is_active = False
        user.save()
        current_site = get_current_site(request)
        # mail_subject = 'Activate your blog account.'
        # message = render_to_string('accounts/acc_active_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })
        # to_email = form.cleaned_data.get('email')
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()
        # return HttpResponse('Please confirm your email address to complete the registration')
        messages.success(request, 'Register success')
        return redirect('login')
    return render(request, 'accounts/register.html', {'form': form, 'categories': categories})


@login_required
def profile(request):
    if request.method == "GET":
        categories = Category.objects.all()
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form, 'categories': categories})

    form = CustomUserChangeForm(data=request.POST, instance=request.user)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
    return redirect('/accounts/profile')


@login_required
def userPayments(request):
    payments = Payment.objects.filter(
        user=request.user).order_by('-created_at')
    categories = Category.objects.all()

    context = {
        'payments': payments,
        'categories': categories
    }

    return render(request, 'accounts/user_payments.html', context)


@login_required
def userPayment(request, id):
    payment = get_object_or_404(Payment, user=request.user, pk=id)
    products = ProductInPayment.objects.filter(
        payment=payment).select_related('product')

    categories = Category.objects.all()

    context = {
        'payment': payment,
        'products': products,
        'categories': categories
    }

    return render(request, 'accounts/user_payment.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# @login_required
# def home(request):
#     contacts = Contact.objects.filter(owner_user=request.user)
#     pre_orders = Pre_Order.objects.filter(owner_user=request.user)

#     context = {
#         'contacts': contacts,
#         'pre_orders': pre_orders
#     }

#     return render(request, 'accounts/home.html', context)


# @login_required
# def contact(request, id):
#     contact = get_object_or_404(Contact, pk=id)
#     if contact.owner_user != request.user:
#         return redirect('home')

#     contact_form = ContactForm(instance=contact)
#     context = {
#         'form': contact_form,
#         'contact': contact,
#     }

#     return render(request, 'houses/contact.html', context)
