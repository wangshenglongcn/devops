const API_URL = "http://117.72.175.93/posts"


$(document).ready(function() {
    $.ajax({
        url: API_URL,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            let html = '';
            data.forEach(post => {
                html += `<div class="">
                    <div class="">发布时间：${post.publish_date}</div>
                    <h1><a href="">标题：${post.title}</a></h1>
                    <p>内容：${post.text}</p>
                </div>
                <hr>
                `;
            });
            $('#posts').html(html);
        },
        success: function (data, textStatus, jqXHR) {
            console.log('成功获取数据:', data);        // 后端返回的 JSON
            console.log('状态:', textStatus);          // "success"
            console.log('响应码:', jqXHR.status);      // 200
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('失败，状态:', textStatus);   // "error"
            console.error('HTTP 状态码:', jqXHR.status); // 404 / 500 等
            console.error('错误信息:', errorThrown);    // "Not Found" 等
        }
    });
});