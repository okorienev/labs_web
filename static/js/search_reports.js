/**
 * Created by Alex Korienev on 6/25/18.
 */

function insert_data(tbodyObj, dataJson){
    let row;
    for (let i in dataJson){
        row = tbodyObj.createElement("tr");
        row.append("<td>{inner}</td>".replace("{inner}", dataJson[i].report_id));
        row.append("<td>{inner}</td>".replace("{inner}", dataJson[i].report_student));
        row.append("<td>{inner}</td>".replace("{inner}", dataJson[i].student_group));
        row.append("<td>{inner}</td>".replace("{inner}", dataJson[i].report_number));
        row.append("<td>{inner}</td>".replace("{inner}", dataJson[i].report_upload_date));
        row.append("<td>{inner}</td>".replace("{inner}", dataJson[i].report_comment));
        row.append("<td>{inner}</td>".replace("{inner}", dataJson[i].report_download_link));
    }
}

$('#search').bind('click', function () {
    $.post({
        url: "/tutor/search-reports",
        success: function (data, status, xhrObject) {
            let tbody = $('#reports-tbody')[0];
            tbody.innerHTML = "";
            insert_data()
        }
    }
    )
});

