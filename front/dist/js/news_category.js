function NewCategory() {

}
NewCategory.prototype.run = function () {
  var self = this;
  self.listenAddCategory();
  self.listenEditCategory();
};

NewCategory.prototype.listenAddCategory = function () {
    var self = this;
    var addCategoryObj = $('#add_category');
    addCategoryObj.click(function () {
        var currentBtn = $(this);
        layer.open({
            type: 2,
            title:'新增分类',
            skin: 'layui-layer-rim', //加上边框
            area: ['400px', '250px'], //宽高
            btn: ['确定', '取消'],
            content: "../../templates/news_category_add.html",
            yes:function (index, layero) {
             var body = layer.getChildFrame('body',index);//建立父子联系
             // var iframeWin = window[layero.find('iframe')[0]['name']];
             var forms = body.find('form');
             csrfajax.post({
                 'url':'/adminlte/news_category/',
                 'data':forms.serialize(),
                 'success':function (result) {
                     if(result['code']===200){
                         layer.msg('ok', {icon: 1});
                         layer.close(index);
                         window.location.reload();
                     }else{
                         layer.msg('error', {icon: 2});
                     }
                 }
             });

            },
            btn2:function (index, layero) {
                layer.close(index);
            }
        });
    });
};



NewCategory.prototype.listenEditCategory = function(){
  var self = this;
  var editCategoryObj = $('.edit_category');
    editCategoryObj.on('click',function () {
      var currentBtn = $(this);
       var categoryId = currentBtn.parent().parent().attr("data-pk");
       var view_url = "../../adminlte/category_detail/".concat(categoryId)+'/';
      layer.open({
            type: 2,
            title:'编辑分类',
            skin: 'layui-layer-rim', //加上边框
            area: ['400px', '250px'], //宽高
            btn: ['确定', '取消'],
            content: view_url,
            yes:function (index, layero) {
             var body = layer.getChildFrame('body',index);//建立父子联系
             // var iframeWin = window[layero.find('iframe')[0]['name']];
             var forms = body.find('form');
             csrfajax.put({
                 'url':'/adminlte/news_category/',
                 'data':forms.serialize(),
                 'success':function (result) {
                     if(result['code']===200){
                         layer.msg('ok', {icon: 1});
                         layer.close(index);
                         window.location.reload();
                     }else{
                         layer.msg('error', {icon: 2});
                     }
                 }
             });

            },
            btn2:function (index, layero) {
                layer.close(index);
            }
        },function () {

      });
  });

};

$(function () {
    var newCategory = new NewCategory();
    newCategory.run();
});