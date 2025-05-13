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