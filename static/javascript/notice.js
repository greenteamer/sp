
// (function(){

    var NoticeModel = Backbone.Model.extend({
        //initialize: function() {
        //},
        //urlRoot : function(){
        //    return '/api/v1/notice/';
        //}
    });


    var NoticeCollection = Backbone.Collection.extend({
        model: NoticeModel,
        url : '/api/v1/notice/'
    });


    var collection = new NoticeCollection;

    collection.fetch({
        success: function(){
            console.log(collection.models);
        }
    });


    var NoticeDetailView = Backbone.View.extend({ 
        tagName : 'div',
        initialize : function(model, options){
            this.options = options
        },
        events : {
        },
        template : _.template("<div>notice name: <%- name %> s</div>"),
        render : function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });


    var NoticeListView = Backbone.View.extend({ 
        el : "#my-model-list",
        initialize : function(options){
            this.listenTo(collection, 'reset', this.addAll, this);
        },
        addOne : function(model) {
            var view = new NoticeDetailView ({ model : model })
            console.log( view.render().el )
            $("#notice_list").append(view.render().el)
        },
        addAll : function(){    
            var that = this;
            collection.each(function(model){
                that.addOne(model);
            });
        },
        render : function() {
            $("#log").html(this.template());
            return this;
        }
    });


    // var note = new Notice({'id': 1});    
    // note = note.fetch({
    //     success: function(){            
    //         note = note.toJSON();
    //         alert(note['description']);
    //     }
    // });

    // _(note.attributes.objects).each(function(obj){
    //     console.log('получен');
    // });


    // var NoticeCollection = Backbone.Collection.extend({
    //     model: Notice,
    //     url : '/api/v1/notice/',
    //     initialize: function(){
    //         // console.log(this);
    //     }
    // });

    // var myCol = new NoticeCollection();
    // myCol = myCol.fetch();

    // console.log(myCol.models);

    // myCol.forEach(function(model){
    //     console.log(model.get('name'));
    // });




    

    // myCol = myCol.fetch();
    // myCol = myCol.toJSON;
    // console.log(myCol);


    // var Controller = Backbone.Router.extend({
    //     routes: {
    //         "": "start", // Пустой hash-тэг
    //         "success": "start"
    //     },

    //     start: function () {
    //         $(".game").hide(); // Прячем все блоки
    //         $("#notice").show(); // Показываем нужный
    //     },

    //     success: function () {
    //         $("#notice").hide();
    //         $(".game").show();
    //     }

    // });


    // var controller = new Controller(); // Создаём контроллер

    // Backbone.history.start();  // Запускаем HTML5 History push

// })();





//var ListNoticesItem = Backbone.View.extend({
//    tagName : 'div',
//    id: 'notice',
//    events: {},
//    template: _.template('<div>Тема: <% name %></div>'),
//    render: function(){
//        this.$el.html(this.template(this.model.toJSON()));
//        return this;
//    }
//});
//
//var ListNotices = Backbone.View.extend({
//    //el: '#notice_list',
//    tagName : 'div',
//    id: 'notice_list',
//    initialize: function(options){
//        this.listenTo(Notices, 'reset', this.addAll, this);
//    },
//    addOne: function(model){
//        var view = new ListNoticesItem ({model: model});
//        console.log(view.render().el);
//        this.$el.append(view.render().el);
//    },
//    addAll: function(){
//        var that = this;
//        Notices.each(function(model){
//            that.addOne(model);
//        })
//    },
//    render: function(){
//        this.$el.html(this.template());
//        return this;
//    }
//});


//var item = new ListNoticesItem;
//var items = new ListNotices;




