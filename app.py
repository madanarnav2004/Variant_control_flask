from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from http import HTTPStatus

mongo_uri="mongodb://127.0.0.1:27017/"  
client = MongoClient(mongo_uri)
db = client["var_control_db"]

product_collection = db["products"]
variant_collection = db["variants"]

# Helper functions
def get_product_by_id(product_id):
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    return product

def validate_request_data(data):
    if not data:
        return False, "Missing request body"
    if not isinstance(data, dict):
        return False, "Invalid request data format (expected a dictionary)"
    if "name" not in data or not isinstance(data["name"], str):
        return False, "Missing or invalid product name (expected a string)"
    if "attributes" not in data or not isinstance(data["attributes"], list):
        return False, "Missing or invalid attributes (expected a list of strings)"
    return True, None

def validate_variant_data(variant):
    if not isinstance(variant, dict):
        return False, "Invalid variant data format (expected a dictionary)"
    if "product_id" not in variant or not isinstance(variant["product_id"], str):
        return False, "Missing or invalid product ID (expected a string)"
    if "values" not in variant or not isinstance(variant["values"], list):
        return False, "Missing or invalid values (expected a list of dictionaries)"
    for value_dict in variant["values"]:
        if not isinstance(value_dict, dict):
            return False, "Invalid value data format (expected a dictionary)"
        if "attribute" not in value_dict or not isinstance(value_dict["attribute"], str):
            return False, "Missing or invalid attribute (expected a string)"
        if "value" not in value_dict or not isinstance(value_dict["value"], (str, int, bool)):
            return False, "Missing or invalid value for attribute (expected string, number, or boolean)"
    return True, None

# Create a Flask app
app = Flask(__name__)
@app.route("/")
def welcome():
    return """
    <h1>Welcome to Variant Control API</h1>
    <p>This API provides endpoints for managing products and their variants.</p>
    <p>Available endpoints:</p>
    <ul>
        <li><b>GET</b> /products</li>
        <li><b>POST</b> /products</li>
        <li><b>GET</b> /products/&lt;product_id&gt;</li>
        <li><b>PUT</b> /products/&lt;product_id&gt;</li>
        <li><b>DELETE</b> /products/&lt;product_id&gt;</li>
        <li><b>POST</b> /products/&lt;product_id&gt;/variants</li>
        <li><b>PUT</b> /products/&lt;product_id&gt;/variants/&lt;variant_id&gt;</li>
        <li><b>DELETE</b> /products/&lt;product_id&gt;/variants/&lt;variant_id&gt;</li>
    </ul>
    """

# Endpoint to display available routes
@app.route("/routes")
def routes():
    """
    Endpoint to display available routes.
    """
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append({"route": str(rule), "methods": list(rule.methods)})
    return jsonify({"routes": routes})
# API endpoints
@app.post("/products")
def add_product():
    """
    Endpoint to add a new product.
    """
    data = request.get_json()
    valid, error_message = validate_request_data(data)
    if not valid:
        return jsonify({"message": error_message}), HTTPStatus.BAD_REQUEST

    try:
        product_id = product_collection.insert_one(data).inserted_id
        return jsonify({"message": "Product added successfully", "product_id": str(product_id)}), HTTPStatus.CREATED
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.get("/products/<product_id>")
def get_product(product_id):
    """
    Endpoint to get product details by ID.
    """
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), HTTPStatus.NOT_FOUND

    
    product['_id'] = str(product['_id'])

    variants = []
    for variant_id in product.get("variants", []):
        variant = variant_collection.find_one({"_id": variant_id})
        if variant:  
            variants.append(variant)

    product["variants"] = variants  
    return jsonify(product), HTTPStatus.OK

@app.put("/products/<product_id>")
def update_product(product_id):
    """
    Endpoint to update product details by ID.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing request body"}), HTTPStatus.BAD_REQUEST

    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), HTTPStatus.NOT_FOUND

    try:
        product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": data})
        return jsonify({"message": "Product updated successfully"}), HTTPStatus.OK
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR
def convert_id_to_str(product):
    product['_id'] = str(product['_id'])
    return product

@app.get("/products")
def get_all_products():
    """
    Endpoint to retrieve all products.
    """
    products = list(product_collection.find())
    if not products:
        return jsonify({"message": "No products found"}), HTTPStatus.NOT_FOUND
    
    # Convert ObjectId to string for each product
    products = [convert_id_to_str(product) for product in products]
    
    return jsonify(products), HTTPStatus.OK


@app.delete("/products/<product_id>")
def delete_product(product_id):
    """
    Endpoint to delete a product by ID.
    """
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), HTTPStatus.NOT_FOUND

    try:
        product_collection.delete_one({"_id": ObjectId(product_id)})
        return jsonify({"message": "Product deleted successfully"}), HTTPStatus.OK
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.post("/products/<product_id>/variants")
def add_variants(product_id):
    """
    Endpoint to add variants to a product.
    """
    data = request.get_json()
    valid, error_message = validate_request_data(data)
    if not valid:
        return jsonify({"message": error_message}), HTTPStatus.BAD_REQUEST

    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), HTTPStatus.NOT_FOUND

    variant_ids = []
    for variant in data.get("variants", []):
        valid, error_message = validate_variant_data(variant)
        if not valid:
            return jsonify({"message": error_message}), HTTPStatus.UNPROCESSABLE_ENTITY

        variant_data = {"product_id": product_id, "values": variant["values"]}
        variant_id = variant_collection.insert_one(variant_data).inserted_id
        variant_ids.append(str(variant_id))

    product_collection.update_one({"_id": ObjectId(product_id)}, {"$push": {"variants": {"$each": variant_ids}}})
    return jsonify({"message": "Variants added successfully"}), HTTPStatus.CREATED

@app.put("/products/<product_id>/variants/<variant_id>")
def update_variant(product_id, variant_id):
    """
    Endpoint to update variant details by ID.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Missing request body"}), HTTPStatus.BAD_REQUEST

    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), HTTPStatus.NOT_FOUND

    try:
        variant_collection.update_one({"_id": ObjectId(variant_id)}, {"$set": data})
        return jsonify({"message": "Variant updated successfully"}), HTTPStatus.OK
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.delete("/products/<product_id>/variants/<variant_id>")
def delete_variant(product_id, variant_id):
    """
    Endpoint to delete a variant by ID.
    """
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), HTTPStatus.NOT_FOUND

    try:
        variant_collection.delete_one({"_id": ObjectId(variant_id)})
        return jsonify({"message": "Variant deleted successfully"}), HTTPStatus.OK
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == "__main__":
    app.run(debug=True,port=5001)

