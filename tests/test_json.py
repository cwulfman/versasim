import pytest
from pyairtable import Base
import versasim.edf as edf


BASE_ID =  "appTNDM2DwCS2vYun"
API_KEY = "keyuXobQvG2xmGv1q"
test_candidate_id = "recGLBFPaB3zMDGem"
test_party_id = "recg6kdFZ9iBvR2nF"
test_office_id = "rec3uGFZUkRJjaxk0"
test_election_district_id = 'recbrO0CGN0P0C1mC'
test_person_id = 'recQ5Qc7GX6PN3VwJ'
test_candidate_id = 'recGLBFPaB3zMDGem'
nntest_candidate_contest_id = 'recE0Oha5OnxNLFv4'
test_election_id = "recPTDvg1KWgN2dzx"
test_ballot_measure_id = 'recmwQAoKWid0DfqC'
test_gp_unit_id = 'recKCyQwhLDHp1cBD'
test_ballot_style_id = 'rec2vgozeUpYdIwac'

identifiers = { 'farallon': 'rec5K8APzm54h7Vnj',
                'gadget_county': 'recKCyQwhLDHp1cBD',
                'orbit_city': 'recbrO0CGN0P0C1mC',
                'hadron_party': 'recg6kdFZ9iBvR2nF',
                'office_mayor': 'rec3uGFZUkRJjaxk0',
                'person_spacely': "recz2KGAdSdAzwgRq",
                'party_hadronicrat': 'recg6kdFZ9iBvR2nF',
                'party_leptonican': 'recxZqCzvl2XEKHYy',
                'candidate_selection_spacely': 'recPrSqz8XFt2Zbei',
                'candidate_spacely': 'recGLBFPaB3zMDGem',
                'candidate_cogswell': 'rec9I3CAGByPKmNef',
                'candidate_selection_cogswell': 'recGkMGp1IBfWi6vy',
                'candidate_contest_mayor': 'recE0Oha5OnxNLFv4',
                'ballot_measure_tax_increase': 'recmwQAoKWid0DfqC'
               }

dicts = {'farallon': {"@type": "ElectionResults.ReportingUnit",
                       "@id": "rec5K8APzm54h7Vnj",
                       "Type": "state",
                       "Name": {
                           "@type": "ElectionResults.InternationalizedText",
                           "Text": [{"@type": "ElectionResults.LanguageString",
                                   "Content": "The State of Farallon",
                                   "Label": "Farallon",
                                   "Language": "en"}]
                       }
                      },
         'office_mayor': { "@type": "ElectionResults.Office",
                "@id": "rec3uGFZUkRJjaxk0",
                    "IsPartisan": True,
                    "Name": {
                        "@type": "ElectionResults.InternationalizedText",
                        "Text": [
                            {
                                "@type": "ElectionResults.LanguageString",
                                "Language": "en",
                                "Label": "Mayor",
                                "Content": "Mayor of Orbit City"
                            }
                        ]
                    }
                   },
         'person_spacely': { "@type": "ElectionResults.Person",
                             "@id": "recz2KGAdSdAzwgRq",
                             "FirstName": "Cosmo",
                             "LastName": "Spacely",
                             "Profession": {
                                 "@type": "ElectionResults.InternationalizedText",
                                 "Text": [
                                     {
                                         "@type": "ElectionResults.LanguageString",
                                         "Language": "en",
                                         "Content": "magnate"
                                     }
                                 ]
                             }
                            },
         'party_leptonican': { "@type": "ElectionResults.Party",
                               "@id": "recxZqCzvl2XEKHYy",
                               "Name": {
                                   "@type": "ElectionResults.InternationalizedText",
                                   "Text": [
                                       {
                                           "@type": "ElectionResults.LanguageString",
                                           "Language": "en",
                                           "Label": "Leptonican",
                                           "Content": "The Lepton Party"
                                       }
                                   ]
                               },
                              },
         'candidate_spacely': {
                    "@type": "ElectionResults.Candidate",
                    "@id": "recGLBFPaB3zMDGem",
                    "PersonId": "recz2KGAdSdAzwgRq",
                    "BallotName": {
                        "Text": [
                            {
                                "Content": "Cosmo Spacely",
                                "Language": "en",
                                "@type": "ElectionResults.LanguageString"
                            }
                        ],
                        "@type": "ElectionResults.InternationalizedText"
                    },
                    "PartyId": "recxZqCzvl2XEKHYy"
                },
         'candidate_selection_spacely': { "@type": "ElectionResults.CandidateSelection",
                                          "@id": "recPrSqz8XFt2Zbei",
                                          "CandidateIds": ["recGLBFPaB3zMDGem"]
                                         },
         'candidate_contest_mayor':  {
                    "OfficeIds": ['rec3uGFZUkRJjaxk0'],
                    "VotesAllowed": 1,
                    "@type": "ElectionResults.CandidateContest",
                    "@id": "recE0Oha5OnxNLFv4",
                    "ContestSelection": [
                        {
                            "CandidateIds": ['recGLBFPaB3zMDGem'],
                            "@type": "ElectionResults.CandidateSelection",
                            "@id": "recPrSqz8XFt2Zbei"
                        },
                        {
                            "CandidateIds": ['rec9I3CAGByPKmNef'],
                            "@type": "ElectionResults.CandidateSelection",
                            "@id": "recGkMGp1IBfWi6vy"
                        },
                        {
                            "IsWriteIn": True,
                            "@type": "ElectionResults.CandidateSelection",
                            "@id": 'recm7Iu8kuvUyNLjd'
                        }
                    ],
                    "ElectionDistrictId": "recbrO0CGN0P0C1mC",
                    "Name": "Contest for Mayor of Orbit City",
                    "VoteVariation": "plurality"
                },
         'ballot_measure_tax_increase': {
                    "@type": "ElectionResults.BallotMeasureContest",
                    "@id": "recmwQAoKWid0DfqC",
                    "ElectionDistrictId": "recKCyQwhLDHp1cBD",
                    "Name": "Air Traffic Control Tax Increase",
                    "FullText": {
                        "@type": "ElectionResults.InternationalizedText",
                        "Text": [
                            {
                                "@type": "ElectionResults.LanguageString",
                                "Language": "en",
                                "Content": "Shall Gadget County increase its sales tax from 1% to 1.1% for the purpose of raising additional revenue to fund expanded air traffic control operations?"
                            }
                        ]
                    },
                    "ContestSelection": [
                        {
                            "Selection": {
                                "Text": [
                                    {
                                        "Content": "Yes",
                                        "Language": "en",
                                        "@type": "ElectionResults.LanguageString"
                                    }
                                ],
                                "@type": "ElectionResults.InternationalizedText"
                            },
                            "@type": "ElectionResults.BallotMeasureSelection",
                            "@id": "recu9g5t3w0eOMoVW"
                        },
                        {
                            "Selection": {
                                "Text": [
                                    {
                                        "Content": "No",
                                        "Language": "en",
                                        "@type": "ElectionResults.LanguageString"
                                    }
                                ],
                                "@type": "ElectionResults.InternationalizedText"
                            },
                            "@type": "ElectionResults.BallotMeasureSelection",
                            "@id": "rec6SD3XPXtW9KIhQ"
                        }
                    ]
                },
         "ordered_contest_mayor": { "@type": "ElectionResults.OrderedContest",
                                    "ContestId": "recE0Oha5OnxNLFv4",
                                    "OrderedContestSelectionIds":
                                    ['recPrSqz8XFt2Zbei', 'recGkMGp1IBfWi6vy', 'recm7Iu8kuvUyNLjd']
                                   }
         }

# fixtures
@pytest.fixture
def base():
    return Base(API_KEY, BASE_ID)

@pytest.fixture
def gadget_county(base):
    return edf.GpUnit(base, identifiers['gadget_county'])

@pytest.fixture
def farallon(base):
    return edf.GpUnit(base, identifiers['farallon'])

@pytest.fixture
def candidate(base):
    return edf.Candidate(base, test_candidate_id)

@pytest.fixture
def candidate_spacely(base):
    return edf.Candidate(base, identifiers['candidate_spacely'])

@pytest.fixture
def candidate_selection_spacely(base):
    return edf.CandidateSelection(base, identifiers['candidate_selection_spacely'])

@pytest.fixture
def party(base):
    return edf.Party(base, test_party_id)

@pytest.fixture
def party_leptonican(base):
    return edf.Party(base, identifiers['party_leptonican'])

@pytest.fixture
def office(base):
    return edf.Office(base, test_office_id)

@pytest.fixture
def office_mayor(base):
    return edf.Office(base, identifiers['office_mayor'])

@pytest.fixture
def person(base):
    return edf.Person(base, test_person_id)

@pytest.fixture
def person_spacely(base):
    return edf.Person(base, identifiers['person_spacely'])


@pytest.fixture
def candidate_contest(base):
    return edf.CandidateContest(base, test_candidate_contest_id)

@pytest.fixture
def ballot_measure_tax_increase(base):
    return edf.BallotMeasure(base, identifiers['ballot_measure_tax_increase'])

@pytest.fixture
def ballot_style(base):
    return edf.BallotStyle(base, test_ballot_style_id)

@pytest.fixture
def election(base):
    return edf.Election(base, test_election_id)

@pytest.fixture
def candidate_contest_mayor(base):
    return edf.CandidateContest(base, identifiers['candidate_contest_mayor'])

@pytest.fixture
def ordered_contest_mayor(base):
    contest = edf.CandidateContest(base, identifiers['candidate_contest_mayor'])
    return edf.OrderedContest(contest)

# tests
def test_gp_unit(farallon):
    assert farallon.as_dict() == dicts['farallon']

def test_office(office_mayor):
    assert office_mayor.as_dict() == dicts['office_mayor']

def test_person(person_spacely):
    assert person_spacely.as_dict() == dicts['person_spacely']

def test_party(party_leptonican):
    assert party_leptonican.as_dict() == dicts['party_leptonican']

def test_candidate(candidate_spacely):
    assert candidate_spacely.as_dict() == dicts['candidate_spacely']

def test_candidate_selection(candidate_selection_spacely):
    assert candidate_selection_spacely.as_dict() == dicts['candidate_selection_spacely']

def test_candidate_contest(candidate_contest_mayor):
    assert candidate_contest_mayor.as_dict() == dicts['candidate_contest_mayor']

def test_ballot_measure(ballot_measure_tax_increase):
    assert ballot_measure_tax_increase.as_dict() == dicts['ballot_measure_tax_increase']

def test_ordered_contest(ordered_contest_mayor):
    assert ordered_contest_mayor.as_dict() == dicts['ordered_contest_mayor']
