window.owner_email;
window.normaltagList;


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
            "url": "http://localhost:5000/api/pending_tag",
            "method": "GET",
            "headers": {}
        };

        $.getJSON(settings).done(function (response) {
            normaltagList = response.data.normaltagList;
            console.log(normaltagList);
            let html = '';
            for (let i = 0; i < normaltagList.length; i++) {
                html = html + '<tr>';
                html = html + '<td>' + normaltagList[i].email_tagger + '</td>';
                html = html + '<td>' + normaltagList[i].item_name + '</td>';
                html = html + '<td>' + normaltagList[i].file_path + '</td>';
                html = html + '<td>' + normaltagList[i].tagtime + '</td>';
                let buttons = `<button type="button" class="btn btn-success" value=` + i + `>Accept</button>
<button type="button" class="btn btn-danger" value=` + i + `>Decline</button>`;
                html = html + '<td>' + buttons + '</td>';
                html = html + '</tr>';
            }
            $('#PendingTagsTableBody').html(html);
        });


        settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/pending_grouptag",
            "method": "GET",
            "headers": {}
        }

        $.ajax(settings).done(function (response) {
            grouptagList = response.data.grouptagList;
            let html = '';
            for (let i = 0; i < grouptagList.length; i++) {
                html = html + '<tr>';
                html = html + '<td>' + grouptagList[i].email_tagger + '</td>';
                html = html + '<td>' + grouptagList[i].item_name + '</td>';
                html = html + '<td>' + grouptagList[i].fg_name + '</td>';
                html = html + '<td>' + grouptagList[i].owner_email + '</td>';
                html = html + '<td>' + grouptagList[i].tagtime + '</td>';
                let buttons = `<button type="button" class="btn btn-success grp" value=` + i + `>Accept</button>
<button type="button" class="btn btn-danger grp" value=` + i + `>Decline</button>`;
                html = html + '<td>' + buttons + '</td>';
                html = html + '</tr>';
            }
            $('#GroupPendingTagsTableBody').html(html);
        });


    });


    $(document).on('click', 'button', function () {
        let cls = this.classList;
        let pd = cls.length;

        if (pd == 2) {
            console.log("clicked")
            let idx = this.value;
            cls = this.classList[1];
            let ctt = normaltagList[idx];
            let status = "0";
            if (cls == "btn-success") {
                status = "1"
            }

            let form = new FormData();
            form.append("status", status);
            form.append("email_tagged", owner_email);
            form.append("email_tagger", ctt.email_tagger);
            form.append("item_id", ctt.item_id);

            let settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:5000/api/tag",
                "method": "PATCH",
                "headers": {},
                "processData": false,
                "contentType": false,
                "mimeType": "multipart/form-data",
                "data": form
            };

            $.getJSON(settings).done(function (response) {
                let state = response.state;
                console.log(response);

                if (state) {
                    // location.reload();

                }
            });

        } else {

        }


    })


});
