class AirplaneModels:
    #dates need to be validated, (are from ChatGPT :) )
    def __init__(self):
        self.models = {'Boeing 757-200': 1983,
                       'Boeing 767-300/300ER': 1986,
                       'Boeing 777-200ER/200LR/233LR': 1995,
                       'Airbus Industrie A320-100/200': 1987,
                       'Boeing 767-200/ER/EM': 1982,
                       'Boeing 737-800': 1997,
                       'Airbus Industrie A319': 1996,
                       'Boeing 737-300': 1984,
                       'McDonnell Douglas DC9 Super 80/MD81/82/83/88': 1980,
                       'Boeing 747-400': 1988,
                       'Boeing 737-700/700LR/Max 7': 1997,
                       'Boeing 727-200/231A': 1967,
                       'Airbus Industrie A330-200': 1998,
                       'Boeing 767-400/ER': 2000,
                       'McDonnell Douglas DC-10-30': 1972,
                       'Airbus Industrie A321/Lr': 1993,
                       'Boeing 737-400': 1988,
                       'Boeing 737-100/200': 1967,
                       'Boeing 737-500': 1987,
                       'Boeing 747-200/300': 1970}

    def get_models(self):
        return self.models


class USAirlines:
    def __init__(self):
        self.airlines = ['Delta Air Lines Inc.',
                         'United Air Lines Inc.',
                         'American Airlines Inc.',
                         'Continental Air Lines Inc.',
                         'US Airways Inc.',
                         'Northwest Airlines Inc.',
                         'Alaska Airlines Inc.',
                         'Trans World Airways LLC',
                         'Envoy Air',
                         'America West Airlines Inc.',
                         'Southwest Airlines Co.',
                         'SkyWest Airlines Inc.',
                         'JetBlue Airways',
                         'Frontier Airlines Inc.',
                         'ExpressJet Airlines LLC d/b/a aha!',
                         'ATA Airlines d/b/a ATA',
                         'Spirit Air Lines',
                         'Hawaiian Airlines Inc.',
                         'Atlas Air Inc.',
                         'ExpressJet Airlines Inc.']

    def get_airlines(self):
        return self.airlines

