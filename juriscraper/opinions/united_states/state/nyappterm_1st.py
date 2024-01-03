# Scraper for New York Appellate Term 1st Dept.
# CourtID: nyappterm_1st
# Court Short Name: NY

import re
from datetime import date, timedelta
from typing import Any, Dict, List, Tuple

from juriscraper.AbstractSite import logger
from juriscraper.lib.date_utils import make_date_range_tuples
from juriscraper.OpinionSiteLinear import OpinionSiteLinear


class Site(OpinionSiteLinear):
    first_document_date = date(2018, 1, 1)
    last_backscraper_date = date.today()

    # Size of interval must ensure that site returns
    # less than 500 results. Otherwise site will error
    search_interval_days = 100

    back_scrape_iterable: List[Tuple[date, date]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.court_id = self.__module__
        self.url = "https://iapps.courts.state.ny.us/lawReporting/Search?searchType=opinion"
        self.court = "Appellate Term, 1st Dept"

        self._set_parameters()

        self.back_scrape_iterable = make_date_range_tuples(
            self.first_document_date,
            self.last_backscraper_date,
            self.search_interval_days,
        )

    def _set_parameters(self) -> None:
        """Set the parameters for the POST request."""
        self.method = "POST"
        today = date.today()
        self.parameters = {
            "rbOpinionMotion": "opinion",
            "and_or": "and",
            "dtStartDate": (today - timedelta(days=30)).strftime("%m/%d/%Y"),
            "dtEndDate": today.strftime("%m/%d/%Y"),
            "court": self.court,
            "and_or2": "and",
            "Order_By": "Decision Date",
            "Submit": "Find",
        }

    def _process_html(self) -> None:
        for row in self.html.xpath(".//table")[-1].xpath(".//tr")[1:]:
            url = row.xpath(".//a")[0].get("href")
            match = re.search(r"http.*(htm|pdf)", url)
            url = match.group(0) if match else ""

            name = row.xpath(".//td")[0].text_content().strip()

            if not name:
                # Some opinions have been withdrawn from publication
                # For example:
                # https://www.nycourts.gov/reporter/3dseries/2019/2019_29160.htm
                # Filter with: 05/21/2019; 'Other Courts'; to find it
                logger.info("Skipping row because it has no name %s" % url)
                continue

            official_citation = " ".join(row.xpath("./td[4]//text()"))
            slip_cite = " ".join(row.xpath("./td[5]//text()"))
            status = "Unpublished" if "(U)" in slip_cite else "Published"

            self.cases.append(
                {
                    "name": name,
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

    def _download_backwards(self, date_range: Tuple[date, date]) -> None:
        """Method used by backscraper to download historical records

        :param date_range: a tuple where the first member is the start date
                            and the second member is the end date
        :return: None
        """
        self.parameters.update(
            {
                "dtStartDate": date_range[0].strftime("%m/%d/%Y"),
                "dtEndDate": date_range[1].strftime("%m/%d/%Y"),
            }
        )
