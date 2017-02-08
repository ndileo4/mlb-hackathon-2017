import pandas as pd
import numpy as np
import time

from pytest import mark

start_time = time.time()

STRIKE_THRESHOLD = 0.80

pitcherToTrain = "Madison Bumgarner"

df = pd.read_csv('2014.csv')

# remove frames without probCalledStrike
df = df[np.isfinite(df['probCalledStrike'])]

# remove frames with prob called strike
df = df.loc[df['probCalledStrike'] > STRIKE_THRESHOLD]

# map strings to vals
leftRightMap = {'R':1,'L':2}
trueFalseMap = {'true':1,'false':0}


df = df.replace({'batterHand': leftRightMap, 'pitcherHand': leftRightMap})

# calculate batterteam to pitchers team run differential
# Calculate run differential
df['batterRunDelta'] = df['homeTeamCurrentRuns'] - df['visitingTeamCurrentRuns']
# Overwrite with run differential if current hitter in on the visiting team
df['batterRunDelta'] = df.apply(lambda x: x['visitingTeamCurrentRuns'] - x['homeTeamCurrentRuns'] if (x['side']=='T') else x['batterRunDelta'], axis=1)

# calculate the on paint column
ftEdge = 1.41667
marginFt = 0.25

# df["onPaint"] = (df['px']<=(ftEdge/2.0-marginFt) and df['px']>=(-ftEdge/2.0+marginFt))
df['onPaint'] = 1
df['onPaint'][(df['px'] <= (ftEdge/2.0-marginFt)) & (df['px'] >= (-ftEdge/2.0+marginFt)) \
                 (df['pz'] >= (df['szb'] + marginFt)) & (df['pz'] <= (df['szt'] - marginFt))] = 0

#TODO: hitter and pitcher stats (krate)

# df['onPaint'] = np.where(df['px']<=(ftEdge/2.0-marginFt) and df['px']>=(-ftEdge/2.0+marginFt), 0, 1)


# Overwrite with difference to watermelon price

# ,'manOnFirst':trueFalseMap,
#             'manOnSecond':trueFalseMap,'manOnThird':trueFalseMap,'endManOnFirst': trueFalseMap,
#             'endManOnSecond': trueFalseMap,'manOnThird': trueFalseMap})



# firstFrame = df[df['pitcher']==pitcherToTrain].iloc[0]
# pitcherID = firstFrame['pitcherId']
#
#
# allPlayersPitches = df.loc[df['pitcherId'] == pitcherID]
print("--- %s seconds ---" % (time.time() - start_time))

print 1