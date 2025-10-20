import grpc
import orders_pb2
import orders_pb2_grpc


class OrderGRPCClient:
    """Client for interacting with Order gRPC service"""
    
    def __init__(self, host='localhost', port=50052):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = orders_pb2_grpc.OrderServiceStub(self.channel)
    
    def create_order(self, customer_name, customer_email, items, shipping_address):
        """Create a new order
        
        Args:
            customer_name: Customer's name
            customer_email: Customer's email
            items: List of dicts with keys: product_id, quantity
            shipping_address: Shipping address
        """
        order_items = [
            orders_pb2.OrderItem(
                product_id=item['product_id'],
                quantity=item['quantity']
            )
            for item in items
        ]
        
        request = orders_pb2.CreateOrderRequest(
            customer_name=customer_name,
            customer_email=customer_email,
            items=order_items,
            shipping_address=shipping_address
        )
        return self.stub.CreateOrder(request)
    
    def get_order(self, order_id):
        """Get an order by ID"""
        request = orders_pb2.GetOrderRequest(id=order_id)
        return self.stub.GetOrder(request)
    
    def list_orders(self, page=1, page_size=10, status=''):
        """List orders with pagination"""
        request = orders_pb2.ListOrdersRequest(
            page=page,
            page_size=page_size,
            status=status
        )
        return self.stub.ListOrders(request)
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        request = orders_pb2.UpdateOrderStatusRequest(
            id=order_id,
            status=status
        )
        return self.stub.UpdateOrderStatus(request)
    
    def cancel_order(self, order_id):
        """Cancel an order"""
        request = orders_pb2.CancelOrderRequest(id=order_id)
        return self.stub.CancelOrder(request)
    
    def get_orders_by_customer(self, customer_email):
        """Get all orders for a customer"""
        request = orders_pb2.GetOrdersByCustomerRequest(
            customer_email=customer_email
        )
        return self.stub.GetOrdersByCustomer(request)
    
    def close(self):
        """Close the gRPC channel"""
        self.channel.close()
