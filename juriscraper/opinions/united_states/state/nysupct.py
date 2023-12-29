# Scraper and Back Scraper for New York Commercial Division
# CourtID: nysupct
# Court Short Name: NY

from datetime import date

from juriscraper.opinions.united_states.state import nyappterm_1st


class Site(nyappterm_1st.Site):
    first_document_date = date(2004, 1, 2)
    search_interval_days = 180

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court = "Commercial Division"
        self.parameters.update({"court": self.court})
