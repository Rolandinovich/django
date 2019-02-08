        $.ajax({
            url: "/get_user_content_ajax/",

            success: function (data) {
                console.log(data);
                $('.top-cart').html(data.top_cart);
                $('.link').html(data.user_menu);
            },
        });
