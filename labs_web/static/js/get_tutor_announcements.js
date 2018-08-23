/**
 * Created by Alex Korienev on 8/23/18.
 */
$.get({
    url:'/tutor/get-announcements/',
    success: function (data, status, XHRObject) {
        let ann_block = $("#announcements")[0];
        for (let i in data){
            ann_block.innerHTML += "<div class='alert alert-primary'><a href='{link}'>{title}<br></a>{date}</div>".
            replace('{link}', data[i].link).replace('{title}', data[i].title).
            replace('{date}', data[i].date.slice(0, data[i].date.length - 7))
        }
    }});