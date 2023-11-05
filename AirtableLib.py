import wifiLib
import secrets
import urequests as requests

# Constants needed for accessing the right airtable data
baseId = secrets.AirtableBaseID
apiKey = secrets.AirtableAPIKey
colorID = secrets.AirtableColorID
tableName = "Tasks"

# Final formatting of url and header values
baseUrl = "https://api.airtable.com/v0/%s/%s" % (baseId, tableName)
headers = {"Authorization": f"Bearer {apiKey}",}

def getColor():
    try:
        # send get request to the right address
        response = requests.get(baseUrl, headers=headers)
        
        # Unpack the json response and return the color value
        data = response.json()
        records = data.get('records', [])
        for record in records:
            if record["id"] == colorID:
                print(record["fields"])
                return record["fields"]["Value"]
        return None
            
    except Exception as e:
        print(f"An error occurred: {e}")
