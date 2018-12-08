window.owner_email;
window.listoffriendgroup;

$(function () {
    $(document).ready(() => {


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


        let settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/friendgroup",
            "method": "GET",
            "headers": {}
        };

        $.getJSON(settings).done(function (response) {
            window.listofriendgroup = response.data.friendgroup;
            console.log(listofriendgroup);

            let html = '';
            for (let i = 0; i < listofriendgroup.length; i++) {
                html = html + `<div class="form-check">
                            <input class="form-check-input" type="checkbox" value=` + i + ` id="FG` + i + `>
                            <label class="form-check-label">
                                ` + listofriendgroup[i].fg_name + `
                            </label>
                        </div>`;
            }
            $('#checklist').after(html);

        });


    });


    $('#inputSubmit').on("click", function () {
        let form = new FormData();
        let contentName = $("#InputContentName")[0].value;
        let filePath = $("#InputFilePath")[0].value;

        let is_pub = "0";
        let l_oe = [];
        let l_fgn = [];

        let l = $("input[type='checkbox']:checked");
        for (let i = 0; i < l.length; i++) {
            let value = l[i].value;
            if (value == "-1") {
                is_pub = "1";
            } else {
                l_oe.push(window.listofriendgroup[value].owner_email);
                l_fgn.push(window.listofriendgroup[value].fg_name);
            }
        }


        if ((l.length == 0) | contentName == "" | filePath == "") {
            alert("Please fill in every blank!")

        } else {
            form.append("owner_emails", l_oe.join(";"));
            form.append("fg_names", l_fgn.join(";"));
            form.append("file_path", filePath);
            form.append("item_name", contentName);
            form.append("is_pub", is_pub);
            form.append("email_post", window.owner_email);

            let checked_value = $('input[name=exampleRadios]:checked').val();
            let values = [];
            if (checked_value == "option1") {
                values.push(1);
                values.push($("#MovieFormat")[0].value);
                values.push($("#MovieResolution")[0].value)

            } else if (checked_value == "option2") {
                values.push(2)
                values.push($("#PictureFormat")[0].value);
                values.push($("#PictureLocation")[0].value)
            } else {
                values.push(0)
            }
            form.append("type", values.join(";"));

            let settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:5000/api/content",
                "method": "POST",
                "headers": {},
                "processData": false,
                "contentType": false,
                "mimeType": "multipart/form-data",
                "data": form
            };

            $.getJSON(settings).done(function (response) {
                console.log(response)
                let state = response.state;
                if (state) {
                    window.location.replace(`/`)
                } else {
                }
            });
        }
    });


});