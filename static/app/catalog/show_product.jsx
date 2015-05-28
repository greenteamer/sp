// рендерим PRODUCT в категории для показа в МОДАЛЬНОМ окне


(function (window){

    // работаем с данными
    var ProductApp = window.ProductApp;
    // var collection = new PostApp.Collections.Post();
    var collection = [];

    $('#modal_callback').click(function(){
            
		ProductApp.Views.Product = React.createClass({
			render: function () {
				return (
					<div id="complete-dialog" className="modal fade" tabIndex="-1">
		              <div className="modal-dialog">
		                <div className="modal-content">
		                  <div className="modal-header">
		                    <button type="button" className="close" data-dismiss="modal" aria-hidden="true">×</button>
		                    <h4 className="modal-title">Dialog</h4>
		                  </div>
		                  <div className="modal-body">
		                    <input ref="input" id="input_content" type="text" className="form-control" placeholder="label" />
		                  </div>
		                  <div className="modal-footer">
		                    <button className="btn btn-primary" data-dismiss="modal" >Dismiss</button>
		                    <button className="btn btn-primary" onClick={this.addPost} data-dismiss="modal">Save</button>
		                  </div>
		                </div>
		              </div>
		            </div>
				)
			}
		});
	});

	React.render(<ProductApp.Views.Product/>, document.getElementById('modal_product'));

    window.ProductApp = ProductApp;

 })(window);