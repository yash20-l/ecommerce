$(document).ready(function () {
	console.log('hello')
	$("#loadMore").on('click', function () {
		var _currentProducts = $(".product-box").length;
		var _limit = $(this).attr('data-limit');
		var _total = $(this).attr('data-total');
		// Start Ajax
		$.ajax({
			url: '/load-more-data',
			data: {
				limit: _limit,
				offset: _currentProducts
			},
			dataType: 'json',
			beforeSend: function () {
				$("#loadMore").attr('disabled', true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success: function (res) {
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled', false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing = $(".product-box").length;
				if (_totalShowing == _total) {
					$("#loadMore").remove();
				}
			}
		});
		// End
	});
	let price = null
	const regulatePrice = (slug, color_id, size_id) => {
		const payload = {
			slug: slug,
			color_id: color_id,
			size_id: size_id
		}
		$.ajax({
			url: '/api/getprodprice',
			type: 'POST',

			data: JSON.stringify({ payload: payload }),
			dataType: 'json',
			// beforeSend: function () {
			// 	$("#loadMore").attr('disabled', true);
			// 	$(".load-more-icon").addClass('fa-spin');
			// },
			success: function (res) {
				price = res
				$(".product-price").text('$'+res)
			}
		});

	}


	// Product Variation
	$(".choose-size").hide();

	let color = null
	let size = null


	// Show size according to selected color
	$(".choose-color").on('click', function () {
		var _color = $(this).attr('data-color');
		var _color_code = $(this).attr('data-color-code')
		var _color_text = $(this).attr('data-color-text')
		$(".color-box").css('background-color', `${_color_code}`)
		$(".color-text").text(`${_color_text}`)
		var _slug = $(".slug-h1").text()
		$(".choose-size").hide();
		$(".color" + _color).show();
		$(".color" + _color).first().addClass('active');
		$(".postselection-row").toggleClass('d-none');
		$(".length-default").text()
		color = _color
		regulatePrice(_slug, color, size)
		// var _price = $(".color" + _color).first().attr('data-price');

	});
	// End

	$(".length-select").on('click', () => {
		$(".length-options-name").toggleClass('d-none')
	})


	// Show the price according to selected size
	$(".choose-size").on('click', function () {
		var _selected_length = $(this).attr('data-selected-length')
		$(".choose-sizes-default").text(`${_selected_length}`)
		$(".choose-size").removeClass('active');
		$(".length-options-name").toggleClass('d-none')
		$(this).addClass('active');
		var _slug = $(".slug-h1").text()
		size = $(this).attr('data-length-id');
		regulatePrice(_slug, color, size)
	})
	// End

	// Show the first selected color
	$(".choose-color").first().addClass('focused');
	var _color = $(".choose-color").first().attr('data-color');
	var _length = $(".choose-sizes-default").attr("data-size-id")
	color = _color
	size = _length
	// var _price = $(".choose-size").first().attr('data-price');
	var _slug = $(".slug-h1").text()
	regulatePrice(_slug, color, size)

	$(".color" + _color).show();
	$(".color" + _color).first().addClass('active');

	// Add to cart
	$('.add-to-cart').on('click', function () {
		var _vm = $(this);
		var _index = _vm.attr('data-index');
		var _qty = $(".product-qty-" + _index).val();
		var _productId = $(".product-id-" + _index).val();
		var _productImage = $(".product-image-" + _index).val();
		var _productTitle = $(".product-title-" + _index).val();
		var _productPrice = $(".product-price-" + _index).text();
		var _color = color
		var _length = size
		payload = {
			'prod_id': _productId,
			'qty': _qty,
			'price': _productPrice,
			'color' : _color,
			'size' : _length
		}
		// Ajax
		$.ajax({
			url: '/add-to-cart',
			type : 'POST',	
			data: JSON.stringify({payload : payload}),
			dataType: 'json',
			beforeSend: function () {
				_vm.attr('disabled', true);
			},
			success: function (res) {
				$(".cart-list").text(res.totalitems);
				if (res.message == 'success'){
					$(".cart-list").text(parseInt($(".cart-list").text()) + 1)
				}else{
					window.location.replace('/login')
				}
				_vm.attr('disabled', false);
			}
		});
		// End
	});
	// End

	// Update item from cart
	$(document).on('click', '.update-item', function () {
		var _pId = $(this).attr('data-item');
		var _pQty = $(".product-qty-" + _pId).val();
		var _vm = $(this);
		// Ajax
		$.ajax({
			url: '/update-cart',
			data: {
				'id': _pId,
				'qty': _pQty
			},
			dataType: 'json',
			beforeSend: function () {
				_vm.attr('disabled', true);
			},
			success: function (res) {
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled', false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});


	// Activate selected address
	$(document).on('click', '.activate-address', function () {
		var _aId = $(this).attr('data-address');
		var _vm = $(this);
		// Ajax
		$.ajax({
			url: '/activate-address',
			data: {
				'id': _aId,
			},
			dataType: 'json',
			success: function (res) {
				if (res.bool == true) {
					$(".address").removeClass('shadow border-secondary');
					$(".address" + _aId).addClass('shadow border-secondary');

					$(".check").hide();
					$(".actbtn").show();

					$(".check" + _aId).show();
					$(".btn" + _aId).hide();
				}
			}
		});
		// End
	});

});
// End Document.Ready
