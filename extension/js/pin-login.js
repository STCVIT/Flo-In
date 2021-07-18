$(function() {
    $("input[name='password']").on('input', function(e) {
        $(this).val($(this).val().replace(/[^0-9]/g, ''));
    });
});

function pincode()
{
var input = document.getElementById("userInput").value;
alert(input);
}