$(document).ready(function() {
    $('.mark-btn').click(function(e) {
        e.preventDefault();
        const card = $(this).closest('.card');
        const postId = card.data('post-id');

        $.ajax({
            url: '/add_bookmark',
            method: 'POST',
            data: { post_id: postId },
            success: function(res) {
                alert(res.message || '북마크 성공');
                card.find('.mark-btn').addClass('active');
            },
            error: function(xhr) {
                if (xhr.status === 401 && xhr.responseJSON?.redirect) {
                    window.location.href = xhr.responseJSON.redirect;
                } else if (xhr.responseJSON?.error) {
                    alert(xhr.responseJSON.error);
                } else {
                    alert('알 수 없는 오류');
                }
            }
        });
    });
});