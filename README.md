# Variant Control API

This repository contains the backend system for managing products with variants. The API is built using Flask and MongoDB.

## Requirements

- Python 3
- MongoDB

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/madanarnav2004/Variant_control_flask.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Start MongoDB server:

    ```bash
    mongosh
    ```

4. Run the Flask application:

    ```bash
    python app.py
    ```

## API Endpoints

### Adding a New Product

- **URL**: `/products`
- **Method**: `POST`
- **Body**:

    ```json
    {
      "name": "Product Name",
      "attributes": ["Attribute 1", "Attribute 2"]
    }
    ```

### Retrieving All Products

- **URL**: `/products`
- **Method**: `GET`

### Retrieving a Product by ID

- **URL**: `/products/<product_id>`
- **Method**: `GET`

### Updating a Product by ID

- **URL**: `/products/<product_id>`
- **Method**: `PUT`
- **Body**:

    ```json
    {
      "name": "Updated Product Name",
      "attributes": ["Updated Attribute 1", "Updated Attribute 2"]
    }
    ```

### Deleting a Product by ID

- **URL**: `/products/<product_id>`
- **Method**: `DELETE`

### Adding Variants to a Product

- **URL**: `/products/<product_id>/variants`
- **Method**: `POST`
- **Body**:

    ```json
    {
      "variants": [
        {
          "values": [{"attribute": "Attribute 1", "value": "Value 1"}]
        }
      ]
    }
    ```

### Updating a Variant by ID

- **URL**: `/products/<product_id>/variants/<variant_id>`
- **Method**: `PUT`
- **Body**:

    ```json
    {
      "values": [{"attribute": "Attribute 1", "value": "Updated Value 1"}]
    }
    ```

### Deleting a Variant by ID

- **URL**: `/products/<product_id>/variants/<variant_id>`
- **Method**: `DELETE`

## Using Postman

You can use Postman to interact with the API endpoints. Make sure you have the Postman Visual Studio Code extension installed.


1. Send requests to the desired endpoints by clicking on the "Send Request" button next to each request.
2. Edit the raw body option to add json wherever needed

###Demo Images
![Screenshot 4](https://github.com/madanarnav2004/Variant_control_flask/raw/main/Screenshot%202024-03-27%20at%2010.16.30%20PM.png)
![Screenshot 1](https://github.com/madanarnav2004/Variant_control_flask/raw/main/Screenshot%202024-03-27%20at%2010.29.45%20PM.png)

![Screenshot 2](https://github.com/madanarnav2004/Variant_control_flask/raw/main/Screenshot%202024-03-27%20at%2010.29.15%20PM.png)

![Screenshot 3](https://github.com/madanarnav2004/Variant_control_flask/raw/main/Screenshot%202024-03-27%20at%208.01.22%20PM.png)

![Screenshot 4](https://github.com/madanarnav2004/Variant_control_flask/raw/main/Screenshot%202024-03-27%20at%2010.16.30%20PM.png)


