import requests
import xmltodict
from xml.etree import ElementTree as ET


writefile = open("dump.xml", "w")
auth_details = ('bramvanulden@live.nl', 'U-8hSW5D50saIgMxCNFI7NpVxGC_nlcEKMKNRm4s2U6SkhdYxOchjw')
readfile = open("dump.xml", "r")

def getVertrektijden(station):
    d = {}
    api_station = "https://webservices.ns.nl/ns-api-avt?station={0}".format(station)
    response_station = requests.get(api_station, auth=auth_details)
    vertrektijdenXML = xmltodict.parse(response_station.text)
    for vertrek in vertrektijdenXML['ActueleVertrekTijden']['VertrekkendeTrein']:
        eindbestemming = vertrek["EindBestemming"]
        vertrekStr = vertrek["VertrekTijd"]
        vertrekTijd = vertrekStr[11:16]
        ritnummer = vertrek["RitNummer"]
        treinsoort = vertrek["TreinSoort"]
        vertrekspoorStr = vertrek["VertrekSpoor"]
        vertrekspoor = vertrekspoorStr.get("#text")

        # IN DICTIONARY:
        #   vertrekTijd  = 0
        #   ritnummer    = 1
        #   treinsoort   = 2
        #   vertrekspoor = 3

        d[eindbestemming] = [vertrekTijd, ritnummer, treinsoort, vertrekspoor]
    return d


def getStoringenWerkzaamheden(station):
    d = {}
    wanneer = ""
    oorzaak = ""
    advies = ""
    nieuwedienstregeling = ""
    extrareistijd = ""
    i = 0
    api_station = "http://webservices.ns.nl/ns-api-storingen?station={0}".format(station)
    response_station = requests.get(api_station, auth=auth_details)
    StoWernXML = xmltodict.parse(response_station.text)
    for werkzaamheed in StoWernXML["Storingen"]["Gepland"]["Storing"]:
        traject = werkzaamheed["Traject"]
        periode = werkzaamheed["Periode"]
        bericht = werkzaamheed["Bericht"]

        with open("dump.xml", "w") as myXMLFile:
            myXMLFile.write(werkzaamheed["Bericht"])

        for line in readfile:
            i += 1
            if "Wanneer:" in line:
                wanneer = line[11:-10]
            if "Oorzaak" in line:
                oorzaak = line[11:-10]
            if "Advies" in line:
                advies = line[10:-5]
            if i == 5:
                nieuwedienstregeling = line[5:]
            if "Extra reistijd:" in line:
                extrareistijd = line[20:-10]

        d[traject] = [periode, bericht, wanneer, oorzaak, advies, nieuwedienstregeling, extrareistijd]


print(getStoringenWerkzaamheden("ut"))

