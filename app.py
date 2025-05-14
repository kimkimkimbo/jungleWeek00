"""
"""


from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId

from models.user import create_user


app = Flask(__name__)


#SSR 방식이라면 jsonify() 대신 redirect()나 render_template()를 써야 함


client = MongoClient('mongodb+srv://week00:250512@cluster0.vsudbri.mongodb.net/')
db = client['dbweek00'] 

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    #회원가입 사용자에게 입력받은 데이터를 DB에 저장
    
    user_id = request.form['user_id']
    name = request.form['name']
    pw = request.form['pw']
    
    create_user(db, user_id, name, pw)
    
    #redirect는 사용자가 요청한 URL로 리다이렉트하는 함수
    return redirect(url_for('login'))  # 회원가입 후 로그인 페이지로 이동


# @app.route('/')
# def home():
#     return render_template('mainpage.html')


#회원가입

#로그인

@app.route('/login')
def login():
    return render_template('login.html')


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
        'user_id': ObjectId(),
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