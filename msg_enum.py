from enum import Enum

class Message(Enum):
    login_success = "User successfully logged in."
    login_fail = "Oops, Wrong Credentials !"
    logout = "User successfully logged out."
    
    customuser_create = "User Created."
    customuser_update = "User Data Updated."
    customuser_delete = "User Data Deleted."
    
    address_create = "Another Address added for currently logged-in user."
    address_update = "Address Data Updated."
    address_delete = "Address Data Deleted."

    review_create = "Review added successfully."
    review_update = "Review Updated."
    review_delete = "Review deleted successfully ."
    
    cart_add_item = "Book added in Cart."
    cart_remove_item = "Book Removed from Cart."
    cart_empty = "Cart is currently empty."
    cart_checkout = "Order Successfully Placed."
    # cart_checkout = f"Order Placed \nFor the Book(s) - {book} \nTotal amount is {sum(amount)}Rs."
    
    wishlist_create = "Wish List created"
    wishlist_add_item = "Book successfully added to your wishlist."
    wishlist_remove_item = "Book is removed from your wihslist."
    
    return_order = "Your request to return the order is approved."
    
    error = "Request couldn't be performed because of - "
