(function (){

	var Rectangle = Backbone.Model.extend({
	    prop: '1'
	});   
    
    
    
    // просто для примера
    // var v1 = new Rectangle();
    // var v2 = new Rectangle();
    // v2.prop = 'one';
    // console.log(v1.prop);
    // console.log(v2.prop);

    


	var RectangleView = Backbone.View.extend({

		tagName: 'div',

		className: 'rectangle',
        
        events: {
            'click': 'move'
        },

		render: function(){
			this.setDimensions();
			this.setPosition();
            this.setColor();
			return this;
		},

		setDimensions: function (){
			this.$el.css({
				width: this.model.get('width') + 'px',
				height: this.model.get('height') + 'px'
			});
		},

		setPosition: function (){
			var position = this.model.get('position');
			this.$el.css({
				left: position.x,
				top: position.y
			});
		},

        setColor: function(){
            this.$el.css('background-color', this.model.get('color'));
        },
        
        move: function(){
            this.$el.css('left', this.$el.position().left + 10);
            console.log('есть');
        }

	});

	var models = [
        new Rectangle({
    		width: 200,
    		height: 60,
    		position: {
    			x: 300,
    			y: 150
    		},
            color: 'red'
    	}),
        new Rectangle({
    		width: 100,
    		height: 60,
    		position: {
    			x: 600,
    			y: 150
    		},
            color: 'green'
    	}),
        new Rectangle({
    		width: 100,
    		height: 60,
    		position: {
    			x: 300,
    			y: 350
    		},
            color: 'blue'
    	}),
    ];
    
    _(models).each(function (model){
        $('div#convas').append(new RectangleView({model: model}).render().el);
    });

    // var myView = new RectangleView({
    //     model: myRectangle
    // });


})();