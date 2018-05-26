/**
 * Created by Alex Korienev on 5/25/18.
 */
try {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/student/ajax/my-courses/', false); //todo make async call and/or rewrite with Jquery
    xhr.send();
    if (xhr.status === 200){
        let json = JSON.parse(xhr.responseText);
        let menu_children = document.getElementById("pure-menu-children");
        for (i in json){
            console.log(json[i]);
            menu_children.innerHTML += '<li class="pure-menu-item"><a href={url} class="pure-menu-link">{name}</a></li>'
                .replace("{url}", json[i].url).replace("{name}", json[i].name);
        }
    }else {
        alert(xhr.status)
        }
}catch (Exception){
    alert("some errors occurred during processing scripts on this pages");
}
