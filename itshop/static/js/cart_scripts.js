window.onload = function () {
    $('.cart_list').on('click', 'input[type="number"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/cart/edit/" + t_href.name + "/" + t_href.value + "/",

            success: function (data) {
                $('.cart_list').html(data.result);
            },
        });

        event.preventDefault();
    });
}
