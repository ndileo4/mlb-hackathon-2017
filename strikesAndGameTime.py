import sys, getopt
import numpy as np
import csv
import mlbgame
from datetime import datetime


STRIKE_THRESHOLD = 0.90

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"h:",["years="])
    except getopt.GetoptError:
        print 'Usage: strikesAndGameTime.py -years <2014>'
        print 'Usage: strikesAndGameTime.py -years <2014-2016>'
        sys.exit(2)

    yearsToGet = -1

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: strikesAndGameTime.py -years <2014>'
            print 'Usage: strikesAndGameTime.py -years <2014-2016>'
            sys.exit()
        elif opt == "--years":
            yearsToGet = arg
            print "Getting Data For: " + yearsToGet
        else:
            print 'Usage: strikesAndGameTime.py -years <2014>'
            print 'Usage: strikesAndGameTime.py -years <2014-2016>'
            sys.exit()

    # do some validation on years
    yearsList = []
    if len(yearsToGet)>4:
        startYear = int(yearsToGet[0:4])
        endYear = int(yearsToGet[5:len(yearsToGet)])
        for year in range(startYear,endYear+1):
            yearsList.append(year)
    else:
        #only one season
        startYear = int(yearsToGet[0:4])
        yearsList.append(startYear)


    # with open('2014.csv', 'r') as csvfile:
    #     csvreader = csv.reader(csvfile)
    #     for row in csvreader:
    #         print(row)
    #         if row[0] in (None, ""):
    #             print("12")
    dict_list = []
    for cYear in yearsList:
        fileName = str(cYear)+".csv"
        reader = csv.DictReader(open(fileName, 'rb'))
        for line in reader: #Uncomment
            if str(line['probCalledStrike']) != '':
                # parse down the data
                newDict = {'gameString': line['gameString'], 'pitchResult': line['pitchResult'],
                           'probCalledStrike': line['probCalledStrike']}
                dict_list.append(newDict)

            # #TODELETE
            # if len(dict_list)>1000:
            #     break

    cGameString = ""
    gameList = []
    for cPitch in dict_list:
        if cPitch['gameString']==cGameString:
            totalPitches = gameDict['totalPitches']+1
            if float(cPitch['probCalledStrike'])>STRIKE_THRESHOLD:
                totalStrikes = gameDict['strikes']+1
                gameDict['strikes'] = totalStrikes

            gameDict['totalPitches'] = totalPitches

        else:
            if cGameString != "":
                # this is not the first entry - gameDict is filled with previous game stats
                # tally the percent strikes
                percentStrikes = float(gameDict['strikes'])/float(gameDict['totalPitches'])
                gameDict['percentStrikes'] = percentStrikes

                isValid, gameHours = isGameValid(gameDict['gameString'])
                if isValid:
                    gameDict['timeOfGameHr'] = gameHours
                    gameList.append(gameDict)


            # new game id
            cGameString = cPitch['gameString']
            gameDict = {'gameString': cGameString, 'strikes': 0, 'totalPitches': 0, 'percentStrikes': 0.0,
                 'timeOfGameHr': 0.0}



    # write to csv for nicer plotting
    outFile = yearsToGet + "_strikesGameTimeOut.csv"
    with open(outFile, 'w') as csvfile:
        fieldnames = gameList[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cRow in gameList:
            writer.writerow(cRow)

    print "Complete - Results Written To: " + outFile



def isGameValid(cGameString):
    MAX_GAME_TIME = 6.5

    # only want to include games that are 9 innings and under 6.5hrs
    gameID = cGameString[4:]
    gameEvents = mlbgame.game_events(gameID)

    if len(gameEvents) !=9:
        # not a nine inning game
        return False, 0.0


    startTimeStr = gameEvents['1']['top'][0].start_tfs_zulu
    if len(gameEvents['9']['bottom'])==0:
        # home team didn't bat in 9th
        endTimeStr = gameEvents['9']['top'][2].start_tfs_zulu
    else:
        endIdx = len(gameEvents['9']['bottom'])-1
        endTimeStr = gameEvents['9']['bottom'][endIdx].start_tfs_zulu


    startDateTime = datetime.strptime(startTimeStr, '%Y-%m-%dT%H:%M:%SZ')
    endDateTime = datetime.strptime(endTimeStr, '%Y-%m-%dT%H:%M:%SZ')
    totalGameTime = endDateTime - startDateTime
    totalHrs = totalGameTime.seconds / 3600.0

    if totalHrs > MAX_GAME_TIME:
        return False,0

    return True,totalHrs

if __name__ == "__main__":
    main(sys.argv[1:])