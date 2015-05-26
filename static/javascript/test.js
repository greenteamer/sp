// An example Backbone application contributed by
// [Jérôme Gravel-Niquet](http://jgn.me/). This demo uses a simple
// [LocalStorage adapter](backbone.localstorage.html)
// to persist Backbone models within your browser.

// Load the application once the DOM is ready, using `jQuery.ready`:
var app = app || {};

$(function(){

    // app.Notices = Backbone.Model.extend({
    //     name: 'name',
    //     description: 'description',
    //     choice: 'all',
    //     initialize: function() {
    //         console.log(this.get('notice'));
    //     },
    //     urlRoot : function(){
    //         return '/api/v1/notice/';
    //     }
    // });

    // app.NoticeCollection = Backbone.Collection.extend({
    //     model: app.Notices,
    //     url : '/api/v1/notice/'
    // });

    // var collention = new app.NoticeCollection;
    // var notices = collention.fetch();



    app.MyObject = Backbone.Model.extend({
        default: {
            name: 'name',
            description: 'description',
            size: 100
        },
        initialize: function(){
            console.log("object created");
            this.on('change', function(){
                $('#log').html("object changed");
                var json = app.newObj.changed;
                console.log(json);
                $('#notice').html(app.newObj.get('size'));
            });
        },
        increaseSize: function(){
            app.newObj.set({
                size: this.get('size') + 100
            });
        },
        changeName: function(new_name){
            app.newObj.set({
                name: new_name
            });
        }
    });

    app.newObj =  new app.MyObject({
        name: "rocket",
        description: "super rocket"
    });

    app.newObj.set({
        size: 250,
        type: 'active'
    });

    $('.btn').on('click', function(){
        app.newObj.increaseSize();
        var n = $('#notice').html();
        console.log(n);
        app.newObj.changeName(n);
    });

    //var object = {};
    //
    //_.extend(object, Backbone.Events);
    //
    //object.on("alert", function(msg) {
    //    alert("Сработало " + msg);
    //});
    //
    //object.on("alert", function(msg){
    //   console.log("вот и пироги такие!" + msg);
    //});
    //
    //object.trigger("alert", "событие");
    //
    //$('.btn').on('click', function(){
    //    object.trigger("alert", "clicked");
    //});

});