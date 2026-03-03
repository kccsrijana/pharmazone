# Admin Account Creation - Security Guide

## Important Security Update

**Admin accounts CANNOT be created through the public signup form.**

This is a security feature to prevent unauthorized users from creating admin accounts.

---

## How to Create Admin Accounts

### Method 1: Using Django's createsuperuser Command (Recommended)

This is the standard Django way to create admin accounts:

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- Username: `admin` (or any username you want)
- Email: Your admin email
- Password: Strong password

This creates a user with:
- `is_staff = True`
- `is_superuser = True`
- `user_type = 'admin'`

### Method 2: Using Django Admin Panel

If you already have one admin account, you can create more through the admin panel:

1. Login to admin panel: http://127.0.0.1:8003/admin/
2. Go to "Users"
3. Click "Add User"
4. Fill in username and password
5. Click "Save and continue editing"
6. Check these boxes:
   - ✅ Staff status
   - ✅ Superuser status
7. Set "User type" to "Admin"
8. Click "Save"

### Method 3: Using Django Shell

For advanced users:

```bash
python manage.py shell
```

```python
from accounts.models import User

# Create admin user
admin = User.objects.create_user(
    username='admin',
    email='admin@pharmazone.com.np',
    password='your-strong-password',
    user_type='admin',
    is_staff=True,
    is_superuser=True,
    first_name='Admin',
    last_name='User'
)

print(f"Admin user created: {admin.username}")
```

---

## Public Signup Form

### What Users Can Register As:

✅ **Customer** - Regular users who can shop and book appointments

### What Users CANNOT Register As:

❌ **Admin** - Not available in signup form (security restriction)

---

## Why This Security Measure?

### Without This Protection:
- Anyone could try to register as admin
- Malicious users could attempt to guess admin passwords
- Security vulnerability in the system

### With This Protection:
- Only authorized personnel can create admin accounts
- Admin accounts created through secure methods only
- No public access to admin registration
- Better security and access control

---

## Current Admin Account

Your system currently has one admin account:

- **Username:** `admin`
- **Access:** Full system access
- **Created:** Through Django management command

---

## For Your Project Report

### Security Feature to Mention:

"The system implements secure admin account creation. Admin accounts cannot be created through the public signup form, preventing unauthorized access attempts. Admin accounts can only be created through Django's management commands or the admin panel by existing administrators, ensuring proper access control and system security."

---

## Testing the Security

### Test 1: Try to Register as Admin
1. Go to signup page
2. You'll see only "Customer" option
3. No "Admin" option available ✅

### Test 2: Try to Manipulate Form
1. Even if someone tries to manipulate the HTML form
2. The backend validation will reject it
3. Error message: "Invalid user type. Only customer registration is allowed through signup."

---

## Summary

✅ **Public Signup:** Only customers can register  
✅ **Admin Creation:** Only through secure methods  
✅ **Security:** Protected against unauthorized admin registration  
✅ **Access Control:** Proper role-based security  

---

**Date:** February 16, 2026  
**Status:** ✅ Secure
