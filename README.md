The files contained in this code were used to build the follwoing website:  
> [capstone1-anna-f](https://capstone1-anna-f.herokuapp.com/)

The idea behind this website was to build a mock real estate application in which new apartments can be added or deleted from a list of currently available apartments with the follwoing features and user flow:  
- A user can sign in either as an agent or an admin. The main difference being that admins can add or delete new apartments to the current inventory.
- Upon signing in the user is brought to the home page which shows a list of the currently available inventory. The user can click any of the list items to view more information about the apartment or add it to their own personal list of apartments. 
- To the left side of the inventory is a form that allows the user to filter through the inventory list and search for apartments with given parameters set. For example, a user can search for all two bedroom apartments in Brooklyn for $2000 or less. 
- From the home page the user can choose where they would like to go in the website by using the nav bar. 
- The map link takes the user to a page with a map filled with markers representing the available inventory. The same form from the home page is available here if the user would like to filter the map for apartments with certain criteria. You can click on the markers and view the address and price of a given marker.
- The My Apartments link will take the user to a list of their currently saved apartments. Each item on the list is a link that will bring the user to a detail page of that apartment. This page also gives the user the ability to upload photos of that apartment to be saved to that detail page. This provides the user with a convenient way to store and organize photos they may have of apartments that they are currently advertising. 
- The New Apartment link is only available to admin users. It allows the user to add a new apartment to the current inventory.

The two main goals of this website were to create an application that would provide an easy way to filter through a list of inventory and to provide an easy way to store and organize photos of property.  

The mapquest geolocation api was used on the backend to insert coordinates of an apartment into the databse when a new apartment is created and the Google Maps Javascript api was used for the client side map rendering. 

Tech stack:
- Python Flask
- Postgresql
- Sqlalchemy
- HTML, CSS, Javascript

