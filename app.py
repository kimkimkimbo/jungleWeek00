"""
"""

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.jungle
# client = MongoClient('mongodb+srv://week00:250512@cluster0.vsudbri.mongodb.net/')
# db = client['dbweek00'] 


@app.route('/')
def home():
    return render_template('mainpage.html')


#회원가입

#로그인

#게시물
@app.route('/restaurant')  # 등록 페이지
def restaurant_page():
    return render_template('add_post.html')

@app.route('/restaurant/post', methods=['POST'])
def create_restaurant():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    address_receive = request.form.get('address_give')

    restaurant = {
        'title': title_receive,
        'user_id': ObjectId('68239775736f481afd9cfce2'),
        'content': content_receive,
        'address': address_receive
    }

    db.restaurant.insert_one(restaurant)
    return jsonify({'result': 'success'})

@app.route('/restaurant/<id>/edit')  # 수정 페이지
def edit_restaurant_page(id):
    restaurant = db.restaurant.find_one({'_id': ObjectId(id)})
    return render_template('edit_post.html', restaurant=restaurant)

@app.route('/restaurant/<id>/update', methods=['POST'])
def edit_restaurant(id):
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    address_receive = request.form['address_give']

    db.restaurant.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'title': title_receive,
            'content': content_receive,
            'address': address_receive
        }}
    )
    return jsonify({'result': 'success'})

#댓글

#북마크

#추천


if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)