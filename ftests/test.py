
from datetime import datetime
from selenium import webdriver
from testarsenal import BrowserTest
from freezegun import freeze_time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase, BrowserTest):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.freezer = freeze_time("2000-01-1 15:00:00") #UTC time
        self.freezer.start()

        self.get("/")


    def tearDown(self):
        self.browser.close()


    def test(self):
        # The user is on the home page and the date is given
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "Sat 1 Jan, 2000")

        # There is a table with a header but no rows
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")[3:]
        self.assertEqual(len(rows), 1)
        column_names = [th.text for th in rows[0].find_elements_by_tag_name("th")]
        self.assertEqual(column_names, ["Date", "Day Total", "Weighted Total", "Running Total"])
