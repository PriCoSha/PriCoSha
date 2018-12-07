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
            window.owner_email = response.data.email;
            console.log(owner_email);
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

        form.append("owner_emails", l_oe.join(";"));
        form.append("fg_names", l_fgn.join(";"));
        form.append("file_path", filePath);
        form.append("item_name", contentName);
        form.append("is_pub", is_pub);
        form.append("email_post", window.owner_email);

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
            let state = response.state;
            console.log(state);

            if (state) {
                window.location.replace(`/`)
            } else {
            }
        });

    });


});