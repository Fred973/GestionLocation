$(function () {
    $('.commonInvoice').change(function () {
        if ($(this).is(':checked')) {
            $("div#selectField").hide();
            $("div#selectField").children().prop('disabled', true);
        } else {
            $("div#selectField").show();
            $("div#selectField").children().prop('disabled', false);
        }
    });
});