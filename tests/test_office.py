import pytest
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

identifiers = {'office_mayor': 'rec3uGFZUkRJjaxk0',
               'orbit_city': 'recbrO0CGN0P0C1mC'}


@pytest.fixture
def base():
    return Base(config['API_KEY'], config['TEST_BASE_ID'])

@pytest.fixture
def mayor(base):
    return edf.Office(base, identifiers['office_mayor'])

@pytest.fixture
def name(mayor):
    return {"@type": "ElectionResults.InternationalizedText",
            "Text": [
                {
                    "@type": "ElectionResults.LanguageString",
                    "Language": "en",
                    "Content": "Mayor of Orbit City"
                }
            ],
            "Label": "Mayor"
            }


def test_object(mayor):
    assert mayor.Label == "Mayor"
    assert mayor.Name == "Mayor of Orbit City"
    assert mayor.IsPartisan == True
    assert identifiers['orbit_city'] == mayor.ElectionDistrict.id

def test_dict(mayor, name):
    values = mayor.as_dict()
    assert values['@type'] == 'ElectionResults.Office'
    assert values['IsPartisan'] == True
    assert values['Name'] == name
