# Order Delivery Service with FastAPI

This project serves as a proof of concept (PoC) for an Order Delivery Service built with FastAPI. It demonstrates my ability to design and implement a basic order management system using a modern Python web framework.
 

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)


## Introduction

This Order Delivery Service PoC is designed to showcase my skills in building a basic order management system using FastAPI. It serves as evidence of my proficiency in designing and implementing RESTful APIs with Python.

## Features

- Create new orders
- Update order
- Update order status
- Get all order details
- Get specific order details
- Get specific customer order details
- Delete specific order

## Technologies Used

- FastAPI
- Python 3.11
- PostgreSQL
- SQLAlchemy
- OpenAPI

## Installation

To run this Order Delivery Service PoC locally, follow these steps:

    1. Clone this repository:

        git clone https://github.com/priyankashettar/order-delivery-service.git

    2. Navigate to the project directory
    
        cd order-delivery-poc

    3. Install Dependencies:

        pip install -r requirements.txt

    4. To Run the Development Server:

        uvicorn src.main:app --reload

    5. The API will be accessible at http://localhost:8000

## Usage

### Create a New Order

To create a new order, make a POST request to the `/order/order` endpoint with the required data in the request body:

    {
        "cust_name": "Samuel",
        "order_size": "SMALL",
        "quantity":2    
    }


## API Endpoints

- `POST /order/order`: Create a new order.
- `GET /order/orders`: List all orders.
- `GET /order/orders/{id}/`: Retrieve order details by ID.
- `GET /order/customer/orders/{id}`: List specific customer orders by ID.
- `PUT /order/order/update/{id}/`: Update order details.
- `PATCH /order/order/update/{id}`: Update order status by ID.
- `DELETE /order/orders/delete/{id}/`: Delete order by ID.


## Contributing

Contributions are welcome! To contribute to this PoC project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.


## License

This project is licensed under the [Apache License 2.0].


## References
https://fastapi.tiangolo.com/
https://www.postgresql.org/docs/current/
https://docs.sqlalchemy.org/en/20/
https://swagger.io/specification/


