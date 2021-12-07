# Scraper for Georgia Appeals Court
# CourtID: gactapp
# Court Short Name: gactapp
# Author: Andrei Chelaru
# Reviewer: mlr
# Date created: 25 July 2014


from datetime import date, timedelta

from juriscraper.lib.string_utils import convert_date_string, titlecase
from juriscraper.OpinionSite import OpinionSite


class Site(OpinionSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.case_date = date.today()
        self.a_while_ago = date.today() - timedelta(days=20)
        self.base_path = "id('art-main')//tr[position() > 1]"
        self.url = (
            "http://www.gaappeals.us/docketdate/results_all.php?searchterm="
            "{mn_ago:02d}%2F{day_ago:02d}%2F{year_ago}&searchterm2="
            "{mn:02d}%2F{day:02d}%2F{year}&submit=Search".format(
                mn_ago=self.a_while_ago.month,
                day_ago=self.a_while_ago.day,
                year_ago=self.a_while_ago.year,
                mn=self.case_date.month,
                day=self.case_date.day,
                year=self.case_date.year,
            )
        )

    def _get_case_names(self):
        path = f"{self.base_path}/td[2]/text()"
        return [titlecase(e) for e in self.html.xpath(path)]

    def _get_download_urls(self):
        path = f"{self.base_path}/td[6]/a/@href"
        return list(self.html.xpath(path))

    def _get_case_dates(self):
        path = f"{self.base_path}/td[3]/text()"
        return [convert_date_string(e) for e in self.html.xpath(path)]

    def _get_precedential_statuses(self):
        return ["Published"] * len(self.case_names)

    def _get_docket_numbers(self):
        path = f"{self.base_path}/td[1]/text()"
        return list(self.html.xpath(path))

    def _get_dispositions(self):
        path = f"{self.base_path}/td[4]/text()"
        return [titlecase(e) for e in self.html.xpath(path)]
