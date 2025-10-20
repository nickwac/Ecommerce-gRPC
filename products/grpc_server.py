import grpc
from concurrent import futures
import sys
import os
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_grpc.settings')
django.setup()

from products.models import Product
from django.db.models import Q
import products_pb2
import products_pb2_grpc


class ProductServiceServicer(products_pb2_grpc.ProductServiceServicer):
    """gRPC service implementation for Product operations"""
    
    def _product_to_proto(self, product):
        """Convert Django Product model to protobuf Product message"""
        return products_pb2.Product(
            id=product.id,
            name=product.name,
            description=product.description,
            price=float(product.price),
            stock_quantity=product.stock_quantity,
            category=product.category,
            created_at=product.created_at.isoformat(),
            updated_at=product.updated_at.isoformat(),
        )
    
    def CreateProduct(self, request, context):
        """Create a new product"""
        try:
            product = Product.objects.create(
                name=request.name,
                description=request.description,
                price=request.price,
                stock_quantity=request.stock_quantity,
                category=request.category,
            )
            return products_pb2.ProductResponse(
                product=self._product_to_proto(product),
                success=True,
                message="Product created successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return products_pb2.ProductResponse(
                success=False,
                message=f"Error creating product: {str(e)}"
            )
    
    def GetProduct(self, request, context):
        """Get a product by ID"""
        try:
            product = Product.objects.get(id=request.id)
            return products_pb2.ProductResponse(
                product=self._product_to_proto(product),
                success=True,
                message="Product retrieved successfully"
            )
        except Product.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return products_pb2.ProductResponse(
                success=False,
                message="Product not found"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return products_pb2.ProductResponse(
                success=False,
                message=f"Error retrieving product: {str(e)}"
            )
    
    def ListProducts(self, request, context):
        """List products with pagination"""
        try:
            page = request.page if request.page > 0 else 1
            page_size = request.page_size if request.page_size > 0 else 10
            
            start = (page - 1) * page_size
            end = start + page_size
            
            products = Product.objects.all()[start:end]
            total_count = Product.objects.count()
            
            product_list = [self._product_to_proto(p) for p in products]
            
            return products_pb2.ListProductsResponse(
                products=product_list,
                total_count=total_count,
                page=page,
                page_size=page_size
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return products_pb2.ListProductsResponse(
                products=[],
                total_count=0,
                page=0,
                page_size=0
            )
    
    def UpdateProduct(self, request, context):
        """Update an existing product"""
        try:
            product = Product.objects.get(id=request.id)
            
            if request.name:
                product.name = request.name
            if request.description:
                product.description = request.description
            if request.price > 0:
                product.price = request.price
            if request.stock_quantity >= 0:
                product.stock_quantity = request.stock_quantity
            if request.category:
                product.category = request.category
            
            product.save()
            
            return products_pb2.ProductResponse(
                product=self._product_to_proto(product),
                success=True,
                message="Product updated successfully"
            )
        except Product.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return products_pb2.ProductResponse(
                success=False,
                message="Product not found"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return products_pb2.ProductResponse(
                success=False,
                message=f"Error updating product: {str(e)}"
            )
    
    def DeleteProduct(self, request, context):
        """Delete a product"""
        try:
            product = Product.objects.get(id=request.id)
            product.delete()
            
            return products_pb2.DeleteProductResponse(
                success=True,
                message="Product deleted successfully"
            )
        except Product.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return products_pb2.DeleteProductResponse(
                success=False,
                message="Product not found"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return products_pb2.DeleteProductResponse(
                success=False,
                message=f"Error deleting product: {str(e)}"
            )
    
    def SearchProducts(self, request, context):
        """Search products by query, category, and price range"""
        try:
            queryset = Product.objects.all()
            
            # Apply filters
            if request.query:
                queryset = queryset.filter(
                    Q(name__icontains=request.query) | 
                    Q(description__icontains=request.query)
                )
            
            if request.category:
                queryset = queryset.filter(category=request.category)
            
            if request.min_price > 0:
                queryset = queryset.filter(price__gte=request.min_price)
            
            if request.max_price > 0:
                queryset = queryset.filter(price__lte=request.max_price)
            
            products = queryset[:50]  # Limit to 50 results
            product_list = [self._product_to_proto(p) for p in products]
            
            return products_pb2.ListProductsResponse(
                products=product_list,
                total_count=queryset.count(),
                page=1,
                page_size=len(product_list)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return products_pb2.ListProductsResponse(
                products=[],
                total_count=0,
                page=0,
                page_size=0
            )


def serve(port=50051):
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    products_pb2_grpc.add_ProductServiceServicer_to_server(
        ProductServiceServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Product gRPC Server started on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
