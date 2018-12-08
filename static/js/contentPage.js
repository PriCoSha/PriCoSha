window.cid

$(function () {
    $(document).ready(() => {
        cid = location.search.split('cid=')[1];


        let settings0 = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/email",
            "method": "GET",
            "headers": {}
        };

        $.getJSON(settings0).done(function (response) {

            let state = response.state;
            if (!state) {
                $("#posttagbutton").hide();
                $("#postratebutton").hide();
                $("#postgrouptagbutton").hide();

            }
        });


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

            if (response.data.location) {
                html = html + `<li class="list-group-item">Location: ` + response.data.location + ` </li>`;
            }


            if (response.data.movie_format) {
                html = html + `<li class="list-group-item">Movie Format: ` + response.data.movie_format + ` </li>`;
            }

            if (response.data.pic_format) {
                html = html + `<li class="list-group-item">Picture Format: ` + response.data.pic_format + ` </li>`;
            }

            if (response.data.resolution) {
                html = html + `<li class="list-group-item">Resolution: ` + response.data.resolution + ` </li>`;
            }


            $('#contentblock').html(html);
        });

        settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/rate?item_id=" + cid,
            "method": "GET",
            "headers": {}
        };

        $.getJSON(settings).done(function (response) {
            console.log(response);


            let contentList = response.data.rateList;
            let html = '';
            for (let i = 0; i < contentList.length; i++) {
                html = html + '<tr>';
                html = html + '<td>' + contentList[i].email + '</td>';
                html = html + '<td>' + contentList[i].emoji + '</td>';
                html = html + '<td>' + contentList[i].rate_time + '</td>';
                html = html + '</tr>';
            }
            $('#RateTableBody').html(html);
        });

        settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/grouptag?item_id=1",
            "method": "GET",
            "headers": {}
        }

        $.getJSON(settings).done(function (response) {
            console.log(response);


            let contentList = response.data.GrouptagList;
            let html = '';
            for (let i = 0; i < contentList.length; i++) {
                html = html + '<tr>';
                html = html + '<td>' + contentList[i].email_tagger + '</td>';
                html = html + '<td>' + contentList[i].fg_name + '</td>';
                html = html + '<td>' + contentList[i].owner_email + '</td>';
                html = html + '<td>' + contentList[i].tagtime + '</td>';
                html = html + '</tr>';
            }
            $('#GroupTagTableBody').html(html);
        });

        settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/tag?item_id=" + cid,
            "method": "GET",
            "headers": {}
        };

        $.getJSON(settings).done(function (response) {
            console.log(response);


            let contentList = response.data.normaltagList;
            let html = '';
            for (let i = 0; i < contentList.length; i++) {
                html = html + '<tr>';
                html = html + '<td>' + contentList[i].email_tagger + '</td>';
                html = html + '<td>' + contentList[i].email_tagged + '</td>';
                html = html + '<td>' + contentList[i].tagtime + '</td>';
                html = html + '</tr>';
            }
            $('#TagTableBody').html(html);
        });


    });

    $('#posttagbutton').on("click", function () {
        window.location.replace('/postTag.html?cid=' + cid)
    });

    $('#postratebutton').on("click", function () {
        window.location.replace('/postRate.html?cid=' + cid)
    });

    $('#postgrouptagbutton').on("click", function () {
        window.location.replace('/postGroupTag.html?cid=' + cid)
    });


});

