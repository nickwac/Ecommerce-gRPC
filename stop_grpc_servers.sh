#!/bin/bash

# Script to stop all gRPC servers

echo "Stopping gRPC servers..."
pkill -f grpc_server.py

if [ $? -eq 0 ]; then
    echo "gRPC servers stopped successfully!"
else
    echo "No gRPC servers found running."
fi
