window.owner_email;
window.tagList;


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
        });

        let settings = {
            "async": true,
            "crossDomain": true,
            "url": "http://localhost:5000/api/pending_tag",
            "method": "GET",
            "headers": {}
        };

        $.getJSON(settings).done(function (response) {
            tagList = response.data.tagList;
            let html = '';
            for (let i = 0; i < tagList.length; i++) {
                html = html + '<tr>';
                html = html + '<td>' + tagList[i].email_tagger + '</td>';
                html = html + '<td>' + tagList[i].item_name + '</td>';
                html = html + '<td>' + tagList[i].file_path + '</td>';
                html = html + '<td>' + tagList[i].tagtime + '</td>';
                let buttons = `<button type="button" class="btn btn-success" value=` + i + `>Accept</button>
<button type="button" class="btn btn-danger" value=` + i + `>Decline</button>`;
                html = html + '<td>' + buttons + '</td>';
                html = html + '</tr>';
            }
            $('#PendingTagsTableBody').html(html);
        });

    });


    $(document).on('click', 'button', function () {

        let idx = this.value;
        let cls = this.classList[1];
        let ctt = tagList[idx];
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

            if (state){
                window.location.replace(`/`)
            }
        });


    });
});
