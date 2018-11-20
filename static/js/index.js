function getFriendGroup() {

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://localhost:5000/api/friendgroup",
        "method": "GET",
        "headers": {}
    }

    $.ajax(settings).done(function (response) {
        console.log(response);

    });
}

window.onload = function () {
    getFriendGroup()
    parameters = window.location.hash;
    if (parameters){
        parameters = parameters.substring(1).split("/");
        console.log(parameters);
    }
}