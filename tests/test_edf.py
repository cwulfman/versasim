import pytest
from pyairtable import Base
import versasim.edf as edf

BASE_ID =  "appTNDM2DwCS2vYun"
API_KEY = "keyuXobQvG2xmGv1q"
test_candidate_id = "recGLBFPaB3zMDGem"
test_party_id = "recg6kdFZ9iBvR2nF"

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

# tests
def test_gp_unit(gp_unit):
    assert gp_unit.Label == "Gadget"
    assert gp_unit.Name == "Gadget County"
    assert gp_unit.Type == "county"

def test_party(party):
    assert party.Label == "Hadronicrat"
    assert party.Name == "The Hadron Party of Farallon"
    assert party.Abbreviation == "HAD"

