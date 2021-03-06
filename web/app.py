from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

#mongo DB and hosting
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
pieces = db.pieces
cart = db.cart

#Flask app
app = Flask(__name__, static_url_path='')

@app.route('/')
#Home page route
def art_index():
    art_items = pieces.find()
    return render_template ('art_index.html', art_items=art_items)

@app.route('/art/new')
#new art submission page
def new_art():
    return render_template('new_art.html')

@app.route('/art', methods=['POST'])
#submit new art to website
def submit_art():
    added_art = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'url': request.form.get('url')
    }
    piece_id = pieces.insert_one(added_art).inserted_id
    return redirect(url_for('art_show', piece_id=piece_id)) # <--------- has to be the app.route's method that renders art_index

@app.route('/art/<piece_id>')
#look at one art piece
def art_show(piece_id):
    piece = pieces.find_one({'_id': ObjectId(piece_id)})
    return render_template('art_show.html', piece=piece)

@app.route('/art/<piece_id>', methods=['POST'])
#edit sumbission
def art_update(piece_id):
    new_art = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'url': request.form.get('url'),
    }
    pieces.update_one(
        {'_id': ObjectId(piece_id)},
        {'$set': new_art})
    return redirect(url_for('art_show', piece_id=piece_id))
    
@app.route('/art/<piece_id>/edit')
#edit form
def chips_edit(piece_id):
    piece = pieces.find_one({'_id': ObjectId(piece_id)})
    return render_template('art_edit.html', piece=piece)

@app.route('/art/<piece_id>/delete', methods=['POST'])
#Delete post method
def pieces_delete(piece_id):
    pieces.delete_one({'_id': ObjectId(piece_id)})
    return redirect(url_for('art_index'))

@app.route('/cart/<item_id>/delete', methods=['POST'])
#delete item from cart
def cart_delete(item_id):
    cart.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('cart_index'))
    
@app.route('/art/<piece_id>/cart', methods=['POST'])
#add item to cart
def add_to_cart(piece_id):
    piece = pieces.find_one({'_id': ObjectId(piece_id)})
    item = {
        'title': piece["title"],
        'description': piece["description"],
        'price': piece["price"],
        'url': piece["url"],
        'item_id': piece["_id"],
        'cart_total': piece["price"]
    }
    cart.insert_one(item)
    return redirect(url_for('cart_index', piece_id=piece_id))
    
@app.route('/art/cart')
#cart page
def cart_index():
    cart_items = cart.find()
    return render_template('cart_index.html', cart_items=cart_items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))