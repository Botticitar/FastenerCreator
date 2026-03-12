from fastapi import FastAPI
from fastapi.responses import FileResponse

from src.stepgen_app.validator import #BaseModel instances for washer and bolt come here
from src.stepgen_app.step_generator import #model generator class comes here 

app=FastAPI()

@app.post