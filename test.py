import requests

tbaApiKey = API KEY HERE"
tbaApiEndpoint = "https://www.thebluealliance.com/api/v3"
tbaHeaders = {"X-TBA-Auth-Key": tbaApiKey}

weeks = {
    "week1": [
        "2024-02-24",
        "2024-02-25",
        "2024-02-26",
        "2024-02-27",
        "2024-02-28",
        "2024-02-29",
        "2024-03-01",
        "2024-03-02",
        "2024-03-03"
    ],
    "week2": [
        "2024-03-05",
        "2024-03-06",
        "2024-03-07",
        "2024-03-08"
    ],
    "week3": [
        "2024-03-13",
        "2024-03-14",
        "2024-03-15"
    ],
    "week4": [
        "2024-03-18",
        "2024-03-19",
        "2024-03-20",
        "2024-03-21",
        "2024-03-22"
    ],
    "week5": [
        "2024-03-27",
        "2024-03-28",
        "2024-03-29"
    ],
    "week6": [
        "2024-04-03",
        "2024-04-04",
        "2024-04-05"
    ],
    "championship": [
        "2024-04-17",
        "2024-04-20"
    ]
}

print("Amplified Speaker Notes Scored (Qualis + Playoffs):")

weekNum = 1

for week in weeks.keys():
    events = requests.get(tbaApiEndpoint + f"/events/2024/simple", headers=tbaHeaders).json()
    eventList = []
    
    for event in events:
        if event["start_date"] in weeks[week]:
            eventList.append(event["key"])
    
    ampLeverage = []
    
    counter = 0
    for event in eventList:
    
        response = requests.get(tbaApiEndpoint + f"/event/{event}/matches", headers=tbaHeaders).json()
    
        matchCounter = 1
        for match in response:
            
            if match["score_breakdown"] is not None:
                speakerAmplifiedNotesBlue = match["score_breakdown"]["blue"]["teleopSpeakerNoteAmplifiedCount"]
                ampNotesBlue = match["score_breakdown"]["blue"]["teleopAmpNoteCount"]
                if ampNotesBlue > 0:
                    ampLeverage.append({"match": matchCounter, "porcentage": speakerAmplifiedNotesBlue / ((ampNotesBlue / 2) * 4)})
    
            if match["score_breakdown"] is not None:
                speakerAmplifiedNotesRed = match["score_breakdown"]["red"]["teleopSpeakerNoteAmplifiedCount"]
                ampNotesRed = match["score_breakdown"]["red"]["teleopAmpNoteCount"]
                if ampNotesRed > 0:
                    ampLeverage.append({"match": matchCounter, "porcentage": speakerAmplifiedNotesRed / ((ampNotesRed / 2) * 4)})
    
            matchCounter += 1
        counter += 1
        #print(f"Event {counter}/{len(eventList)}")
    
    total = 0
    for metric in ampLeverage:
        total += metric["porcentage"]
    
    leverage = total / len(ampLeverage)
    
    if weekNum == 7:
        print(f"Championship: {str(leverage * 100)[:5]}%")
    
    weekNum += 1
