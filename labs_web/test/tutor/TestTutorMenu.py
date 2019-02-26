from . import AbstractTutorTest


class TestTutorMenu(AbstractTutorTest):
    """
    Test that menu is correct
    """
    _MENU_ITEMS = [
        ('#navbarNavDropdown > ul > li:nth-child(4)', 'Add Course'),
        ('#navbarNavDropdown > ul > li:nth-child(5)', 'Report archive'),
        ('#navbarNavDropdown > ul > li:nth-child(6)', 'Make Announcement'),
        ('#navbarNavDropdown > ul > li:nth-child(7)', 'Answer Ticket'),
        ('#navbarNavDropdown > ul > li:nth-child(8)', 'Course Snapshot')
    ]

    def _menu_item_alive(self, selector: str, title: str):
        """
        click on menu item, compare page title with given, return back
        separated into a function to keep the code DRY
        :param selector: CSS selector
        :param title: page title
        """
        self.driver.find_element_by_css_selector(selector).click()
        self.assertEqual(self.driver.title.lower(), title.lower())
        self.driver.back()

    def test_menu_is_populated(self):
        """
        test that all menu items are accessible and return no errors when clicking on them
        """
        home = self.driver.find_element_by_xpath('//*[@id="navbarNavDropdown"]/ul/li[1]')
        home.click()
        self.assertEqual(self.driver.title, "Homepage")
        self.driver.back()
        course_stats_menu = self.driver.find_element_by_id("navbarDropdownMenuLink")
        course_stats_menu.click()
        menu_items_container = self.driver.find_element_by_id("dropdown-children")
        menu_item = menu_items_container.find_element_by_xpath("./*")
        menu_item.click()
        self.driver.back()
        for entry in self._MENU_ITEMS:
            self._menu_item_alive(*entry)



