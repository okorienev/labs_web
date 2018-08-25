/**
 * Created by Alex Korienev on 8/23/18.
 */
$.get({
    url:'/tutor/get-announcements/',
    success: function (data, status, XHRObject) {
        let ann_block = $("#announcements")[0];
        let template =
            "<div class='alert alert-primary'>" +
                "<a href='{link}'>{title}<br></a>" +
                "{date}<br>" +
                "<button id='{link}' style='width: 100%' class='delete-button btn btn-danger'>Delete</button>" +
            "</div>";
        for (let i in data){
            ann_block.innerHTML += template.
            replace('{link}', data[i].link).replace('{link}', data[i].link).replace('{title}', data[i].title).
            replace('{date}', data[i].date.slice(0, data[i].date.length - 7))
        }
        $(".delete-button").click(function (event) {
            if (confirm("Are You sure?")){
                $.ajax({
                    url: event.target.id,
                    method: 'DELETE',
                    success: function (data, status, XHRObject) {
                        alert(data.text);
                        $(event.target).parent().remove();
                    },
                    error: function (data, status, XHROBject) {
                        alert("Something went wrong")
                    }
            })
            }
        })
    }});