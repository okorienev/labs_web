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

$.get({
    url:"/tutor/check-reports-menu-items/",
    success: insert_check_reports_menu
});
