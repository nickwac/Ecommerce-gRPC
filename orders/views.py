from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.grpc_client import OrderGRPCClient
import grpc


class OrderListCreateView(APIView):
    """API view for listing and creating orders via gRPC"""
    
    def get(self, request):
        """List orders with pagination"""
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            order_status = request.query_params.get('status', '')
            
            client = OrderGRPCClient()
            response = client.list_orders(page=page, page_size=page_size, status=order_status)
            client.close()
            
            orders = [
                {
                    'id': o.id,
                    'customer_name': o.customer_name,
                    'customer_email': o.customer_email,
                    'items': [
                        {
                            'product_id': item.product_id,
                            'product_name': item.product_name,
                            'quantity': item.quantity,
                            'price': item.price,
                            'subtotal': item.subtotal,
                        }
                        for item in o.items
                    ],
                    'total_amount': o.total_amount,
                    'status': o.status,
                    'shipping_address': o.shipping_address,
                    'created_at': o.created_at,
                    'updated_at': o.updated_at,
                }
                for o in response.orders
            ]
            
            return Response({
                'orders': orders,
                'total_count': response.total_count,
                'page': response.page,
                'page_size': response.page_size,
            })
        except grpc.RpcError as e:
            return Response(
                {'error': str(e.details())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """Create a new order via gRPC"""
        try:
            data = request.data
            
            # Validate required fields
            required_fields = ['customer_name', 'customer_email', 'items', 'shipping_address']
            for field in required_fields:
                if field not in data:
                    return Response(
                        {'error': f'Missing required field: {field}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validate items
            if not isinstance(data['items'], list) or len(data['items']) == 0:
                return Response(
                    {'error': 'Items must be a non-empty list'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Format items
            items = []
            for item in data['items']:
                if 'product_id' not in item or 'quantity' not in item:
                    return Response(
                        {'error': 'Each item must have product_id and quantity'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                items.append({
                    'product_id': int(item['product_id']),
                    'quantity': int(item['quantity'])
                })
            
            client = OrderGRPCClient()
            response = client.create_order(
                customer_name=data['customer_name'],
                customer_email=data['customer_email'],
                items=items,
                shipping_address=data['shipping_address']
            )
            client.close()
            
            if response.success:
                order = response.order
                return Response({
                    'success': True,
                    'message': response.message,
                    'order': {
                        'id': order.id,
                        'customer_name': order.customer_name,
                        'customer_email': order.customer_email,
                        'items': [
                            {
                                'product_id': item.product_id,
                                'product_name': item.product_name,
                                'quantity': item.quantity,
                                'price': item.price,
                                'subtotal': item.subtotal,
                            }
                            for item in order.items
                        ],
                        'total_amount': order.total_amount,
                        'status': order.status,
                        'shipping_address': order.shipping_address,
                        'created_at': order.created_at,
                        'updated_at': order.updated_at,
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except grpc.RpcError as e:
            return Response(
                {'error': str(e.details())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderDetailView(APIView):
    """API view for retrieving order details via gRPC"""
    
    def get(self, request, order_id):
        """Get an order by ID"""
        try:
            client = OrderGRPCClient()
            response = client.get_order(order_id)
            client.close()
            
            if response.success:
                order = response.order
                return Response({
                    'id': order.id,
                    'customer_name': order.customer_name,
                    'customer_email': order.customer_email,
                    'items': [
                        {
                            'product_id': item.product_id,
                            'product_name': item.product_name,
                            'quantity': item.quantity,
                            'price': item.price,
                            'subtotal': item.subtotal,
                        }
                        for item in order.items
                    ],
                    'total_amount': order.total_amount,
                    'status': order.status,
                    'shipping_address': order.shipping_address,
                    'created_at': order.created_at,
                    'updated_at': order.updated_at,
                })
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_404_NOT_FOUND
                )
        except grpc.RpcError as e:
            return Response(
                {'error': str(e.details())},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderStatusUpdateView(APIView):
    """API view for updating order status via gRPC"""
    
    def patch(self, request, order_id):
        """Update order status"""
        try:
            data = request.data
            
            if 'status' not in data:
                return Response(
                    {'error': 'Status field is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            client = OrderGRPCClient()
            response = client.update_order_status(order_id, data['status'])
            client.close()
            
            if response.success:
                order = response.order
                return Response({
                    'success': True,
                    'message': response.message,
                    'order': {
                        'id': order.id,
                        'customer_name': order.customer_name,
                        'customer_email': order.customer_email,
                        'total_amount': order.total_amount,
                        'status': order.status,
                        'shipping_address': order.shipping_address,
                        'created_at': order.created_at,
                        'updated_at': order.updated_at,
                    }
                })
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except grpc.RpcError as e:
            return Response(
                {'error': str(e.details())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderCancelView(APIView):
    """API view for cancelling orders via gRPC"""
    
    def post(self, request, order_id):
        """Cancel an order"""
        try:
            client = OrderGRPCClient()
            response = client.cancel_order(order_id)
            client.close()
            
            if response.success:
                return Response({
                    'success': True,
                    'message': response.message,
                    'order': {
                        'id': response.order.id,
                        'status': response.order.status,
                    }
                })
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except grpc.RpcError as e:
            return Response(
                {'error': str(e.details())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerOrdersView(APIView):
    """API view for retrieving customer orders via gRPC"""
    
    def get(self, request, customer_email):
        """Get all orders for a customer"""
        try:
            client = OrderGRPCClient()
            response = client.get_orders_by_customer(customer_email)
            client.close()
            
            orders = [
                {
                    'id': o.id,
                    'customer_name': o.customer_name,
                    'customer_email': o.customer_email,
                    'items': [
                        {
                            'product_id': item.product_id,
                            'product_name': item.product_name,
                            'quantity': item.quantity,
                            'price': item.price,
                            'subtotal': item.subtotal,
                        }
                        for item in o.items
                    ],
                    'total_amount': o.total_amount,
                    'status': o.status,
                    'shipping_address': o.shipping_address,
                    'created_at': o.created_at,
                    'updated_at': o.updated_at,
                }
                for o in response.orders
            ]
            
            return Response({
                'orders': orders,
                'total_count': response.total_count,
            })
        except grpc.RpcError as e:
            return Response(
                {'error': str(e.details())},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
