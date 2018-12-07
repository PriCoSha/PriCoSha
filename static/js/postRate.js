window.cid
window.owner_email

$(function () {
    $(document).ready(() => {
        cid = location.search.split('cid=')[1];


        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/content?item_id=" + cid,
            "method": "GET",
            "headers": {}
        };

        $.getJSON(settings).done(function (response) {
            let html = "";
            html = html + `<li class="list-group-item">Item ID: ` + response.data.item_id + ` </li>`;
            html = html + `<li class="list-group-item">Item name: ` + response.data.item_name + ` </li>`;
            html = html + `<li class="list-group-item">Post By: ` + response.data.email_post + ` </li>`;
            html = html + `<li class="list-group-item">Post Time: ` + response.data.post_time + ` </li>`;
            html = html + `<li class="list-group-item">File path: ` + response.data.file_path + ` </li>`;

            $('#contentblock').html(html);
        });


        $('#inputSubmit').on("click", function () {


            let settings0 = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:5000/api/email",
                "method": "GET",
                "headers": {}
            };

            $.getJSON(settings0).done(function (response) {
                window.owner_email = response.data.email;
            });


            var form = new FormData();


            form.append("rater_email", owner_email);
            form.append("item_id", cid);
            form.append("emoji", $("#InputEmoji")[0].value);


            var settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:5000/api/rate",
                "method": "POST",
                "headers": {},
                "processData": false,
                "contentType": false,
                "mimeType": "multipart/form-data",
                "data": form
            };

            $.getJSON(settings).done(function (response) {
                console.log(response);
            });

        });
    });


});

