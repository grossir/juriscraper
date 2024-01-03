import unittest

from juriscraper.lib.importer import build_module_list
from juriscraper.OpinionSite import OpinionSite


class ScraperExtractFromText(unittest.TestCase):
    """Adds specific tests to specific courts that are more-easily tested
    without a full integration test.
    """

    test_data = {
        "juriscraper.opinions.united_states.administrative_agency.bia": [
            (
                """Matter of Emmanuel LAGUERRE, Respondent \nDecided January 20, 2022 and more """,
                {
                    "OpinionCluster": {
                        "date_filed": "2022-01-20",
                        "date_filed_is_approximate": False,
                    }
                },
            ),
            (
                "Matter of Enrique ALDAY-DOMINGUEZ, Respondent\nDecided June 1, 2017",
                {
                    "OpinionCluster": {
                        "date_filed": "2017-06-01",
                        "date_filed_is_approximate": False,
                    }
                },
            ),
        ],
        "juriscraper.opinions.united_states.state.nm": [
            (
                """Opinion Number: _______________ Filing Date: January 10, 2022\nNO. S-1-SC-38247\nCITIZENS FOR FAIR RATES""",
                {"OpinionCluster": {"docket_number": "S-1-SC-38247"}},
            )
        ],
        "juriscraper.opinions.united_states.state.nmctapp": [
            (
                """Opinion Number: _______________ Filing Date: January 10, 2022\nNo. A-1-CA-39059\nCITIZENS FOR FAIR RATES""",
                {"OpinionCluster": {"docket_number": "A-1-CA-39059"}},
            )
        ],
        "juriscraper.opinions.united_states.state.ark": [
            (
                """HONORABLE JODI RAINES DENNIS,\nCite as 2022 Ark. 19\nSUPREME COURT OF ARKANSAS No. CV-21-173\n  ARKANSAS DEPARTMENT OF CORRECTION""",
                {"OpinionCluster": {"docket_number": "CV-21-173"}},
            ),
            # Some opinions don't have dockets because Arkansas publishes important announcements.
            (
                """Cite as 2022 Ark. 14\nSUPREME COURT OF ARKANSAS Opinion Delivered: January 27, 2022""",
                {"OpinionCluster": {"docket_number": ""}},
            ),
        ],
        "juriscraper.opinions.united_states.state.arkctapp": [
            (
                """Cite as 2022 Ark. App. 51\nARKANSAS COURT OF APPEALS\nDIVISION II No. CV-20-579\n  ADDAM MAXWELL V.\nLORI MAXWELL""",
                {"OpinionCluster": {"docket_number": "CV-20-579"}},
            ),
            (
                """Cite as 2022 Ark. App. 43\nARKANSAS COURT OF APPEALS\nDIVISION IV No. E-21-215\n  FRED JACKSON""",
                {"OpinionCluster": {"docket_number": "E-21-215"}},
            ),
        ],
        "juriscraper.opinions.united_states.federal_appellate.ca4": [
            (
                """USCA4 Appeal: 22-6079      Doc: 17         Filed: 07/26/2022    Pg: 1 of 2\n\n\n\n\n                                            UNPUBLISHED \n\n                               UNITED STATES COURT OF APPEALS\n""",
                {"OpinionCluster": {"precedential_status": "Unpublished"}},
            ),
            (
                """USCA4 Appeal: 22-6079      Doc: 17         Filed: 07/26/2022    Pg: 1 of 2\n\n\n\n\n                                            PUBLISHED\n\n                               UNITED STATES COURT OF APPEALS\n""",
                {"OpinionCluster": {"precedential_status": "Published"}},
            ),
        ],
        "juriscraper.opinions.united_states.state.nyappterm_1st": [
            (
                """<br>PRESENT: Brigantti, J.P., Hagler, Tisch, JJ. \n\n <br>570410/22 \n and more and more """,
                {"Docket": {"docket_number": "570410/22"}},
            ),
        ],
        "juriscraper.opinions.united_states.state.nyappterm_2nd": [
            (
                """SUPREME COURT, APPELLATE TERM, FIRST DEPARTMENT \nPRESENT: Brigantti, J.P., Hagler, Tisch, JJ. \n 570613/17 """,
                {"Docket": {"docket_number": "570613/17"}},
            ),
        ],
        "juriscraper.opinions.united_states.state.nysupct": [
            (
                """<br>Index No. 154867/2022 Robert R. Reed, J. \nThe following """,
                {"Docket": {"docket_number": "154867/2022"}},
            ),
        ],
        "juriscraper.opinions.united_states.state.nymisc": [
            (
                # https://www.nycourts.gov/reporter/pdfs/2019/2019_32654.pdf
                """2019 NY Slip Op 32654(U)\nSeptember 4, 2019\nSupreme Court, New York County\nDocket Number: 654329/2018""",
                {"Docket": {"docket_number": "654329/2018"}},
            ),
            (
                # https://www.nycourts.gov/reporter/pdfs/2019/2019_30152.pdf
                """1809 Emns Ave Inc. v American Signcrafters LLC\n2019 NY Slip Op 30152(U)\nJanuary 10, 2019\nSupreme Court, Kings County\nDocket Number: 517955/18\nJudge: Leon Ruchelsman""",
                {"Docket": {"docket_number": "517955/18"}},
            ),
            (
                # https://www.nycourts.gov/reporter/pdfs/2021/2021_33275.pdf
                """Ciardiello v Village of New Paltz\n2021 NY Slip Op 33275(U)\nMarch 8, 2021\nSupreme Court, Ulster County\nDocket Number: Index No. EF18-3323\nJudge: Christopher E. Cahill""",
                {"Docket": {"docket_number": "EF18-3323"}},
            ),
            (
                # https://www.nycourts.gov/reporter/pdfs/2018/2018_33955.pdf
                """People v Wiltshire\n2018 NY Slip Op 33955(U)\nAugust 15, 2018\nCounty Court, Westchester County\nDocket Number: 18-0465-01\nJudge: Larry J. Schwartz""",
                {"Docket": {"docket_number": "18-0465-01"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2023/2023_23397.htm
                """City of New York v "Doe"\n2023 NY Slip Op 23397\nDecided on December 18, 2023\nCivil Court Of The City Of New York, Bronx County\nZellan, J.\nPublished by New York State Law Reporting Bureau pursuant to Judiciary Law § 431.\nThis opinion is uncorrected and subject to revision before publication in the printed Official Reports.\n\n\nDecided on December 18, 2023\nCivil Court of the City of New York, Bronx County\n\n\nCity of New York, Petitioner(s),\n\nagainst\n\n"John" "Doe"; "Jane" "Doe"; "John" "Doe"; "Jane" "Doe", Respondent(s).\n\n\n\n\nIndex No. LT-300755-22/BX""",
                {"Docket": {"docket_number": "LT-300755-22/BX"}},
            ),
            (
                # https://www.nycourts.gov/reporter/pdfs/2023/2023_32445.pdf
                """Rothman v Puretz\n2023 NY Slip Op 32445(U)\nJuly 18, 2023\nSupreme Court, Monroe County\nDocket Number: Index No. E2023001856\nJudge: J. Scott Odorisi\nCases posted with a "30000" identifier, i""",
                {"Docket": {"docket_number": "E2023001856"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2023/2023_51159.htm
                """Supreme Court, Monroe County\n\n\nJacek Woloszuk, Individually and as Executor\nof the Estate of ELLEN WOLOSZUK, deceased, Plaintiff,\n\nagainst\n\nWende Logan-Young, M.D., WENDE LOGAN-YOUNG, M.D. d/b/a ELIZABETH WENDE BREAST CLINIC, PHILIP MURPHY, M.D., SOUTHEAST OBSTETRICS & GYNECOLOGY, P.C. and RITA CLEMENT, M.D., Defendants.\n\n\n\n\nIndex No. I2009006547\n""",
                {"Docket": {"docket_number": "I2009006547"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2023/2023_50144.htm
                """Decided on February 28, 2023\nSurrogate's Court, Queens County\n\n\nProbate Proceeding, Will of Pia Jeong Yoon, a/k/a PIA JEONG AE YOON,\na/k/a PIA J. YOON, a/k/a JEONG YOON, a/k/a JEONG AE YOON, Deceased.\nFile No. 2021-31/C""",
                {"Docket": {"docket_number": "2021-31/C"}},
            ),
            (
                # https://www.nycourts.gov/reporter/pdfs/2021/2021_30613.pdf
                """Dodaj v Lofti\n2021 NY Slip Op 30613(U)\nJanuary 13, 2021\nSupreme Court, Bronx County\nDocket Number: 20240/2019E\nJudge: Veronica G. Hummel""",
                {"Docket": {"docket_number": "20240/2019E"}},
            ),
            (
                # http://www.nycourts.gov/reporter/pdfs/2021/2021_33610.pdf
                """D'Angelo v Kujawski\n2021 NY Slip Op 33610(U)\nJanuary 14, 2021\nSupreme Court, Suffolk County\nDocket Number: Index No. 620413-2016""",
                {"Docket": {"docket_number": "620413-2016"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2020/2020_50084.htm  Docket number seems to be censored
                """Decided on January 17, 2020\nCounty Court, Nassau County\n\n\nThe People of the State of New York, Plaintiff,\n\nagainst\n\nJ.S., Adolescent Offender.\n\nFYC-00000-00""",
                {"Docket": {"docket_number": "FYC-00000-00"}},
            ),
            (
                # https://www.nycourts.gov/reporter/pdfs/2020/2020_34495.pdf
                """Matter of Christopher J. A.\n2020 NY Slip Op 34495(U)\nMarch 16, 2020\nSurrogate's Court, Bronx County\nDocket Number: 81G1998/K""",
                {"Docket": {"docket_number": "81G1998/K"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2018/2018_50128.htm
                "The People of the State of New York\n\nagainst\n\nAmela Hot, Defendant.\n2017KN054132\nLabe M. Richman, 305 Broadway, Suite 100, New York, New York, 10007,",
                {"Docket": {"docket_number": "2017KN054132"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2018/2018_50128.htm
                "The People of the State of New York\n\nagainst\n\nAmaury Guzman, Defendant.\nDocket No. CR-014209-22NY",
                {"Docket": {"docket_number": "CR-014209-22NY"}},
            ),
            (
                # https://www.nycourts.gov/reporter/pdfs/2022/2022_31361.pdf
                """McDonough v 50 E. 96th St., LLC\n2022 NY Slip Op 31361(U)\nMay 19, 2022\nSupreme Court, Broome County\nDocket Number: Index No. EFCA2020001541\nJudge: Eugene D. Faughnan""",
                {"Docket": {"docket_number": "EFCA2020001541"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2021/2021_50464.htm
                """Surrogate's Court, Nassau County\nIn the Matter of the Accounting by Public Administrator of Nassau County, as the Administrator of the Estate of Joseph W. Honor, Deceased.\n\n\n\n\n96764/C""",
                {"Docket": {"docket_number": "96764/C"}},                                
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2021/2021_50022.htm
                """Decided on January 14, 2021\nFamily Court, Bronx County\n\n\nIn the Matter of a Support Proceeding, R.O., Petitioner,\n\nagainst\n\nE.R.R., Respondent.\nF-28630-19/19A\n""",
                {"Docket": {"docket_number": "F-28630-19/19A"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2018/2018_50503.htm
                """Criminal Court of the City of New York, Queens County\n\n\nThe People of the State of New York, Plaintiff,\n\nagainst\n\nJames Smith, Defendant.\nnCR-024874-17QN""",
                {"Docket": {"docket_number": "CR-024874-17QN"}},
            ),
            (
                # https://www.nycourts.gov/reporter/pdfs/2018/2018_33709.pdf
                """Matter of Micklas v Town of Halfmoon Planning Bd.\n2018 NY Slip Op 33709(U)\nJanuary 10, 2018\nSupreme Court, Saratoga County\n Docket Number: 20171554""",
                {"Docket": {"docket_number": "20171554"}},
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2020/2020_50049.htm"
                """Family Court, Kings County\nIn the Matter of a Proceeding Under Article 6 of the Family Court Act Robyn C., Petitioner,\n\nagainst\n\nWilliam M. J. (Deceased) and EVA JANE P., Respondent.\nG-10994-19""",
                {"Docket": {"docket_number": "G-10994-19"}}
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2022/2022_50020.htm
                """'Family Court, Kings County\nIn the Matter of a Proceeding for Support Under Article 4 of the Family Court Act Michelle B., Petitioner,\n\nagainst\n\nThomas Y., Respondent.\nDocket No. F-30317/2004/19F""",
                {"Docket": {"docket_number": "F-30317/2004/19F"}}
            ),
            (
                # https://www.nycourts.gov/reporter/3dseries/2023/2023_50204.htm
                """Court of Claims\n\n\nBernardo Martinaj, Claimant,\n\nagainst\n\nState of New York, Defendant.\n\n\n\n\nClaim No. 136323-A""",
                {"Docket": {"docket_number": "136323-A"}}
            )
            

        ],
        "juriscraper.opinions.united_states.state.sd": [
            (
                """#30018-a-MES\n2023 S.D. 4""",
                {"Docket": {"docket_number": "#30018-a-MES"}},
            ),
        ],
        "juriscraper.opinions.united_states.territories.nmariana": [
            (
                """#E-FILED\nCNMI SUPREME COURT\nE-filed: Apr 18 2022 06:53AM\nClerk Review: Apr 18 2022 06:54AM Filing ID: 67483376\nCase No.: 2021-SCC-0017-CIV\nJudy Aldan""",
                {"Docket": {"docket_number": "2021-SCC-0017-CIV"}},
            ),
        ],
        "juriscraper.opinions.united_states.state.colo": [
            (
                """       The Supreme Court of the State of Colorado 2 East 14th Avenue • Denver, Colorado 80203                                  2023 CO 63 Supreme Court Case No. 23SA300""",
                {
                    "Citation": {
                        "volume": "2023",
                        "reporter": "CO",
                        "page": "63",
                    }
                },
            ),
        ],
        "juriscraper.opinions.united_states.federal_special.cavc": [
            (
                """           UNITED STATES COURT OF APPEALS FOR VETERANS CLAIMS\n\n                                             NO. 22-3306\n\n                               GEORGE D. PREWITT, JR., PETITIONER,\n\n                                                  V.\n\n                                     DENIS MCDONOUGH,\n                         SECRETARY OF VETERANS AFFAIRS, RESPONDENT.\n\n                       Before""",
                {
                    "OpinionCluster": {
                        "case_name": "George D. Prewitt, Jr. v. Denis McDonough"
                    }
                },
            ),
            (
                """          UNITED STATES COURT OF APPEALS FOR VETERANS CLAIMS\n\n                                            No. 17-1428\n\n                                  JESUS G. ATILANO, APPELLANT,\n\n                                                 V.\n\n                                    DENIS MCDONOUGH,\n                          SECRETARY OF VETERANS AFFAIRS, APPELLEE.\n\n               On Remand""",
                {
                    "OpinionCluster": {
                        "case_name": "Jesus G. Atilano v. Denis McDonough"
                    }
                },
            ),
            (
                """                UNITED STATES COURT OF APPEALS FOR VETERANS CLAIMS\n\nNO. 20-4372\n\nSHERRY CRAIG-DAVIDSON,                                                            APPELLANT,\n\n         V.\n\nDENIS MCDONOUGH,\nSECRETARY OF VETERANS AFFAIRS,                                                    APPELLEE.\n\n                      Before GREENBERG, MEREDITH, and LAURER, Judges.""",
                {
                    "OpinionCluster": {
                        "case_name": "Sherry Craig-Davidson v. Denis McDonough"
                    }
                },
            ),
        ],
        "juriscraper.opinions.united_states.federal_bankruptcy.bap1": [
            (
                """UNITED STATES BANKRUPTCY APPELLATE PANEL\n           FOR THE FIRST CIRCUIT\n                      _______________________________\n\n                            BAP No. MW 00-005\n                      _______________________________\n\n              IN RE: INDIAN MOTOCYCLE CO., INC. ,\n       INDIAN MOTOCYCLE APPAREL AND ACCESSORIES, INC.\n              INDIAN MOTOCYCLE MANUF CO., INC.,\n                              Debtors.\n                  _______________________________\n\n                      UNITED STATES OF AMERICA,\n                               Appellant,\n\n                                       v.\n\n        STERLING CONSULTING CORP., COLORADO RECEIVER\n          and STEVEN M. RODOLAKIS, CHAPTER 7 TRUSTEE,\n                             Appellees.\n                  _______________________________\n\n               Appeal from the United States Bankruptcy Court\n                 for the District of Massachusetts (Worcester)\n                (Hon. Henry J. Boroff, U.S. Bankruptcy Judge)\n\n                      _______________________________\n\n                             Before\n         GOODMAN, DE JESÚS, VAUGHN, U.S. Bankruptcy Judges\n                _______________________________\n\n  Peter Sklarew, U.S. Department of Justice, and Donald K. Stern, U.S. Attorney, on\n  brief for the Appellant.\n\n  Joseph H. Baldiga, Paul W. Carey of Mirick, O’Connell, DeMallie & Lougee and\n  Stephan M. Rodolakis, Mark S. Foss of Peters Massad & Rodolakis, on brief for the\n  Appellees.\n\n                      _______________________________\n\n                               April 26, 2001\n                      _______________________________\n\n""",
                {
                    "OpinionCluster": {"date_filed": "April 26, 2001"},
                },
            ),
        ],
    }

    def test_extract_from_text(self):
        """Test that extract_from_text returns the expected data."""
        for module_string, test_cases in self.test_data.items():
            package, module = module_string.rsplit(".", 1)
            mod = __import__(
                f"{package}.{module}", globals(), locals(), [module]
            )
            site = mod.Site()
            for test_case in test_cases:
                self.assertEqual(
                    site.extract_from_text(test_case[0]), test_case[1]
                )

    def test_extract_from_text_properly_implemented(self):
        """Ensure that extract_from_text is properly implemented."""

        module_strings = build_module_list(
            "juriscraper.opinions.united_states"
        )
        for module_string in module_strings:
            package, module = module_string.rsplit(".", 1)
            mod = __import__(
                f"{package}.{module}", globals(), locals(), [module]
            )
            site = mod.Site()
            if mod.Site.extract_from_text == OpinionSite.extract_from_text:
                # Method is not overridden, so skip it.
                continue
            self.assertIn(
                module_string,
                self.test_data.keys(),
                msg=f"{module_string} not yet added to extract_from_text test data.",
            )
