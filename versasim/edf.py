""" Airtable interface. """

from datetime import datetime
from pyairtable import Base, Table

def language_string(content, language="en"):
    """returns a dictionary-model of a LanguageString"""
    return {"@type": "ElectionResults.LanguageString",
            "Content": content,
            "Language": language}

def internationalized_text(content, label='', language="en"):
    """returns a dictionary-model of an InternationalizedText"""

    data = {"@type": "ElectionResults.InternationalizedText",
            "Text": [language_string(content, language)]}
    if label:
        data['Label'] = label

    return data

class Edf():
    def __init__(self, base, id, table, type):
        self.type = type
        self.base = base
        self.id = id
        self.record = base.get(table, id)['fields']


class GpUnit(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'GpUnit',
                         'ElectionResults.ReportingUnit')
        self.Label = self.record['Label']
        self.Name = self.record['Name']
        self.Type = self.record['Type']
        self._composing_gp_units = []

    @property
    def ComposingGpUnits(self):
        if not self._composing_gp_units:
            self._composing_gp_units =[GpUnit(self.base, unit_id)
                                    for unit_id
                                    in self.record['ComposingGpUnits']]
        return self._composing_gp_units

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Type": self.Type,
                "Name": internationalized_text(self.Name, self.Label)
                }
        return data


class Party(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Party',
                         'ElectionResults.Party')
        self.Label = self.record['Label']
        self.Name = self.record['Name']
        self.Abbreviation = self.record['Abbreviation']

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Name": internationalized_text(self.Name, self.Label)
                }
        return data


class Office(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Office',
                         'ElectionResults.Office')
        if 'Name' in self.record:
            self.Name = self.record['Name']
        self.Label = self.record['Label']
        if 'IsPartisan' in self.record:
            self.IsPartisan = self.record['IsPartisan']
        self._election_district = None

    @property
    def ElectionDistrict(self):
        if not self._election_district:
            if 'ElectionDistrict' in self.record:
                self._election_district = GpUnit(self.base,
                                                 self.record['ElectionDistrict'][0])
        return self._election_district

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "IsPartisan": True,
                "Name": internationalized_text(self.Name, self.Label)
                }
        return data


class Person(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Person',
                         'ElectionResults.Person')
        self.LastName = self.record['LastName']
        self.FirstName = self.record['FirstName']
        self.Profession = self.record['Profession']

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "FirstName": self.FirstName,
                "LastName": self.LastName,
                "Profession": internationalized_text(self.Profession)}
        return data


class Candidate(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'Candidate',
                         'ElectionResults.Candidate')
        self.BallotName = self.record['BallotName']

        self._person = None
        self._party = None


    @property
    def Person(self):
        if not self._person:
            if 'Person' in self.record:
                self._person = Person(self.base, self.record['Person'][0])
        return self._person

    @property
    def Party(self):
        if not self._party:
            if 'Party' in self.record:
                self._party = Party(self.base, self.record['Party'][0])
        return self._party


    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "PersonId": self.Person.id,
                "BallotName": internationalized_text(self.BallotName),
                "PartyId": self.Party.id}
        return data


class CandidateSelection(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier, 'CandidateSelections',
                         'ElectionResults.CandidateSelection')
        self.CandidateIds = self.record['Candidates']
        self.Label = self.record['Label']
        if 'IsWriteIn' in self.record:
            self.IsWriteIn = self.record['IsWriteIn']
        else:
            self.IsWriteIn = False

    def as_dict(self):
        data = {"@type": self.type, "@id": self.id}
        if self.IsWriteIn:
            data["IsWriteIn"] = True
        else:
            data["CandidateIds"] = self.CandidateIds

        return data


class Contest(Edf):
    def __init__(self, base, id, table, type):
        super().__init__(base, id, table, type)
        self.Abbreviation = None
        self.BallotSubTitle = None
        self.BallotTitle = None
        self.ContestSelection = []
        self.ElectionDistrict = GpUnit(base,
                                       self.record['ElectionDistrict'][0])
        self.Name = self.record['Name']
        if 'VoteVariation' in self.record:
            self.VoteVariation = self.record['VoteVariation']
        self.ContestSelection = []


class CandidateContest(Contest):
    def __init__(self, base, id):
        super().__init__(base, id, 'CandidateContest',
                         'ElectionResults.CandidateContest')
        self.VotesAllowed = self.record['VotesAllowed']
        self.Office = self.record['Office']

        if 'ContestSelections' in self.record:
            self.ContestSelection = [CandidateSelection(self.base, selection_id)
                                     for selection_id
                                     in self.record['ContestSelections']]

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Name": self.Name,
                "OfficeIds": self.Office,
                "VoteVariation": self.VoteVariation,
                "VotesAllowed": self.VotesAllowed,
                "ElectionDistrictId": self.ElectionDistrict.id,
                "ContestSelection": [selection.as_dict()
                                     for selection
                                     in self.ContestSelection]
                }
        return data


class BallotMeasure(Contest):
    def __init__(self, base, id):
        super().__init__(base, id, 'BallotMeasure',
                         'ElectionResults.BallotMeasureContest')
        self.FullText = self.record['FullText']
        if 'ContestSelections' in self.record:
            self.ContestSelection = [BallotMeasureSelection(self.base,
                                                            selection_id)
                                     for selection_id
                                     in self.record['ContestSelections']]

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "ElectionDistrictId": self.ElectionDistrict.id,
                "Name": self.Name,
                "FullText": internationalized_text(self.FullText),
                "ContestSelection": [selection.as_dict()
                                     for selection
                                     in self.ContestSelection]
                }
        return data


class BallotMeasureSelection(Edf):
    def __init__(self, base, identifier):
        super().__init__(base, identifier,
                         'BallotMeasureSelections',
                         'ElectionResults.BallotMeasureSelection')
        self.Selection = self.record['Selection']

    def as_dict(self):
        data = {"@type": self.type,
                "@id": self.id,
                "Selection": internationalized_text(self.Selection)}
        return data


class OrderedContest(Edf):
    def __init__(self, contest_object):
        self.type = 'ElectionResults.OrderedContest'
        self.Contest = contest_object
        self.OrderedContestSelection = self.Contest.ContestSelection

    def as_dict(self):
        data = {"@type": self.type,
                "ContestId": self.Contest.id,
                "OrderedContestSelectionIds":
                [selection.id
                 for selection
                 in self.OrderedContestSelection]}
        return data


class BallotStyle(Edf):
    def __init__(self, base, id):
        super().__init__(base, id, 'BallotStyle',
                         'ElectionResults.BallotStyle')
        if 'Name' in self.record:
            self.name = internationalized_text(self.record['Name'])

        if 'GpUnits' in self.record:
            self.GpUnit = self.record['GpUnits']
        self._contests = []
        if 'Contests' in self.record:
            self._contests += [CandidateContest(base, id)
                               for id in
                               self.record['Contests']]
        if 'BallotMeasures' in self.record:
            self._contests += [BallotMeasure(base, id)
                               for id in
                               self.record['BallotMeasures']]

    @property
    def OrderedContests(self):
        return [OrderedContest(contest) for contest in self._contests]

    def as_dict(self):
        data = {"@type": self.type,
                "GpUnitIds": self.record['GpUnits'],
                "OrderedContent": [c.as_dict() for c in self.OrderedContests]}
        return data


class Election(Edf):
    def __init__(self, base, id, precinct=None):
        super().__init__(base, id, "Election", "ElectionResults.Election")
        candidate_contests = [CandidateContest(base, id)
                              for id in
                              self.record['CandidateContest']]
        ballot_measure_contests = [BallotMeasure(base, id)
                                   for id in
                                   self.record['BallotMeasure']]
        self.Contest = candidate_contests + ballot_measure_contests
        ballot_styles = [BallotStyle(base, id)
                            for id in
                            self.record['BallotStyle']]
        if precinct:
            filt = filter(lambda x: precinct in x.GpUnit, ballot_styles)
            self.BallotStyle = list(filt)
        else:
            self.BallotStyle = ballot_styles

        self.Name = self.record['Name']
        self.StartDate = self.record['StartDate']
        self.EndDate = self.record['EndDate']
        self.Type = self.record['Type']
        self.ElectionScopeId = self.record['ElectionScope'][0]

    def ballot_style_for(self, precinct_id):
        filt = filter(lambda x: precinct_id in x.GpUnit, self.BallotStyle)
        return list(filt)

    def as_dict(self):
        data = {"@type": self.type,
                "ElectionScopeId": self.ElectionScopeId,
                "StartDate": self.StartDate,
                "EndDate": self.EndDate,
                "Type": self.Type,
                "Name": internationalized_text(self.Name),
                "Contest": [c.as_dict() for c in self.Contest],
                "BallotStyle": [b.as_dict() for b in self.BallotStyle]
                }

        return data


class ElectionReport(Edf):
    def __init__(self, base, election_id=None, precinct_id=None):
        self.type = "ElectionResults.ElectionReport"
        self.base = base
        if election_id:
            self.Election = [Election(self.base, election_id, precinct_id)]
        else:
            self.Election = [Election(self.base, id, precinct_id)
                             for id in self.record_ids('Election')]

        self.Party = [Party(self.base, id)
                      for id in self.record_ids('Party')]

        self.GpUnit = [GpUnit(self.base, id)
                       for id in self.record_ids('GpUnit')]

        self.Office = [Office(self.base, id)
                       for id in self.record_ids('Office')]

        self.Person = [Person(self.base, id)
                       for id in self.record_ids('Person')]

    def record_ids(self, table_name):
        return [r['id'] for r in self.base.get_table(table_name).all()]

    def report_for(self, election_id, precinct_id):
        election = Election(self.base, election_id)
        ballot_style = election.ballot_style_for(precinct_id)
        self.BallotStyle = [ballot_style]
        return self

    def as_dict():
        report = {"@type": "ElectionResults.ElectionReport",
                  "Format": "precinct-level",
                  "GeneratedDate":
                  datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "VendorApplicationId": "ElectionReporter",
                  "Issuer": "TrustTheVote",
                  "IssuerAbbreviation": "TTV",
                  "Status": "pre-election",
                  "SequenceStart": 1,
                  "SequenceEnd": 1,
                  "Election": [e.as_dict() for e in self.Election],
                  "GpUnit": [g.as_dict() for g in self.GpUnit],
                  "Party": [p.as_dict() for p in self.Party],
                  "Office": [o.as_dict() for o in self.Office],
                  "Person": [p.as_dict() for p in self.Person]}
        return report
