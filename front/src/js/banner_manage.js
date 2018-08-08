function BannerManage() {
    this.addBannerBtn = $("#add-banner");
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
                 'url':'/adminlte/add_banner/',
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

BannerManage.prototype.run = function(){
    var self = this;
    self.listenAddNewBanner()
};

$(function () {
   var  bannerManage = new BannerManage();
   bannerManage.run()
});