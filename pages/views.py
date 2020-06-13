from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse

from product.models import Product, Category, Cart, ProductInCart, Payment, PaymentType, Delivery, ProductInPayment

from django.core.serializers import serialize

from accounts.forms import CustomUserChangeForm

from .forms import ContactPageForm

from .models import Contact

from .choices import limit_choices as l, price_choices

from django.contrib import messages

from django.contrib.auth.decorators import login_required


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    limit_choices = l

    context = {
        'products': products,
        'categories': categories,
        'limit_choices': limit_choices
    }

    return render(request, 'pages/index.html', context)


def about(request):
    categories = Category.objects.all()

    context = {

        'categories': categories
    }
    return render(request, 'pages/about.html', context)


def listings(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    limit_choices = l
    params = dict(request.GET.lists())

    if "category" in params:
        category = params['category'][0]
        if category:
            products = products.filter(category=category)

    if "search" in params:
        search = params['search'][0]
        if search:
            products = products.filter(name__icontains=search)

    limit = 1

    if "limit" in params:
        limit = params["limit"][0]

    # paginator
    paginator = Paginator(products, limit)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'products': paged_listings,
        'categories': categories,
        'values': request.GET,
        'limit_choices': limit_choices,
        'limit': limit

    }
    return render(request, 'pages/listings.html', context)


def listing(request, id):
    product = get_object_or_404(Product, pk=id)
    categories = Category.objects.all()

    context = {
        'product': product,
        'categories': categories

    }
    return render(request, 'pages/listing.html', context)


@login_required
def cart(request):
    categories = Category.objects.all()

    context = {}
    ids = []
    quantity = {}
    count = 0
    total = 0
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user, total=0)

        # Get all products in cart
    productsInCart = ProductInCart.objects.filter(
        cart=cart).select_related('product')
    for product in productsInCart:

        ids.append(product.product.id)
        quantity[product.product] = product.quantity
        count = count + product.quantity
        total = total + product.quantity * product.product.price

    request.session['count'] = count
    products = Product.objects.filter(id__in=ids)

    context = {
        'products': products,
        'quantity': quantity,
        'productsInCart': productsInCart,
        'count': count,
        'categories': categories,
        'total': total
    }

    return render(request, 'pages/cart.html', context)


def contact(request):
    if request.method == "GET":
        categories = Category.objects.all()

        form = ContactPageForm()
        context = {
            'form': form,
            'categories': categories
        }
        return render(request, 'pages/contact.html', context)

    if request.method == "POST":
        try:
            print(request.POST)
            print(1)
            contact = Contact(name=request.POST['name'], email=request.POST['email'], mobile=request.POST['mobile'],
                              address=request.POST['address'], title=request.POST['title'], content=request.POST['content'])
            print(2)

            print(3)
            contact.save()
            print(4)
            messages.success(request, 'Contact form sent succecully.')
            return redirect('contact')
        except:
            messages.error(request, 'Contact form sent unsuccecully.')
            return redirect('contact')

    return redirect('contact')


@login_required
def addToCart(request, id):
    quantity = request.POST['quantity']
    product = get_object_or_404(Product, pk=id)
    if (request.method == 'POST'):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, total=0)

            # Get all products in cart
        productsInCart = ProductInCart.objects.filter(cart=cart)

        found = False
        for productInCart in productsInCart:
            if product.id == productInCart.product.id:
                print(True)
                productInCart.quantity = productInCart.quantity + int(quantity)
                productInCart.save()
                found = True

        if found == False:
            p = ProductInCart.objects.create(
                cart=cart, product=product, quantity=quantity)
            p.save()

        productsInCart = ProductInCart.objects.filter(
            cart=cart).select_related('product')

        count = 0
        total = 0

        for p in productsInCart:
            count = count + p.quantity
            total = total + p.product.price * p.quantity

        request.session['productsInCart'] = serialize('json', productsInCart)
        request.session['count'] = count

        context = {
            'cart': {
                'productsInCart': serialize('json', productsInCart),
                'count': count
            }
        }

        return JsonResponse(context)


@login_required
def deleteFromCart(request, id):
    if request.method == 'GET':
        return redirect('cart')
    product = get_object_or_404(Product, pk=id)
    product = get_object_or_404(Product, pk=id)
    if (request.method == 'POST'):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, total=0)

            # Get all products in cart
        try:
            deletedProduct = ProductInCart.objects.get(
                cart=cart, product=product)
            deletedProduct.delete()
        except ProductInCart.DoesNotExist:
            pass

    return redirect('cart')


@login_required
def payment(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        paymentTypes = PaymentType.objects.all()
        deliveries = Delivery.objects.all()

        context = {}
        ids = []
        quantity = {}
        count = 0
        total = 0

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, total=0)

            # Get all products in cart
        productsInCart = ProductInCart.objects.filter(
            cart=cart).select_related('product')
        for product in productsInCart:

            ids.append(product.product.id)
            quantity[product.product] = product.quantity
            count = count + product.quantity
            total = total + product.quantity * product.product.price

        request.session['count'] = count
        products = Product.objects.filter(id__in=ids)

        context = {
            'products': products,
            'quantity': quantity,
            'productsInCart': productsInCart,
            'count': count,
            'categories': categories,
            'paymentTypes': paymentTypes,
            'deliveries': deliveries,
            'total': total
        }
        return render(request, 'pages/payment.html', context)

    if request.method == 'POST':
        print("cc")
        print(request.POST)
        payment = None
        try:
            print(1)
            total = 0
            print(2)
            print(request.POST['delivery'])
            delivery = get_object_or_404(Delivery, pk=request.POST['delivery'])
            print(3)
            paymentType = get_object_or_404(
                PaymentType, pk=request.POST['type'])
            print(3)
            payment = Payment(user=request.user, name=request.POST['name'], email=request.POST['email'],
                              mobile=request.POST['mobile'], address=request.POST['address'], delivery=delivery, paymentType=paymentType)
            print(4)
            payment.total = 0
            payment.save()
            cart = Cart.objects.get(user=request.user)
            productsInCart = ProductInCart.objects.filter(
                cart=cart).select_related('product')
            print(5)
            for product in productsInCart:
                print(6)
                paymentProduct = ProductInPayment(
                    payment=payment, quantity=product.quantity, product=product.product)
                paymentProduct.price = product.quantity * product.product.price
                paymentProduct.save()
                total = total + product.quantity * product.product.price
            print(7)
            payment.total = total
            payment.save()
            cart.delete()
            request.session['count'] = 0
            print(8)
            messages.success(request, "Buy product(s) successfully")

            return redirect('index')
        except:
            if payment is not None:
                payment.delete()
            messages.error(request, "There is some error")

            return redirect('payment')

        return redirect('payment')


@login_required
def changeQuantity(request, id):
    quantity = request.POST['quantity']
    product = get_object_or_404(Product, pk=id)
    if (request.method == 'POST'):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, total=0)

            # Get all products in cart
        productsInCart = ProductInCart.objects.filter(
            cart=cart).select_related('product')

        price = 0

        found = False
        for productInCart in productsInCart:
            if product.id == productInCart.product.id:
                print(True)
                productInCart.quantity = int(quantity)
                productInCart.save()
                price = productInCart.product.price * int(quantity)
                found = True

        if found == False:
            p = ProductInCart.objects.create(
                cart=cart, product=product, quantity=quantity)
            price = p.product.price * int(quantity)
            p.save()

        productsInCart = ProductInCart.objects.filter(
            cart=cart).select_related('product')

        count = 0
        total = 0

        for p in productsInCart:
            count = count + p.quantity
            total = total + p.product.price * p.quantity

        request.session['productsInCart'] = serialize('json', productsInCart)
        request.session['count'] = count

        context = {
            'productsInCart': serialize('json', productsInCart),
            'count': count,
            'total': total,
            'price': price

        }

        return JsonResponse(context)


@login_required
def buy(request, id):
    quantity = 1
    product = get_object_or_404(Product, pk=id)
    if (request.method == 'POST'):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user, total=0)

            # Get all products in cart
        productsInCart = ProductInCart.objects.filter(cart=cart)

        found = False
        for productInCart in productsInCart:
            if product.id == productInCart.product.id:
                print(True)
                productInCart.quantity = productInCart.quantity + int(quantity)
                productInCart.save()
                found = True

        if found == False:
            p = ProductInCart.objects.create(
                cart=cart, product=product, quantity=quantity)
            p.save()

        productsInCart = ProductInCart.objects.filter(
            cart=cart).select_related('product')

        count = 0
        total = 0

        for p in productsInCart:
            count = count + p.quantity
            total = total + p.product.price * p.quantity

        request.session['productsInCart'] = serialize('json', productsInCart)
        request.session['count'] = count

        context = {
            'cart': {
                'productsInCart': serialize('json', productsInCart),
                'count': count
            }
        }

        return redirect('cart')
    return redirect('cart')

    # def about(request):

    #     return render(request, 'pages/about.html', {'status': 'about', })

    # def listings(request):
    #     houses = House.objects.all().order_by('-created_at')
    #     paginator = Paginator(houses, 9)
    #     page = request.GET.get('page')
    #     paged_listings = paginator.get_page(page)
    #     context = {
    #         'houses': paged_listings,
    #         'status': 'listings',
    #     }

    #     return render(request, 'pages/listings.html', context)

    # def listing(request, id):
    #     house = get_object_or_404(House, pk=id)
    #     if request.method == 'GET':
    #         house = get_object_or_404(House, pk=id)
    #         print(house.status)
    #         if house.status == 'AVAILABLE' or house.status == 'Available':
    #             form = ContactPageForm()
    #         else:
    #             form = Pre_OrderPageForm()
    #         context = {
    #             'house': house,
    #             'form': form
    #         }

    #         return render(request, 'pages/listing.html', context)
    #     else:
    #         if house.status == 'AVAILABLE' or house.status == 'Available':
    #             form = ContactPageForm(request.POST)
    #         else:
    #             form = Pre_OrderPageForm(request.POST)

    #         contact = form.save(commit=False)
    #         contact.house = house
    #         contact.renter_user = request.user
    #         contact.owner_user = house.owner_user
    #         contact.save()
    #         return redirect('listings')

    # def search(request):
    #     houses = House.objects.all().order_by('-created_at')

    #     # Keywords
    #     if 'keywords' in request.GET:
    #         keywords = request.GET['keywords']
    #         if keywords:
    #             houses = houses.filter(description__icontains=keywords)

    #     if 'city' in request.GET:
    #         city = request.GET['city']
    #         if city:
    #             houses = houses.filter(city__icontains=city)

    #     if 'state' in request.GET:
    #         state = request.GET['state']
    #         if state:
    #             houses = houses.filter(state__icontains=state)

    #     if 'number_of_room' in request.GET:
    #         number_of_room = request.GET['number_of_room']
    #         if number_of_room:
    #             houses = houses.filter(number_of_room__lte=number_of_room)

    #     if 'price' in request.GET:
    #         price = request.GET['price']
    #         if price:
    #             houses = houses.filter(price__lte=price)

    #     paginator = Paginator(houses, 9)
    #     page = request.GET.get('page')
    #     paged_listings = paginator.get_page(page)
    #     context = {
    #         'houses': paged_listings,
    #         'price_choices': price_choices,
    #         'number_of_room_choices': number_of_room_choices,
    #         'state_choices': state_choices,
    #         'values': request.GET
    #     }

    #     return render(request, 'pages/search.html', context)
