function get_form_serialize(form_name) {
    let $data = {};
    $(form_name).find('input, textarea, select, switch').each(function () {
        let b = $(this)
        if (b.attr('type') === 'checkbox')
            $data[b.attr('name')] = b.is(':checked');
        else
            $data[b.attr('name')] = b.val();
    })
    return $data
}
