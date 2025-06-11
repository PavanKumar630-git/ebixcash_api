from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from get_ebixcash_data import *
from queries import *
import pyodbc

app = FastAPI()



@app.post("/get_ebixcash_data/")
async def get_ebixcash_data(
    pincode: str = Query(..., description="Pincode to search for agents")
):
    try:
        final_data = {}
        # Example logic using the pincode
        get_data = search_ebix_agents(pincode)

        if get_data.status_code == 200:
            final_data = extract_agents_from_html(get_data,pincode)

        return {
            "data":final_data,
            "pincode": pincode
        }

    except Exception as ee:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(ee)})
