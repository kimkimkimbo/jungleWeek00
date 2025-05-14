"""
"""
#SSR 방식이라면 jsonify() 대신 redirect()나 render_template()를 써야 함

from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from models.user import create_user, get_user_by_user_id, validate_user_password
from flask_cors import CORS
import os 
from bson import ObjectId  


app = Flask(__name__)
CORS(app) #모든 출처 허용, 매우 위험! 사용하지 않는 게 좋지만 당장 개발 편의를 위해 사용
app.secret_key = os.urandom(24) #session을 사용하려면 secret_key 반드시 설정, 임의 문자열도 가능

client = MongoClient('mongodb+srv://week00:250512@cluster0.vsudbri.mongodb.net/')
db = client['dbweek00'] 



@app.route('/')
def home():
    return render_template('mainpage.html')



#회원가입
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #회원가입 사용자에게 입력받은 데이터를 DB에 저장
        user_id = request.form['user_id']
        name = request.form['name']
        pw = request.form['pw']
        
        #print("회원가입 시도:", user_id, name)
        
        #회원가입 페이지에서 입력받은 데이터가 비어있지 않은지 확인
        if not user_id or not name or not pw:
            return render_template('signup.html', error='모두 입력해주세요.')
        
        # 중복 아이디 확인
        if get_user_by_user_id(db, user_id):
            return render_template('signup.html', error='이미 존재하는 아이디입니다.')

        
        # 비밀번호 길이 체크 (예: 최소 8자 이상)
        if len(pw) < 8:
            return render_template('signup.html', error='비밀번호는 최소 8자 이상이어야 합니다.')


    
        create_user(db, user_id, name, pw)
        
        #SSR 방식이라면 jsonify() 대신 redirect()나 render_template()를 써야 함
        #redirect는 사용자가 요청한 URL로 리다이렉트하는 함수
        return redirect(url_for('login'))  # 회원가입 후 로그인 페이지로 이동
    
    else :
        return render_template('signup.html')
    
    


#로그인
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':


        #로그인 사용자에게 입력받은 데이터를 DB에서 조회
        user_id = request.form['user_id']
        pw = request.form['pw']
        
        #로그인 페이지에서 입력받은 데이터가 비어있지 않은지 확인
        if not user_id or not pw:
            return render_template('login.html', error='모두 입력해주세요.')
        
        #DB에서 사용자 정보 조회
        user = get_user_by_user_id(db, user_id)
        #print('입력받은 아이디', user_id)
    
        if user and validate_user_password(user, pw):
            session.clear() #꼬이지 않도록 세션 초기화
            session['user_id'] = user_id  # 세션에 사용자 ID 저장
            session['user_oid'] = str(user['_id'])  # MongoDB 고유 ObjectId
            
            return redirect(url_for('home'))  # 로그인 성공 시 이동
        else:
                return render_template('login.html', error='아이디 또는 비밀번호가 잘못되었습니다.')
    else:
        return render_template('login.html')



#게시물
@app.route('/post', methods=['GET', 'POST'])
def post_page():
    user_id = session.get("user_id")
    if request.method == 'POST':
        if user_id is None:
            flash('로그인이 필요합니다.')
            return redirect(url_for('post_page'))

        title = request.form.get('title')
        content = request.form.get('content')
        address = request.form.get('address')

        post = {
            'title': title,
            'user_id': user_id,
            'content': content,
            'address': address
        }

        result = db.jungle.insert_one(post)
        post_id = str(result.inserted_id)
        flash('등록이 완료되었습니다.')
        return redirect(url_for('detail', id=post_id)) 
        # return redirect(url_for('home'))

    return render_template('add_post.html')


@app.route('/post/<id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = db.jungle.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        address = request.form.get('address')

        db.jungle.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'title': title,
                'content': content,
                'address': address
            }}
        )

        flash('수정이 완료되었습니다.')
        return redirect(url_for('detail', id=post_id))
        # return redirect(url_for('home'))

    return render_template('edit_post.html', post=post)


@app.route('/post/<id>/delete', methods=['POST'])
def delete_post(id):
    result = db.jungle.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        flash('삭제가 완료되었습니다.')
    else:
        flash('삭제할 게시글이 존재하지 않습니다.')
    return redirect(url_for('home'))






# @app.route('/restaurant')  # 등록 페이지
# def restaurant_page():
#     return render_template('add_post.html')

# @app.route('/restaurant/post', methods=['POST'])
# def create_restaurant():
#     user_id = session.get("user_id")

#     if user_id is None:
#       return jsonify({'result': 'fail', 'msg': '로그인이 필요합니다.'}), 401
    
#     title_receive = request.form.get('title_give')
#     content_receive = request.form.get('content_give')
#     address_receive = request.form.get('address_give')

#     restaurant = {
#         'title': title_receive,
#         'user_id': user_id,
#         'content': content_receive,
#         'address': address_receive
#     }

#     db.restaurant.insert_one(restaurant)
#     return jsonify({'result': 'success'})

# @app.route('/restaurant/<id>/edit')  # 수정 페이지
# def edit_restaurant_page(id):
#     restaurant = db.restaurant.find_one({'_id': ObjectId(id)})
#     return render_template('edit_post.html', restaurant=restaurant)

# @app.route('/restaurant/<id>/update', methods=['POST'])
# def edit_restaurant(id):
#     title_receive = request.form['title_give']
#     content_receive = request.form['content_give']
#     address_receive = request.form['address_give']

#     db.restaurant.update_one(
#         {'_id': ObjectId(id)},
#         {'$set': {
#             'title': title_receive,
#             'content': content_receive,
#             'address': address_receive
#         }}
#     )
#     return jsonify({'result': 'success'})

#댓글

#북마크

#추천


if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)

