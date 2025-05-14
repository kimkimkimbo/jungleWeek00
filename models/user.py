

from pymongo import MongoClient
from werkzeug.security import check_password_hash  # 비밀번호 검증 함수
from werkzeug.security import generate_password_hash #비밀번호 해시화! 암호화 해야 함
from bson import ObjectId 


#사용자 정보 저장
def create_user(db, user_id, name, pw):
    """
    db: MongoDB 데이터베이스 객체
    user_id: 사용자 로그인 아이디
    name: 사용자 이름
    pw: 비밀번호
    """

    hashed_pw = generate_password_hash(pw)

    user = {
        "user_id": user_id,
        "name": name,
        "pw": hashed_pw,
    }
    
    #print('받은 아이디:', user_id)
    #print('받은 이름', name)


    result = db.users.insert_one(user)
    return str(result.inserted_id)


#로그인 아이디 조회
def get_user_by_user_id(db, user_id):
    """
    db: MongoDB 데이터베이스 객체
    user_id: 사용자 로그인 아이디
    return: 사용자 정보 (딕셔너리 형태)
    """
    #print('받은 아이디:', user_id)
    #print('DB에서 찾은 사용자:', db.users.find_one({"user_id": user_id}))

    return db.users.find_one({"user_id": user_id})

#로그인 비밀번호 검증
def validate_user_password(user, password):
    """
    user: 데이터베이스에서 조회한 사용자 정보
    password: 로그인 시 입력된 비밀번호
    return: 비밀번호 일치 여부 (True/False)
    """
    return check_password_hash(user['pw'], password)  # 비밀번호 비교

#object_id 조회
def get_user_by_object_id(db, object_id_str):
    """
    db: MongoDB 데이터베이스 객체
    object_id_str: MongoDB의 ObjectId를 문자열로 전달
    return: 해당 ObjectId에 맞는 사용자 정보
    """
    try:
        object_id = ObjectId(object_id_str)
        return db.users.find_one({"_id": object_id})
    except:

        return None  # 잘못된 ID 형식이면 None 반환
