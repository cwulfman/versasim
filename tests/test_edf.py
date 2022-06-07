import pytest
from pyairtable import Base
import versasim.edf as edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()



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
                'select_spacely': 'recPrSqz8XFt2Zbei'
               }

# fixtures
@pytest.fixture
def base():
    return Base(config['API_KEY'], config['TEST_BASE_ID'])

@pytest.fixture
def gadget_county(base):
    return edf.GpUnit(base, identifiers['gadget_county'])

@pytest.fixture
def candidate(base):
    return edf.Candidate(base, test_candidate_id)

@pytest.fixture
def party(base):
    return edf.Party(base, test_party_id)

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
def candidate(base):
    return edf.Candidate(base, test_candidate_id)

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
def test_gp_unit(gadget_county):
    assert gadget_county.Label == "Gadget"
    assert gadget_county.Name == "Gadget County"
    assert gadget_county.Type == "county"
    gpu_ids = [gpu.id for gpu in gadget_county.ComposingGpUnits]
    assert identifiers['orbit_city'] in gpu_ids

def test_party(party):
    assert party.Label == "Hadronicrat"
    assert party.Name == "The Hadron Party of Farallon"
    assert party.Abbreviation == "HAD"

def test_office(mayor):
    assert mayor.Label == "Mayor"
    assert mayor.Name == "Mayor of Orbit City"
    assert mayor.IsPartisan == True
    assert identifiers['orbit_city'] == mayor.ElectionDistrict.id

def test_person(person):
    assert person.LastName == 'Jetson'
    assert person.FirstName == 'Jane'
    assert person.Profession == 'consultant'

def test_candidate(candidate):
    assert candidate.BallotName == 'Cosmo Spacely'

def test_candidate_contest(candidate_contest):
    assert candidate_contest.Name == 'Contest for Mayor of Orbit City'
    assert candidate_contest.VoteVariation == 'plurality'
    assert candidate_contest.ElectionDistrict.id == identifiers['orbit_city']
    assert identifiers['select_spacely'] in [c.id for c in candidate_contest.ContestSelection]
    
def test_ballot_measure(ballot_measure):
    assert ballot_measure.Name == 'Air Traffic Control Tax Increase'
    assert ballot_measure.FullText == 'Shall Gadget County increase its sales tax from 1% to 1.1% for the purpose of raising additional revenue to fund expanded air traffic control operations?'

def test_election(election):
    assert election.Name == 'Special Election'
    assert election.Type == 'special'
    assert election.StartDate == '2022-06-14'
    assert election.EndDate == '2022-06-14'
