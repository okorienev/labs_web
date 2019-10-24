import unittest
from pyvirtualdisplay import Display
# noinspection PyUnresolvedReferences
from labs_web.test import (TestServiceIsUp,
                           TestLogin,
                           TestTutorMenu)


if __name__ == "__main__":
    display = Display(visible=0, size=(1366, 768))
    display.start()
    unittest.main()
    display.stop()
