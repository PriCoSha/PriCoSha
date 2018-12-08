var alltagnumber = 0;

$(function () {
    $(document).ready(() => {
        getFriendGroup();

        let settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/public_content",
            "method": "GET",
            "headers": {}
        };

        $.getJSON(settings).done(function (response) {
            // console.log(response.data.contentList);
            let contentList = response.data.contentList;
            let html = '';
            for (let i = 0; i < contentList.length; i++) {
                html = html + '<tr>';
                html = html + '<td>' + `<a href="contentPage.html?cid=` + contentList[i].item_id + `">` + contentList[i].item_name + '</td>';
                html = html + '<td>' + contentList[i].item_id + '</td>';
                html = html + '<td>' + contentList[i].email_post + '</td>';
                html = html + '<td>' + contentList[i].post_time + '</td>';
                html = html + '<td>' + contentList[i].file_path + '</td>';
                html = html + '</tr>';
            }
            $('#publicContentTableBody').html(html);
        });

    });

    // Click Logout
    $('#logoutlink').on("click", function () {
        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/logout",
            "method": "GET",
            "headers": {}
        };

        $.ajax(settings).done(function (response) {
            // console.log(response);
        });
    });

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


                // tag count
                var settings = {
                    "async": true,
                    "crossDomain": true,
                    "url": "http://localhost:5000/api/tag_count",
                    "method": "GET",
                    "headers": {}
                };

                $.ajax(settings).done(function (response) {
                    let number = response.data.tag_number;
                    window.alltagnumber = window.alltagnumber + number;


                    var settings = {
                        "async": true,
                        "crossDomain": true,
                        "url": "http://localhost:5000/api/grouptag_count",
                        "method": "GET",
                        "headers": {}
                    };

                    $.ajax(settings).done(function (response) {
                        let number = response.data.grouptag_number;
                        window.alltagnumber = window.alltagnumber + number;

                        if (window.alltagnumber > 0) {
                            $("#tagRequestOption").show();
                            $("#tagRequestNumber").text(window.alltagnumber);

                        } else {
                            $("#tagRequestOption").hide();
                        }


                    });


                });


                let lofFriendGroup = response.data.friendgroup;

                for (let i = 0; i < lofFriendGroup.length; i++) {

                    let settings = {
                        "async": true,
                        "crossDomain": true,
                        "url": "http://localhost:5000/api/private_content?fg_name=" + lofFriendGroup[i].fg_name + "&owner_email=" + lofFriendGroup[i].owner_email,
                        "method": "GET",
                        "headers": {}
                    };
                    $.getJSON(settings).done(function (response) {
                        let contentList = response.data.contentList;
                        let html = `<div class="row">
                    <div class="col-10 offset-1">
                        <div class="card">
                            <div class="card-header">` +
                            "Contents shared in " + lofFriendGroup[i].fg_name + " (owned by " + lofFriendGroup[i].owner_email + ")"
                            +
                            `</div>
                            <div class="card-block">
                                <table id="privateContentTable" class="table table-striped">
                                    <thead>
                                    <tr>
                                        <th>Item name</th>
                                        <th>Item ID</th>
                                        <th>Post by</th>
                                        <th>Post time</th>
                                        <th>File Path</th>
                                    </tr>
                                    </thead>
                                    <tbody id="privateContentTableBody">`;
                        for (let i = 0; i < contentList.length; i++) {
                            html = html + '<tr>';
                            html = html + '<td>' + `<a href="contentPage.html?cid=` + contentList[i].item_id + `">` + contentList[i].item_name + '</td>';
                            html = html + '<td>' + contentList[i].item_id + '</td>';
                            html = html + '<td>' + contentList[i].email_post + '</td>';
                            html = html + '<td>' + contentList[i].post_time + '</td>';
                            html = html + '<td>' + contentList[i].file_path + '</td>';
                            html = html + '</tr>';
                        }
                        html = html + `</tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>`;
                        $('#main111').after(html);
                    });
                }


                // Do not log in
            } else {
                $("#userNav").hide();
            }
        });

    }

});
