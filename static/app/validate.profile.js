(function ($) {
	$(document).ready(function () {
		// $('input').iCheck().on('ifChecked', function(){
		// 	console.log('okokok');
		// });

		// $('input').on('ifChecked', function(event){
		//   	console.log('checked');
		// 	$('input').iCheck('check');
		// });

		// $('input').on('ifUnchecked', function(event){
		//   	console.log('unchecked');
		// 	$('input').iCheck('uncheck');
		// });

		$("#populate-profile").validate({
			rules: {
				firstName: {
					required: true,
					minlength: 3	
				},
				lastName: {
					required: true,
					minlength: 4
				},
				email: {
					required: true,
					email: true					
				},
				phone: {
					required: true,
					number: true,
					minlength: 11,
					maxlength: 11					
				},
				address: {
					required: true,
					minlength: 5
				},
				city: {
					required: true,
					minlength: 3	
				},
				zipCode: {
					required: true,
					number: true,
					minlength: 6,
					maxlength: 6	
				},
				terms: {
					equalTo: 1
				}
			},
			messages: {
				firstName: {
					required: "Имя обязательно для заполнения",
					minlength: 'Имя должно быть не менее {0} символов'
				},
				lastName: {
					required: "Фамилия обязательна для заполнения",
					minlength: 'Фамилия должна быть не менее {0} символов'
				},
				email: {
					required: "email обязателен для заполнения",
					email: "Введите корректный email",
				},
				phone: {
					required: "Телефон обязателен для заполнения",
					number: "Введите корректный телефон",
					minlength: "Введите номер вашего телефона полностью",
					maxlength: "Номер телефона не должен превышать {0} символов"
				},
				address: {
					required: "Адрес обязателен для заполнения",
					minlength: "Адрес не должен быть меньше {0} симовол"
				},
				city: {
					required: "Город обязателен для заполнения",
					minlength: "Город не должен быть меньше {0} симовол"
				},
				zipCode: {
					required: "Индекс обязателен для заполнения",
					number: "Введите корректный индекс",
					minlength: "Введите Ваш индекс полностью",
					maxlength: "Индекс не должен превышать {0} символов"
				},
			},
			errorElement: "em"
		});

	});
})(jQuery);