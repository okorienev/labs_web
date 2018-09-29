/** Deprecated script
 * Created by Alex Korienev on 5/28/18.
 */
function insert_menu_items(data, status, xhrObject) {
    let menu_children = $.find("#dropdown-children")[0];
    for (i in data){
        menu_children.innerHTML += '<a class="dropdown-item" href={url}>{name}</a>'
                .replace("{url}", data[i].url).replace("{name}", data[i].name);
    }
}
