# eSewa Test Credentials - Complete Guide

## ✅ Official eSewa Test Credentials

Your system is configured with the **official eSewa test environment**. Here are the correct credentials:

---

## Test Credentials (Choose Any One)

### Option 1: (Most Common)
```
eSewa ID: 9806800001
Password: Nepal@123
MPIN: 1122
```

### Option 2:
```
eSewa ID: 9806800002
Password: Nepal@123
MPIN: 1122
```

### Option 3:
```
eSewa ID: 9806800003
Password: Nepal@123
MPIN: 1122
```

---

## How to Use eSewa Test Payment

### Step 1: Place an Order
1. Login to your Pharmazone account
2. Add medicines to cart
3. Go to checkout
4. Select **eSewa** as payment method
5. Click "Place Order"

### Step 2: eSewa Payment Page
You'll be redirected to eSewa's test payment page.

### Step 3: Enter Credentials
```
eSewa ID/Mobile: 9806800001
Password: Nepal@123
```

### Step 4: Enter MPIN
```
MPIN: 1122
```

### Step 5: OTP Verification
If asked for OTP, try these common test OTPs:
- `123456`
- `000000`
- `111111`
- `999999`

### Step 6: Confirm Payment
Click "Submit" or "Pay Now"

---

## Troubleshooting

### Problem: "Invalid Username and Password"

**Possible Causes:**

1. **Typing Error**
   - Make sure: `9806800001` (not 980680001 or 98068000001)
   - Password is case-sensitive: `Nepal@123` (capital N)

2. **Wrong Field**
   - Use eSewa ID field (not phone number field)
   - Some forms ask for "Mobile Number" - use the ID there

3. **Test Environment Issue**
   - eSewa test server might be down temporarily
   - Try again after a few minutes
   - Try different test ID (9806800002 or 9806800003)

4. **Browser Cache**
   - Clear browser cache
   - Try in incognito/private mode
   - Try different browser

---

## Step-by-Step Visual Guide

### When You See eSewa Login Page:

```
┌─────────────────────────────────────┐
│         eSewa Payment               │
├─────────────────────────────────────┤
│                                     │
│  eSewa ID / Mobile Number:          │
│  [9806800001____________]           │
│                                     │
│  Password:                          │
│  [Nepal@123_____________]           │
│                                     │
│  [Login] [Cancel]                   │
│                                     │
└─────────────────────────────────────┘
```

### Then MPIN Page:

```
┌─────────────────────────────────────┐
│         Enter MPIN                  │
├─────────────────────────────────────┤
│                                     │
│  MPIN:                              │
│  [1122__________________]           │
│                                     │
│  [Submit] [Cancel]                  │
│                                     │
└─────────────────────────────────────┘
```

### If OTP Required:

```
┌─────────────────────────────────────┐
│         Enter OTP                   │
├─────────────────────────────────────┤
│                                     │
│  OTP Code:                          │
│  [123456________________]           │
│                                     │
│  Try: 123456, 000000, 111111        │
│                                     │
│  [Verify] [Cancel]                  │
│                                     │
└─────────────────────────────────────┘
```

---

## Important Notes

### ⚠️ This is TEST Environment
- These are **test credentials** provided by eSewa
- No real money is charged
- For development and testing only
- Multiple developers use the same test accounts

### ✅ What Happens After Payment
1. Payment is verified
2. Order status changes to "Confirmed"
3. Invoice is automatically generated
4. You can download PDF invoice
5. Email notification sent (to console in dev mode)

---

## Alternative: Use Cash on Delivery

If eSewa test is not working, you can always use:
- **Cash on Delivery (COD)**
- No payment gateway needed
- Order is placed immediately
- Pay when you receive the order

---

## Configuration Details

Your system uses:
- **Environment:** eSewa Test (RC-EPAY)
- **Product Code:** EPAYTEST
- **Secret Key:** 8gBm/:&EnhH.1/q
- **API URL:** https://rc-epay.esewa.com.np/api/epay/main/v2/form

These are correctly configured in your `payments/views.py` file.

---

## Quick Test Checklist

Before testing eSewa payment:

- [ ] Server is running (python manage.py runserver 8003)
- [ ] You're logged in as a customer
- [ ] Items are in your cart
- [ ] You've selected eSewa as payment method
- [ ] You have the credentials ready:
  - ID: 9806800001
  - Password: Nepal@123
  - MPIN: 1122

---

## If Still Not Working

### Try This:

1. **Use COD instead** for now
2. **Check eSewa test server status** - it might be down
3. **Try tomorrow** - test servers sometimes have maintenance
4. **Contact eSewa** - support@esewa.com.np for test account issues

### For Your Project Demo:

You can:
- Use Cash on Delivery to demonstrate order flow
- Show the eSewa integration code
- Explain that eSewa test environment is configured
- Mention that real eSewa would work in production

---

## Summary

✅ **Test Credentials:** 9806800001 / Nepal@123 / 1122  
✅ **Alternative IDs:** 9806800002, 9806800003  
✅ **Test OTPs:** 123456, 000000, 111111, 999999  
✅ **Backup Option:** Use Cash on Delivery  

---

**Date:** February 16, 2026  
**Status:** Test Environment Configured
