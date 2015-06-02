// рендерим PRODUCT в категории для показа в МОДАЛЬНОМ окне


(function (window){

    // работаем с данными
    var ProductApp = window.ProductApp;
    // var collection = new PostApp.Collections.Post();
    var collection = [];

    $('#modal_callback').click(function(){
            
		ProductApp.Views.Product = React.createClass({displayName: "Product",
			render: function () {
				return (
					React.createElement("div", {id: "complete-dialog", className: "modal fade", tabIndex: "-1"}, 
		              React.createElement("div", {className: "modal-dialog"}, 
		                React.createElement("div", {className: "modal-content"}, 
		                  React.createElement("div", {className: "modal-header"}, 
		                    React.createElement("button", {type: "button", className: "close", "data-dismiss": "modal", "aria-hidden": "true"}, "×"), 
		                    React.createElement("h4", {className: "modal-title"}, "Dialog")
		                  ), 
		                  React.createElement("div", {className: "modal-body"}, 
		                    React.createElement("input", {ref: "input", id: "input_content", type: "text", className: "form-control", placeholder: "label"})
		                  ), 
		                  React.createElement("div", {className: "modal-footer"}, 
		                    React.createElement("button", {className: "btn btn-primary", "data-dismiss": "modal"}, "Dismiss"), 
		                    React.createElement("button", {className: "btn btn-primary", onClick: this.addPost, "data-dismiss": "modal"}, "Save")
		                  )
		                )
		              )
		            )
				)
			}
		});
	});

	React.render(React.createElement(ProductApp.Views.Product, null), document.getElementById('modal_product'));

    window.ProductApp = ProductApp;

 })(window);