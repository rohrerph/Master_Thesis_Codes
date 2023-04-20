class AirplaneModels:
    #dates need to be validated, (are from ChatGPT :) )
    def __init__(self):
        self.models = {"Boeing 757-200": 1984,
                       "Boeing 767-300/300ER": 1987,
                       "Boeing 777-200ER/200LR/233LR": 1995,
                       "Airbus Industrie A320-100/200": 1988,
                       "Boeing 767-200/ER/EM": 1983,
                       "Boeing 737-800": 1998,
                       "Airbus Industrie A319": 1996,
                       "Boeing 737-300": 1984,
                       "McDonnell Douglas DC9 Super 80/MD81/82/83/88": 1980,
                       "Boeing 747-400": 1989,
                       "Boeing 737-700/700LR/Max 7": 1997,
                       "Boeing 727-200/231A": 1967,
                       "Airbus Industrie A330-200": 1998,
                       "Boeing 767-400/ER": 2000,
                       "McDonnell Douglas DC-10-30": 1972,
                       "Airbus Industrie A321/Lr": 1994,
                       "Boeing 737-400": 1988,
                       "Boeing 737-100/200": 1967,
                       "Boeing 737-500": 1990,
                       "Boeing 747-200/300": 1970,
                       "McDonnell Douglas MD-11": 1990,
                       "Boeing 757-300": 1999,
                       "Boeing 737-900": 2001,
                       "Boeing 747-100": 1970,
                       "Canadair RJ-700": 1999,
                       "B787-800 Dreamliner": 2011,
                       "McDonnell Douglas DC-9-30": 1966,
                       "Airbus Industrie A330-300/333": 1992,
                       "Embraer-145": 1996,
                       "Boeing 777-300/300ER/333ER": 1998,
                       "Embraer 190": 2004,
                       "B787-900 Dreamliner": 2014,
                       "McDonnell Douglas DC-10-10": 1970,
                       "Lockheed L-1011-1/100/200": 1973,
                       "Airbus Industrie A300-600/R/CF/RCF": 1984,
                       "Boeing 737-900ER": 2007,
                       "Canadair RJ-200ER /RJ-440": 1996,
                       "McDonnell Douglas MD-90": 1995,
                       "McDonnell Douglas DC-10-40": 1972,
                       "Boeing 717-200": 1999,
                       "Embraer ERJ-175": 2005,
                       "Boeing B737 Max 800": 2017,
                       "Boeing 787-10 Dreamliner": 2018,
                       "Airbus Industrie A330-900": 2018,
                       "Boeing B737 Max 900": 2018
                       }

    def get_models(self):
        return self.models

class AirplaneTypes:
    #dates need to be validated, (are from ChatGPT :) )
    def __init__(self):
        self.types = {"Boeing 757-200": 'Narrow',
                       "Boeing 767-300/300ER": 'Wide',
                       "Boeing 777-200ER/200LR/233LR": 'Wide',
                       "Airbus Industrie A320-100/200": 'Narrow',
                       "Boeing 767-200/ER/EM": 'Wide',
                       "Boeing 737-800": 'Narrow',
                       "Airbus Industrie A319": 'Narrow',
                       "Boeing 737-300": 'Narrow',
                       "McDonnell Douglas DC9 Super 80/MD81/82/83/88": 'Narrow',
                       "Boeing 747-400": 'Wide',
                       "Boeing 737-700/700LR/Max 7": 'Narrow',
                       "Boeing 727-200/231A": 'Narrow',
                       "Airbus Industrie A330-200": 'Wide',
                       "Boeing 767-400/ER": 'Wide',
                       "McDonnell Douglas DC-10-30": 'Wide',
                       "Airbus Industrie A321/Lr": 'Narrow',
                       "Boeing 737-400": 'Narrow',
                       "Boeing 737-100/200": 'Narrow',
                       "Boeing 737-500": 'Narrow',
                       "Boeing 747-200/300": 'Wide',
                       "McDonnell Douglas MD-11": 'Wide',
                       "Boeing 757-300": 'Narrow',
                       "Boeing 737-900": 'Narrow',
                       "Boeing 747-100": 'Wide',
                       "Canadair RJ-700": 'Regional',
                       "B787-800 Dreamliner": 'Wide',
                       "McDonnell Douglas DC-9-30": 'Narrow',
                       "Airbus Industrie A330-300/333": 'Wide',
                       "Embraer-145": 'Regional',
                       "Boeing 777-300/300ER/333ER": 'Wide',
                       "Embraer 190": 'Narrow',
                       "B787-900 Dreamliner": 'Wide',
                       "McDonnell Douglas DC-10-10": 'Wide',
                       "Lockheed L-1011-1/100/200": 'Wide',
                       "Airbus Industrie A300-600/R/CF/RCF": 'Wide',
                       "Boeing 737-900ER": 'Narrow',
                       "Canadair RJ-200ER /RJ-440": 'Regional',
                       "McDonnell Douglas MD-90": 'Narrow',
                       "McDonnell Douglas DC-10-40": 'Wide',
                       "Boeing 717-200": 'Narrow',
                       "Embraer ERJ-175": 'Regional',
                       "Boeing B737 Max 800": 'Narrow',
                       "Boeing 787-10 Dreamliner": 'Wide',
                       "Airbus Industrie A330-900": 'Wide',
                       "Boeing B737 Max 900": 'Narrow'
                       }

    def get_types(self):
        return self.types


class USAirlines:
    def __init__(self):
        self.airlines = ['American Airlines Inc.',
                          'United Air Lines Inc.',
                          'Delta Air Lines Inc.',
                          'Southwest Airlines Co.',
                          'Northwest Airlines Inc.',
                          'Continental Air Lines Inc.',
                          'US Airways Inc.',
                          'Alaska Airlines Inc.',
                          'JetBlue Airways',
                          'Trans World Airways LLC',
                          'America West Airlines Inc.',
                          'SkyWest Airlines Inc.',
                          'Spirit Air Lines',
                          'Frontier Airlines Inc.',
                          'Hawaiian Airlines Inc.',
                          'Envoy Air',
                          'AirTran Airways Corporation',
                          'ExpressJet Airlines LLC d/b/a aha!',
                          'ATA Airlines d/b/a ATA']

    def get_airlines(self):
        return self.airlines

class AircraftNames:
    def __init__(self):
        self.aircraftnames = {'B707-300':'B707-300',
                         'B720-000':'B720-000',
                         'DC9-10':'DC9-10',
                         'DC9-30':'McDonnell Douglas DC-9-30',
                         'B727-200/231A':'Boeing 727-200/231A',
                         'B737-100/200':'Boeing 737-100/200',
                         'DC9-40':'DC9-40',
                         'DC10-10': 'McDonnell Douglas DC-10-10',
                         'B747-200/300':'Boeing 747-200/300',
                         'B747-100': 'Boeing 747-100',
                         'DC10-40':'McDonnell Douglas DC-10-40',
                         'DC10-30':'McDonnell Douglas DC-10-30',
                         'L1011-1/100/200':'Lockheed L-1011-1/100/200',
                         'DC9-50':'DC9-50',
                         'L1011-500':'L1011-500',
                         'MD80/DC9-80':'McDonnell Douglas DC9 Super 80/MD81/82/83/88',
                         'B767-200/ER': 'Boeing 767-200/ER/EM',
                         'A300-600':'Airbus Industrie A300-600/R/CF/RCF',
                         'B757-200':'Boeing 757-200',
                         'B737-300':'Boeing 737-300',
                         'A310-300': 'A310-300',
                         'B767-300/ER':'Boeing 767-300/300ER',
                         'A320-100/200': 'Airbus Industrie A320-100/200',
                         'B737-400':'Boeing 737-400',
                         'B747-400':'Boeing 747-400',
                         'MD11':'McDonnell Douglas MD-11',
                         'B737-500/600':'Boeing 737-500',
                         'B777': 'Boeing 777-200ER/200LR/233LR'}

    def get_aircraftnames(self):
        return self.aircraftnames

class Substitutes:
    def __init__(self):
        self.engines = {'CF34-8C6': 'CF34-8C5', #same family
                        'CF34-8C7': 'CF34-8C5', #same family
                        'CF34-8C8': 'CF34-8C5', #same family
                        'CF34-8C9': 'CF34-8C5',#same family
                        'RB211-535E4B': 'RB211-535E4',#same family
                        'PW2043': 'PW2040', #same series
                        'PW4098':'PW4090'} #same series
    def engine_substitute(self):
        return self.engines

class B737_family:
    def __init__(self):
        self.b737 = ['737-200',
                      '737-700/700LR/Max 7',
                      '737-800',
                      '737-900',
                      '737-900ER']
    def get_b737(self):
        return self.b737

class fullname:
    def __init__(self):
        self.aircraftfullnames = {
                                "Airbus Industrie A300-600/R/CF/RCF": "A300-600",
                                "Airbus Industrie A319": "A319",
                                "Airbus Industrie A320-100/200": "A320-100/200",
                                "Airbus Industrie A321/Lr": "A321/Lr",
                                "Airbus Industrie A330-200": "A330-200",
                                "Airbus Industrie A330-300/333": "A330-300/333",
                                "Airbus Industrie A330-900": "A330-900",
                                "B787-800 Dreamliner": "B787-800 Dreamliner",
                                "B787-900 Dreamliner": "B787-900 Dreamliner",
                                "Boeing 717-200": "717-200",
                                "Boeing 727-200/231A": "B727-200/231A",
                                "Boeing 737-100/200": "B737-100/200",
                                "Boeing 737-300": "B737-300",
                                "Boeing 737-400": "B737-400",
                                "Boeing 737-500": "B737-500/600",
                                "Boeing 737-700/700LR/Max 7": "737-700/700LR/Max 7",
                                "Boeing 737-800": "737-800",
                                "Boeing 737-900": "737-900",
                                "Boeing 737-900ER": "737-900ER",
                                "Boeing 747-100": "747-100",
                                "Boeing 747-200/300": "B747-200/300",
                                "Boeing 747-400": "B747-400",
                                "Boeing 757-200": "B757-200",
                                "Boeing 757-300": "757-300",
                                "Boeing 767-200/ER/EM": "B767-200/ER/EM",
                                "Boeing 767-300/300ER": "B767-300/300ER",
                                "Boeing 767-400/ER": "767-400/ER",
                                "Boeing 777-200ER/200LR/233LR": "B777",
                                "Boeing 777-300/300ER/333ER": "777-300/300ER/333ER",
                                "Boeing 787-10 Dreamliner": "787-10 Dreamliner",
                                "Boeing B737 Max 800": "B737 Max 800",
                                "Boeing B737 Max 900": "B737 Max 900",
                                "Canadair RJ-200ER /RJ-440": "RJ-200ER /RJ-440",
                                "Canadair RJ-700": "RJ-700",
                                "Embraer 190": "Embraer 190",
                                "Embraer ERJ-175": "Embraer ERJ-175",
                                "Embraer-145": "Embraer-145",
                                "Lockheed L-1011-1/100/200": "L1011-1/100/200",
                                "McDonnell Douglas DC-10-10": "DC10-10",
                                "McDonnell Douglas DC-10-30": "DC10-30",
                                "McDonnell Douglas DC-10-40": "DC10-40",
                                "McDonnell Douglas DC-9-30": "DC9-30",
                                "McDonnell Douglas DC9 Super 80/MD81/82/83/88": "MD80/DC9-80",
                                "McDonnell Douglas MD-11": "MD-11",
                                "McDonnell Douglas MD-90": "MD-90"}
    def get_aircraftfullnames(self):
        return self.aircraftfullnames