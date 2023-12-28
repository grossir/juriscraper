# Scraper for New York Appellate Term 1st Dept.
# CourtID: nyappterm_1st
# Court Short Name: NY

import re
from datetime import date, timedelta, datetime
from typing import Any, Dict, Tuple, List

from juriscraper.OpinionSiteLinear import OpinionSiteLinear


class NYSlipDecisionsSite(OpinionSiteLinear):
    url = "https://iapps.courts.state.ny.us/lawReporting/Search?searchType=opinion"
    court: str  # Must be defined on inheriting classes

    first_document_date: str  # in the %m/%d/%Y format
    search_interval_days: int  # Size of interval were site returns less than 500 results
    back_scrape_iterable: List[Tuple[str, str]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self._set_parameters()
        self.create_back_scrape_iterable()

    def _set_parameters(self) -> None:
        """Set the parameters for the POST request."""
        self.method = "POST"
        today = date.today()
        self.parameters = {
            "rbOpinionMotion": "opinion",
            "Pty": "",
            "and_or": "and",
            "dtStartDate": (today - timedelta(days=30)).strftime("%m/%d/%Y"),
            "dtEndDate": today.strftime("%m/%d/%Y"),
            "court": self.court,
            "docket": "",
            "judge": "",
            "slipYear": "",
            "slipNo": "",
            "OffVol": "",
            "Rptr": "",
            "OffPage": "",
            "fullText": "",
            "and_or2": "and",
            "Order_By": "Decision Date",
            "Submit": "Find",
            "hidden1": "",
            "hidden2": "",
        }

    def _process_html(self):
        for row in self.html.xpath(".//table")[-1].xpath(".//tr")[1:]:
            official_citation = " ".join(row.xpath("./td[4]//text()"))
            slip_cite = " ".join(row.xpath("./td[5]//text()"))
            status = "Unpublished" if "(U)" in slip_cite else "Published"

            url = row.xpath(".//a")[0].get("href")
            url = re.findall(r"(http.*htm)", url)[0]

            self.cases.append(
                {
                    "name": row.xpath(".//td")[0].text_content(),
                    "date": row.xpath(".//td")[1].text_content(),
                    "url": url,
                    "status": status,
                    "docket": "",
                    "citation": official_citation,
                    "parallel_citation": slip_cite,
                }
            )

    def extract_from_text(self, scraped_text: str) -> Dict[str, Any]:
        """Can we extract the date filed from the text?

        :param scraped_text: The content of the document downloaded
        :return: Metadata to be added to the case
        """
        # Ny App Term 1st Dept. 2nd and Sup Ct all have different varying
        # docket number types.
        # ie. 123413/03 vs. 51706 vs. 2003-718 Q C or 2003-1288 K C

        dockets = re.findall(
            r"(\d+\/\d+)|^(\d{5,})|^(\d+-\d+ \w+\s\w+)", scraped_text
        )
        dockets = [list(filter(None, x)) for x in dockets]
        metadata = {
            "Docket": {
                "docket_number": dockets[0][0] if dockets else "",
            },
        }
        return metadata

    def create_back_scrape_iterable(self):
        # TODO: wip
        # TODO: redefine all the sources that use this template
        self.first_document_date = "01/11/2001"
        self.search_interval_days = 15

        start_date = datetime.strptime(
            self.first_document_date, "%m/%d/%Y"
        ) - timedelta(days=1)
        today = date.today()

    def _download_backwards(self, date_range: Tuple[str, str]) -> None:
        """Method used by backscraper to download historical records

        :param date_range: a tuple where the first member is the start date
                            and the second member is the end date
        :return: None
        """
        self.parameters.update(
            {
                "dtStartDate": date_range[0],
                "dtEndDate": date_range[1],
            }
        )


class Site(NYSlipDecisionsSite):
    court = "Appellate Term, 1st Dept"
