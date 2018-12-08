window.owner_email;
window.contentList;
window.fg_name;
window.nowstate = 0;

$(function () {
    $(document).ready(() => {


        var url_string = window.location.href;
        var url = new URL(url_string);
        fg_name = url.searchParams.get("fg_name");
        var owner_email = url.searchParams.get("owner_email");

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
                window.location.replace(`/`)
            }
            window.owner_email = response.data.email;
        });

        $("#fln_ipt").show();
        $("#email_ipt").hide();

        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/member?fg_name=" + fg_name + "&owner_email=" + owner_email,
            "method": "GET",
            "headers": {}
        }

        $.ajax(settings).done(function (response) {

            window.contentList = response.data.contentList;
            let html = '';
            for (let i = 0; i < contentList.length; i++) {
                html = html + '<tr>';
                html = html + '<td>' + contentList[i].email + '</td>';
                html = html + '<td>' + contentList[i].fname + " " + contentList[i].lname + '</td>';
                let buttons;
                if (owner_email == contentList[i].email) {
                    buttons = ""
                } else {
                    buttons = `<button type="button" class="btn btn-danger" value=` + i + `>Delete</button>`;

                }
                html = html + '<td>' + buttons + '</td>';
                html = html + '</tr>';
            }
            $('#ManageGroupTableBody').html(html);
        });


    });


    $(document).on('click', 'button', function () {

        if (this.id == "inputSubmit") {
            if (nowstate == 0) {
                var form = new FormData();
                form.append("fname", $("#InputFriendFN")[0].value);
                form.append("lname", $("#InputFriendLN")[0].value);
                form.append("fg_name", fg_name);
                form.append("owner_email", owner_email);

                settings = {
                    "async": true,
                    "crossDomain": true,
                    "url": "http://localhost:5000/api/friendgroup",
                    "method": "PATCH",
                    "headers": {},
                    "processData": false,
                    "contentType": false,
                    "mimeType": "multipart/form-data",
                    "data": form
                };

                $.getJSON(settings).done(function (response) {
                    let state = response.state;

                    if (state) {
                        window.location.reload()
                    } else {
                        if (response.error.code == 8) {
                            nowstate = 1;
                            $("#fln_ipt").hide();
                            $("#email_ipt").show();
                        }
                        alert(response.error.errormsg)
                    }
                });
            } else {
                var form = new FormData();
                form.append("email", $("#inputEmail")[0].value);
                form.append("fg_name", fg_name);
                form.append("owner_email", owner_email);

                settings = {
                    "async": true,
                    "crossDomain": true,
                    "url": "http://localhost:5000/api/friendgroup",
                    "method": "PATCH",
                    "headers": {},
                    "processData": false,
                    "contentType": false,
                    "mimeType": "multipart/form-data",
                    "data": form
                };

                $.getJSON(settings).done(function (response) {
                    let state = response.state;

                    if (state) {
                        window.location.reload()
                        nowstate = 0;
                        $("#fln_ipt").show();
                        $("#email_ipt").hide();
                    } else {
                        alert(response.error.errormsg)
                    }
                });
            }


        } else {

            let idx = this.value;
            let ctt = contentList[idx];

            var form = new FormData();
            form.append("email", ctt.email);
            form.append("fg_name", fg_name);
            form.append("owner_email", owner_email);

            var settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:5000/api/friendgroup",
                "method": "DELETE",
                "headers": {},
                "processData": false,
                "contentType": false,
                "mimeType": "multipart/form-data",
                "data": form
            }

            $.getJSON(settings).done(function (response) {
                let state = response.state;
                console.log(response);

                if (state) {
                    location.reload();
                }
            });
        }


    })


});
