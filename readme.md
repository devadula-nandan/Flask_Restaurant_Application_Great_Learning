<!-- '{"name":"Flask restaurent application","version": 12,"tech": ["Python","Flask","RestAPI","Swagger","MySQL"],"tags":["api","backend"],"snapshots":[]}' -->
# Flask Restaurant Project Assignment

## Introduction
This Flask Restaurant Project Assignment implements a restaurant management system using Flask framework. It includes features such as adding food items, managing orders, and handling a shopping cart.

## Features
1. Added an extra cart table and implemented an "add to cart" API. The "place order" API will only confirm and place the order without any additional parameters.

2. Unique ID generation for each table is implemented using a 5-digit integer. It is suggested to use a bigger string such as `uuid4()` for better uniqueness and to avoid collisions.

3. All the problem statement points are covered, and the points are commented in the `apis.py` file for reference.

4. Duplicate food item entries are allowed as different vendors can sell the same food item with different parameters. However, if the same vendor lists the same dish with the same price and calories, the available quantity will be incremented according to the given value.

    **Important Note:** Make sure to add the correct vendor ID in the "add-food-item" API to test this functionality. The vendor ID is taken as a parameter in the API. It is recommended to take the logged-in vendor's ID as the default, but the problem statement asked to provide it as a parameter.

## API Documentation
The API documentation can be accessed by running `main.py` and navigating to the following link: [http://127.0.0.1:8000/swagger-ui/](http://127.0.0.1:8000/swagger-ui/)

**Note:** There is no API provided to get admin rights in this assignment. To test the "Get_All_Orders" API, the level should be edited from the table to grant admin rights.

Feel free to explore the project and refer to the API documentation for further details on available endpoints and functionalities.

Thank you!
