import dateutil.parser

def iso8601toHHMM(input):
    datetime = dateutil.parser.parse(input)
    return datetime.strftime("%H:%M")


def treinToText(treininfo):
    if treininfo['via']:
        header = "*{} {} {} richting {} via {}*\n".format(treininfo['vervoerder'], treininfo['soort'], treininfo['treinNr'], treininfo['bestemming'], treininfo['via'])
    else:
        header = "*{} {} {} richting {}*\n".format(treininfo['vervoerder'], treininfo['soort'], treininfo['treinNr'], treininfo['bestemming'])


    if len(treininfo['vleugels']) > 1:
        vleugeltekst = "trein bevat > 1 vleugel, not yet implemented"
    else:
        stops = "*Stops:*\n"
        vleugel = treininfo['vleugels'][0]
        for stop in vleugel['stopstations']:
            if stop['aankomst'] == None and stop['vertrek']: # Beginstation
                stops += "_{}_ ({}) V {} spoor {}\n".format(stop['naam'], stop['code'].upper(), iso8601toHHMM(stop['vertrek']), stop['vertrekspoor'])
            elif stop['vertrek'] == None and stop['aankomst']: # Eindstation
                stops += "_{}_ ({}) A {} spoor {}\n".format(stop['naam'], stop['code'].upper(), iso8601toHHMM(stop['aankomst']), stop['aankomstspoor'])
            else: # Tussenstation
                stops += "_{}_ ({}) A {} V {} spoor {}\n".format(stop['naam'], stop['code'].upper(), iso8601toHHMM(stop['aankomst']), iso8601toHHMM(stop['vertrek']), stop['vertrekspoor'])
        stops += "\n"
        
        mat_text = "*Materieel:*\n"
        if len(vleugel['mat']) is 0:
            mat_text += "Materieelinfo niet beschikbaar"
        else:
            for materieel in vleugel['mat']:
                if materieel[2] is None: # geen mat-nr
                    mat_text += "{}, eindbestemming {}\n".format(materieel[0], materieel[1])
                else:
                    mat_text += "{} {}, eindbestemming {}\n".format(materieel[0], materieel[2], materieel[1])

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

def stationToText(station):
    message = ""
    if len(station) is 0:
        return False
    for vertrek in station:
        message += "*{}* spoor {} {} {} {} naar {}".format(iso8601toHHMM(vertrek['vertrek']), vertrek['spoor'], vertrek['vervoerder'], vertrek['soortAfk'], vertrek['treinNr'], vertrek['bestemming'])
        if vertrek['via'] is not None:
            message += " via {}".format(vertrek['via'])

        message += "\n"

    
    return message
