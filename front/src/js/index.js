//轮播图
function Banner() {
    this.bannerWidth = 798;
    this.bannerGroup = $("#banner-group");
    this.index=1;
    this.leftArrow = $(".left-arrow");
    this.rightArrow = $(".right-arrow");
    this.bannerUl = $("#banner-ul");
    this.liList = this.bannerUl.children("li");
    this.bannerCount = this.liList.length;
    this.pageControl = $(".page-control");
}

//动态设置放置轮播图ul的宽度，防止写死
Banner.prototype.initBanner = function () {
    var self = this;
    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount-1).clone();
    self.bannerUl.append(firstBanner);
    self.bannerUl.prepend(lastBanner);
    self.bannerUl.css({"width":self.bannerWidth*(self.bannerCount+2),"left":-self.bannerWidth});
};

//动态添加圆点控制器
Banner.prototype.initPageControl = function () {
    var self = this;
    var pageControl = $(".page-control");
    for(var i=0;i<self.bannerCount;i++){
        var circle = $("<li></li>");
        pageControl.append(circle);
        if(i===0){
            circle.addClass("active");
        }
    }
    pageControl.css({"width":self.bannerCount*12+8*2+16*(self.bannerCount)});
};


Banner.prototype.toggleArrow = function (isShow) {
    var self = this;
    if(isShow){
        self.leftArrow.show();
        self.rightArrow.show();
    }
    else{
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};

Banner.prototype.animate = function () {
    var self = this;
    self.bannerUl.stop().animate({"left":-798*self.index},500);
    var index = self.index;
    if(index===0){
        index = self.bannerCount-1;
    }else if(index===self.bannerCount+1){
        index = 0;
    }else{
        index = self.index-1;
    }
    self.pageControl.children("li").eq(index).addClass("active").siblings().removeClass("active");
};

Banner.prototype.loop = function () {
    var self =this;
    self.timer = setInterval(function(){
        if(self.index>=self.bannerCount+1){
            self.bannerUl.css({"left":-self.bannerWidth});
            self.index=2;
        }
        else{
            self.index++;
        }
        self.animate();
    },2000);
};

//监听鼠标移入移出事件
Banner.prototype.listenBannerHover = function(){
    var self = this;
    this.bannerGroup.hover(function () {
        //鼠标移入事件
        clearInterval(self.timer);
        self.toggleArrow(true);
    },function () {
        //鼠标移出事件
        self.loop();
        self.toggleArrow(false);
    })
};


//监听箭头点击事件
Banner.prototype.listenArrowClick = function () {
    var self = this;
    self.leftArrow.click(function () {
        if(self.index===0){
            self.bannerUl.css({"left":-self.bannerCount*self.bannerWidth});
            self.index = self.bannerCount-1;
        }
        else{
            self.index--;
        }
        self.animate();
    });
    self.rightArrow.click(function () {
        if(self.index===self.bannerCount+1){
            self.bannerUl.css({"left":-self.bannerWidth});
            self.index = 2;
        }
        else{
            self.index++;
        }
        self.animate();
    });
};

//监听圆点点击事件
Banner.prototype.listenPageControl = function () {
    var self = this;
    self.pageControl.children("li").each(function (i,obj) {
        $(obj).click(function () {
            // self.pageControl.children("li").removeClass("active");
            self.index = i+1;
            self.animate();
            $(obj).addClass("active").siblings().removeClass("active");
        })
    })
};


Banner.prototype.run=function(){
    this.loop();
    this.initBanner();
    this.initPageControl();
    this.listenBannerHover();
    this.listenArrowClick();
    this.listenPageControl();
};

function Index(){
    this.page = 2;
    this.category = 0;
    this.ulObj = $('.list-inner-group');
    this.loadMoreBtn = $('#load-more-btn');
}

Index.prototype.ListenLoadMoreEvent = function(){
    var self = this;

    self.loadMoreBtn.click(function () {
        csrfajax.get({
            'url':'/news/news_list/',
            'data':{
                'page':self.page,
                'category':self.category
            },
            'success':function (result) {
                if(result['code']===200){
                    var news = result['data'];
                    if(news.length !== 0){
                        var tpl = template('more_news',{'news':news});
                        self.ulObj.append(tpl);
                        self.page+=1;
                    }else{
                        self.loadMoreBtn.hide();
                    }

                }
            }
        })
    })
};

Index.prototype.listenCategorySwitchEvent = function(){
    var self = this;
    var tabgroup = $(".list-tab li");
    tabgroup.click(function () {
        self.page = 1;
        var currentLi = $(this);
        var category = currentLi.attr("data-category");
        csrfajax.get({
            'url':'/news/news_list/',
            'data':{
                "page":self.page,
                "category":category
            },
            'success':function (result) {
                if(result['code']===200){
                    self.ulObj.empty();
                    var news = result['data'];
                    var tpl = template('more_news',{'news':news});
                    self.ulObj.append(tpl);
                    currentLi.addClass('active').siblings().removeClass('active');
                    self.page = 2;
                    self.category = category;
                    self.loadMoreBtn.show();
                }
            },
            'error':function (error) {
                console.log(error);
            }
        })
    })
};

Index.prototype.run = function(){
    var self = this;
    self.ListenLoadMoreEvent();
    self.listenCategorySwitchEvent()
};



$(function () {
    var banner = new Banner();
    banner.run();
    var index = new Index();
    index.run();
});