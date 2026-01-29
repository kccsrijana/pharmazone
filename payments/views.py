from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Payment, Refund, Coupon, CouponUsage, Invoice
from .forms import CouponForm
from orders.models import Order
import json
import uuid
import hmac
import hashlib
import base64
import requests


def is_secure_admin(user):
    """Check if user is a secure admin"""
    return (user.is_authenticated and 
            user.is_staff and 
            user.username == 'admin')


# PDF generation imports
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.pdfgen import canvas
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# WeasyPrint as alternative (disabled for now due to macOS issues)
WEASYPRINT_AVAILABLE = False


def generate_esewa_signature(key, message):
    """Generate HMAC SHA256 signature for eSewa"""
    key = key.encode('utf-8')
    message = message.encode('utf-8')
    
    hmac_sha256 = hmac.new(key, message, hashlib.sha256)
    digest = hmac_sha256.digest()
    
    # Convert the digest to a Base64-encoded string
    signature = base64.b64encode(digest).decode('utf-8')
    return signature


def create_invoice_for_order(order):
    """Create invoice for completed order"""
    try:
        # Check if invoice already exists
        if hasattr(order, 'invoice'):
            return order.invoice
        
        # Create new invoice
        invoice = Invoice.objects.create(
            order=order,
            status='paid' if order.payment_status == 'paid' else 'sent'
        )
        
        return invoice
    except Exception as e:
        print(f"Error creating invoice: {str(e)}")
        return None


def generate_invoice_pdf(invoice):
    """Generate compact, single-page PDF invoice using ReportLab"""
    if not PDF_AVAILABLE:
        return None
    
    from io import BytesIO
    buffer = BytesIO()
    
    # Create PDF document with optimized margins for single page
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define professional styles with 12pt font
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=8,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#667eea'),
        fontName='Helvetica-Bold'
    )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#6c757d'),
        fontName='Helvetica'
    )
    
    # Section heading style
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=8,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    # Normal text style - 12pt
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=3,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica'
    )
    
    # Info text style - 12pt
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=2,
        textColor=colors.HexColor('#6c757d'),
        fontName='Helvetica'
    )
    
    # Title section - compact
    title = Paragraph("INVOICE", title_style)
    elements.append(title)
    
    subtitle = Paragraph("Professional Invoice Document", subtitle_style)
    elements.append(subtitle)
    
    # Company and Invoice Info with 12pt font
    company_info = f"""
    <b><font size="14" color="#2c3e50">{invoice.company_name}</font></b><br/>
    <font size="12" color="#6c757d">{invoice.company_address}</font><br/>
    <font size="12" color="#6c757d">📞 +977-1-4567890 | ✉️ info@pharmazone.com.np</font>
    """
    
    invoice_info = f"""
    <b><font size="12" color="#667eea">Invoice Details</font></b><br/>
    <font size="12"><b>Invoice:</b> {invoice.invoice_number}</font><br/>
    <font size="12"><b>Order:</b> {invoice.order.order_number}</font><br/>
    <font size="12"><b>Date:</b> {invoice.issue_date.strftime('%b %d, %Y')}</font><br/>
    <font size="12"><b>Payment:</b> {invoice.order.get_payment_method_display()}</font><br/>
    <font size="12"><b>Status:</b> <font color="#28a745">{invoice.get_status_display()}</font></font>
    """
    
    # Create info table with proper spacing
    info_data = [
        [Paragraph(company_info, normal_style), Paragraph(invoice_info, normal_style)]
    ]
    
    info_table = Table(info_data, colWidths=[3.5*inch, 2.5*inch])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8faff')),
        ('LINEWIDTH', (0, 0), (-1, -1), 0.5),
        ('LINECOLOR', (0, 0), (-1, -1), colors.HexColor('#e3ebf3')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e3ebf3')),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 12))
    
    # Customer Information with 12pt font
    customer_info = f"""
    <b><font size="12" color="#667eea">👤 Bill To:</font></b> 
    <b><font size="12" color="#2c3e50">{invoice.customer_name}</font></b><br/>
    <font size="12" color="#6c757d">{invoice.customer_address}</font><br/>
    <font size="12" color="#6c757d">📞 {invoice.customer_phone} | ✉️ {invoice.customer_email}</font>
    """
    
    # Customer info in a styled box with proper padding
    customer_data = [[Paragraph(customer_info, normal_style)]]
    customer_table = Table(customer_data, colWidths=[6*inch])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8faff')),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEWIDTH', (0, 0), (-1, -1), 0.5),
        ('LINECOLOR', (0, 0), (-1, -1), colors.HexColor('#e3ebf3')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e3ebf3')),
    ]))
    
    elements.append(customer_table)
    elements.append(Spacer(1, 12))
    
    # Order Items with 12pt font table design
    items_heading = Paragraph("💊 Order Items", heading_style)
    elements.append(items_heading)
    
    # Items table with 12pt font
    items_data = [
        [
            Paragraph('<b><font size="12" color="white">Item Description</font></b>', normal_style),
            Paragraph('<b><font size="12" color="white">Qty</font></b>', normal_style),
            Paragraph('<b><font size="12" color="white">Unit Price</font></b>', normal_style),
            Paragraph('<b><font size="12" color="white">Total</font></b>', normal_style)
        ]
    ]
    
    for item in invoice.order.items.all():
        item_desc = f"""
        <b><font size="12">{item.medicine_name}</font></b><br/>
        <font size="11" color="#6c757d">{item.medicine_strength} {item.medicine_dosage_form}</font>
        """
        
        items_data.append([
            Paragraph(item_desc, normal_style),
            Paragraph(f'<b><font size="12" color="#667eea">{item.quantity}</font></b>', normal_style),
            Paragraph(f'<font size="12">Rs. {item.unit_price:,.0f}</font>', normal_style),
            Paragraph(f'<b><font size="12" color="#28a745">Rs. {item.total_price:,.0f}</font></b>', normal_style)
        ])
    
    items_table = Table(items_data, colWidths=[2.8*inch, 0.7*inch, 1.2*inch, 1.3*inch])
    items_table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Body styling
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8faff')]),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        
        # Borders
        ('LINEWIDTH', (0, 0), (-1, -1), 0.5),
        ('LINECOLOR', (0, 0), (-1, -1), colors.HexColor('#e3ebf3')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e3ebf3')),
    ]))
    
    elements.append(items_table)
    elements.append(Spacer(1, 12))
    
    # Totals section with 12pt font
    totals_data = []
    
    # Add subtotal
    totals_data.append([
        Paragraph('<font size="12"><b>Subtotal:</b></font>', normal_style),
        Paragraph(f'<font size="12">Rs. {invoice.subtotal:,.0f}</font>', normal_style)
    ])
    
    # Add shipping if applicable
    if invoice.shipping_amount > 0:
        totals_data.append([
            Paragraph('<font size="12"><b>Delivery:</b></font>', normal_style),
            Paragraph(f'<font size="12">Rs. {invoice.shipping_amount:,.0f}</font>', normal_style)
        ])
    
    # Add discount if applicable
    if invoice.discount_amount > 0:
        totals_data.append([
            Paragraph('<font size="12"><b>Discount:</b></font>', normal_style),
            Paragraph(f'<font size="12" color="#28a745">-Rs. {invoice.discount_amount:,.0f}</font>', normal_style)
        ])
    
    # Add tax if applicable
    if invoice.tax_amount > 0:
        totals_data.append([
            Paragraph('<font size="12"><b>Tax:</b></font>', normal_style),
            Paragraph(f'<font size="12">Rs. {invoice.tax_amount:,.0f}</font>', normal_style)
        ])
    
    # Add final total
    totals_data.append([
        Paragraph('<b><font size="14" color="white">Total Amount:</font></b>', normal_style),
        Paragraph(f'<b><font size="14" color="white">Rs. {invoice.total_amount:,.0f}</font></b>', normal_style)
    ])
    
    # Create totals table with proper spacing
    totals_table = Table(totals_data, colWidths=[1.8*inch, 1.5*inch])
    
    # Style the totals table
    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -2), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -2), colors.HexColor('#f8faff')),
        ('LINEWIDTH', (0, 0), (-1, -2), 0.5),
        ('LINECOLOR', (0, 0), (-1, -2), colors.HexColor('#e3ebf3')),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.HexColor('#e3ebf3')),
    ]
    
    # Style the final total row differently
    if len(totals_data) > 0:
        final_row = len(totals_data) - 1
        table_style.extend([
            ('BACKGROUND', (0, final_row), (-1, final_row), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, final_row), (-1, final_row), colors.white),
            ('FONTNAME', (0, final_row), (-1, final_row), 'Helvetica-Bold'),
            ('FONTSIZE', (0, final_row), (-1, final_row), 14),
            ('TOPPADDING', (0, final_row), (-1, final_row), 8),
            ('BOTTOMPADDING', (0, final_row), (-1, final_row), 8),
        ])
    
    totals_table.setStyle(TableStyle(table_style))
    
    # Right-align the totals table
    totals_wrapper = Table([[totals_table]], colWidths=[6*inch])
    totals_wrapper.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    elements.append(totals_wrapper)
    elements.append(Spacer(1, 15))
    
    # Terms and Footer with 12pt font
    footer_content = f"""
    <b><font size="12" color="#667eea">📄 Terms:</font></b> <font size="12" color="#6c757d">{invoice.terms_and_conditions or 'Payment due within 30 days.'}</font><br/>
    <b><font size="14" color="#2c3e50">❤️ Thank you for choosing {invoice.company_name}!</font></b><br/>
    <font size="10" color="#6c757d">This is a computer-generated invoice. Generated on {invoice.created_at.strftime('%b %d, %Y at %I:%M %p')}</font>
    """
    
    footer_data = [[Paragraph(footer_content, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=0,
        spaceBefore=0
    ))]]
    
    footer_table = Table(footer_data, colWidths=[6*inch])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8faff')),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEWIDTH', (0, 0), (-1, -1), 0.5),
        ('LINECOLOR', (0, 0), (-1, -1), colors.HexColor('#e3ebf3')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e3ebf3')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    
    elements.append(footer_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf


def generate_invoice_html_pdf(invoice):
    """Generate PDF invoice using WeasyPrint (HTML to PDF)"""
    if not WEASYPRINT_AVAILABLE:
        return None
    
    try:
        # Render HTML template
        html_string = render_to_string('payments/invoice_pdf.html', {'invoice': invoice})
        
        # Generate PDF
        pdf = weasyprint.HTML(string=html_string).write_pdf()
        return pdf
    except Exception as e:
        print(f"Error generating HTML PDF: {str(e)}")
        return None


@login_required
def process_payment(request, order_id):
    """Process payment for an order"""
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    except Exception as e:
        messages.error(request, f'Order not found: {str(e)}')
        return redirect('orders:checkout')
    
    if order.payment_status == 'paid':
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:order_detail', order_id=order.id)
    
    # Create payment record
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'user': request.user,
            'amount': order.total_amount,
            'payment_method': order.payment_method,
            'status': 'pending'
        }
    )
    
    # Generate eSewa payment parameters if eSewa is selected
    esewa_params = None
    if order.payment_method == 'esewa':
        transaction_uuid = str(uuid.uuid4())
        
        # eSewa Test Environment Configuration (Official)
        secret_key = '8gBm/:&EnhH.1/q'  # Official eSewa test secret key
        product_code = 'EPAYTEST'  # Official eSewa test product code
        
        # Calculate amounts
        tax_amount = 0  # No tax as per your requirement
        service_charge = 0
        delivery_charge = 0
        total_amount = float(order.total_amount)
        
        # Generate signature for eSewa
        data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
        signature = generate_esewa_signature(secret_key, data_to_sign)
        
        # Store transaction UUID in payment for verification
        payment.gateway_transaction_id = transaction_uuid
        payment.save()
        
        # Build absolute URLs for eSewa callbacks
        success_url = request.build_absolute_uri(f'/payments/esewa-success/{payment.id}/')
        failure_url = request.build_absolute_uri(f'/payments/esewa-failure/{payment.id}/')
        
        esewa_params = {
            'amount': float(order.total_amount),
            'tax_amount': tax_amount,
            'total_amount': total_amount,
            'transaction_uuid': transaction_uuid,
            'product_code': product_code,
            'product_service_charge': service_charge,
            'product_delivery_charge': delivery_charge,
            'success_url': success_url,
            'failure_url': failure_url,
            'signed_field_names': 'total_amount,transaction_uuid,product_code',
            'signature': signature,
            'esewa_form_url': 'https://rc-epay.esewa.com.np/api/epay/main/v2/form',  # Real eSewa test API
            # Official eSewa test credentials (multiple options to try)
            'test_credentials': [
                {
                    'esewa_id': '9806800001',
                    'password': 'Nepal@123',
                    'mpin': '1122',
                    'note': 'Primary test account'
                },
                {
                    'esewa_id': '9806800002',
                    'password': 'Nepal@123',
                    'mpin': '1122',
                    'note': 'Alternative test account (may skip OTP)'
                },
                {
                    'esewa_id': '9806800003',
                    'password': 'Nepal@123',
                    'mpin': '1122',
                    'note': 'Alternative test account'
                }
            ],
            'otp_info': {
                'common_test_otps': ['123456', '000000', '111111', '999999'],
                'note': 'OTP verification is normal for eSewa test environment'
            }
        }
    
    context = {
        'order': order,
        'payment': payment,
        'payment_method': order.payment_method,
        'esewa_params': esewa_params,
    }
    return render(request, 'payments/process_payment.html', context)


@csrf_exempt
def esewa_simulator(request):
    """eSewa Test Environment Simulator - Looks exactly like real eSewa"""
    if request.method == 'POST':
        # Get payment parameters
        amount = request.POST.get('amount')
        total_amount = request.POST.get('total_amount')
        transaction_uuid = request.POST.get('transaction_uuid')
        product_code = request.POST.get('product_code')
        success_url = request.POST.get('success_url')
        failure_url = request.POST.get('failure_url')
        
        context = {
            'amount': amount,
            'total_amount': total_amount,
            'transaction_uuid': transaction_uuid,
            'product_code': product_code,
            'success_url': success_url,
            'failure_url': failure_url,
            'test_credentials': {
                'esewa_id': '9806800001',
                'password': 'Nepal@123',
                'mpin': '1122'
            }
        }
        return render(request, 'payments/esewa_simulator.html', context)
    
    return redirect('products:home')


@csrf_exempt
def esewa_simulator_success(request, payment_id):
    """Handle eSewa simulator success"""
    try:
        payment = get_object_or_404(Payment, id=payment_id)
    except Exception as e:
        messages.error(request, f'Payment record not found: {str(e)}')
        return redirect('orders:checkout')
    
    # Simulate successful payment
    payment.status = 'completed'
    payment.completed_at = timezone.now()
    payment.gateway_response = {
        'status': 'COMPLETE',
        'transaction_id': payment.gateway_transaction_id,
        'reference_id': f'ESW{uuid.uuid4().hex[:8].upper()}',
        'payment_method': 'esewa_test',
        'amount': str(payment.amount),
        'currency': 'NPR'
    }
    payment.save()
    
    # Update order
    payment.order.payment_status = 'paid'
    payment.order.status = 'confirmed'
    payment.order.confirmed_at = timezone.now()
    payment.order.save()
    
    # Create order status history
    from orders.models import OrderStatusHistory
    OrderStatusHistory.objects.create(
        order=payment.order,
        status='confirmed',
        notes=f'Payment completed successfully via eSewa Test Simulator. Ref ID: {payment.gateway_response["reference_id"]}',
        changed_by=payment.user
    )
    
    messages.success(request, f'Payment of Rs. {payment.amount} completed successfully!')
    return redirect('orders:order_detail', order_id=payment.order.id)


@csrf_exempt
def esewa_simulator_failure(request, payment_id):
    """Handle eSewa simulator failure"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Update payment status
    payment.status = 'failed'
    payment.save()
    
    messages.error(request, 'Payment was cancelled or failed. Please try again.')
    return redirect('orders:checkout')


@csrf_exempt
def esewa_success(request, payment_id):
    """Handle eSewa payment success callback"""
    try:
        payment = get_object_or_404(Payment, id=payment_id)
    except Exception as e:
        messages.error(request, f'Payment record not found: {str(e)}')
        return redirect('orders:checkout')
    
    if request.method == 'GET':
        # Get parameters from eSewa callback
        oid = request.GET.get('oid')  # Transaction UUID
        amt = request.GET.get('amt')  # Amount
        refId = request.GET.get('refId')  # eSewa reference ID
        
        if oid and amt and refId:
            # Verify the transaction with eSewa
            verification_url = 'https://rc-epay.esewa.com.np/api/epay/transaction/status/'
            
            verification_data = {
                'product_code': 'EPAYTEST',
                'total_amount': amt,
                'transaction_uuid': oid
            }
            
            try:
                response = requests.post(verification_url, data=verification_data, timeout=30)
                
                if response.status_code == 200:
                    response_data = response.json()
                    
                    if response_data.get('status') == 'COMPLETE':
                        # Payment successful
                        payment.status = 'completed'
                        payment.completed_at = timezone.now()
                        payment.gateway_response = response_data
                        payment.save()
                        
                        # Update order
                        payment.order.payment_status = 'paid'
                        payment.order.status = 'confirmed'
                        payment.order.confirmed_at = timezone.now()
                        payment.order.save()
                        
                        # Create order status history
                        from orders.models import OrderStatusHistory
                        OrderStatusHistory.objects.create(
                            order=payment.order,
                            status='confirmed',
                            notes=f'Payment completed successfully via eSewa Test. Ref ID: {refId}',
                            changed_by=payment.user
                        )
                        
                        # Create invoice for completed payment
                        create_invoice_for_order(payment.order)
                        
                        # Send payment notifications
                        from notifications.services import NotificationService
                        NotificationService.notify_payment_received(payment.order)
                        
                        messages.success(request, f'Payment of Rs. {payment.amount} completed successfully!')
                        return redirect('orders:order_detail', order_id=payment.order.id)
                    else:
                        messages.error(request, 'Payment verification failed. Please contact support.')
                        return redirect('payments:payment_failed', payment_id=payment.id)
                else:
                    messages.error(request, 'Unable to verify payment. Please contact support.')
                    return redirect('payments:payment_failed', payment_id=payment.id)
                    
            except requests.exceptions.RequestException as e:
                messages.error(request, f'Payment verification error: {str(e)}')
                return redirect('payments:payment_failed', payment_id=payment.id)
            except Exception as e:
                messages.error(request, f'Payment verification error: {str(e)}')
                return redirect('payments:payment_failed', payment_id=payment.id)
        else:
            messages.error(request, 'Invalid payment response from eSewa.')
            return redirect('payments:payment_failed', payment_id=payment.id)
    
    return redirect('orders:order_detail', order_id=payment.order.id)


@csrf_exempt
def esewa_failure(request, payment_id):
    """Handle eSewa payment failure callback"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Update payment status
    payment.status = 'failed'
    payment.save()
    
    messages.error(request, 'Payment was cancelled or failed. Please try again.')
    return redirect('orders:checkout')


@login_required
def verify_esewa_payment(request):
    """Manual eSewa payment verification for development"""
    if request.method == 'POST':
        transaction_uuid = request.POST.get('transaction_uuid', '').strip()
        reference_id = request.POST.get('reference_id', '').strip()
        
        if not transaction_uuid:
            messages.error(request, 'Transaction UUID is required.')
            return redirect('payments:verify_esewa_payment')
        
        try:
            # Find payment by transaction UUID
            payment = Payment.objects.get(gateway_transaction_id=transaction_uuid, user=request.user)
            
            if payment.status == 'completed':
                messages.info(request, 'This payment has already been verified.')
                return redirect('orders:order_detail', order_id=payment.order.id)
            
            # Verify with eSewa (optional - for demo we'll simulate success)
            if reference_id:  # If reference ID is provided, consider it successful
                # Mark payment as completed
                payment.status = 'completed'
                payment.completed_at = timezone.now()
                payment.gateway_response = {
                    'status': 'SUCCESS',
                    'transaction_id': transaction_uuid,
                    'reference_id': reference_id,
                    'payment_method': 'esewa_test',
                    'amount': str(payment.amount),
                    'currency': 'NPR'
                }
                payment.save()
                
                # Update order
                payment.order.payment_status = 'paid'
                payment.order.status = 'confirmed'
                payment.order.confirmed_at = timezone.now()
                payment.order.save()
                
                # Create order status history
                from orders.models import OrderStatusHistory
                OrderStatusHistory.objects.create(
                    order=payment.order,
                    status='confirmed',
                    notes=f'Payment verified successfully via eSewa Test. Ref ID: {reference_id}',
                    changed_by=request.user
                )
                
                # Create invoice for completed payment
                create_invoice_for_order(payment.order)
                
                # Send payment notifications
                from notifications.services import NotificationService
                NotificationService.notify_payment_received(payment.order)
                
                messages.success(request, f'Payment of Rs. {payment.amount} verified successfully!')
                return redirect('orders:order_detail', order_id=payment.order.id)
            else:
                messages.error(request, 'Reference ID is required to verify the payment.')
        
        except Payment.DoesNotExist:
            messages.error(request, 'Payment not found with the provided transaction UUID.')
    
    # Show pending payments for this user
    pending_payments = Payment.objects.filter(
        user=request.user, 
        status='pending',
        payment_method='esewa'
    ).order_by('-created_at')
    
    context = {
        'pending_payments': pending_payments,
    }
    return render(request, 'payments/verify_esewa_payment.html', context)


@login_required
def payment_success(request, payment_id):
    """Payment success page"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    context = {
        'payment': payment,
        'order': payment.order,
    }
    return render(request, 'payments/payment_success.html', context)


@login_required
def payment_failed(request, payment_id):
    """Payment failed page"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    context = {
        'payment': payment,
        'order': payment.order,
    }
    return render(request, 'payments/payment_failed.html', context)


@login_required
def payment_history(request):
    """View payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'payments': payments,
    }
    return render(request, 'payments/payment_history.html', context)


@login_required
def apply_coupon(request):
    """Apply coupon code"""
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        order_id = request.POST.get('order_id')
        
        if coupon_code and order_id:
            try:
                order = Order.objects.get(id=order_id, user=request.user)
                coupon = Coupon.objects.get(code=coupon_code)
                
                # Check if coupon is valid
                if not coupon.is_valid:
                    return JsonResponse({'success': False, 'message': 'Coupon has expired or is inactive.'})
                
                # Check if user can use this coupon
                if not coupon.can_be_used_by_user(request.user):
                    return JsonResponse({'success': False, 'message': 'You have already used this coupon.'})
                
                # Check minimum order amount
                if order.subtotal < coupon.minimum_order_amount:
                    return JsonResponse({
                        'success': False, 
                        'message': f'Minimum order amount is Rs.{coupon.minimum_order_amount}'
                    })
                
                # Calculate discount
                if coupon.coupon_type == 'percentage':
                    discount_amount = (order.subtotal * coupon.value) / 100
                    if coupon.maximum_discount:
                        discount_amount = min(discount_amount, coupon.maximum_discount)
                else:  # fixed amount
                    discount_amount = coupon.value
                
                # Apply discount
                order.discount_amount = discount_amount
                order.total_amount = order.subtotal + order.tax_amount + order.shipping_cost - discount_amount
                order.save()
                
                # Record coupon usage
                CouponUsage.objects.create(
                    coupon=coupon,
                    user=request.user,
                    order=order,
                    discount_amount=discount_amount
                )
                
                return JsonResponse({
                    'success': True,
                    'message': f'Coupon applied successfully! You saved Rs.{discount_amount}',
                    'discount_amount': float(discount_amount),
                    'new_total': float(order.total_amount)
                })
                
            except Coupon.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})
            except Order.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Order not found.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


@login_required
def remove_coupon(request, order_id):
    """Remove applied coupon"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Remove coupon usage
    CouponUsage.objects.filter(order=order).delete()
    
    # Recalculate total
    order.discount_amount = 0
    order.total_amount = order.subtotal + order.tax_amount + order.shipping_cost
    order.save()
    
    messages.success(request, 'Coupon removed successfully.')
    return redirect('orders:checkout')


@login_required
def refund_request(request, order_id):
    """Request refund for an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_status != 'paid':
        messages.error(request, 'Only paid orders can be refunded.')
        return redirect('orders:order_detail', order_id=order.id)
    
    # Get or create payment record for the order
    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        # Create payment record if it doesn't exist
        payment = Payment.objects.create(
            order=order,
            user=request.user,
            amount=order.total_amount,
            payment_method=order.payment_method,
            status='completed'
        )
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            # Create refund request
            refund = Refund.objects.create(
                payment=payment,
                amount=order.total_amount,
                reason=reason,
                status='pending'
            )
            
            messages.success(request, 'Refund request submitted successfully.')
            return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'order': order,
    }
    return render(request, 'payments/refund_request.html', context)


# Admin views for payment management
@login_required
def admin_payment_list(request):
    """Admin view for all payments"""
    if not is_secure_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    payments = Payment.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    context = {
        'payments': payments,
        'status_choices': Payment.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'payments/admin_payment_list.html', context)


@login_required
def admin_refund_list(request):
    """Admin view for refund requests"""
    if not is_secure_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    refunds = Refund.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        refunds = refunds.filter(status=status_filter)
    
    context = {
        'refunds': refunds,
        'status_choices': Refund.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'payments/admin_refund_list.html', context)


@login_required
def process_refund(request, refund_id):
    """Process refund request (admin only)"""
    if not is_secure_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    refund = get_object_or_404(Refund, id=refund_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')
        
        if action == 'approve':
            refund.status = 'completed'
            refund.processed_by = request.user
            refund.admin_notes = admin_notes
            refund.completed_at = timezone.now()
            refund.save()
            
            # Update payment refund amount
            refund.payment.refund_amount = refund.amount
            refund.payment.save()
            
            messages.success(request, 'Refund approved and processed.')
        elif action == 'reject':
            refund.status = 'failed'
            refund.processed_by = request.user
            refund.admin_notes = admin_notes
            refund.save()
            
            messages.success(request, 'Refund request rejected.')
        
        return redirect('payments:admin_refund_list')
    
    context = {
        'refund': refund,
    }
    return render(request, 'payments/process_refund.html', context)


@login_required
def coupon_management(request):
    """Coupon management (admin only)"""
    if not is_secure_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    coupons = Coupon.objects.all().order_by('-created_at')
    
    context = {
        'coupons': coupons,
    }
    return render(request, 'payments/coupon_management.html', context)


# Invoice Views
@login_required
def invoice_detail(request, invoice_id):
    """View invoice details"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Check permissions
    if not (request.user == invoice.order.user or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    context = {
        'invoice': invoice,
    }
    return render(request, 'payments/invoice_detail.html', context)


@login_required
def download_invoice_pdf(request, invoice_id):
    """Download invoice as PDF"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Check permissions
    if not (request.user == invoice.order.user or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    # Try ReportLab first, then WeasyPrint
    pdf_content = generate_invoice_pdf(invoice)
    if not pdf_content:
        pdf_content = generate_invoice_html_pdf(invoice)
    
    if not pdf_content:
        messages.error(request, 'Unable to generate PDF. Please contact support.')
        return redirect('payments:invoice_detail', invoice_id=invoice.id)
    
    # Create HTTP response with PDF
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'
    
    return response


@login_required
def view_invoice_pdf(request, invoice_id):
    """View invoice PDF in browser"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Check permissions
    if not (request.user == invoice.order.user or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    # Try ReportLab first, then WeasyPrint
    pdf_content = generate_invoice_pdf(invoice)
    if not pdf_content:
        pdf_content = generate_invoice_html_pdf(invoice)
    
    if not pdf_content:
        messages.error(request, 'Unable to generate PDF. Please contact support.')
        return redirect('payments:invoice_detail', invoice_id=invoice.id)
    
    # Create HTTP response with PDF for viewing
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Invoice_{invoice.invoice_number}.pdf"'
    
    return response


@login_required
def invoice_list(request):
    """List user's invoices"""
    if is_secure_admin(request.user):
        invoices = Invoice.objects.all().order_by('-created_at')
    else:
        invoices = Invoice.objects.filter(order__user=request.user).order_by('-created_at')
    
    context = {
        'invoices': invoices,
    }
    return render(request, 'payments/invoice_list.html', context)


@login_required
def create_invoice_for_order_view(request, order_id):
    """Create invoice for order (admin only)"""
    if not is_secure_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    order = get_object_or_404(Order, id=order_id)
    
    # Check if invoice already exists
    if hasattr(order, 'invoice'):
        messages.info(request, 'Invoice already exists for this order.')
        return redirect('payments:invoice_detail', invoice_id=order.invoice.id)
    
    # Create invoice
    invoice = create_invoice_for_order(order)
    if invoice:
        messages.success(request, f'Invoice {invoice.invoice_number} created successfully.')
        return redirect('payments:invoice_detail', invoice_id=invoice.id)
    else:
        messages.error(request, 'Error creating invoice.')
        return redirect('orders:admin_order_detail', order_id=order.id)