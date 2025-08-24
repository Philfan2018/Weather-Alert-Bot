import requests
import json
import datetime

"""
PowerPoint with VTEC explanation:
https://www.weather.gov/media/vtec/VTEC_explanation_ver9.pdf
"""

current_alerts_url = "https://api.weather.gov/alerts/active"

response = requests.get(current_alerts_url)
if response.status_code != 200:
    print(f"Error fetching data: {response.status_code}")
    weather_alerts_now = {}
else:
    weather_alerts_now = response.json()

weather_alerts_now = json.dumps(weather_alerts_now, indent=4)  # Pretty print the JSON data

# Checking to see the it works
# Print the json data
# print(weather_alerts_now)

# VTEC Alert Action Codes
event_condition_map = {
    "NEW": "New",
    "CON": "Continue",
    "EXT": "Extend",
    "EXA": "Expand Area",
    "EXB": "Expand Both",
    "UPG": "Upgrade",
    "CAN": "Cancel",
    "EXP": "Expire",
    "COR": "Correct",
    "ROU": "Routine"
}

WWA_type = {
    "W": "Warning",
    "A": "Watch",
    "Y": "Advisory",
    "S": "Statement",
    "F": "Forecast",
    "O": "Outlook",
    "N": "Synopsis"
}

# Reading in a separate json file that maps VTEC codes to their full names
VTEC_Alert_names_map = "vtec_wxalert_code.json"
with open(VTEC_Alert_names_map, "r") as file:
    vtec_alerts = json.load(file)

# Figuring out how to parse the json data
parsed_alerts = json.loads(weather_alerts_now)
for alert in parsed_alerts.get("features", []):
    properties = alert.get("properties", {})
    headline = properties.get("headline", "No headline available")
    description = properties.get("description", "No description available")
    flashflood = properties.get("flashFloodDetection", "No flash flood detection available")
    is_updated = properties.get("messageType", "No update status available")
    parameters = properties.get("parameters", {})
    vetc = parameters.get("VTEC", ["No VTEC data available"])
    eventCode = properties.get("eventCode", [["No event code available"]])
    SAME_code = eventCode.get("SAME", ["No SAME code available"])
    print(f"SAME Code: {SAME_code[0]}")
    
    """
    Special Weather Statements (SPS), Figure out later
    if SAME_code[0] == "SPS":
        Time_issued = properties.get("sent", "No time issued available")
        Time_issued_dt = datetime.datetime.fromisoformat(Time_issued.replace("Z", "+00:00"))
        Time_issued_str = Time_issued_dt.strftime("%Y%m%d%H%M")
        print(f"Severe Weather Statement issued at {Time_issued_str}")
        print("Severe Weather Statement - Skipping")
        continue
    """

    # print(f"Headline: {headline}\nDescription: {description}\n")
    # print(f"Flash Flood Detection: {flashflood}\nMessage Type: {is_updated}\n")

    # Skipping if no VTEC data is available
    if vetc == ["No VTEC data available"]:
        continue

    # Splitting the VTEC data into a list
    vtec_list = vetc[0].split(".")

    # Checking that the split worked
    # print(vtec_list)

    Alert_action = vtec_list[1]  # e.g., NEW/CON/EXT/EXA/EXB/UPG
    # CAN/EXP/COR/ROU

    WFO = vtec_list[2]  # e.g., KLZK/KSHV/KTSA/KAMA etc. 
    WFO_no_k = WFO[1:]   

    event_condition = event_condition_map.get(Alert_action, Alert_action)
    Alert_name = vtec_list[3]  # e.g., FFW/FFS/SVR/TOA etc.

    Alert_name_full = vtec_alerts.get(Alert_name, Alert_name)

    VTEC_WWA_type = vtec_list[4]  # e.g., W/A/Y/S/F/O/N

    WWA_type_full = WWA_type.get(VTEC_WWA_type, VTEC_WWA_type)
    print(f"{event_condition} {Alert_name_full} {WWA_type_full} issued by {WFO_no_k}\n")
    print(f"Headline: {headline}\nDescription: {description}\n")

    Warn_image_base_url = "https://mesonet.agron.iastate.edu/plotting/auto/plot/208/network" \
    ":WFO::wfo:CTP::year:2025::phenomenav:TO::significancev:W::etn:00001::opt:single::" \
    "n:auto::_r:t::dpi:100.png"
