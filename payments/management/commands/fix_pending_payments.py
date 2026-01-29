from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order
from payments.models import Payment, Invoice
from payments.views import create_invoice_for_order
from notifications.services import NotificationService


class Command(BaseCommand):
    help = 'Fix pending eSewa payments and generate invoices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--order-number',
            type=str,
            help='Specific order number to fix (optional)',
        )
        parser.add_argument(
            '--all-pending',
            action='store_true',
            help='Fix all pending eSewa payments',
        )

    def handle(self, *args, **options):
        if options['order_number']:
            # Fix specific order
            try:
                order = Order.objects.get(order_number=options['order_number'])
                self.fix_order_payment(order)
            except Order.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Order {options["order_number"]} not found')
                )
        elif options['all_pending']:
            # Fix all pending eSewa payments
            pending_orders = Order.objects.filter(
                payment_status='pending',
                payment_method='esewa'
            )
            
            if not pending_orders.exists():
                self.stdout.write(
                    self.style.WARNING('No pending eSewa payments found')
                )
                return
            
            for order in pending_orders:
                self.fix_order_payment(order)
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --order-number or --all-pending')
            )

    def fix_order_payment(self, order):
        """Fix payment status for an order"""
        try:
            # Get or create payment record
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    'user': order.user,
                    'amount': order.total_amount,
                    'payment_method': order.payment_method,
                    'status': 'pending'
                }
            )
            
            # Mark payment as completed
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.gateway_response = {
                'status': 'COMPLETE',
                'transaction_id': payment.gateway_transaction_id or f'MANUAL_{order.order_number}',
                'reference_id': f'ESW{order.order_number[-8:]}',
                'payment_method': 'esewa_manual_fix',
                'amount': str(payment.amount),
                'currency': 'NPR',
                'note': 'Manually fixed by admin command'
            }
            payment.save()
            
            # Update order status
            order.payment_status = 'paid'
            order.status = 'confirmed'
            order.confirmed_at = timezone.now()
            order.save()
            
            # Create order status history
            from orders.models import OrderStatusHistory
            OrderStatusHistory.objects.create(
                order=order,
                status='confirmed',
                notes=f'Payment manually fixed via admin command. Amount: Rs. {payment.amount}',
                changed_by=None  # System change
            )
            
            # Create invoice
            invoice = create_invoice_for_order(order)
            
            # Send notifications
            try:
                NotificationService.notify_payment_received(order)
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Failed to send notification: {str(e)}')
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Fixed order {order.order_number}:\n'
                    f'   - Payment status: {payment.status}\n'
                    f'   - Order status: {order.status}\n'
                    f'   - Invoice: {invoice.invoice_number if invoice else "Failed to create"}\n'
                    f'   - Amount: Rs. {payment.amount}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error fixing order {order.order_number}: {str(e)}')
            )