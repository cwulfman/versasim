import pytest
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

candidate_spacely_id = 'recGLBFPaB3zMDGem'

@pytest.fixture
def base():
    return Base(config['API_KEY'], config['TEST_BASE_ID'])

@pytest.fixture
def candidate_spacely(base):
    return edf.Candidate(base, candidate_spacely_id)

def test_candidate_id(candidate_spacely):
    assert candidate_spacely.id == candidate_spacely_id

def test_candidate_party(candidate_spacely):
    assert candidate_spacely.Party.Name == 'The Lepton Party'

def test_candidate_ballot_name(candidate_spacely):
    assert candidate_spacely.BallotName == 'Cosmo Spacely'

def test_candidate_person(candidate_spacely):
    assert candidate_spacely.Person.LastName == 'Spacely'
