from flask import Flask, request, make_response, jsonify
from dbhelpers import run_statement
from helpers import check_data

app = Flask(__name__)

# GET products, with optional price arg to limit search by price
@app.get('/api/products')
def get_products():
    """
    Optional Arguments:
    limit by price, 
    """
    price_limit = request.args.get('priceLimit')
    keys = ["productId", "name", "description", "price"]
    result = run_statement("CALL get_products(?)", [price_limit])
    products = []
    if (type(result) == list):
        for product in result:
            zipped = zip(keys, product)
            products.append(dict(zipped))
        return make_response(jsonify(products), 200)
    else:
        return make_response(jsonify(result), 500)

# GET User with Valid User ID
@app.get('/api/user')
def get_user():
    """
    Needs 1 Argument:
    userId
    """
    required_data = ['userId']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    user_id = request.json.get('userId')
    keys = ["userId", "username", "country", "created_at"]
    result = run_statement("CALL get_user(?)", [user_id])
    if (type(result) == list):
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify(result), 500)

# POST new purchases
# Response is NULL but request works
@app.post('/api/purchases')
def post_sale():
    """
    Needs 2 Arguments:
    userId, productId
    """
    required_data = ['userId', 'productId']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    user_id = request.json.get('userId')
    product_id = request.json.get('productId')
    result = run_statement("CALL post_purchase(?,?)", [user_id, product_id])
    if (type(result) == list):
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify(result), 500)

app.run(debug = True)