"""
post
{
  "_id": ObjectId,
  "title": "게시물 제목",
  "user_id": ObjectId,  // 작성자
  "content": "글 내용",
  "address": “영문로 55
}

이 파일은 게시글(Post) 관련 데이터베이스 작업을 담당하는 모듈입니다.
MongoDB를 사용하는 Flask 프로젝트에서 게시글을 저장하고 불러오는 로직을 여기에 모아둡니다.
Flask 라우터와 분리함으로써 코드의 유지보수성과 재사용성을 높일 수 있습니다.
"""

from bson import ObjectId
from flask import jsonify, request


def get_valid_post_oid(post_id):
  
  # 클라이언트로부터 post_id를 받아옴
    post_id = request.form.get('post_id')
    if not post_id:
        return jsonify({'result': 'fail', 'msg': 'post_id가 필요합니다.'}), 400

# post_id를 ObjectId로 변환 (MongoDB용)
    try:
        post_oid = ObjectId(post_id)
    except Exception:
        return jsonify({'error': '유효하지 않은 post_id입니다.'}), 400



def add_bookmark_if_not_exists(db, user_oid, post_oid, bookmarks):
  
  # 이미 북마크한 게시물인지 확인
    if post_oid in bookmarks:
        return jsonify({'error': '이미 북마크한 게시물입니다.'}), 409

    # 중복 없이 북마크 추가
    db.users.update_one(
        {'_id': ObjectId(user_oid)},
        {'$addToSet': {'bookmarks': post_oid}}  # 중복 없이 추가
    )