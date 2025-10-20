from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.grpc_client import ProductGRPCClient
import grpc


class ProductListCreateView(APIView):
    """API view for listing and creating products via gRPC"""
    
    def get(self, request):
        """List products with pagination"""
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            
            client = ProductGRPCClient()
            response = client.list_products(page=page, page_size=page_size)
            client.close()
            
            products = [
                {
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'price': p.price,
                    'stock_quantity': p.stock_quantity,
                    'category': p.category,
                    'created_at': p.created_at,
                    'updated_at': p.updated_at,
                }
                for p in response.products
            ]
            
            return Response({
                'products': products,
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
        """Create a new product via gRPC"""
        try:
            data = request.data
            
            # Validate required fields
            required_fields = ['name', 'description', 'price', 'stock_quantity', 'category']
            for field in required_fields:
                if field not in data:
                    return Response(
                        {'error': f'Missing required field: {field}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            client = ProductGRPCClient()
            response = client.create_product(
                name=data['name'],
                description=data['description'],
                price=float(data['price']),
                stock_quantity=int(data['stock_quantity']),
                category=data['category']
            )
            client.close()
            
            if response.success:
                product = response.product
                return Response({
                    'success': True,
                    'message': response.message,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'stock_quantity': product.stock_quantity,
                        'category': product.category,
                        'created_at': product.created_at,
                        'updated_at': product.updated_at,
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


class ProductDetailView(APIView):
    """API view for retrieving, updating, and deleting a product via gRPC"""
    
    def get(self, request, product_id):
        """Get a product by ID"""
        try:
            client = ProductGRPCClient()
            response = client.get_product(product_id)
            client.close()
            
            if response.success:
                product = response.product
                return Response({
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'stock_quantity': product.stock_quantity,
                    'category': product.category,
                    'created_at': product.created_at,
                    'updated_at': product.updated_at,
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
    
    def put(self, request, product_id):
        """Update a product"""
        try:
            data = request.data
            
            client = ProductGRPCClient()
            response = client.update_product(
                product_id=product_id,
                name=data.get('name'),
                description=data.get('description'),
                price=float(data['price']) if 'price' in data else None,
                stock_quantity=int(data['stock_quantity']) if 'stock_quantity' in data else None,
                category=data.get('category')
            )
            client.close()
            
            if response.success:
                product = response.product
                return Response({
                    'success': True,
                    'message': response.message,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'stock_quantity': product.stock_quantity,
                        'category': product.category,
                        'created_at': product.created_at,
                        'updated_at': product.updated_at,
                    }
                })
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_404_NOT_FOUND
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
    
    def delete(self, request, product_id):
        """Delete a product"""
        try:
            client = ProductGRPCClient()
            response = client.delete_product(product_id)
            client.close()
            
            if response.success:
                return Response({
                    'success': True,
                    'message': response.message
                })
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_404_NOT_FOUND
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


class ProductSearchView(APIView):
    """API view for searching products via gRPC"""
    
    def get(self, request):
        """Search products"""
        try:
            query = request.query_params.get('query', '')
            category = request.query_params.get('category', '')
            min_price = float(request.query_params.get('min_price', 0))
            max_price = float(request.query_params.get('max_price', 0))
            
            client = ProductGRPCClient()
            response = client.search_products(
                query=query,
                category=category,
                min_price=min_price,
                max_price=max_price
            )
            client.close()
            
            products = [
                {
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'price': p.price,
                    'stock_quantity': p.stock_quantity,
                    'category': p.category,
                    'created_at': p.created_at,
                    'updated_at': p.updated_at,
                }
                for p in response.products
            ]
            
            return Response({
                'products': products,
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
