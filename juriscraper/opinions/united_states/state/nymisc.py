"""
Scraper for the 
CourtID: nymisc
Court Short Name: ...
Court Contact: ...
Author: Gianfranco Rossi
History:
 - 2023-12-28, grossir: created
"""

from juriscraper.opinions.united_states.state import nyappterm_1st


class Site(nyappterm_1st.NYSlipDecisionsSite):
    court = "Other Courts"
    first_document_date = "01/11/2001"
    search_interval_days = 15
    