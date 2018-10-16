import requests
import xmltodict

writefile = open("dump.xml", "w")
auth_details = ('bramvanulden@live.nl', 'U-8hSW5D50saIgMxCNFI7NpVxGC_nlcEKMKNRm4s2U6SkhdYxOchjw')

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

        d[eindbestemming] = [vertrekTijd, ritnummer, treinsoort, vertrekspoor]
