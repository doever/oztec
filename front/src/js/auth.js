function getStyle(obj,name){
    if(obj.currentStyle){
        return obj.currentStyle[name];
    }
    else{
        return getComputedStyle(obj,false)[name];
    }
}
$(function () {
    $("#auth").click(function () {
        $(".mask-wrapper").show();
    });
    $(".close-btn").click(function () {
        $(".mask-wrapper").hide();
    });
});

$(function () {
    $(".switch").click(function () {
        var scrollWrapper = document.getElementsByClassName("auth-inner-group")[0];
        // console.log(scrollWrapper);
        var current_width = parseInt(getStyle(scrollWrapper,"left"));
        // console.log(current_width);
        if(current_width>=0){
            // $(scrollWrapper).animate({"left":"-400px"});
            $(".auth-inner-group").animate({"left":"-400px"});
        }
        else{
            // $(scrollWrapper).animate({"left":0});
            $(".auth-inner-group").animate({"left":0});
        }
    });
});