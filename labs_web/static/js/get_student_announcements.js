/**
 * Created by Alex Korienev on 8/20/18.
 */
$.get({
    url:'/student/get-announcements-ajax/',
    success: function (data, status, XHRObject) {
        let ann_block = $("#announcements")[0];
        for (let i in data){
            ann_block.innerHTML += "<div class='alert alert-primary'><a href='{link}'>{title}</a><br>{tutor}<br>{date}</div>".
            replace('{link}', data[i].link).replace('{title}', data[i].title).
            replace('{tutor}', data[i].tutor).replace('{date}', data[i].date.slice(0, data[i].date.length - 7))
        }
    }});
