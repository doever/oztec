function NewsDetail() {

}

NewsDetail.prototype.listenCommentSubmit = function(){
    var self = this;
    var submitBtn = $('#submit-btn');
    submitBtn.click(function () {
        var contentObj = $("textarea[name='comment']");
        var content = contentObj.val();
        var new_id = submitBtn.attr('data-pk');
        console.log(content);
        console.log(new_id);
        csrfajax.post({
            'url':'/news/publish_comment/',
            'data':{
                'content':content,
                'new':new_id
            },
            'success':function (result) {
                if(result['code']===200){
                    console.log(result['data']);
                    var tpl = template('comment-item',{'comment':result['data']});
                    var commentList = $('.comment-list');
                    commentList.prepend(tpl);
                    contentObj.val('');
                    layer.msg('评论成功');
                }else{
                    //如果失败,弹出失败信息
                    layer.msg(result['message']);
                }
            },
            'error':function (error) {
                layer.msg('服务器内部错误');
            }
        })
    })
};

NewsDetail.prototype.run = function () {
    var self = this;
    self.listenCommentSubmit();
};

$(function () {
    var newsDetail = new NewsDetail();
    newsDetail.run();
});