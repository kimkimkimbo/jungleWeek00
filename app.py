"""
"""
#SSR 방식이라면 jsonify() 대신 redirect()나 render_template()를 써야 함

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from models.user import create_user, get_user_by_user_id, validate_user_password, get_user_by_object_id
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
    info_list = list(db.jungle.find({}))
    for info in info_list:
        info['_id'] = str(info['_id'])
    return render_template('mainpage.html', info_list=info_list)


#-----------------보아
#회원가입
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #회원가입 사용자에게 입력받은 데이터를 DB에 저장
        user_id = request.form['user_id']
        name = request.form['name']
        pw = request.form['pw']
        
        #print("회원가입 시도:", user_id, name)
        
        validate_user_info(db, user_id, name, pw)

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



#로그아웃
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None) 
    session.pop('user_oid', None)
    return redirect(url_for('home'))



# 북마크 페이지 렌더링 (SSR 방식)
@app.route('/bookmark', methods=['GET'])
def bookmark():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = get_user_by_object_id(db, session['user_oid'])
    bookmark_ids = user.get('bookmarks', [])

    # ObjectId 리스트로 변환 (MongoDB 쿼리용)
    try:
        bookmark_object_ids = [ObjectId(bid) if isinstance(bid, str) else bid for bid in bookmark_ids]
    except Exception as e:
        print("ObjectId 변환 실패:", e)
        bookmark_object_ids = []

    posts = list(db.jungle.find({'_id': {'$in': bookmark_object_ids}}))

    # 템플릿에서 사용할 수 있도록 _id를 문자열로 변환
    for post in posts:
        post['_id'] = str(post['_id'])

    return render_template('bookmarkpage.html', posts=posts)



#사용자 UX 경험을 고려했을 때 AJAX로 구현하는 것이 좋음
#SSR로 구현 시 -> 즐겨찾기 누를 때마다 페이지 전체 새로고침 , flash()띄우면 북마크 페이지로 리디렉션되어야만 사용자에게 보여짐 -> 당장 나가고 싶은 UX됨....
@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    
    # 로그인 되어 있지 않으면 로그인 페이지로 리디렉션
    if 'user_id' not in session:
        return jsonify({'result': 'fail', 'msg': '로그인이 필요합니다.'}), 401
    
    # 클라이언트로부터 post_id를 받아옴
    post_id = request.form.get('post_id')
    if not post_id:
        return jsonify({'result': 'fail', 'msg': 'post_id가 필요합니다.'}), 400
    
    # post_id를 ObjectId로 변환 (MongoDB용)
    try:
        post_oid = ObjectId(post_id)
    except Exception:
        return jsonify({'error': '유효하지 않은 post_id입니다.'}), 400
    
    # 사용자 정보 불러오기
    user_oid = session['user_oid']
    user = db.users.find_one({'_id': ObjectId(user_oid)})
    
    
    # 북마크 필드가 없으면 빈 리스트로 초기화
    bookmarks = user.get('bookmarks', [])
    
    
    # 이미 북마크한 게시물인지 확인
    if post_oid in bookmarks:
        return jsonify({'error': '이미 북마크한 게시물입니다.'}), 409
    
    
    # 중복 없이 북마크 추가
    db.users.update_one(
        {'_id': ObjectId(user_oid)},
        {'$addToSet': {'bookmarks': post_oid}}  # 중복 없이 추가
    )
    
    
    return jsonify({'message': '북마크 추가됨'})

#------------------- 혜린

#게시물
@app.route('/restaurant')  # 등록 페이지
def restaurant_page():
    return render_template('add_post.html')

@app.route('/restaurant/post', methods=['POST'])
def create_restaurant():
    user_id = session.get("user_id")

    if user_id is None:
      return jsonify({'result': 'fail', 'msg': '로그인이 필요합니다.'}), 401
    
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    address_receive = request.form.get('address_give')

    restaurant = {
        'title': title_receive,
        'user_id': user_id,
        'content': content_receive,
        'address': address_receive
    }

    db.jungle.insert_one(restaurant)
    return jsonify({'result': 'success'})

@app.route('/restaurant/<id>/edit')  # 수정 페이지
def edit_restaurant_page(id):
    restaurant = db.jungle.find_one({'_id': ObjectId(id)})
    return render_template('edit_post.html', restaurant=restaurant)

@app.route('/restaurant/<id>/update', methods=['POST'])
def edit_restaurant(id):
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    address_receive = request.form['address_give']

    db.jungle.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'title': title_receive,
            'content': content_receive,
            'address': address_receive
        }}
    )
    return jsonify({'result': 'success'})








#---------------주형
#상세 페이지
@app.route('/detail/<post_id>')
def detail(post_id):
    post_info = db.jungle.find_one({'_id':ObjectId(post_id)})
    review_dict = list(db.comment.find({'post_id':str(post_info['_id'])},{'_id':0, 'post_id':0}))
    reviews = [[*v.values()][0] for v in review_dict]


    return render_template('detail_page.html', post_info=post_info, reviews=reviews)

@app.route('/review', methods=['POST'])
def review():
    post_id = request.form['post_id']
    review = request.form['review']
    db.comment.insert_one({'post_id':post_id, 'content':review})

    return redirect(url_for('detail', post_id=post_id))





if __name__ == '__main__':  
   app.run('0.0.0.0', port=5001, debug=True)
