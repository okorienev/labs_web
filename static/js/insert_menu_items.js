/**
 * Created by Alex Korienev on 5/28/18.
 */
type='module';
function insert_menu_items(data, status, xhrObject) {
    let menu_children = $.find("#pure-menu-children")[0];
    for (i in data){
        menu_children.innerHTML += '<li class="pure-menu-item"><a href={url} class="pure-menu-link">{name}</a></li>'
                .replace("{url}", data[i].url).replace("{name}", data[i].name);
    }
}

export default insert_menu_items;