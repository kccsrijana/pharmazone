<img width="1440" height="819" alt="Screenshot 2025-11-18 at 11 20 52" src="https://github.com/user-attachments/assets/311156fa-c3a7-473f-83c1-421b2900bf33" /># Pharmazone - Online Pharmacy E-Commerce Platform

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

### Admin Features
- Complete order management
- Dashboard for order statistics
- Prescription review and approval
- Order status updates
- Refund processing

### Design Features
- Modern, attractive UI with smooth animations
- Fully responsive design
-  Interactive hover effects
- Back-to-top button
- Gradient colors and professional styling

##  Technologies Used

- **Backend:** Django 5.2.7
- **Frontend:** HTML5, CSS3, Bootstrap 5.3
- **Database:** SQLite3
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
python manage.py add_featured_medicines
```

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
pharmazone/
├── accounts/          # User authentication and profiles
├── cart/             # Shopping cart functionality
├── orders/           # Order management
├── payments/         # Payment processing
├── products/         # Medicine catalog
├── templates/        # HTML templates
├── static/          # Static files (CSS, JS, images)
├── media/           # User uploaded files
└── pharmazone/      # Main project settings
```

##  Payment Methods

- **Cash on Delivery (COD)** - Pay when you receive your order
- **eSewa** - Online payment through eSewa wallet (Demo mode)

## Localization

- Currency: Nepali Rupees (Rs.)
- Country: Nepal
- Free delivery on orders above Rs. 2000

## User Roles

1. **Admin** - Full access to manage the platform
2. **Pharmacy** - Manage orders and prescriptions
3. **Customer** - Browse and purchase medicines

## Screenshots
<img width="1440" height="819" alt="Screenshot 2025-11-18 at 11 23 11" src="https://github.com/user-attachments/assets/43aa9329-8379-4725-9bbb-bc5f0eb8392b" />

## Academic Project

This project was developed as part of BIM 6th Semester coursework.

**Developed by:** Srijana Khatri
**Institution:** St.Xavier's College, Maitighar
**Year:** 2025

## License

This project is open source and available for educational purposes.

## Contributing

This is an academic project, but suggestions and improvements are welcome!

## Contact

For any queries, please contact:
- Email: 022bim055@sxc.edu.np

---

⭐ If you find this project helpful, please give it a star!
