import unittest

from juriscraper.DeferringList import DeferringList
from juriscraper.OpinionSiteLinear import OpinionSiteLinear


class ExpectedException(Exception):
    pass


class TestSite(OpinionSiteLinear):
    def __init__(self):
        super().__init__()
        self.url = "https://example.com"
        self.status = "Published"

    def _process_html(self) -> None:
        print(f"Processing source {self.url} html")
        for index in range(1,3):
            self.cases.append(
                {
                    "url": self.url,
                    "docket": f"{index}",
                    "date": f"11/{index}/2024",
                }
            )

    def _get_case_names(self) -> DeferringList:
        seeds = ["https://example.org/", "https://example.net/"]

        def get_name(link: str) -> str:
            print("Inside the DeferringList fetcher")
            self._get_html_tree_by_url(link)
            raise ExpectedException(
                "Data has been downloaded. Catch this exception if you expect it"
            )

        return DeferringList(seed=seeds, fetcher=get_name)


class DeferringListTest(unittest.TestCase):
    """Test the authentication methods"""

    def test_deferring_list(self):
        site = TestSite().parse()
        print("Site parsing has finished")

        # We would expect DeferringList to be executed here
        # Emulating the iteration from the cl_scrape_opinions.py caller
        # in courtlistener
        try:
            for case in site.cases:
                case["case_name"]
        except ExpectedException:
            pass

        return True
