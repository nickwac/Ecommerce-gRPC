# 🛒 Wishlist & Cart API - Quick Testing Guide

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Ensure server is running
./venv/bin/python manage.py runserver

# Create a test user if you haven't
./venv/bin/python manage.py createsuperuser
```

### 2. Get Authentication Token
```bash
# Login to get JWT token
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'

# Save the access token from response
export TOKEN="your_access_token_here"
```

---

## 📋 Wishlist API Testing

### Test 1: Add Product to Wishlist
```bash
curl -X POST http://localhost:8000/api/v1/wishlist/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "notes": "Want to buy this for Christmas"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Product added to wishlist",
  "item": {
    "id": 1,
    "product": {...},
    "notes": "Want to buy this for Christmas",
    "added_at": "2025-10-20T15:00:00Z",
    "is_in_stock": true,
    "product_price": "99.99"
  }
}
```

### Test 2: View Wishlist
```bash
curl -X GET http://localhost:8000/api/v1/wishlist/ \
  -H "Authorization: Bearer $TOKEN"
```

### Test 3: Check if Product in Wishlist
```bash
curl -X GET http://localhost:8000/api/v1/wishlist/check/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "in_wishlist": true,
  "product_id": 1
}
```

### Test 4: Move to Cart
```bash
curl -X POST http://localhost:8000/api/v1/wishlist/move-to-cart/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Product moved to cart",
  "cart_item_id": 1
}
```

### Test 5: Remove from Wishlist
```bash
curl -X DELETE http://localhost:8000/api/v1/wishlist/remove/1/ \
  -H "Authorization: Bearer $TOKEN"
```

### Test 6: Clear Wishlist
```bash
curl -X POST http://localhost:8000/api/v1/wishlist/clear/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🛒 Shopping Cart API Testing

### Test 1: Add to Cart
```bash
curl -X POST http://localhost:8000/api/v1/cart/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Product added to cart",
  "cart_item": {
    "id": 1,
    "product": {...},
    "quantity": 2,
    "price": "99.99",
    "subtotal": "199.98",
    "is_available": true
  }
}
```

### Test 2: View Cart
```bash
curl -X GET http://localhost:8000/api/v1/cart/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "success": true,
  "cart": {
    "id": 1,
    "items": [
      {
        "id": 1,
        "product": {...},
        "quantity": 2,
        "price": "99.99",
        "subtotal": "199.98",
        "is_available": true
      }
    ],
    "total_items": 2,
    "subtotal": "199.98",
    "total": "199.98"
  }
}
```

### Test 3: Update Item Quantity
```bash
curl -X PATCH http://localhost:8000/api/v1/cart/item/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 5
  }'
```

### Test 4: Get Cart Summary
```bash
curl -X GET http://localhost:8000/api/v1/cart/summary/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "success": true,
  "summary": {
    "total_items": 5,
    "subtotal": 499.95,
    "total": 499.95,
    "items_count": 1
  }
}
```

### Test 5: Remove Item from Cart
```bash
curl -X DELETE http://localhost:8000/api/v1/cart/item/1/remove/ \
  -H "Authorization: Bearer $TOKEN"
```

### Test 6: Clear Cart
```bash
curl -X POST http://localhost:8000/api/v1/cart/clear/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧪 Complete Test Workflow

### Scenario: User adds products, manages wishlist and cart

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}' \
  | jq -r '.access')

# 2. Add product to wishlist
curl -X POST http://localhost:8000/api/v1/wishlist/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "notes": "Birthday gift"}'

# 3. View wishlist
curl -X GET http://localhost:8000/api/v1/wishlist/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Move wishlist item to cart
curl -X POST http://localhost:8000/api/v1/wishlist/move-to-cart/1/ \
  -H "Authorization: Bearer $TOKEN"

# 5. Add more items directly to cart
curl -X POST http://localhost:8000/api/v1/cart/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 2, "quantity": 3}'

# 6. View cart
curl -X GET http://localhost:8000/api/v1/cart/ \
  -H "Authorization: Bearer $TOKEN"

# 7. Update quantity
curl -X PATCH http://localhost:8000/api/v1/cart/item/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 2}'

# 8. Get cart summary
curl -X GET http://localhost:8000/api/v1/cart/summary/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔍 Error Testing

### Test Invalid Product ID
```bash
curl -X POST http://localhost:8000/api/v1/wishlist/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 99999}'
```

**Expected Response:**
```json
{
  "success": false,
  "errors": {
    "product_id": ["Product does not exist."]
  }
}
```

### Test Duplicate Wishlist Item
```bash
# Add same product twice
curl -X POST http://localhost:8000/api/v1/wishlist/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'

# Try adding again
curl -X POST http://localhost:8000/api/v1/wishlist/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'
```

**Expected Response:**
```json
{
  "success": false,
  "errors": ["Product already in wishlist."]
}
```

### Test Insufficient Stock
```bash
# Try to add more than available stock
curl -X POST http://localhost:8000/api/v1/cart/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 1000}'
```

**Expected Response:**
```json
{
  "success": false,
  "error": "Only 50 units available"
}
```

### Test Invalid Quantity
```bash
curl -X POST http://localhost:8000/api/v1/cart/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 0}'
```

**Expected Response:**
```json
{
  "success": false,
  "errors": {
    "quantity": ["Ensure this value is greater than or equal to 1."]
  }
}
```

---

## 📊 Using Swagger UI (Recommended)

The easiest way to test is using the interactive Swagger UI:

1. **Open Swagger**: http://localhost:8000/api/docs/
2. **Authorize**: Click "Authorize" button, enter token as `Bearer YOUR_TOKEN`
3. **Navigate to sections**:
   - Scroll to **Wishlist** section
   - Scroll to **Shopping Cart** section
4. **Try endpoints**: Click "Try it out" on any endpoint
5. **Execute**: Fill in parameters and click "Execute"
6. **View response**: See the response below

---

## 🎯 Common Use Cases

### Use Case 1: Browse and Save for Later
```bash
# 1. User browses products
curl http://localhost:8000/api/v1/products/

# 2. Adds interesting product to wishlist
curl -X POST http://localhost:8000/api/v1/wishlist/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"product_id": 5}'

# 3. Continues browsing...
# 4. Later, views wishlist
curl http://localhost:8000/api/v1/wishlist/ \
  -H "Authorization: Bearer $TOKEN"
```

### Use Case 2: Ready to Purchase
```bash
# 1. User decides to buy from wishlist
curl -X POST http://localhost:8000/api/v1/wishlist/move-to-cart/5/ \
  -H "Authorization: Bearer $TOKEN"

# 2. Adds more items directly to cart
curl -X POST http://localhost:8000/api/v1/cart/add/ \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"product_id": 3, "quantity": 2}'

# 3. Reviews cart before checkout
curl http://localhost:8000/api/v1/cart/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Adjusts quantities
curl -X PATCH http://localhost:8000/api/v1/cart/item/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"quantity": 1}'

# 5. Proceeds to checkout (to be implemented)
```

### Use Case 3: Cart Management
```bash
# 1. User adds multiple items
for id in 1 2 3 4 5; do
  curl -X POST http://localhost:8000/api/v1/cart/add/ \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"product_id\": $id, \"quantity\": 1}"
done

# 2. Reviews cart
curl http://localhost:8000/api/v1/cart/ \
  -H "Authorization: Bearer $TOKEN"

# 3. Removes unwanted items
curl -X DELETE http://localhost:8000/api/v1/cart/item/2/remove/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Gets final summary
curl http://localhost:8000/api/v1/cart/summary/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔧 Python Testing Script

Save as `test_wishlist_cart.py`:

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Login
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "username": "admin",
    "password": "admin"
})
token = response.json()['access']
headers = {"Authorization": f"Bearer {token}"}

# 2. Add to wishlist
response = requests.post(
    f"{BASE_URL}/wishlist/add/",
    headers=headers,
    json={"product_id": 1, "notes": "Test item"}
)
print("Add to wishlist:", response.json())

# 3. View wishlist
response = requests.get(f"{BASE_URL}/wishlist/", headers=headers)
print("Wishlist:", response.json())

# 4. Move to cart
response = requests.post(
    f"{BASE_URL}/wishlist/move-to-cart/1/",
    headers=headers
)
print("Move to cart:", response.json())

# 5. Add to cart
response = requests.post(
    f"{BASE_URL}/cart/add/",
    headers=headers,
    json={"product_id": 2, "quantity": 3}
)
print("Add to cart:", response.json())

# 6. View cart
response = requests.get(f"{BASE_URL}/cart/", headers=headers)
print("Cart:", response.json())

# 7. Get summary
response = requests.get(f"{BASE_URL}/cart/summary/", headers=headers)
print("Cart summary:", response.json())
```

Run with:
```bash
python test_wishlist_cart.py
```

---

## ✅ Verification Checklist

After testing, verify:

- [ ] Can add products to wishlist
- [ ] Can view wishlist with correct data
- [ ] Can remove items from wishlist
- [ ] Can move wishlist items to cart
- [ ] Can add products to cart with quantity
- [ ] Can update cart item quantities
- [ ] Can remove items from cart
- [ ] Can view cart with correct totals
- [ ] Stock validation works (can't add more than available)
- [ ] Duplicate prevention works
- [ ] Authentication is required for all endpoints
- [ ] Error messages are clear and helpful
- [ ] Cart persists across requests
- [ ] Wishlist persists across requests

---

## 🎉 Success!

If all tests pass, your Wishlist and Shopping Cart features are working perfectly!

**Next Steps:**
1. Integrate with frontend
2. Add checkout process
3. Implement payment processing
4. Add order creation from cart
5. Enable email notifications

---

**Happy Testing!** 🚀
