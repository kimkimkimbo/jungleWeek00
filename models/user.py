"""
Users
{
  "_id": ObjectId,
  "name": “김보아”,
  “pw”: ******,
}

"""
#사용자 정보를 데이터베이스에 저장하는 함수
def create_user(db, user_id, name, pw):
    """
    db: MongoDB 데이터베이스 객체
    name: 사용자 이름
    pw: 사용자 비밀번호
    return: 생성된 사용자 ID
    post_id: 즐겨찾기 게시물 아이디
    """
    user = {
        "user_id": name,  # 사용자 ID는 이름으로 설정
        "name": name,
        "pw": pw,
    }

    result = db.users.insert_one(user)
    return str(result.inserted_id)
  

#사용자 정보를 데이터베이스에서 조회하는 함수
def get_user(db, user_id):
    """
    db: MongoDB 데이터베이스 객체
    user_id: 사용자 ID
    return: 사용자 정보 (딕셔너리 형태)
    """
    user = db.users.find_one({"_id": user_id})
    return user