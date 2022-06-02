import json
from fastapi import FastAPI
from pyairtable import Base
from versasim import edf
from dotenv import load_dotenv, dotenv_values

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return json.JSONEncoder.default(self, o)

load_dotenv()
config = dotenv_values()

base = Base(config['API_KEY'], config['BASE_ID'])

elections_table = base.get_table('Election')

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Again"}

@app.get("/elections")
async def get_elections():
    elections = elections_table.all()

    return {"elections": elections}

@app.get("/elections/{election_id}")
async def get_election(election_id):
    election = edf.Election(base, election_id)
    return election.as_dict()

@app.get("/electionReport/{election_id}")
async def get_election_report(election_id):
    report = edf.ElectionReport(base) # ignore id for now and return all
    return report.generate_report()

@app.get("/gpunits")
async def get_gpunits():
    return base.get_table('GpUnit').all()

@app.get("/offices")
async def get_offices():
    return base.get_table('Office').all()

@app.get("/persons")
async def get_persons():
    pass

@app.get("/candidates")
async def get_candidates():
    pass

@app.get("/contests")
async def get_contests():
    pass

@app.get("/ballotstyles")
async def get_ballotstyles():
    pass
