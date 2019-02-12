
from datetime import datetime as dt
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


    def check_table(self, dates, targets, wins, habits, data):
        table = self.browser.find_element_by_tag_name("table")
        rows = table.find_elements_by_tag_name("tr")
        if dates:
            self.assertEqual(
             [td.text for td in rows[0].find_elements_by_tag_name("td")[1:-3]],
             [d.strftime("%a %-d %b, %Y") for d in dates]
            )
        if targets:
            self.assertEqual(
             [td.text[:-1].strip() for td in rows[1].find_elements_by_tag_name("td")[1:]],
             [str(t) for t in targets]
            )
        if wins:
            self.assertEqual(
             [td.text[:-1].strip() for td in rows[2].find_elements_by_tag_name("td")[1:]],
             [str(w) for w in wins]
            )
        rows = rows[3:]
        self.assertEqual(len(rows), len(data) + 1)
        column_names = [th.text for th in rows[0].find_elements_by_tag_name("th")]
        self.assertEqual(column_names, ["Date"] + habits +  ["Day Total", "Weighted Total", "Running Total"])
        for table_row, data_row in zip(rows[1:], data):
            for table_cell, data_cell in zip(table_row.find_elements_by_tag_name("td"), data_row):
                table_cell = table_cell.text
                try:
                    table_cell = float(table_cell)
                except: pass
                self.assertEqual(table_cell, data_cell)


    def test(self):
        # The user is on the home page and the date is given
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "Sat 1 Jan, 2000")

        # There is a table with a header but no rows
        self.check_table([], [], [], [], [])

        # They create a habit to start today
        self.click(
         self.browser.find_element_by_xpath("//*[contains(text(), 'New Habit')]")
        )
        self.check_page("/new/")
        form = self.browser.find_element_by_tag_name("form")
        inputs = form.find_elements_by_tag_name("input")
        inputs[0].send_keys("No Smoking")
        form.find_element_by_tag_name("textarea").send_keys("Don't smoke anything with tobacco")
        inputs[1].send_keys("2000-01-01")
        inputs[2].send_keys("1")
        inputs[3].send_keys("3,7,5")
        self.click(inputs[-1])
        self.check_page("/")

        # The habit is in the table, and is currently positive
        self.check_table(
         [dt(2000, 1, 4)],
         [3], [0],
         ["No Smoking"],
         [
          ["Today", 1, 1, 1, 1]
         ]
        )
