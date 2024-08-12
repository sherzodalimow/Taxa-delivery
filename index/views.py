from django.shortcuts import render, redirect
from .models import Product, Category, Cart
from .forms import RegisterForm
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
import telebot


# Объект бота
bot = telebot.TeleBot('7156064615:AAFa-i3wse6JNo8kkw6N45wzaq37nijr6QI')
admin_id = 1942281512


# Create your views here.
def home_page(request):
    # Получаем данные из БД
    products = Product.objects.all()
    categories = Category.objects.all()

    # Передаем данные на фронт
    context = {'products': products,
               'categories': categories}
    return render(request, 'home.html', context)


def get_exact_pr(request, pk):
    exact_product = Product.objects.get(id=pk)

    # Передаем данные на фронт
    context = {'product': exact_product}
    return render(request, 'product.html', context)


def get_exact_category(request, pk):
    exact_category = Category.objects.get(id=pk)
    products = Product.objects.filter(pr_category=exact_category)

    # Передаем данные на фронт
    context = {'products': products}
    return render(request, 'category.html', context)


def to_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        if product.pr_count >= int(request.POST.get('user_product_quantity')):
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_product_quantity=int(request.POST.get
                                                          ('user_product_quantity'))).save()
        return redirect('/')


def get_user_cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)
    pr_id = [t.user_product.id for t in user_cart]
    user_prices = [i.user_product.pr_price for i in user_cart]
    user_pr_amounts = [e.user_product_quantity for e in user_cart]
    pr_amounts = [c.user_product.pr_count for c in user_cart]
    total = 0
    text = (f'Новый заказ!\n\n'
            f'Клиент: {User.objects.get(id=request.user.id).username}\n')
    for p in range(len(user_prices)):
        total += user_prices[p] * user_pr_amounts[p]

    if request.method == 'POST':
        for i in user_cart:
            text += (f'Товар: {i.user_product}\n'
                     f'Количество: {i.user_product_quantity}\n')
        text += f'Итог: {round(total, 2)}'
        bot.send_message(-1002213254265, text)
        for p in range(len(user_prices)):
            product = Product.objects.get(id=pr_id[p])
            product.pr_count = pr_amounts[p] - user_pr_amounts[p]
            product.save(update_fields=["pr_count"])
        user_cart.delete()
        return redirect('/')

    # Отправляем данные на фронт
    context = {'cart': user_cart, 'total': round(total, 2)}
    return render(request, 'cart.html', context)


def del_from_cart(request, pk):
    product_to_delete = Product.objects.get(id=pk)
    Cart.objects.filter(user_id=request.user.id,
                        user_product=product_to_delete).delete()

    return redirect('/cart')


def search_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')

        try:
            exact_product = Product.objects.get(pr_name__icontains=get_product)
            return redirect(f'product/{exact_product.id}')
        except:
            print('не нашел')
            return redirect('/')


class Register(View):
    template_name = 'registration/register.html'


    def get(self, request):
        context = {'form': RegisterForm}
        return render(request, self.template_name, context)


    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.clean_username()
            password2 = form.clean_password2()
            email = form.cleaned_data.get("email")
            user = User.objects.create_user(username, password=password2, email=email)
            user.save()
            login(request, user)
            return redirect('/')
        context = {'form': RegisterForm}
        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    return redirect('/')
