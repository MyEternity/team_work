$(function () {
    $('#id_birthday').datepicker({ dateFormat: 'yy-mm-dd' }).attr('autocomplete', 'off');
});

$(document).ready(function () {
    $('#id_phone_number').usPhoneFormat({
        format: '(xxx) xxx-xxxx',
    });
});
