import pytest
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

identifiers = {'farallon': 'rec5K8APzm54h7Vnj',
               'gadget_county': 'recKCyQwhLDHp1cBD',
               'orbit_city': 'recbrO0CGN0P0C1mC'}


@pytest.fixture
def base():
    return Base(config['API_KEY'], config['BASE_ID'])

@pytest.fixture
def gadget_county(base):
    return edf.GpUnit(base, identifiers['gadget_county'])


@pytest.fixture
def gadget_county_name(gadget_county):
    return {"@type": "ElectionResults.InternationalizedText",
            "Label": "Gadget",
            "Text": [{"@type": "ElectionResults.LanguageString",
                      "Language": "en",
                      "Content": "Gadget County"}]}


def test_object(gadget_county):
    assert gadget_county.type == "ElectionResults.ReportingUnit"
    assert gadget_county.id == "recKCyQwhLDHp1cBD"
    assert gadget_county.Label == "Gadget"
    assert gadget_county.Name == "Gadget County"
    assert gadget_county.Type == "county"
    gpu_ids = [gpu.id for gpu in gadget_county.ComposingGpUnits]
    assert identifiers['orbit_city'] in gpu_ids

def test_dict(gadget_county, gadget_county_name):
    values = gadget_county.as_dict()
    assert values['@type'] == 'ElectionResults.ReportingUnit'
    assert values['Type'] == 'county'
    assert values['Name'] == gadget_county_name
