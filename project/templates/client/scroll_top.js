$(document).ready(function() {
    $.material.init();
    var width = $(window).width();
    $(window).scroll(function() {
        // фиксируем основное меню при скроле
        var bool = false;
        var top = $(document).scrollTop();
        if (top < 50) {
            $(".scroll-class").css({
                position: "fixed",
                top:"0px",
                left:0,
                zIndex:"10"
            });
            $(".scroll-class #main-menu").css({
                padding: "0"
            });
            $(".main-menu-container").addClass('container');
            $("#cartmenu").css({
                marginRight: "-7px",
                position: "absolute",
                top: "4px",
                right: "12px",
                zIndex: 888,
                color: "#333"
            });
            $(".mobile #cartmenu").css({
                marginRight: "-7px",
                position: "absolute",
                top: "48px",
                right: "22px",
                left: "initial",
                zIndex: 888,
                color: "#333"
            });
        } else if (top >= 150) {
            $(".scroll-class").css({
                position: "fixed",
                top: "-109px",
                left:0 ,
                zIndex:"10",
                width: "100%"
            });
            $(".scroll-class #main-menu").css({
                padding: "0 15px"
            });
            $(".mobile .scroll-class").css({position: "fixed", top: "-109px", left:0 , zIndex:"10", width: "100%"});
            $(".main-menu-container").removeClass('container');
            $("#cartmenu").css({
                marginRight: "-7px",
                position: "absolute",
                top: "67px",
                right: "28px",
                zIndex: 888,
                color: "#fff"
            });
            $(".mobile #cartmenu").css({
                marginRight: "-7px",
                position: "absolute",
                top: "105px",
                left: "28px",
                right: "initial",
                zIndex: 888,
                color: "#fff"
            });
        }
    });
});
