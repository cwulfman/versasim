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
test_candidate_contest_id = 'recE0Oha5OnxNLFv4'
test_election_id = "recPTDvg1KWgN2dzx"
test_ballot_measure_id = 'recmwQAoKWid0DfqC'
test_gp_unit_id = 'recKCyQwhLDHp1cBD'
test_ballot_style_id = 'rec2vgozeUpYdIwac'

identifiers = { 'farallon': 'rec5K8APzm54h7Vnj',
                'gadget_county': 'recKCyQwhLDHp1cBD',
                'orbit_city': 'recbrO0CGN0P0C1mC',
                'hadron_party': 'recg6kdFZ9iBvR2nF',
                'mayor': 'rec3uGFZUkRJjaxk0',
                'person_spacely': "recz2KGAdSdAzwgRq",
                'party_hadronicrat': 'recg6kdFZ9iBvR2nF',
                'party_leptonican': 'recxZqCzvl2XEKHYy',
                'select_spacely': 'recPrSqz8XFt2Zbei',
                'candidate_spacely': 'recGLBFPaB3zMDGem'
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
         'mayor': { "@type": "ElectionResults.Office",
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
def party(base):
    return edf.Party(base, test_party_id)

@pytest.fixture
def party_leptonican(base):
    return edf.Party(base, identifiers['party_leptonican'])

@pytest.fixture
def office(base):
    return edf.Office(base, test_office_id)

@pytest.fixture
def mayor(base):
    return edf.Office(base, identifiers['mayor'])

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
def ballot_measure(base):
    return edf.BallotMeasure(base, test_ballot_measure_id)

@pytest.fixture
def ballot_style(base):
    return edf.BallotStyle(base, test_ballot_style_id)

@pytest.fixture
def election(base):
    return edf.Election(base, test_election_id)

# tests
def test_gp_unit(farallon):
    assert farallon.as_dict() == dicts['farallon']

def test_office(mayor):
    assert mayor.as_dict() == dicts['mayor']

def test_person(person_spacely):
    assert person_spacely.as_dict() == dicts['person_spacely']

def test_party(party_leptonican):
    assert party_leptonican.as_dict() == dicts['party_leptonican']

def test_candidate(candidate_spacely):
    assert candidate_spacely.as_dict() == dicts['candidate_spacely']
