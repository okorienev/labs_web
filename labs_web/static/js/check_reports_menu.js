/**
 * Created by Alex Korienev on 6/22/18.
 */
function insert_check_reports_menu(data, status, XHRObject) {
    let menu_children = $.find("#check-reports")[0];
    for (i in data){
        menu_children.innerHTML += ('<a href={url} class="dropdown-item">{shortened} ({unchecked} unchecked)</a>')
                .replace("{url}", data[i].url).replace("{shortened}",
                data[i].shortened).replace("{unchecked}", data[i].unchecked);
    }
}
function insert_unchecked_labs_events(data, status, XHRObject){
    let events = $("#last-events")[0];
    for (i in data){
        events.innerHTML = events.innerHTML + ('<div ' +
            'class="alert alert-info" role="alert">Amount of unchecked reports in course {c}: {u}</div>'
                .replace('{u}', data[i].unchecked).replace('{c}', data[i].shortened));
    }
}

$(document).ready(function () {
    $.get({
        url: "/tutor/check-reports-menu-items/",
        success: function (data, status, XHROBject) {
            insert_check_reports_menu(data, status, XHROBject);
            insert_unchecked_labs_events(data, status, XHROBject);
        }
    })
});
