// Компонент принимает condition
// Если condition не false и не undefined компонент возвращает свой children компонент
// Используется для упрощения логики внутри компонентов что бы не писать безконечные if

// Пример использования: 
// <IF condition={condition == true}>
//     <PurchaseListView key={item.id} purchase={item}/>
// </IF>

// Можно использовать как:
// <IF condition={condition}>
//     <PurchaseListView key={item.id} purchase={item}/>
// </IF>

// В обоих примерах возвращает компонент <PurchaseListView key={key} item={item}/>

var React = require('react');


var IF = React.createClass({
	render: function  () {
		if (this.props.condition) {
			return this.props.children;
		} else {
			return false;
		}
	}
});


module.exports = IF;