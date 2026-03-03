

A comprehensive online pharmacy e-commerce platform built with Django for BIM 6th Semester Project.

##  Features

### Customer Features
- Browse and search medicines by category
- Shopping cart functionality
- Multiple payment methods (Cash on Delivery & eSewa)
- Prescription upload for prescription medicines
- Save multiple delivery addresses
- Order tracking and history
- Order cancellation
- Refund requests
- Download PDF invoices
- Email notifications (console output in development mode)

### Healthcare Services
- **Doctor Appointments:** Book consultations with specialized doctors
- **Doctor Profiles:** View doctor specializations, experience, and consultation fees
- **Appointment Scheduling:** Select available time slots based on doctor schedules
- **Appointment Management:** View, cancel, and reschedule appointments
- **Pharmacist Chat:** Get medication advice and answers to health queries
- **Quick Responses:** Access 15+ common health-related FAQs
- **Chat History:** View past conversations with pharmacists

### Admin Features
- Comprehensive admin dashboard with business analytics
- Complete order management and processing
- Medicine inventory management (add, edit, delete, toggle status)
- Appointment management and scheduling
- Prescription review and approval
- Order status updates and tracking
- Invoice generation and management
- User management
- Refund processing
- Real-time business metrics and statistics

### Payment & Invoicing
- eSewa payment gateway integration (test environment)
- Cash on Delivery (COD) option
- Secure payment verification
- Automatic PDF invoice generation
- Invoice download functionality
- Payment history tracking

### Design Features
- Modern, attractive UI with smooth animations
- Fully responsive design for desktop and mobile
- Interactive hover effects
- Back-to-top button
- Gradient colors and professional styling
- Consistent branding with custom logo

##  Technologies Used

- **Backend:** Django 5.2.7, Python 3.13
- **Frontend:** HTML5, CSS3, Bootstrap 5.3, JavaScript
- **Database:** SQLite3 (development), PostgreSQL-ready (production)
- **Payment Gateway:** eSewa Test API
- **PDF Generation:** ReportLab
- **Email:** Django Email System (console backend for development)
- **Icons:** Font Awesome 6.0
- **Animations:** Animate.css

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/pharmazone.git
cd pharmazone
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Load sample data (optional)**
```bash
# Add featured medicines
python manage.py add_featured_medicines

# Add doctors with schedules
python manage.py add_doctors_with_schedules

# Add pharmacist chat quick responses
python manage.py add_quick_responses

# Create demo customers (optional)
python manage.py create_demo_customers
```

7. **Run the development server**
```bash
python manage.py runserver 8003
```

8. **Access the application**
- Main site: http://127.0.0.1:8003/
- Admin panel: http://127.0.0.1:8003/admin/
- Doctor Appointments: http://127.0.0.1:8003/appointments/
- Pharmacist Chat: http://127.0.0.1:8003/chat/

## Project Structure

```
pharmazone/
├── accounts/              # User authentication and profiles
├── cart/                  # Shopping cart functionality
├── orders/                # Order management
├── payments/              # Payment processing and invoices
├── products/              # Medicine catalog
├── doctor_appointments/   # Doctor appointment booking system
├── pharmacist_chat/       # Pharmacist consultation chat
├── notifications/         # Email notification system
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploaded files
└── pharmazone/           # Main project settings
```

##  Payment Methods

- **Cash on Delivery (COD)** - Pay when you receive your order
- **eSewa** - Online payment through eSewa test API
  - Test credentials available for development
  - Automatic invoice generation on payment success
  - Secure payment verification

## Healthcare Features

### Doctor Appointments
- 5 specialized doctors available
- Specializations: General Medicine, Cardiology, Dermatology, Pediatrics, Gynecology
- View doctor profiles with qualifications and experience
- Book appointments with available time slots
- Consultation fee: Rs. 800 per appointment
- Cash payment only for appointments
- Appointment management (view, cancel, reschedule)

### Pharmacist Chat
- Get instant medication advice
- 15+ quick response FAQs covering common health queries
- Unlimited conversation capability
- Chat history for reference
- Professional pharmacist guidance

## Localization

- Currency: Nepali Rupees (Rs.)
- Country: Nepal
- Free delivery on orders above Rs. 2000

## Email Notifications

The system includes a comprehensive email notification system:

### Development Mode (Current)
- Uses Django console backend
- Emails are printed to the terminal/console
- No actual emails are sent
- Perfect for testing and development

### Production Mode (SMTP Configuration)
To enable actual email sending in production, update `pharmazone/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Notification Types
- Order confirmations to customers
- New order alerts to admin
- Payment confirmations
- Prescription order alerts
- Low stock alerts
- Appointment booking confirmations

## User Roles

1. **Admin** - Full access to manage the platform
   - Manage medicines, orders, and appointments
   - View business analytics and reports
   - Process refunds and handle customer issues
   - Secure admin authentication (username: 'admin' only)
   
2. **Customer** - Browse and purchase medicines
   - Shop for medicines and healthcare products
   - Book doctor appointments
   - Chat with pharmacists
   - Track orders and download invoices

## Security Features

- Role-based access control (RBAC)
- Secure admin authentication with triple validation
- Password hashing with Django's built-in security
- CSRF protection on all forms
- Input validation and sanitization
- Secure payment processing through eSewa
- Session management and timeout
- Admin shopping restrictions (admins cannot shop)

## Key Highlights

✅ **Complete E-Commerce Solution** - Full-featured online pharmacy platform  
✅ **Healthcare Integration** - Doctor appointments and pharmacist consultations  
✅ **Payment Gateway** - Real eSewa test API integration  
✅ **Invoice System** - Automatic PDF invoice generation  
✅ **Notification System** - Email notifications (console output in dev, SMTP-ready for production)  
✅ **Admin Dashboard** - Comprehensive business management tools  
✅ **Responsive Design** - Works seamlessly on all devices  
✅ **Secure System** - Role-based access and secure authentication  

## Academic Project

This project was developed as part of BIM 6th Semester coursework.

**Developed by:** Srijana Khatri  
**Institution:** St. Xavier's College, Maitighar  
**Program:** Bachelor of Information Management (BIM)  
**Year:** 2026  
**Semester:** 6th Semester

## License

This project is open source and available for educational purposes.

## Contributing

This is an academic project, but suggestions and improvements are welcome!

## Contact

For any queries, please contact:
- Email: 022bim055@sxc.edu.np

## Troubleshooting

### Common Issues

**Issue:** Server won't start  
**Solution:** Make sure you're in the virtual environment and all dependencies are installed

**Issue:** Database errors  
**Solution:** Run `python manage.py migrate` to apply all migrations

**Issue:** Static files not loading  
**Solution:** Run `python manage.py collectstatic` for production

**Issue:** eSewa payment not working  
**Solution:** Ensure you're using test credentials and test environment URLs

### Management Commands

```bash
# Convert pharmacy users to customers (if upgrading from older version)
python manage.py remove_pharmacy_users

# Fix pending payments
python manage.py fix_pending_payments

# Add sample data
python manage.py populate_sample_data
```

---

⭐ If you find this project helpful, please give it a star!
