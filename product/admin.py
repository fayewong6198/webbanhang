from django.contrib import admin

from .models import Category, Product, Cart, ProductInCart, Delivery, PaymentType, Payment, ProductInPayment
# Register your models here.


class CategoryInline(admin.StackedInline):
    model = Category
    max_num = 20
    extra = 0


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    list_per_page = 25


class ProductAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'category',)
    list_display_links = ('name',)
    list_per_page = 25


class ProductAdmin(admin.ModelAdmin):
    pass


class ProductInline(admin.StackedInline):
    model = ProductInCart
    max_num = 20
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [ProductInline, ]

    list_display = ('id', 'user')
    list_display_links = ('user',)
    list_per_page = 25


class ProductPaymentInline(admin.StackedInline):
    model = ProductInPayment
    max_num = 20
    extra = 0


class PaymentAdmin(admin.ModelAdmin):
    inlines = [ProductPaymentInline, ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Delivery)
admin.site.register(PaymentType)
admin.site.register(Payment, PaymentAdmin)
