from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
client = MongoClient()
db = client.Contractor
pieces = db.pieces


app = Flask(__name__)

@app.route('/')
def store_index():
    art_items = pieces.find()
    return render_template ('art_index.html', art_items=art_items)

@app.route('/art/new')
def new_art():
    return render_template('new_art.html')

@app.route('/pieces', methods=['POST'])
def submit_art():
    added_art = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price')
    }
    print(added_art)
    pieces.insert_one(added_art)
    return redirect(url_for('store_index'))

if __name__ == '__main__':
  app.run(debug=True)