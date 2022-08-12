import json

# return all updates containing the specified value in the Added or Updated table
# returns a string of format "update_version | update_date | update_status | update_url"
def search(data, detection):
    results = []

    for item in data:
        for detection_name in item["update_added_detections"]:
            if detection in detection_name:
                results.append(f"{item['update_id']} | {item['update_date']} | Added   | {detection_name} | {item['update_url']}")

        for detection_name in item["update_updated_detections"]:
            if detection in detection_name:
                results.append(f"{item['update_id']} | {item['update_date']} | Updated | {detection_name} | {item['update_url']}")

    return results

update_data = None

# load data from system
with open("update_data.json", 'r') as f:
    update_data = json.load(f)

# loop, prompt user for detection to search for
user_input = ""
while user_input != "exit":
    user_input = input("\nEnter the full or partial name of a detection, or \"exit\" to terminate: ").strip()
    print("\n")

    # search for user input in data
    results = search(update_data, user_input)

    # sort results by date
    for result in results:
        print(result)

    if len(results) == 0:
        print("No results found for", user_input)