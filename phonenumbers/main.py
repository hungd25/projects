from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from phonenumbers import get_phone_numbers

app = FastAPI()
phone_list = get_phone_numbers()
response = {'Description': 'List of phone numbers', 'Count': len(phone_list),
            'Phone Numbers': phone_list, 'timestamp': str(datetime.now())}

@app.get("/")
async def root():
    return {"message": "Get phone numbers"}


@app.get("/phonenumbers")
async def get_phone_numbers():
    return JSONResponse(response)