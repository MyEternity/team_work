window.onload = function () {

    $(document).on('click', '.btn_notification', function (event) {
        let t_href = event.target
        console.log(t_href)
        $.ajax(
            {
                url: "read/" + t_href.value + "/",
                type: "GET",
                dataType: "json",
                success: function (data) {
                    $('.notifications-table').html(data.result)
                },
                error: function (data){
                    console.log(data)
                }
            });
        event.preventDefault();
    });
}