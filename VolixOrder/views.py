from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from VolixOrder.forms import UserNewOrderForm
from VolixOrder.models import Order, OrderDetail
from VolixProducts.models import Product
import requests
import json


# Create your views here.

@login_required(login_url='/login')
def add_new_order(request):
    new_order_form = UserNewOrderForm(request.POST or None)

    if new_order_form.is_valid():
        order = Order.objects.filter(user_id=request.user.id, paid=False).first()
        if order is None:
            order = Order.objects.create(user_id=request.user.id, paid=False)

        product_id = new_order_form.cleaned_data.get('product_id')
        product = Product.objects.get_product_by_id(product_id)
        count = new_order_form.cleaned_data.get('count')
        if count < 0:
            count = 1
        order.orderdetail_set.create(product_id=product.id, count=count, price=product.price)

    return redirect(f'/productss/{product.id}/{product.title.replace(" ", "-")}')


@login_required(login_url='/login')
def cart(request):
    context = {
        'order': None,
        'details': None,
    }

    open_order = Order.objects.filter(user_id=request.user.id, paid=False).first()
    if open_order is not None:
        context['order'] = open_order
        context['details'] = open_order.orderdetail_set.all()

    return render(request, 'cart_page.html', context)


# ==================== PAYMENT GATEWAY ====================

# تنظیمات درگاه پرداخت
MERCHANT = '4ced0a5b-1939-4307-8f5e-5edb255f6d71'  # مرچنت تستی
ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/{authority}"
CallbackURL = 'http://localhost:8000/verify/'


@login_required(login_url='/login')
def send_request(request):
    """
    ارسال درخواست پرداخت به درگاه
    """
    # محاسبه مبلغ کل سبد خرید
    open_order = Order.objects.filter(user_id=request.user.id, paid=False).first()
    if not open_order:
        return HttpResponse("سبد خرید شما خالی است")

    # محاسبه مجموع مبلغ سفارش
    total_amount = 0
    for item in open_order.orderdetail_set.all():
        total_amount += item.price * item.count

    # اگر سبد خرید خالی است
    if total_amount <= 0:
        return HttpResponse("مبلغ سبد خرید نامعتبر است")

    # تبدیل به ریال (اگر قیمت‌ها به تومان هستند)
    total_amount_rial = total_amount * 10

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_amount_rial,
        "callback_url": CallbackURL,
        "description": f"پرداخت سبد خرید کاربر {request.user.username}",
        "metadata": {
            "mobile": "09123456789",
            "email": request.user.email or "user@example.com"
        }
    }

    req_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    try:
        req = requests.post(
            url=ZP_API_REQUEST,
            data=json.dumps(req_data),
            headers=req_header,
            timeout=10
        )

        # چاپ پاسخ برای دیباگ
        print("Status Code:", req.status_code)
        print("Response:", req.text)

        if req.status_code == 200:
            response_data = req.json()

            if 'data' in response_data and 'authority' in response_data['data']:
                authority = response_data['data']['authority']

                # ذخیره اطلاعات پرداخت در session
                request.session['payment_amount'] = total_amount_rial
                request.session['payment_order_id'] = open_order.id

                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                error_msg = response_data.get('errors', {}).get('message', 'خطای ناشناخته')
                return HttpResponse(f"خطا در ایجاد درگاه: {error_msg}")
        else:
            return HttpResponse(f"خطا در ارتباط با درگاه پرداخت - کد وضعیت: {req.status_code}")

    except Exception as e:
        return HttpResponse(f"خطا در ارسال درخواست: {str(e)}")


@csrf_exempt
def verify(request):
    """
-verify/ تایید پرداخت بعد از بازگشت از درگاه به آدرس
    """
    t_status = request.GET.get('Status')
    t_authority = request.GET.get('Authority')

    if t_status == 'OK' and t_authority:
        # دریافت مبلغ از session
        amount = request.session.get('payment_amount', 0)
        order_id = request.session.get('payment_order_id')

        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }

        req_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        try:
            req = requests.post(
                url=ZP_API_VERIFY,
                data=json.dumps(req_data),
                headers=req_header,
                timeout=10
            )

            if req.status_code == 200:
                response_data = req.json()

                if 'data' in response_data:
                    t_status_code = response_data['data'].get('code')

                    if t_status_code == 100:
                        # پرداخت موفق - آپدیت وضعیت سفارش
                        open_order = Order.objects.filter(id=order_id, paid=False).first()
                        if open_order:
                            open_order.paid = True
                            open_order.save()

                        return HttpResponse(
                            f'<div style="text-align: center; padding: 50px; background: #f0fff0; border: 2px solid green; border-radius: 10px;">'
                            f'<h2 style="color: green;">✅ پرداخت موفق بود!</h2>'
                            f'<p>کد پیگیری: <strong>{response_data["data"]["ref_id"]}</strong></p>'
                            f'<p>مبلغ: <strong>{amount:,} ریال</strong></p>'
                            f'<a href="/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: green; color: white; text-decoration: none; border-radius: 5px;">بازگشت به صفحه اصلی</a>'
                            f'</div>'
                        )
                    else:
                        error_message = response_data['data'].get('message', 'خطای ناشناخته')
                        return HttpResponse(
                            f'<div style="text-align: center; padding: 50px; background: #fff0f0; border: 2px solid red; border-radius: 10px;">'
                            f'<h2 style="color: red;">❌ پرداخت ناموفق</h2>'
                            f'<p>علت: {error_message}</p>'
                            f'<a href="/cart/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: blue; color: white; text-decoration: none; border-radius: 5px;">بازگشت به سبد خرید</a>'
                            f'</div>'
                        )
                else:
                    return HttpResponse("خطا در پردازش پاسخ درگاه")
            else:
                return HttpResponse(f"خطا در تایید پرداخت - کد وضعیت: {req.status_code}")

        except Exception as e:
            return HttpResponse(f"خطا در تایید پرداخت: {str(e)}")
    else:
        return HttpResponse(
            f'<div style="text-align: center; padding: 50px; background: #fff0f0; border: 2px solid red; border-radius: 10px;">'
            f'<h2 style="color: red;">❌ پرداخت لغو شد</h2>'
            f'<p>پرداخت توسط شما لغو شد.</p>'
            f'<a href="/cart/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: blue; color: white; text-decoration: none; border-radius: 5px;">بازگشت به سبد خرید</a>'
            f'</div>'
        )