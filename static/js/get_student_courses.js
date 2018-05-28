/**
 * Created by Alex Korienev on 5/26/18.
 */
type="module";
import insert_menu_items from "insert_menu_items";
$.get({
    url:"/student/ajax/my-courses/",
    success: insert_menu_items
});