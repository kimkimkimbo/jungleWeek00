// function postRestaurant() {
//   let restaurant = $('#restaurant').val();
//   let comment = $('#comment').val();
//   let location = $('#location').val();

//   if (restaurant === "") {
//     alert("식당 이름을 입력해 주세요.");
//     $('#restaurant').focus();
//     return;
//   } else if (location === "") {
//     alert("주소를 입력해 주세요.");
//     $('#location').focus();
//     return;
//   }

//   $.ajax({
//     type: "POST",
//     url: "/restaurant/post",
//     data: {
//       'title_give': restaurant,
//       'content_give': comment,
//       'address_give': location
//     },
//     success: function (response) {
//       if (response["result"] === "success") {
//         alert("포스팅 성공!");
//         window.location.href = '/';  // 또는 detail 페이지로 이동
//       } else {
//         alert("서버 오류!");
//       }
//     },
//     error: function (xhr) {
//       // 서버에서 HTTP 에러 응답 (예: 401, 500 등)을 보낸 경우
//       if (xhr.status === 401) {
//         alert("로그인이 필요합니다.");
//         window.location.href = '/login';  // 로그인 페이지로 이동할 수도 있음
//       } else {
//         alert("알 수 없는 오류가 발생했습니다. 다시 시도해 주세요.");
//       }
//     }
//   });
// }

// function editRestaurant(id) {
//   let title = $('#restaurant').val();
//   let content = $('#comment').val();
//   let address = $('#location').val();

//   $.ajax({
//     type: 'POST',
//     url: `/restaurant/${id}/update`,
//     data: {
//       'title_give': title,
//       'content_give': content,
//       'address_give': address
//     },
//     success: function (response) {
//       if (response.result === 'success') {
//         alert('수정되었습니다!');
//         window.location.href = '/';
//       } else {
//         alert('수정 실패');
//       }
//     }
//   });
// }


// document.addEventListener('DOMContentLoaded', function() {
//   var flashMessage = document.getElementById('flash-messages');

//   if (flashMessage) {
//     var message = flashMessage.getAttribute('data-flash');  // 메시지 속성 가져오기
//     if (message) {
//       alert(message);  // 메시지가 있으면 alert로 표시
//     }
//   }
// });


// document.addEventListener('DOMContentLoaded', function () {
//   const params = new URLSearchParams(window.location.search);
//   const msg = params.get('msg');
//   if (msg) {
//     alert(msg);
//   }
// });

