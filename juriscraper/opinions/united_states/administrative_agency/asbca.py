"""Scraper for Armed Services Board of Contract Appeals
CourtID: asbca
Court Short Name: ASBCA
Author: Jon Andersen
Reviewer: mlr
History:
    2014-09-11: Created by Jon Andersen
    2016-03-17: Website and phone are dead. Scraper disabled in __init__.py.
    2024-01-24: Add parsing of judges
"""

from datetime import datetime

from juriscraper.lib.string_utils import clean_string
from juriscraper.OpinionSiteLinear import OpinionSiteLinear


class Site(OpinionSiteLinear):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.url = f"http://www.asbca.mil/Decisions/decisions{datetime.today().year}.html"
        self.status = "Published"

    def _process_html(self) -> None:
        """Parse HTML into case objects

        :return: None
        """
        for row in self.html.xpath(".//tr")[1:]:
            date, docket, *_, judge = (
                clean_string(cell) for cell in row.xpath("td/text()")
            )
            if not docket:
                # Row that separates months
                continue

            url = row.xpath(".//a/@href")[0]
            # Part of the name may be inside <a>, part inside <span> or
            # floating as <td>'s text
            name = clean_string(row.xpath("string(.//td[3])"))

            self.cases.append(
                {
                    "date": date,
                    "name": name,
                    "url": url,
                    "docket": docket,
                    "judge": judge,
                }
            )
