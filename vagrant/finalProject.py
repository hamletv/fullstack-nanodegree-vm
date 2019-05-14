from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/restaurants')
def showRestaurant():
    #"This page will show all my restaurants."
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new')
def newRestaurant():
    #"This page will be for making a new restaurant."
    return render_template('newrestaurant.html', new_restaurant = new_restaurant)

@app.route('/restaurant/restaurant_id/edit')
def editRestaurant():
    #"This page will be for editing restaurant %s" % restaurant_id
    return render_template('editrestaurant.html', restaurant_id = restaurant_id)

@app.route('/restaurant/restaurant_id/delete')
def deleteRestaurant():
    #"This page will be for deleting restaurant %s" % restaurant_id
    return render_template('deleterestaurant.html', restaurant_id = restaurant_id)

@app.route('/restaurant/restaurant_id')
@app.route('/restaurant/restaurant_id/menu')
def showMenu():
    #"This page is the menu for restaurant %s" restaurant_id
    return render_template('menu.html', restaurant_id = restaurant_id, menu_id = menu_id)

@app.route('restaurant/restaurant_id/menu/new')
def newMenuItem():
    #"This page is for making a new menu item for restaurant %s" % restaurant_id
    return render_template('newmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id)

@app.route('/restaurant/restaurant_id/menu/edit')
def editMenuItem():
    #"This page is for editing menu item %s" % menu_id
    return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id)

@app.route('/restaurant/restaurant_id/menu/delete')
def deleteMenuItem():
    #"This page is for deleting menu item %s" %menu_id
    return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host = 0.0.0.0, port = 5000)
