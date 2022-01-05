# Flask Restaurant Project Assignment

# created extra cart table and add to cart api and now the place order will only confirm and place the order without any additional parameters

# The unique id generation for each tables is of 5 digit int and there is a function in apis.py, we could use a bigger string of uuid4() for more uniqueness and to avoid collisions

# all the problem statement points are covered, and the points are commented in apis.py

# duplicate food item entries are allowed as the different vendors can sell the same food item for different parameters, however if same vendor lists same dish with same price and calories, the available quantity will be incremented according to given value 
# imp note - make sure to add correct (logged in)vendor id in add-food-item api to test this functionality, as the vendor id is taken as parameter in it , (its better to take the logged in vendors id as default but the problem statement asked to give it as a parameter)



# api documentation link after running main.py http://127.0.0.1:8000/swagger-ui/
# since there is no api to get admin rights, in this assignment, the level should be edited from table for admin rights and to test Get_All_Orders api