window.onload = function() {
    var _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_price, prev_price, prev_orderitem_num, _quantity_rest;
    var _quantity_rest_str, _price_str;
    var quantity_arr = [];
    var price_arr = [];
    var quantity_rest_arr = [];

    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    var order_total_price = parseFloat($('.order_total_price').text().replace(',', '.')) || 0;

    for(var i = 0; i < TOTAL_FORMS; i++){
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.').replace(' руб.', ''));
        _quantity_rest = parseInt($('.orderitems-' + i + '-quantity_rest').text().replace(' шт.', ''));

        quantity_arr[i] = _quantity;
        price_arr[i] = _price ? _price : 0;
        quantity_rest_arr[i] = _quantity_rest ? _quantity_rest : 0;
    }

    if (!order_total_quantity){
        for(var i = 0; i < TOTAL_FORMS; i++){
            order_total_quantity += quantity_arr[i];
            order_total_price += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_price').html(Number(order_total_price.toFixed(2)).toString());
    }
    $('.order_form').on('change', 'input[type="number"]', function() {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);

            quantity_rest_arr[orderitem_num] -= delta_quantity;
            _quantity_rest_str = quantity_rest_arr[orderitem_num].toString() + ' шт.'
            $('.orderitems-'+orderitem_num+'-quantity_rest').html(_quantity_rest_str);
         }
    });
//    $('.order_form').on('click', 'input[type="checkbox"]', function() {
//        var target = event.target;
//        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
//        delta_quantity = target.checked ? -quantity_arr[orderitem_num] : quantity_arr[orderitem_num];
//        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
//    });

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_price = orderitem_price * delta_quantity;
        order_total_quantity = order_total_quantity + delta_quantity;
        order_total_price = Number((order_total_price + delta_price).toFixed(2));

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_price').html(order_total_price.toString());
    };

    function orderProductUpdate(from_price, to_price, quantity) {
        console.log("order_total_price  " + order_total_price);
        if (quantity) {
            delta_price = (to_price - from_price) * quantity;
        }
        else {
            delta_price = 0;
        }
        order_total_price = Number((order_total_price + delta_price).toFixed(2));
        console.log(order_total_price);
        $('.order_total_price').html(order_total_price.toString());
    }

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-DELETE', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);

//        row[0].className += ' order_deleted';

    }

    function addOrderItem(row) {
        let target_row = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_row.replace('orderitems-', '').replace('-DELETE', ''));

//        let target_column = row[0].querySelector('.td3');
//        $('<span class="orderitems-'+orderitem_num+'-price"></span>').appendTo(target_column);
        let target_price = row[0].querySelector('.td3 > span');
        target_price.className = 'orderitems-'+orderitem_num+'-price';

        let target_quantity_rest = row[0].querySelector('.td4 > span');
        target_quantity_rest.className = 'orderitems-'+orderitem_num+'-quantity_rest';

        price_arr[orderitem_num] = 0;
        quantity_arr[orderitem_num] = 0;
        quantity_rest_arr[orderitem_num] = 0;

        let target_input = $('#id_orderitems-'+orderitem_num+'-quantity')
        target_input.val(0);
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
        added: addOrderItem
    });

    $('.order_form input[type="number"]').each(function(orderitem_num) {
        if (price_arr[orderitem_num]) {
            $( this ).attr({"max": (quantity_rest_arr[orderitem_num] + quantity_arr[orderitem_num]).toString()});
        }
    });

    $('.order_form').on('click', 'select', function() {
        let target = event.target;
        prev_orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        if (!price_arr[prev_orderitem_num]) {
            price_arr[prev_orderitem_num] = 0;
        }
        prev_price = price_arr[prev_orderitem_num];
    });

    $('.order_form').on('change', 'select', function() {
        let target = event.target;

        if (target) {
             $.ajax({
                url: "/orders/product/" + target.value + "/price/quantity/",

                success: function (data) {
                    orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
                    if (orderitem_num == prev_orderitem_num){
                        _price_str = (Number(data.price).toFixed(2)).toString() + " руб.";
                        $('.orderitems-'+orderitem_num+'-price').html(_price_str);
                        price_arr[orderitem_num] = Number(data.price).toFixed(2);
                        orderProductUpdate(prev_price, price_arr[orderitem_num], quantity_arr[orderitem_num]);

                        quantity_rest_arr[orderitem_num] = Number(data.quantity);
                        _quantity_rest_str = (data.quantity).toString() + " шт.";
                        $('.orderitems-'+orderitem_num+'-quantity_rest').html(_quantity_rest_str);
                        $('#id_orderitems-'+orderitem_num+'-quantity').attr({"max": (quantity_rest_arr[orderitem_num] + quantity_arr[orderitem_num]).toString()});
                    }
                },
             });
         }
    });
};