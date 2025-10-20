#!/bin/bash

# Script to start both gRPC servers in the background

echo "Starting Product gRPC Server on port 50051..."
python products/grpc_server.py &
PRODUCT_PID=$!

echo "Starting Order gRPC Server on port 50052..."
python orders/grpc_server.py &
ORDER_PID=$!

echo ""
echo "gRPC Servers started successfully!"
echo "Product Server PID: $PRODUCT_PID"
echo "Order Server PID: $ORDER_PID"
echo ""
echo "To stop the servers, run: kill $PRODUCT_PID $ORDER_PID"
echo "Or use: pkill -f grpc_server.py"
echo ""
echo "Now you can start the Django server with: python manage.py runserver"
