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
}
Auth.prototype.run = function () {
    this.listenCloseEvent();
    this.listenAuthClickEnevt();
    this.listenSwitchEvent();
    this.listenSignIn();
};

Auth.prototype.listenAuthClickEnevt = function(){
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
            'fail':function (error) {
                console.log(error);
            }
        })
    })
};

$(function () {
    var auth = new Auth();
    auth.run();
});