$(function () {

    $('#inputSubmit').on("click", function () {

        let email = $("#inputEmail")[0].value;

        let form = new FormData();
        form.append("email", email);
        let password = $("#inputPassword")[0].value;


        form.append("password", Sha1.hash(password));

        let settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/loginAuth",
            "method": "POST",
            "headers": {},
            "processData": false,
            "contentType": false,
            "mimeType": "multipart/form-data",
            "data": form
        }

        $.getJSON(settings).done(function (response) {
            let state = response.state

            let fname = response.data.fname
            let lname = response.data.lname
            if (state){
                window.location.replace(`/#${email}/${fname}/${lname}`)
            }
            else {
                alert(response.error.errormsg)
            }
        });

    });


})