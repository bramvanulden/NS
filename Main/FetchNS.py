import requests
import xmltodict


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

        # IN LIST:
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
    extrareistijd = ""
    toDelete = ["<p>", "</p>", "<b>", "</b>", "<br>", "<br/>"]
    api_station = "http://webservices.ns.nl/ns-api-storingen?station={0}".format(station)
    response_station = requests.get(api_station, auth=auth_details)
    StoWernXML = xmltodict.parse(response_station.text)
    for werkzaamheed in StoWernXML["Storingen"]["Gepland"]["Storing"]:
        traject = werkzaamheed["Traject"]

        with open("dump.xml", "w") as myXMLFile:
            myXMLFile.write(werkzaamheed["Bericht"])

        for line in readfile:
            for string in toDelete:
                line = line.replace(string, "")
            writefile.write(line)
            if "Wanneer:" in line:
                wanneer = line
            if "Oorzaak" in line:
                oorzaak = line
            if "Advies" in line:
                advies = line
            if "Extra reistijd:" in line:
                extrareistijd = line

        # IN LIST:
        #   wanneer         = 0
        #   oorzaak         = 1
        #   advies          = 2
        #   extrareistijd   = 3

        d[traject] = [wanneer, oorzaak, advies, extrareistijd]
    return d

def getReisadvies(vanstation, naarstation):
    d = {}
    api_station = "http://webservices.ns.nl/ns-api-treinplanner?fromStation={0}&toStation={1}&departure=true".format(vanstation, naarstation)
    response_station = requests.get(api_station, auth=auth_details)
    vertrektijdenXML = xmltodict.parse(response_station.text)
    for mogelijkheid in vertrektijdenXML["ReisMogelijkheden"]["ReisMogelijkheid"]:
        overstappen = mogelijkheid["AantalOverstappen"]
        reistijd = mogelijkheid["GeplandeReisTijd"]
        vertrekStr = mogelijkheid["ActueleVertrekTijd"]
        vertrektijd = vertrekStr[11:16]
        aankomstStr = mogelijkheid["ActueleAankomstTijd"]
        aankomst = aankomstStr[11:16]
        treinsoort = mogelijkheid["ReisDeel"]["VervoerType"]
        vertrekspoor = mogelijkheid["ReisDeel"]["ReisStop"][0]["Spoor"].get("#text")

        # IN LIST:
        #   overstappen     = 0
        #   reistijd        = 1
        #   aankomst        = 2
        #   treinsoort      = 3
        #   vertrekspoor    = 4
        #   vertrektijd     = 5

        d[vertrektijd] = [overstappen, reistijd, aankomst, treinsoort, vertrekspoor, vertrektijd]
    return d

