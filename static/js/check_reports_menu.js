/**
 * Created by Alex Korienev on 6/22/18.
 */
function insert_check_reports_menu(data, status, XHRObject) {
    let menu_children = $.find("#check-reports")[0];
    for (i in data){
        console.log(data[i].url);
        menu_children.innerHTML += ('<li class="pure-menu-item"><a href={url} ' +
            'class="pure-menu-link">{shortened} ({unchecked} unchecked)</a></li>')
                .replace("{url}", data[i].url).replace("{shortened}",
                data[i].shortened).replace("{unchecked}", data[i].unchecked);
    }
}

$.get({
    url:"/tutor/check-reports-menu-items/",
    success: insert_check_reports_menu
});