function postRestaurant() {
  let restaurant = $('#restaurant').val();
  let comment = $('#comment').val();
  let location = $('#location').val();

  if (restaurant === "") {
    alert("식당 이름을 입력해 주세요.");
    $('#restaurant').focus();
    return;
  } else if (location === "") {
    alert("주소를 입력해 주세요.");
    $('#location').focus();
    return;
  }

  $.ajax({
    type: "POST",
    url: "/restaurant/post",
    data: {
      'title_give': restaurant,
      'content_give': comment,
      'address_give': location
    },
    success: function (response) {
      if (response["result"] === "success") {
        alert("포스팅 성공!");
        window.location.href = '/';  // 또는 detail 페이지로 이동
      } else {
        alert("서버 오류!");
      }
    }
  });
}

function editRestaurant(id) {
  let title = $('#restaurant').val();
  let content = $('#comment').val();
  let address = $('#location').val();

  $.ajax({
    type: 'POST',
    url: `/restaurant/${id}/update`,
    data: {
      'title_give': title,
      'content_give': content,
      'address_give': address
    },
    success: function (response) {
      if (response.result === 'success') {
        alert('수정되었습니다!');
        window.location.href = '/';
      } else {
        alert('수정 실패');
      }
    }
  });
}
