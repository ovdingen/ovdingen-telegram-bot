import dateutil.parser

def iso8601toHHMM(input):
    datetime = dateutil.parser.parse(input)
    return datetime.strftime("%H:%M")


def treinToText(treininfo, instant = False):
    if treininfo is False:
        if instant is True:
            return treininfo
        else:
            return "Niet gevonden"
    if treininfo['via']:
        header = u"*{} {} {} richting {} via {}*\n".format(treininfo['vervoerder'], treininfo['soort'], treininfo['treinNr'], treininfo['bestemming'], treininfo['via'])
    else:
        header = u"*{} {} {} richting {}*\n".format(treininfo['vervoerder'], treininfo['soort'], treininfo['treinNr'], treininfo['bestemming'])


    if len(treininfo['vleugels']) > 1:
        vleugeltekst = "trein bevat > 1 vleugel, not yet implemented"
    else:
        stops = "*Stops:*\n"
        vleugel = treininfo['vleugels'][0]
        for stop in vleugel['stopstations']:
            if stop['aankomst'] == None and stop['vertrek']: # Beginstation
                stops += u"_{}_ ({}) V {} spoor {}\n".format(stop['naam'], stop['code'].upper(), iso8601toHHMM(stop['vertrek']), stop['vertrekspoor'])
            elif stop['vertrek'] == None and stop['aankomst']: # Eindstation
                stops += u"_{}_ ({}) A {} spoor {}\n".format(stop['naam'], stop['code'].upper(), iso8601toHHMM(stop['aankomst']), stop['aankomstspoor'])
            else: # Tussenstation
                stops += u"_{}_ ({}) A {} V {} spoor {}\n".format(stop['naam'], stop['code'].upper(), iso8601toHHMM(stop['aankomst']), iso8601toHHMM(stop['vertrek']), stop['vertrekspoor'])
        stops += "\n"
        
        mat_text = "*Materieel:*\n"
        if len(vleugel['mat']) is 0:
            mat_text += "Materieelinfo niet beschikbaar"
        else:
            for materieel in vleugel['mat']:
                if materieel[2] is None: # geen mat-nr
                    mat_text += u"{}, eindbestemming {}\n".format(materieel[0], materieel[1])
                else:
                    mat_text += u"{} {}, eindbestemming {}\n".format(materieel[0], materieel[2], materieel[1])

        vleugeltekst = stops + mat_text
            
    notices = ""
    if len(treininfo['tips']) > 0:
        reistips = "*Reistip(s):*\n"
        for tip in treininfo['tips']:
            reistips += tip + "\n"
    else:
        reistips = ""
    if len(treininfo['opmerkingen']) > 0:
        opmerkingen = "*Opmerking(en):*\n"
        for opmerking in treininfo['opmerkingen']:
            opmerkingen += opmerking + "\n"
    else:
        opmerkingen = ""

    if treininfo['opgeheven'] is True:
        opgeheven = "\n\n*Deze trein is opgeheven!*"
    else:
        opgeheven = ""
    
    notices = reistips + opmerkingen + opgeheven
    

    
    return header + vleugeltekst + notices

def stationToText(station, instant = False, limit = 20):
    message = ""


    if station is False:
        if instant is True:
            return False
        else:
            return "Niet gevonden."
    if len(station) is 0:
        if instant is True:
            return False
        else:
            return "Niet gevonden."

    amount_of_departures = len(station)
    if amount_of_departures > limit:
        ar = amount_of_departures - limit
        station = station[:-ar]

    for vertrek in station:
        message += u"*{}* spoor {} {} {} {} naar {}".format(iso8601toHHMM(vertrek['vertrek']), vertrek['spoor'], vertrek['vervoerder'], vertrek['soortAfk'], vertrek['treinNr'], vertrek['bestemming'])
        if vertrek['via'] is not None:
            message += u" via {}".format(vertrek['via'])
        if vertrek['vertraging']:
            message += u" *+{} min.*".format(vertrek['vertraging'])
        message += "\n"
        if len(vertrek['tips']) is not 0:
            for tip in vertrek['tips']:
                message += u"_" + tip + "_\n"
        if len(vertrek['opmerkingen']) is not 0:
            for opmerking in vertrek['opmerkingen']:
                message += u"*" + opmerking + "*\n"
        if vertrek['opgeheven'] is True:
            message += "*Rijdt niet*\n"

        message += "\n"

    return message
