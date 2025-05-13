"""
"""

from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient('mongodb+srv://week00:250512@cluster0.vsudbri.mongodb.net/')
db = client['dbweek00'] 



@app.route('/')
def home():
    return render_template('mainpage.html')


#회원가입

#로그인

#게시물

#댓글

#북마크

#추천


if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)
