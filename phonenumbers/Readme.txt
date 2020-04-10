This is a mini web project that parses a text file with phone numbers and return the list through a REST interface.
Example: 127.0.0.1:8000/phonenumbers

To bring up the server:
Python3
1. Run pip install -r requirements.txt
2. CD into \phonenumbers
3. Execute: uvicorn main:app --reload
4. Browse to 127.0.0.1:8000/phonenumbers