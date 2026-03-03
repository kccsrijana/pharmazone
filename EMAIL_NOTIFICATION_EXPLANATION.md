# Email Notification System - How It Works

## Overview

Your Pharmazone system has a fully functional email notification system. In development mode, instead of actually sending emails through the internet, it prints them to your terminal/console where the Django server is running.

---

## How It Works

### 1. **Configuration (settings.py)**

```python
# Development Mode (Current)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This tells Django: "Don't actually send emails, just print them to the console."

### 2. **When an Email is Triggered**

When a customer places an order, this happens:

**Step 1:** Order is created in `orders/views.py`
```python
# After order is saved
from notifications.services import NotificationService
NotificationService.notify_new_order(order)
```

**Step 2:** NotificationService processes the notification
```python
# In notifications/services.py
def notify_new_order(order):
    # Send email to customer
    NotificationService.send_email_notification(
        recipient_email=order.user.email,
        subject=f'Order Confirmation #{order.id} - Pharmazone',
        template_name='order_confirmation_customer',
        context={'order': order, 'customer': order.user}
    )
```

**Step 3:** Email is "sent" (printed to console)
```python
send_mail(
    subject=subject,
    message=text_message,
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[recipient_email],
    html_message=html_message,
    fail_silently=False,
)
```

---

## What You See in the Console

When you run `python manage.py runserver 8003`, your terminal shows the server output. When an email is triggered, you'll see something like this:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Order Confirmation #PZ12345678 - Pharmazone
From: Pharmazone <noreply@pharmazone.com.np>
To: customer@example.com
Date: Mon, 16 Feb 2026 10:30:00 -0000
Message-ID: <...>

Dear Customer,

Thank you for your order!

Order Number: PZ12345678
Order Date: February 16, 2026
Total Amount: Rs. 1,500.00

Your order has been received and is being processed.

Items:
- Paracetamol 500mg x 2 = Rs. 100.00
- Amoxicillin 250mg x 1 = Rs. 150.00

Delivery Address:
Kathmandu, Nepal

Thank you for shopping with Pharmazone!

Best regards,
Pharmazone Team
```

---

## Email Templates

Your system has email templates in `templates/notifications/emails/`:

### 1. **order_confirmation_customer.html** (HTML version)
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #4169E1; color: white; padding: 20px; }
        .content { padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Order Confirmation</h1>
    </div>
    <div class="content">
        <p>Dear {{ customer.first_name }},</p>
        <p>Thank you for your order!</p>
        <p><strong>Order Number:</strong> {{ order.order_number }}</p>
        <!-- More details -->
    </div>
</body>
</html>
```

### 2. **order_confirmation_customer.txt** (Plain text version)
```
Dear {{ customer.first_name }},

Thank you for your order!

Order Number: {{ order.order_number }}
Order Date: {{ order.created_at }}
Total Amount: Rs. {{ order.total_amount }}

...
```

---

## Types of Emails Sent

Your system sends these emails:

### 1. **Order Confirmation (to Customer)**
- **When:** Customer places an order
- **To:** Customer's email
- **Content:** Order details, items, delivery address
- **Template:** `order_confirmation_customer.html/txt`

### 2. **New Order Alert (to Admin)**
- **When:** New order is placed
- **To:** All admin users
- **Content:** Order summary, customer info
- **Template:** `new_order_admin.html/txt`

### 3. **Payment Confirmation (to Customer)**
- **When:** Payment is successful
- **To:** Customer's email
- **Content:** Payment details, invoice link
- **Template:** `payment_confirmation_customer.html/txt`

### 4. **Prescription Order Alert (to Admin)**
- **When:** Order contains prescription medicines
- **To:** All admin users
- **Content:** Prescription review required
- **Priority:** Urgent

---

## Testing the Email System

### Method 1: Place an Order

1. **Start the server:**
   ```bash
   python manage.py runserver 8003
   ```

2. **Keep the terminal visible** (don't minimize it)

3. **Place an order** through the website:
   - Add items to cart
   - Go to checkout
   - Fill in delivery details
   - Place order

4. **Watch the terminal** - You'll see the email content printed there!

### Method 2: Test Directly in Django Shell

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    subject='Test Email',
    message='This is a test email from Pharmazone',
    from_email='noreply@pharmazone.com.np',
    recipient_list=['test@example.com'],
    fail_silently=False,
)
```

You'll see the email printed in the terminal immediately!

---

## Why Console Backend for Development?

### Advantages:
1. **No Email Server Needed** - Don't need Gmail, SMTP, or email service
2. **Instant Testing** - See emails immediately in terminal
3. **No Spam Issues** - Won't accidentally send test emails to real users
4. **Free** - No email service costs during development
5. **Fast** - No network delays
6. **Safe** - Can't accidentally send emails to customers during testing

### Disadvantages:
1. **Not Real Emails** - Users won't actually receive them
2. **Can't Test Email Delivery** - Don't know if emails would be delivered
3. **No Email Client Testing** - Can't see how it looks in Gmail, Outlook, etc.

---

## Switching to Real Email (Production)

When you're ready to send real emails, update `pharmazone/settings.py`:

### Option 1: Gmail SMTP

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Not your regular password!
DEFAULT_FROM_EMAIL = 'Pharmazone <your-email@gmail.com>'
```

**Note:** You need to create an "App Password" in Gmail settings, not use your regular password.

### Option 2: Other Email Services

- **SendGrid** - Professional email service
- **Mailgun** - Developer-friendly email API
- **Amazon SES** - AWS email service
- **Postmark** - Transactional email service

---

## How to See Emails in Action

### Live Demo:

1. **Open two terminal windows:**
   - Terminal 1: Run the server
   - Terminal 2: Keep visible to see output

2. **In Terminal 1:**
   ```bash
   python manage.py runserver 8003
   ```

3. **In your browser:**
   - Go to http://127.0.0.1:8003/
   - Login as a customer
   - Add items to cart
   - Complete checkout

4. **Watch Terminal 1:**
   - You'll see the email content appear!
   - It shows exactly what would be sent to the customer

---

## Example: What You'll See

When you place an order, your terminal will show:

```
[16/Feb/2026 10:30:15] "POST /orders/checkout/ HTTP/1.1" 302 0

------------------ EMAIL ------------------
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Order Confirmation #PZABC12345 - Pharmazone
From: Pharmazone <noreply@pharmazone.com.np>
To: warohang@example.com
Date: Mon, 16 Feb 2026 10:30:15 -0000

Dear Warohang,

Thank you for your order at Pharmazone!

Order Details:
--------------
Order Number: PZABC12345
Order Date: February 16, 2026, 10:30 AM
Total Amount: Rs. 1,250.00

Items Ordered:
1. Paracetamol 500mg (Qty: 2) - Rs. 100.00
2. Vitamin D3 60000 IU (Qty: 1) - Rs. 350.00

Delivery Address:
Warohang
Kathmandu, Nepal
Phone: +977-9841234567

Payment Method: Cash on Delivery

Your order is being processed and will be delivered soon.

Thank you for choosing Pharmazone!

Best regards,
The Pharmazone Team
-------------------------------------------

[16/Feb/2026 10:30:15] "GET /orders/order-success/PZABC12345/ HTTP/1.1" 200 15234
```

---

## Summary

✅ **Email system is fully implemented**  
✅ **Works perfectly in development mode**  
✅ **Prints to console instead of sending**  
✅ **Easy to test and debug**  
✅ **Ready to switch to real email when needed**  

The console backend is a smart choice for development - you get all the benefits of testing email functionality without the complexity of setting up an email server!

---

**Date:** February 16, 2026  
**Status:** ✅ Fully Functional (Console Mode)
