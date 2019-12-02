from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Contractor
pieces = db.pieces


app = Flask(__name__)

@app.route('/')
#Home page route
def art_index():
    art_items = pieces.find()
    return render_template ('art_index.html', art_items=art_items)

@app.route('/art/new')
#new art submission page
def new_art():
    return render_template('new_art.html')

@app.route('/pieces', methods=['POST'])
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
    art = pieces.find_one({'_id': ObjectId(piece_id)})
    return render_template('art_show.html', art=art)

if __name__ == '__main__':
  app.run(debug=True)