import requests
from bs4 import BeautifulSoup
import json
from multiprocessing.dummy import Pool as ThreadPool
import time


def get_detections_list(soup, table_name):

    table_body = soup.find(id=table_name).find("tbody")
    table_contents = table_body.find_all("td")

    detection_names = [name.find("a").text for name in table_contents if name.find("a")]
    
    return detection_names

def get_update_info(update_num):
    response = requests.get("https://www.microsoft.com/en-us/wdsi/definitions/antimalware-definition-release-notes?requestVersion=" + update_num)
    soup = BeautifulSoup(response.content, 'html.parser')

    result = {
        "update_id": update_num,
        "update_url": "https://www.microsoft.com/en-us/wdsi/definitions/antimalware-definition-release-notes?requestVersion=" + update_num,
        "update_date": soup.find(id="releaseDate_0").text
    }

    try:
        result["update_added_detections"] = get_detections_list(soup, "gvAddedThreatsTable")
    except:
        result["update_added_detections"] = []

    try:
        result["update_updated_detections"] = get_detections_list(soup, "gvUpdatedThreatsTable")
    except:
        result["update_updated_detections"] = []

    return result
start = time.time()

response = requests.get("https://www.microsoft.com/en-us/wdsi/definitions/antimalware-definition-release-notes")
soup = BeautifulSoup(response.content, 'html.parser')

# get list of all signature options
options = soup.find(id="comboVersionList")
options = [item.text.strip() for item in options if item != '\n']

# this is where we'll store all update information
updates = []

# for each update version, we need to get the data
# data needed:
# string -> update version number
# string -> update date
# list -> Added threat detections
# list -> Updated threat detections
with ThreadPool(20) as pool:
    updates = pool.map(get_update_info, options)

end = time.time()
print(f"scraped {len(options)} updates in {end - start} s")

# once we have the data, write to file
with open("update_data.json", 'w') as f:
    json.dump(updates, f)
