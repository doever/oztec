//处理导航条事件
function FrontBase() {
     this.authBox = $('.auth-box');
     this.userMoreBox = $('.user-more-box');
}

FrontBase.prototype.run = function () {
    this.listenAuthBoxHover();
};

FrontBase.prototype.listenAuthBoxHover = function(){
    var self = this;
    self.authBox.hover(function () {
        self.userMoreBox.show();
    },function () {
        self.userMoreBox.hide();
    })
};



//处理登录相关功能
function getStyle(obj,name){
    if(obj.currentStyle){
        return obj.currentStyle[name];
    }
    else{
        return getComputedStyle(obj,false)[name];
    }
}

function  Auth() {
    var self = this;
    self.maskWrapper = $(".mask-wrapper");
    self.signInBtn = $(".signin-btn");
    self.signUpBtn = $(".signup-btn");
    self.closeBtn = $(".close-btn");
    self.authBox = $(".auth-inner-group");
    self.smsCaptchaBtn = $(".sms-captcha-btn");
}
Auth.prototype.run = function () {
    this.listenCloseEvent();
    this.listenAuthBoxClickEvent();
    this.listenSwitchEvent();
    this.listenSignIn();
    this.listenSignUp();
    this.listenImgCaptchaEvent();
    this.listenSmsCaptchaEvent();
};

Auth.prototype.listenAuthBoxClickEvent = function(){
    var self = this;
    self.signInBtn.click(function () {
        self.authBox.css({"left":0});
        self.showEvent();
    });
    self.signUpBtn.click(function () {
        self.authBox.css({"left":-400});
        self.showEvent();
    })
};

Auth.prototype.showEvent = function(){
  var self = this;
  self.maskWrapper.show();
};
Auth.prototype.hiddenEvent = function(){
    var self = this;
    self.maskWrapper.hide();
};

Auth.prototype.listenCloseEvent = function(){
    var self = this;
    self.closeBtn.click(
        function () {
            self.hiddenEvent();
        }
    );
};
Auth.prototype.listenSwitchEvent = function(){
    var self = this;
    var switchBtn = $(".switch");
    switchBtn.click(function () {
    var current_width = parseInt(getStyle(self.authBox[0],"left"));
    if(current_width>=0){
        self.authBox.animate({"left":"-400px"});
    }
    else{
        self.authBox.animate({"left":0});
    }
});
};

Auth.prototype.listenSignIn = function(){
    var self = this;
    var loginBtn =  $(".signin-group").find(".submit-btn");
    loginBtn.click(function () {
        var telephone = $(".signin-group").find('input[name="telephone"]').val();
        var password = $(".signin-group").find('input[name="password"]').val();
        var remember = $(".signin-group").find('input[name="remember"]').prop("checked");
        remember = remember?1:0;
        csrfajax.post({
            'url':'/account/login/',
            'data':{
                'telephone':telephone,
                'password':password,
                'remember':remember
            },
            'success':function (result) {
                if(result['code']===200){
                    self.hiddenEvent();
                    window.location.reload();
                }else{
                    var messageObj = result['message'];
                    if(typeof messageObj =='string' || messageObj.constructor == String){
                        window.messageBox.show(messageObj);
                    }else{
                        // {'password':['xxx','sss']}
                        for(var key in messageObj){
                            var messages = messageObj[key];
                            var message = messages[0];
                            window.messageBox.show(message);
                        }
                    }
                }

            },
            'error':function (error) {
                console.log(error);
            }
        })
    })
};

Auth.prototype.listenSignUp = function (){
    var self =this;
    var signupInput = $('.signup-group').find('.submit-btn');
    signupInput.click(function (event) {
        event.preventDefault();
        var telephone = $('.signup-group input[name=telephone]').val();
        var username = $('.signup-group input[name=username]').val();
        var img_captcha = $('.signup-group input[name=img_captcha]').val();
        var password = $('.signup-group input[name=password]').val();
        var re_password = $('.signup-group input[name=re_password]').val();
        var sms_captcha = $('.signup-group input[name=sms_captcha]').val();
        csrfajax.post({
            'url':'/account/register/',
            'data':{
                'telephone':telephone,
                'username':username,
                'img_captcha':img_captcha,
                'password':password,
                're_password':re_password,
                'sms_captcha':sms_captcha
            },
            'success':function (result) {
                if(result['code']===200){
                    console.log(result);
                    self.hiddenEvent();
                    window.location.reload();
                }else{
                    var messageObj = result['message'];
                    if(typeof messageObj =='string' || messageObj.constructor == String){
                        window.messageBox.show(messageObj);
                    }else{
                        // {'password':['xxx','sss']}
                        for(var key in messageObj){
                            var messages = messageObj[key];
                            var message = messages[0];
                            window.messageBox.show(message);
                        }
                    }
                }

            },
            'error':function (error) {
                window.alert('服务器错误')
            }
        })
    })
};

Auth.prototype.listenImgCaptchaEvent = function(){
    var self = this;
    var captchaObj = $('.img-captcha');
    captchaObj.click(function () {
        $(this).attr({"src":"/account/img_captcha?random"+Math.random()})
    })
};

Auth.prototype.listenSmsCaptchaEvent = function(){
    var self = this;
    // console.log($(".signup-group input[name='telephone']"));
    var telephoneInput = $(".signup-group input[name='telephone']");
    // console.log($(".signup-group input[name='telephone']")[0]);
    // var telephone = $(".signup-group input[name='telephone']")[0].val();
    self.smsCaptchaBtn.click(function () {
        var telephone = telephoneInput.val();
        if(/^1\d{10}$/.test(telephone)){
            csrfajax.get({
                'url':'/account/sms_code/',
                'data':{
                    'telephone':telephone
                },
                'success':function (result) {
                    if(result['code']===200){
                        window.messageBox.showSuccess('短信发送成功');
                        self.smsCaptchaBtn.addClass('disabled');
                        self.smsCaptchaBtn.text('60s');
                        var count = 59;
                        var timer = setInterval(function () {
                            self.smsCaptchaBtn.unbind('click');
                            self.smsCaptchaBtn.text(count+'s');
                            count-=1;
                            if(count<=0){
                                self.smsCaptchaBtn.removeClass('disabled');
                                self.smsCaptchaBtn.text("发送短信");
                                clearInterval(timer);
                                self.listenSmsCaptchaEvent();
                            }
                        },1000)
                    }

                },
                'fail':function (error) {
                    console.log(error);
                }
            })
        }else if(!telephone){
            console.log(telephone);
            window.messageBox.showInfo("请输入手机号");
        }else{
            window.messageBox.showError("请输入合法的手机号啊");
        }
    })
};

$(function () {
   var auth = new Auth();
   auth.run();
   var frontBase = new FrontBase();
   frontBase.run();
});


// 前端模板arttemplates的过滤器,写法类似django模板过滤器
$(function () {
    if(template){
        template.defaults.imports.timeSince = function (dataValue) {
        var date = new Date(dataValue);
        var datets = date.getTime();
        var now = (new Date()).getTime();
        var timestamp = (now-datets)/1000;
        if(timestamp<60){
            return '刚刚';
        }else if(timestamp>=60 && timestamp<60*60){
            minutes = parseInt(timestamp/60);
            return minutes+'分钟前';
        }else if(timestamp>=60*60 && timestamp<60*60*24){
            hours = parseInt(timestamp/60/60);
            return hours+'小时前';
        }else if(timestamp>=60*60*24 && timestamp<60*60*24*30){
            days = parseInt(timestamp/60/60/24);
            return days+'天前';
        }else{
            var year = date.getFullYear();
            var mouth = date.getMonth();
            var day = date.getDay();
            var hour = date.getHours();
            var minute = date.getMinutes();
            var second = date.getSeconds();
            return year+'-'+mouth+'-'+day+' '+hour+':'+minute+':'+second;
        }
    }
    }
});