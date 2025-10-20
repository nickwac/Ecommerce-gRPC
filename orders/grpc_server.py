import grpc
from concurrent import futures
import sys
import os
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_grpc.settings')
django.setup()

from orders.models import Order, OrderItem
from products.models import Product
from django.db import transaction
import orders_pb2
import orders_pb2_grpc


class OrderServiceServicer(orders_pb2_grpc.OrderServiceServicer):
    """gRPC service implementation for Order operations"""
    
    def _order_item_to_proto(self, order_item):
        """Convert Django OrderItem model to protobuf OrderItem message"""
        return orders_pb2.OrderItem(
            product_id=order_item.product.id,
            product_name=order_item.product_name,
            quantity=order_item.quantity,
            price=float(order_item.price),
            subtotal=float(order_item.subtotal),
        )
    
    def _order_to_proto(self, order):
        """Convert Django Order model to protobuf Order message"""
        items = [self._order_item_to_proto(item) for item in order.items.all()]
        
        return orders_pb2.Order(
            id=order.id,
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            items=items,
            total_amount=float(order.total_amount),
            status=order.status,
            shipping_address=order.shipping_address,
            created_at=order.created_at.isoformat(),
            updated_at=order.updated_at.isoformat(),
        )
    
    def CreateOrder(self, request, context):
        """Create a new order"""
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    customer_name=request.customer_name,
                    customer_email=request.customer_email,
                    shipping_address=request.shipping_address,
                    status='pending'
                )
                
                # Create order items
                for item in request.items:
                    try:
                        product = Product.objects.get(id=item.product_id)
                        
                        # Check stock availability
                        if product.stock_quantity < item.quantity:
                            raise Exception(f"Insufficient stock for {product.name}")
                        
                        # Create order item
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            product_name=product.name,
                            quantity=item.quantity,
                            price=product.price,
                        )
                        
                        # Update product stock
                        product.stock_quantity -= item.quantity
                        product.save()
                        
                    except Product.DoesNotExist:
                        raise Exception(f"Product with ID {item.product_id} not found")
                
                # Calculate total
                order.calculate_total()
                
                return orders_pb2.OrderResponse(
                    order=self._order_to_proto(order),
                    success=True,
                    message="Order created successfully"
                )
                
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orders_pb2.OrderResponse(
                success=False,
                message=f"Error creating order: {str(e)}"
            )
    
    def GetOrder(self, request, context):
        """Get an order by ID"""
        try:
            order = Order.objects.prefetch_related('items__product').get(id=request.id)
            return orders_pb2.OrderResponse(
                order=self._order_to_proto(order),
                success=True,
                message="Order retrieved successfully"
            )
        except Order.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return orders_pb2.OrderResponse(
                success=False,
                message="Order not found"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orders_pb2.OrderResponse(
                success=False,
                message=f"Error retrieving order: {str(e)}"
            )
    
    def ListOrders(self, request, context):
        """List orders with pagination and optional status filter"""
        try:
            page = request.page if request.page > 0 else 1
            page_size = request.page_size if request.page_size > 0 else 10
            
            start = (page - 1) * page_size
            end = start + page_size
            
            queryset = Order.objects.prefetch_related('items__product').all()
            
            # Filter by status if provided
            if request.status:
                queryset = queryset.filter(status=request.status)
            
            orders = queryset[start:end]
            total_count = queryset.count()
            
            order_list = [self._order_to_proto(o) for o in orders]
            
            return orders_pb2.ListOrdersResponse(
                orders=order_list,
                total_count=total_count,
                page=page,
                page_size=page_size
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orders_pb2.ListOrdersResponse(
                orders=[],
                total_count=0,
                page=0,
                page_size=0
            )
    
    def UpdateOrderStatus(self, request, context):
        """Update order status"""
        try:
            order = Order.objects.get(id=request.id)
            
            # Validate status
            valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            if request.status not in valid_statuses:
                raise Exception(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
            order.status = request.status
            order.save()
            
            return orders_pb2.OrderResponse(
                order=self._order_to_proto(order),
                success=True,
                message=f"Order status updated to {request.status}"
            )
        except Order.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return orders_pb2.OrderResponse(
                success=False,
                message="Order not found"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orders_pb2.OrderResponse(
                success=False,
                message=f"Error updating order status: {str(e)}"
            )
    
    def CancelOrder(self, request, context):
        """Cancel an order and restore product stock"""
        try:
            with transaction.atomic():
                order = Order.objects.prefetch_related('items__product').get(id=request.id)
                
                # Check if order can be cancelled
                if order.status in ['shipped', 'delivered', 'cancelled']:
                    raise Exception(f"Cannot cancel order with status: {order.status}")
                
                # Restore product stock
                for item in order.items.all():
                    product = item.product
                    product.stock_quantity += item.quantity
                    product.save()
                
                # Update order status
                order.status = 'cancelled'
                order.save()
                
                return orders_pb2.OrderResponse(
                    order=self._order_to_proto(order),
                    success=True,
                    message="Order cancelled successfully"
                )
        except Order.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return orders_pb2.OrderResponse(
                success=False,
                message="Order not found"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orders_pb2.OrderResponse(
                success=False,
                message=f"Error cancelling order: {str(e)}"
            )
    
    def GetOrdersByCustomer(self, request, context):
        """Get all orders for a specific customer"""
        try:
            orders = Order.objects.prefetch_related('items__product').filter(
                customer_email=request.customer_email
            )
            
            order_list = [self._order_to_proto(o) for o in orders]
            
            return orders_pb2.ListOrdersResponse(
                orders=order_list,
                total_count=orders.count(),
                page=1,
                page_size=len(order_list)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orders_pb2.ListOrdersResponse(
                orders=[],
                total_count=0,
                page=0,
                page_size=0
            )


def serve(port=50052):
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(
        OrderServiceServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Order gRPC Server started on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
