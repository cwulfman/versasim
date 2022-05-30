import os
from pyairtable import Table, Base

api_key = "keyuXobQvG2xmGv1q"
base_id = "appTNDM2DwCS2vYun"

base = Base(api_key, base_id)

elections = Table(api_key, base_id, "Election")

