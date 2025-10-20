import grpc
import products_pb2
import products_pb2_grpc


class ProductGRPCClient:
    """Client for interacting with Product gRPC service"""
    
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = products_pb2_grpc.ProductServiceStub(self.channel)
    
    def create_product(self, name, description, price, stock_quantity, category):
        """Create a new product"""
        request = products_pb2.CreateProductRequest(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            category=category
        )
        return self.stub.CreateProduct(request)
    
    def get_product(self, product_id):
        """Get a product by ID"""
        request = products_pb2.GetProductRequest(id=product_id)
        return self.stub.GetProduct(request)
    
    def list_products(self, page=1, page_size=10):
        """List products with pagination"""
        request = products_pb2.ListProductsRequest(
            page=page,
            page_size=page_size
        )
        return self.stub.ListProducts(request)
    
    def update_product(self, product_id, name=None, description=None, 
                      price=None, stock_quantity=None, category=None):
        """Update a product"""
        request = products_pb2.UpdateProductRequest(
            id=product_id,
            name=name or '',
            description=description or '',
            price=price or 0,
            stock_quantity=stock_quantity if stock_quantity is not None else -1,
            category=category or ''
        )
        return self.stub.UpdateProduct(request)
    
    def delete_product(self, product_id):
        """Delete a product"""
        request = products_pb2.DeleteProductRequest(id=product_id)
        return self.stub.DeleteProduct(request)
    
    def search_products(self, query='', category='', min_price=0, max_price=0):
        """Search products"""
        request = products_pb2.SearchProductsRequest(
            query=query,
            category=category,
            min_price=min_price,
            max_price=max_price
        )
        return self.stub.SearchProducts(request)
    
    def close(self):
        """Close the gRPC channel"""
        self.channel.close()
