#!/usr/bin/env python3

import urllib
import urllib.request
import urllib.error
import json
import datetime
import sys

'''
Get SSO key by logging in on browser, then go to
https://developer.betfair.com/exchange-api/betting-api-demo/

64001 Arkestra

51284
1.0 - DELAY
XVLrYrBkLplUcNwe
matt_morris_zz @ yahoo.co.uk
Yes Yes Yes No

51283
1.0
rTnyUNLcaFHUsAQa
matt_morris_zz @ yahoo.co.uk
No
No
Yes
No
'''

"""
make a call API-NG
"""

def callAping(jsonrpc_req):
    try:
        req = urllib.request.Request(url, jsonrpc_req.encode('utf-8'), headers)
        response = urllib.request.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse.decode('utf-8')
    except urllib.error.URLError as e:
        print (e.reason)
        print ('Oops no service available at ' + str(url))
        exit()
    except urllib.error.HTTPError:
        print ('Oops not a valid operation from the service ' + str(url))
        exit()

def makeRequestString(method, params):
    return '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/' + method + '", "params": ' + params + ', "id": 1}'

"""
calling getEventTypes operation
"""

def getEventTypes():
    event_type_req = makeRequestString('listEventTypes', '{"filter":{ }}')
    print ('Calling listEventTypes to get event Type ID')
    eventTypesResponse = callAping(event_type_req)
    eventTypeLoads = json.loads(eventTypesResponse)
    try:
        eventTypeResults = eventTypeLoads['result']
        return eventTypeResults
    except:
        print ('Exception from API-NG: ' + str(eventTypeLoads['error']))
        e = eventTypeLoads['error']
        if('data' in e):
            e0 = e['data']
            if('APINGException' in e0):
                e1 = e0['APINGException']
                if('errorCode' in e1):
                    e2 = e1['errorCode']
                    print('error.data.APINGException.errorCode: ' + e2)
        exit()


"""
Extraction eventypeId for eventTypeName from evetypeResults
"""

def getIDForName(typesResult, typeName, requestedEventTypeName):
    if(typesResult is not None):
        for obj in typesResult:
            eventTypeName = obj[typeName]['name']
            if( eventTypeName == requestedEventTypeName):
                return obj[typeName]['id']
    else:
        print ('Oops there is an issue with the input')
        exit()


"""
Extraction eventypeId for eventTypeName from evetypeResults
"""

def getEventTypeIDForEventTypeName(eventTypesResult, requestedEventTypeName):
    return getIDForName(eventTypesResult, 'eventType', requestedEventTypeName)

def getEventIDForEventName(eventsResult, requestedEventName):
    return getIDForName(eventsResult, 'event', requestedEventName)

def getMarketInfoForMarketName(marketsResult, requestedMarketName):
    if(marketsResult is not None):
        for obj in marketsResult:
            eventTypeName = obj['marketName']
            if( eventTypeName == requestedMarketName):
                return obj
    else:
        print ('Oops there is an issue with the input')
        exit()

def getMarketIDForMarketName(marketsResult, requestedMarketName):
    if(marketsResult is not None):
        for obj in marketsResult:
            eventTypeName = obj['marketName']
            if( eventTypeName == requestedMarketName):
                return obj['marketId']
    else:
        print ('Oops there is an issue with the input')
        exit()

def getEventsForCountry(eventTypeID, countryCode):
    if (eventTypeID is not None):
        print ('Calling listEvents Operation')
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        listEventsReq = makeRequestString('listEvents', '{"filter":{"eventTypeIds":["' + eventTypeID + '"],'\
                                '"countryCode":"' + countryCode + '",'\
                                '"marketStartTime":{"from":"' + now + '"}},'\
                                '"sort":"FIRST_TO_START",'\
                                '"maxResults":"1",'\
                                '"marketProjection":["RUNNER_METADATA"]}')
        listEventsResponse = callAping(listEventsReq)
        listEventsObject = json.loads(listEventsResponse)
        try:
            listEventsResult = listEventsObject['result']
            return listEventsResult
        except:
            print ('Exception from API-NG' + str(listEventsObject['error']))
            exit()

def getMarketPrices(marketID):
    if (eventID is not None):
        print ('Calling getMarketPrices Operation')
        event_type_req = makeRequestString('listMarketBook', '{"marketIds": ["' + marketID + '"],'\
                    '"priceProjection": {'\
                        '"priceData": ["EX_BEST_OFFERS"],'\
                        '"exBestOffersOverrides": {'\
                        '"bestPricesDepth": "20"}}}')
        eventTypesResponse = callAping(event_type_req)
        eventTypeLoads = json.loads(eventTypesResponse)
        try:
            eventTypeResults = eventTypeLoads['result']
            return eventTypeResults
        except:
            print('Exception from API-NG' + str(eventTypeLoads['error']))
            exit()


def getMarketCatalogueForEvent(eventID):
    if (eventID is not None):
        print ('Calling listMarketCatalogue Operation to get MarketID and selectionId')
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        proj = '"MARKET_START_TIME","RUNNER_DESCRIPTION","EVENT_TYPE","RUNNER_METADATA"' # '"MARKET_DESCRIPTION"' # '"RUNNER_METADATA"'
        market_catalogue_req = makeRequestString('listMarketCatalogue', '{'\
                '"filter":{"eventIds":["' + eventID + '"],'\
                '"marketStartTime":{"from":"' + now + '"}},'\
                '"sort":"FIRST_TO_START",'\
                '"maxResults":"1000",'\
                '"marketProjection":[' + proj + ']}')
        market_catalogue_response = callAping(market_catalogue_req)
        market_catalouge_loads = json.loads(market_catalogue_response)
        try:
            market_catalouge_results = market_catalouge_loads['result']
            return market_catalouge_results
        except:
            print ('Exception from API-NG' + str(market_catalouge_results['error']))
            exit()


url = "https://api.betfair.com/exchange/betting/json-rpc/v1"

appKey = "XVLrYrBkLplUcNwe"
sessionToken = "Wpte3QGhp0LQPi1IT5YfFDfRIuyrsNacgNQp0TfkaOM="

headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}

eventTypeName = 'Politics'
eventCountryCode = 'GB'
eventName = 'UK - Next General Election'
marketName = 'Total Seats - Lib Dems'

# event type
eventTypesResult = getEventTypes()
politicsEventTypeID = getEventTypeIDForEventTypeName(eventTypesResult, eventTypeName)
print ('Eventype Id for "' + eventTypeName + '" is :' + str(politicsEventTypeID))
# individual event
eventsResult = getEventsForCountry(politicsEventTypeID, eventCountryCode)
eventID = getEventIDForEventName(eventsResult, eventName)
print('Event Id for "' + eventName + '" is :' + str(eventID))
# marketCatalogue
marketCatalogue = getMarketCatalogueForEvent(eventID)
marketInfo = getMarketInfoForMarketName(marketCatalogue, marketName)
print('Market Info for "' + marketName + '" is :' + str(marketInfo))
for marketInfoRunner in marketInfo['runners']:
    print(marketInfoRunner)
marketID = getMarketIDForMarketName(marketCatalogue, marketName)
print('Market Id for "' + marketName + '" is :' + str(marketID))
# marketBook
marketPrices = getMarketPrices(marketID)
print(str(marketPrices))
for marketPrice in marketPrices[0]['runners']:
    print(marketPrice)
