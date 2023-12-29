"""
Scraper for New York Court of Appeals
CourtID: ny
Court Short Name: NY
History:
    2015-10-27  Created by Andrei Chelaru
    2023-12-29, grossir: Adapted to changes in base class
"""
from datetime import date

from juriscraper.opinions.united_states.state.nyappterm_1st import (
    Site as NySite,
)


class Site(NySite):
    first_document_date = date(2003, 6, 1)
    last_backscraper_date = date(2016, 1, 1)
    search_interval_days = 200

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court = "Court of Appeals"
        self.parameters.update({"court": self.court})
