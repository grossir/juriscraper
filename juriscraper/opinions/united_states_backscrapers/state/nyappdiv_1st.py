# Back Scraper for New York Appellate Divisions 1st Dept.
# CourtID: nyappdiv_1st
# Court Short Name: NY
# Author: Andrei Chelaru
# Reviewer:
# Date: 2015-10-30

from juriscraper.opinions.united_states_backscrapers.state import ny


class Site(ny.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court = "App+Div,+1st+Dept"
        self.interval = 30
