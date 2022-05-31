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

test_election_id = "recPTDvg1KWgN2dzx"
test_candidate_contest_id = 'recE0Oha5OnxNLFv4'
test_ballot_measure_id = 'recmwQAoKWid0DfqC'
test_gp_unit_id = 'recKCyQwhLDHp1cBD'
test_ballot_style_id = 'rec2vgozeUpYdIwac'

# fixtures
@pytest.fixture
def base():
    return Base(API_KEY, BASE_ID)

@pytest.fixture
def gp_unit(base):
    return edf.GpUnit(base, test_gp_unit_id)

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
def person(base):
    return edf.Person(base, test_person_id)


# tests
def test_gp_unit(gp_unit):
    assert gp_unit.Label == "Gadget"
    assert gp_unit.Name == "Gadget County"
    assert gp_unit.Type == "county"

def test_party(party):
    assert party.Label == "Hadronicrat"
    assert party.Name == "The Hadron Party of Farallon"
    assert party.Abbreviation == "HAD"

def test_office(office):
    assert office.Name == "Mayor"
    assert office.IsPartisan == True
    assert test_election_district_id in office.ElectionDistrict

def test_person(person):
    assert person.LastName == 'Jetson'
    assert person.FirstName == 'Jane'
    assert person.Profession == 'consultant'
