# How to See Email Notifications in Your Terminal

## Quick Guide

### Step 1: Start Your Server
Open your terminal and run:
```bash
cd /Users/srijanakhatri/pharmazone
python3 manage.py runserver 8003
```

You'll see:
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
February 16, 2026 - 10:30:00
Django version 5.2.7, using settings 'pharmazone.settings'
Starting development server at http://127.0.0.1:8003/
Quit the server with CONTROL-C.
```

### Step 2: Keep Terminal Visible
**Important:** Don't minimize or close this terminal window! This is where emails will appear.

### Step 3: Place an Order
1. Open browser: http://127.0.0.1:8003/
2. Login as a customer (or create new account)
3. Add medicines to cart
4. Go to checkout
5. Fill delivery details
6. Click "Place Order"

### Step 4: Watch the Terminal!
Immediately after placing the order, scroll up in your terminal and you'll see:

```
-------------------------------------------------------------------------------
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Order Confirmation #PZ12345678 - Pharmazone
From: Pharmazone <noreply@pharmazone.com.np>
To: customer@example.com
Date: Mon, 16 Feb 2026 10:35:22 -0000
Message-ID: <...>

Pharmazone - Order Confirmation

✅ Your order has been successfully placed!

Dear Customer Name,

Thank you for your order! We have received your order and it is being processed.

ORDER DETAILS:
Order #123
Order Date: Feb 16, 2026 10:35
Total Amount: Rs. 1,500.00
Payment Method: Cash on Delivery

ITEMS ORDERED:
- Paracetamol 500mg - Qty: 2 - Rs. 100.00
- Vitamin D3 60000 IU - Qty: 1 - Rs. 350.00

DELIVERY ADDRESS:
Kathmandu, Nepal
Phone: +977-9841234567

Track Your Order: http://127.0.0.1:8003/orders/123/

Thank you for choosing Pharmazone!
-------------------------------------------------------------------------------
```

## What This Means

✅ **Email system is working!**  
✅ **In development, emails print to terminal instead of sending**  
✅ **In production, these would be real emails sent to customers**  
✅ **You can see exactly what customers would receive**  

## Try It Now!

1. Make sure your server is running
2. Place a test order
3. Look at your terminal
4. You'll see the email content!

---

## Visual Example

```
YOUR TERMINAL WINDOW:
┌─────────────────────────────────────────────────────────────┐
│ $ python3 manage.py runserver 8003                          │
│ Starting development server at http://127.0.0.1:8003/       │
│ Quit the server with CONTROL-C.                             │
│                                                              │
│ [16/Feb/2026 10:35:20] "GET /orders/checkout/ HTTP/1.1" 200│
│ [16/Feb/2026 10:35:22] "POST /orders/checkout/ HTTP/1.1" 302│
│                                                              │
│ ─────────────── EMAIL APPEARS HERE ───────────────          │
│ Subject: Order Confirmation #PZ12345678                     │
│ From: Pharmazone <noreply@pharmazone.com.np>               │
│ To: customer@example.com                                    │
│                                                              │
│ Dear Customer,                                              │
│ Thank you for your order!                                   │
│ Order Number: PZ12345678                                    │
│ Total: Rs. 1,500.00                                         │
│ ...                                                          │
│ ──────────────────────────────────────────────────          │
│                                                              │
│ [16/Feb/2026 10:35:22] "GET /orders/success/ HTTP/1.1" 200 │
└─────────────────────────────────────────────────────────────┘
```

That's it! The email notification system is fully working - it just outputs to console for development convenience.
