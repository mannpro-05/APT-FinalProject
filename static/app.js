/**
 * This function will get the input form the user when they click on the submit button.
 * It will create a json data out of it.
 * The ajax will sent the json data to the backend and will refresh the content of the page once the
 * processing is finished in the backend. */
function getData() {
    var formData = JSON.stringify($("#myForm").serializeArray());
    console.log(formData)
    $('#loading').show();

    $.ajax({
        type: "POST",
        url: "getVideoName",
        data: formData,
        dataType: "html",
        success: function () {
        },
        contentType: "application/json",
        success: function (response) {
            $('#loading').hide();
            $('#pageBody').remove();
            document.write(response)
        }
    });
}
