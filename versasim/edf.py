""" Airtable interface. """

from datetime import datetime
from pyairtable import Base, Table

def language_string(content, language="en"):
    return {"@type": "ElectionResults.LanguageString",
            "Content": content,
            "Language": language}

def internationalized_text(content, language="en"):
    return {"@type": "ElectionResults.InternationalizedText",
            "Text": language_string(content, language)}


def gp_unit(record):
    fields = record['fields']
    return {"@type": "ElectionResults.ReportingUnit",
            "@id": record['id'],
            "Name": internationalized_text(fields['Name'])}

def election(record):
    fields = record['fields']
    data = {"@type": "ElectionResults.Election",
            "@id": record['id'],
            "Type": fields['Type'],
            "StartDate": fields['StartDate'],
            "EndDate": fields['EndDate'],
            "ElectionScopeId": fields['ElectionScope'],
            "Name": internationalized_text(fields['Name'])
            }
    return data    


class ElectionReporter:
    def __init__(self, base_id, api_key):
        self._base_id = base_id
        self._api_key = api_key
        self._base = Base(self._api_key, self._base_id)
        self._election_table = None
        self.election_reports = []

    @property
    def election_table(self):
        if not self._election_table:
            self._election_table = self._base.get_table("Election")
        return self._election_table

    @property
    def elections(self):
        elections_list = []
        for record in self.election_table.all():
            data = {"id": record['id']}
            elections_list.append(data)
        return elections_list

    def generate_election_report(self, election_id):
        report = {
            "@type": "ElectionResults.ElectionReport",
            "Format": "precinct-level",
            "GeneratedDate" : datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "VendorApplicationId": "ElectionReporter",
            "Issuer": "TrustTheVote",
            "IssuerAbbreviation": "TTV",
            "SequenceStart": 1,
            "SequenceEnd": 1
        }
        election_record = self.election_table.get(election_id)
        report['Election'] = [election(election_record)]
        return report
