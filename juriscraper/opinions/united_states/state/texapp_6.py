# Scraper for Texas 6th Court of Appeals
# CourtID: texapp6
# Court Short Name: TX
# Author: Andrei Chelaru
# Reviewer: mlr
# Date: 2014-07-10


from juriscraper.opinions.united_states.state import texapp_1


class Site(texapp_1.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.court_name = "capp_6"
        self.checkbox = 7
