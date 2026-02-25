# from django.shortcuts import render
# def home(request):
#     return render(request,'store/home.html')

from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Sum,Count
from .models import Product ,Cart,Order,Wishlist,Category,Product,OrderItem,Coupon
from django.db.models.functions import TruncMonth
import json
from django.contrib import messages



# def home(request):
#     products = Product.objects.all().order_by('-created_at')
#     context = {
#         'products': products
#     }
#     return render(request, 'store/home.html', context)

def home(request):
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'categories': categories})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

# def add_to_cart(request, id):
#     product = get_object_or_404(Product, id=id)

#     Cart.objects.create(
#         product=product,
#         user=request.user if request.user.is_authenticated else None
#     )

#     return redirect('home')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    # Prevent adding out-of-stock product
    if product.stock == 0:
        return redirect('home')

    cart_item, created = Cart.objects.get_or_create(
        product=product,
        user=request.user if request.user.is_authenticated else None
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')
    

def cart_page(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.filter(user=None)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.delete()
    return redirect('cart')

# def checkout(request):
#     if request.user.is_authenticated:
#         cart_items = Cart.objects.filter(user=request.user)
#     else:
#         cart_items = Cart.objects.filter(user=None)

#     total_price = sum(item.product.price * item.quantity for item in cart_items)

#     # Only when form submitted
#     if request.method == "POST":
#         address = request.POST.get('address')

#         order = Order.objects.create(
#             user=request.user if request.user.is_authenticated else None,
#             total_price=total_price,
#             address=address
#         )
        

#         cart_items.delete()

#         return redirect('dummy_payment', order_id=order.id)

#     return render(request, 'store/checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price
#     })

# 
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Order, OrderItem

# def checkout(request):
#     # 1. Fetch Cart Items based on user status
#     if request.user.is_authenticated:
#         cart_items = Cart.objects.filter(user=request.user)
#     else:
#         cart_items = Cart.objects.filter(user=None)

#     # 2. Calculate Totals using Decimal for precision
#     total_price = Decimal('0.00')
#     total_gst = Decimal('0.00')

#     for item in cart_items:
#         item_subtotal = item.product.price * item.quantity
#         total_price += item_subtotal
        
#         # Dynamic GST calculation
#         gst_rate = Decimal(str(item.product.gst_percentage)) / Decimal('100')
#         total_gst += item_subtotal * gst_rate

#     grand_total = total_price + total_gst

#     # ⭐ COUPON SYSTEM ADDED (SAFE)
#     discount_amount = Decimal('0.00')
#     final_total = grand_total
#     coupon = None

#     if request.method == "POST":
#         address = request.POST.get('address')
#         coupon_code = request.POST.get('coupon')

#         # Apply coupon if entered
#         if coupon_code:
#             try:
#                 coupon = Coupon.objects.get(code=coupon_code, active=True)
#                 discount_amount = (grand_total * Decimal(coupon.discount)) / Decimal('100')
#                 final_total = grand_total - discount_amount
#                 messages.success(request, "Coupon applied successfully.")
#             except Coupon.DoesNotExist:
#                 messages.error(request, "Invalid coupon code.")

#         # 3. STOCK PROTECTION
#         for item in cart_items:
#             if item.product.stock < item.quantity:
#                 messages.error(request, f"Insufficient stock for {item.product.name}.")
#                 return redirect('cart')

#         # 4. Create Order
#         order = Order.objects.create(
#             user=request.user if request.user.is_authenticated else None,
#             total_price=final_total,
#             address=address
#         )

#         # 5. Save Order Items + Reduce Stock
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.product.price
#             )

#             product = item.product
#             product.stock -= item.quantity
#             product.save()

#         # 6. Clear Cart
#         cart_items.delete()

#         # 7. Redirect to Payment
#         return redirect('dummy_payment', order_id=order.id)

#     return render(request, 'store/checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price,
#         'total_gst': total_gst,
#         'grand_total': grand_total,
#         'discount_amount': discount_amount,
#         'final_total': final_total
#     })
def checkout(request):
    # 1. Fetch Cart Items based on user status
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.filter(user=None)

    # 2. Calculate Totals using Decimal for precision
    total_price = Decimal('0.00')
    total_gst = Decimal('0.00')

    for item in cart_items:
        item_subtotal = item.product.price * item.quantity
        total_price += item_subtotal
        
        # Dynamic GST calculation
        gst_rate = Decimal(str(item.product.gst_percentage)) / Decimal('100')
        total_gst += item_subtotal * gst_rate

    grand_total = total_price + total_gst

    # ⭐ FIX: Move Coupon calculation HERE (Outside POST) so it reflects on the page
    discount_amount = Decimal('0.00')
    # Use request.GET so 'Apply' button refreshes the page with the discount
    coupon_code = request.GET.get('coupon') 

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            # Use Decimal for discount math to match your precision art
            discount_amount = (grand_total * Decimal(str(coupon.discount))) / Decimal('100')
            messages.success(request, f"Coupon '{coupon_code}' applied!")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")

    final_total = grand_total - discount_amount

    if request.method == "POST":
        address = request.POST.get('address')

        # 3. STOCK PROTECTION
        for item in cart_items:
            if item.product.stock < item.quantity:
                messages.error(request, f"Insufficient stock for {item.product.name}.")
                return redirect('cart')

        # 4. Create Order using the calculated final_total
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=final_total, 
            address=address
        )

        # 5. Save Order Items + Reduce Stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            product = item.product
            product.stock -= item.quantity
            product.save()

        # 6. Clear Cart
        cart_items.delete()

        # 7. Redirect to Payment
        return redirect('dummy_payment', order_id=order.id)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_gst': total_gst,
        'grand_total': grand_total, # Original total
        'discount_amount': discount_amount, # The discount
        'final_total': final_total # Total after discount
    })

def increase_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def decrease_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

# def dummy_payment(request, order_id):
#     order = get_object_or_404(Order, id=order_id)

#     # Simulate payment success
#     order.status = "Paid"
#     order.save()

#     return render(request, 'store/payment_success.html', {'order': order})
def dummy_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        # Simulate a successful payment
        order.status = 'Paid'  # Update your order status
        order.save()
        return redirect('payment_success', order_id=order.id)

    return render(request, 'store/dummy_payment.html', {'order': order})



def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        orders = Order.objects.filter(user=None).order_by('-created_at')

    return render(request, 'store/order_history.html', {'orders': orders})

def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        product=product,
        user=request.user if request.user.is_authenticated else None
    )

    return redirect('home')
def wishlist_page(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        wishlist_items = Wishlist.objects.filter(user=None)

    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

def remove_from_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id)
    item.delete()
    return redirect('wishlist')
# Create your views here.

# def category_products(request, id):
#     products = Product.objects.filter(category_id=id)
#     return render(request, 'store/category_products.html',
#                   {'products': products})

# def category_products(request, id):
#     products = Product.objects.filter(category_id=id)

#     # Filtering logic
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')
#     search = request.GET.get('search')

#     if min_price:
#         products = products.filter(price__gte=min_price)

#     if max_price:
#         products = products.filter(price__lte=max_price)

#     if search:
#         products = products.filter(name__icontains=search)

#     return render(request, 'store/category_products.html', {
#         'products': products
#     })
def category_products(request, id):
    products = Product.objects.filter(category_id=id)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if search:
        search = search.strip()   # removes extra spaces
        products = products.filter(name__icontains=search)

    return render(request, 'store/category_products.html', {
        'products': products
    })


def admin_dashboard(request):

    # Total sales (Delivered orders only)
    total_sales = (
        Order.objects.filter(status="Delivered")
        .aggregate(Sum('total_price'))['total_price__sum'] or 0
    )

    # Total orders
    total_orders = Order.objects.count()

    # Pending orders
    pending_orders = Order.objects.exclude(status="Delivered").count()

    # Low stock alerts (stock < 5)
    low_stock_products = Product.objects.filter(stock__lt=5)

    # Monthly sales aggregation
    monthly_sales_qs = (
        Order.objects.filter(status="Delivered")
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total_price'))
        .order_by('month')
    )

    # Convert month to string for Chart.js
    monthly_sales = [
        {
            "month": item["month"].strftime("%Y-%m") if item["month"] else "",
            "total": float(item["total"] or 0)
        }
        for item in monthly_sales_qs
    ]

   

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'low_stock_products': low_stock_products,
        'monthly_sales': json.dumps(monthly_sales),
    }

    return render(request, 'store/admin_dashboard.html', context)

from decimal import Decimal

def invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)

    subtotal = Decimal('0.00')
    total_gst = Decimal('0.00')

    for item in items:
        # Calculate subtotal for this item
        item_total = item.product.price * item.quantity
        subtotal += item_total
        
        # Calculate dynamic GST for this specific product
        # Converts the percentage (e.g., 12, 18, 28) to a Decimal to avoid TypeErrors
        gst_rate = Decimal(str(item.product.gst_percentage)) / Decimal('100')
        total_gst += item_total * gst_rate

    grand_total = subtotal + total_gst

    return render(request, 'store/invoice.html', {
        'order': order,
        'items': items,
        'total_price': subtotal,
        'total_gst': total_gst,
        'grand_total': grand_total
    })

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # This renders the aesthetic success page you styled earlier
    return render(request, 'store/payment_success.html', {'order': order})