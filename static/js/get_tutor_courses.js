/**
 * Created by Alex Korienev on 5/28/18.
 */
type="module";
import insert_menu_items  from 'insert_menu_items'
$.get({
    url:"/tutor/courses_ajax",
    success: insert_menu_items
});