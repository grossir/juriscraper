"""
Scraper for the 
CourtID: nymisc
Court Short Name: ...
Court Contact: ...
Author: Gianfranco Rossi
History:
 - 2023-12-28, grossir: created
"""

from datetime import date

from juriscraper.opinions.united_states.state import nyappterm_1st


class Site(nyappterm_1st.Site):
    search_interval_days = 15
    first_document_date = date(2018, 1, 1)

    # First document available in this source for 'Other Courts'
    # is from 01/11/2001. Since Harvard's data https://cite.case.law/#ny
    # that we ingested contains opinions from these courts up to 2017
    # we don't backscrape to the beginning

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court = "Other Courts"
        self.parameters.update({"court": self.court})
