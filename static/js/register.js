$(function () {

    $('#inputSubmit').on("click", function () {

        let email = $("#inputEmail")[0].value;

        let form = new FormData();
        form.append("email", email);
        let password = $("#inputPassword")[0].value;

        form.append("password", Sha1.hash(password));
        let fname = $("#inputFname")[0].value;
        form.append("fname", fname);
        let lname = $("#inputLname")[0].value;
        form.append("lname", lname);
        let settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/register",
            "method": "POST",
            "headers": {},
            "processData": false,
            "contentType": false,
            "mimeType": "multipart/form-data",
            "data": form
        };

        $.getJSON(settings).done(function (response) {
            let state = response.state;

            if (state){
                window.location.replace(`/`)
            }
            else {
                alert(response.error.errormsg)
            }
        });

    });


});