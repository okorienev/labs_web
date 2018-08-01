/**
 * Created by Alex Korienev on 8/1/18.
 */
$(document).ready(function () {
    let buttons = $(".card-header:button");
    for (i in buttons){
        buttons[i].click(function () {
            let hidden_attr = buttons[i].parent().parent().$(".card-body").hidden;
            hidden_attr = !hidden_attr
        })
    }
});
