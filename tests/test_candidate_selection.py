import pytest
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

selection_spacely_id = 'recPrSqz8XFt2Zbei'
candidate_spacely_id = 'recGLBFPaB3zMDGem'

@pytest.fixture
def base():
    return Base(config['API_KEY'], config['TEST_BASE_ID'])

@pytest.fixture
def select_spacely(base):
    return edf.CandidateSelection(base, selection_spacely_id)

@pytest.fixture
def candidate_spacely(base):
    return edf.Candidate(base, candidate_spacely_id)

def test_for_candidate(select_spacely, candidate_spacely):
    assert select_spacely.CandidateIds[0] == candidate_spacely.id
