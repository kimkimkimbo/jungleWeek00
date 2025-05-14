"""
"""

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

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

#댓글

#북마크

#추천


if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)
