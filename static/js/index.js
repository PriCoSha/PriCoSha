$(function () {


    $(document).ready(() => {
        getFriendGroup();


    });

    $('#logoutlink').on("click", function () {
        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/logout",
            "method": "GET",
            "headers": {}
        }

        $.ajax(settings).done(function (response) {
            // console.log(response);
        });
    });
    // parameters = window.location.hash;
    // if (parameters) {
    //     parameters = parameters.substring(1).split("/");
    //     console.log(parameters);
    // }
    function getFriendGroup() {
        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/friendgroup",
            "method": "GET",
            "headers": {}
        };
        $.getJSON(settings).done(function (response) {
            let state = response.state;
            // Logged in
            if (state) {
                // Nav Bar
                $("#guestNav").hide();

                // Welcome Message
                var settings = {
                    "async": true,
                    "crossDomain": true,
                    "url": "http://localhost:5000/api/name",
                    "method": "GET",
                    "headers": {}
                };
                $.getJSON(settings).done(function (response) {
                    let fname = response.data.fname;
                    let lname = response.data.lname;
                    $("#welcomeMessage").text("Welcome, " + fname + " " + lname + "!");
                });


                var settings = {
                    "async": true,
                    "crossDomain": true,
                    "url": "http://localhost:5000/api/tag_count",
                    "method": "GET",
                    "headers": {}
                }

                $.ajax(settings).done(function (response) {
                    let number = response.data.tag_number;
                    if (number > 0) {
                        $("#tagRequestOption").show();
                        $("#tagRequestNumber").text(number);

                    } else {
                        $("#tagRequestOption").hide();
                    }
                });


                // Does not log in
            } else {
                $("#userNav").hide();
            }
        });


    }

});
