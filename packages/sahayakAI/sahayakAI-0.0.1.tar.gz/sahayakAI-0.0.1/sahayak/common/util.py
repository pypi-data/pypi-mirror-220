def extract_train_details(train_details):
    details = "*Train Details*"
    details = details + "\n*" + \
        train_details["name"] + " (" + train_details["number"] + ")*"
    details = details + "\n*Source Station:* " + \
        train_details["source_station"]
    details = details + "\n*Arrival:* " + train_details["arrival_at_source"]
    details = details + "\n*Departure:* " + \
        train_details["departure_from_source"]
    details = details + "\n\n*Destination Station:* " + \
        train_details["destination_station"]
    details = details + "\n*Arrival:* " + \
        train_details["arrival_at_destination"]
    details = details + "\n*Departure:* " + \
        train_details["departure_from_destination"]
    details = details + "\n*Days:* "

    for day in train_details["days"]:
        details = details + day + ", "

    details = details[:-2]
    details = details + "\n-----------------------\n\n"
    return details
