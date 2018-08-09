function BannerManage() {
    this.addBannerBtn = $("#add-banner");
    this.deleteBannerBtn = $(".banner-close-btn");
    this.editBannerBtn = $(".edit-banner-btn");
}

BannerManage.prototype.listenAddNewBanner = function () {
    var self = this;
    self.addBannerBtn.click(function () {
        layer.open({
            type: 2,
            title:'新增轮播图',
            skin: 'layui-layer-rim', //加上边框
            area: ['600px', '400px'], //宽高
            btn: ['确定', '取消'],
            content: "../../templates/add_banner.html",
            yes:function (index, layero) {
             var body = layer.getChildFrame('body',index);//建立父子联系
             var forms = body.find('form');
             // var forms = $("#add-banner-form");
             csrfajax.post({
                 'url':'/adminlte/banner_list/',
                 'data':forms.serialize(),
                 'success':function (result) {
                     if(result['code']===200){
                         layer.close(index);
                         layer.msg('ok', {icon: 1,time:1000});
                         window.location.reload();
                     }else{
                         layer.msg('error', {icon: 2,time:1000});
                     }
                 }
             });

            },
            btn2:function (index, layero) {
                layer.close(index);
            }
        });
    })
};

BannerManage.prototype.listerDeleteBanner = function(){
  var self = this;
  // var bannerId = $(".banner-close-btn");
  self.deleteBannerBtn.click(function () {
      var currentBtn = $(this);
      var bannerId = currentBtn.parent().parent().attr("data-pk");
      layer.confirm('确定删除?', {
                            btn: ['确定', '取消'],
                            btn2: function (index, layero)
                                {
                                    layer.close();
                                }
                            }, function (index, layero) {
                                csrfajax.delete({
                                    'url': '/adminlte/banner/'+bannerId+'/',
                                    'data':{},
                                    'success': function(result){
                                        if(result['code']===200){
                                            layer.close();
                                            layer.msg('删除成功',{icon: 1,time: 1000});
                                            window.location.reload();
                                        }else{
                                            layer.msg(result['message'], {icon: 2, time:1000});
                                        }
                                    },
                                    'fail': function (error) {
                                        layer.msg('服务器内部错误', {icon:2, time:1000});
                                    }
                                })
                            })
                        })
};

BannerManage.prototype.listenEditBanner = function(){
      var self = this;
      self.editBannerBtn.click(function () {
          var currentBtn = $(this);
          var bannerId = currentBtn.parent().parent().attr("data-pk");
          var formGroup = currentBtn.parent().siblings().eq(1).children().eq(1);
          // console.log(formGroup);
          var positionInput = formGroup.find("input[name=position]");
          var linkUrlInput = formGroup.find("input[name=link_url]");
          var position = positionInput.val();
          var linkUrl = linkUrlInput.val();
          console.log('position:'+position, 'linkUrl:'+linkUrl);
          csrfajax.put({
              'url': '/adminlte/banner/'+bannerId+'/',
              'data':{
                  'position': position,
                  'link_url': linkUrl
              },
              'success': function (result) {
                  if(result['code']===200){
                      layer.msg('保存成功', {icon:1, time:1000});
                      window.location.reload();
                  }else{
                      layer.msg(result['message'], {icon:2, time:1000});
                  }
              },
              'fail': function (error) {
                  layer.msg('服务器内部错误', {icon:2, time:1000});
              }
          })
      })
};

BannerManage.prototype.run = function(){
    var self = this;
    self.listenAddNewBanner();
    self.listerDeleteBanner();
    self.listenEditBanner();
};

$(function () {
   var  bannerManage = new BannerManage();
   bannerManage.run()
});