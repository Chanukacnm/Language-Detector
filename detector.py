import sys
import string

statSinhala = {}
statTamil = {}
statTarget = {}

meanAbsoluteError = {'sinhala': 0, 'tamil': 0}
letterTolerance = 0.01
cvTolerance = 0.01
cvvTolerance = 0.02

detectedLanguage = ''

cvcvvCountStatsSinhala = {'cv': {}, 'cvv': {}, 'letters': {}}
cvcvvCountStatsTamil = {'cv': {}, 'cvv': {}, 'letters': {}}
cvcvvCountStatsTarget = {'cv': {}, 'cvv': {}, 'letters': {}}
error = False


def calculateDistributionForStats(statsFile, statsData, cvcvvCountStats):

    with open(statsFile, 'r') as f:
        data = [line.strip() for line in f]
        totalLetters = eval(data[0].split('-')[1].strip())
        letterCounts = eval(data[1].split('-')[1].strip())
        cvCount = eval(data[2].split('-')[1].strip())
        cvvCount = eval(data[3].split('-')[1].strip())
        cvcvvCount = eval(data[4].split('-')[1].strip())

        statsData['totalLetters']  = totalLetters
        statsData['letterCounts']  = letterCounts
        statsData['cvCount']  = cvCount
        statsData['cvvCount']  = cvvCount
        statsData['cvcvvCount']  = cvcvvCount

        # Updating stats
        for key, value in cvcvvCount['cv'].items():
            cvcvvCountStats['cv'][key] = float(value)/cvCount
        
        for key, value in cvcvvCount['cvv'].items():
            cvcvvCountStats['cvv'][key] = float(value)/cvvCount
        
        for key, value in letterCounts.items():
            cvcvvCountStats['letters'][key] = float(value)/totalLetters


def calculateDistributions(sinhala, tamil, target):
    calculateDistributionForStats(sinhala, statSinhala, cvcvvCountStatsSinhala)
    calculateDistributionForStats(tamil, statTamil, cvcvvCountStatsTamil)
    calculateDistributionForStats(target, statTarget, cvcvvCountStatsTarget)

def calculateError():
    global cvcvvCountStatsSinhala, cvcvvCountStatsTamil, cvcvvCountStatsTarget, meanAbsoluteError
    for key, value in cvcvvCountStatsTarget['cv'].items():
        if abs(cvcvvCountStatsSinhala['cv'][key]-cvcvvCountStatsTamil['cv'][key]) > cvTolerance:
            meanAbsoluteError['sinhala'] += abs(cvcvvCountStatsSinhala['cv'][key] - cvcvvCountStatsTarget['cv'][key])
            meanAbsoluteError['tamil'] += abs(cvcvvCountStatsTamil['cv'][key] - cvcvvCountStatsTarget['cv'][key])
    
    for key, value in cvcvvCountStatsTarget['cvv'].items():
        if abs(cvcvvCountStatsSinhala['cvv'][key]-cvcvvCountStatsTamil['cvv'][key]) > cvvTolerance:
            meanAbsoluteError['sinhala'] += abs(cvcvvCountStatsSinhala['cvv'][key] - cvcvvCountStatsTarget['cvv'][key])
            meanAbsoluteError['tamil'] += abs(cvcvvCountStatsTamil['cvv'][key] - cvcvvCountStatsTarget['cvv'][key])
    
    for key, value in cvcvvCountStatsTarget['letters'].items():
        if abs(cvcvvCountStatsSinhala['letters'][key]-cvcvvCountStatsTamil['letters'][key]) > letterTolerance:
            meanAbsoluteError['sinhala'] += abs(cvcvvCountStatsSinhala['letters'][key] - cvcvvCountStatsTarget['letters'][key])
            meanAbsoluteError['tamil'] += abs(cvcvvCountStatsTamil['letters'][key] - cvcvvCountStatsTarget['letters'][key])


# Update the model stats again using detected language file stats
def updateModel(statsModel, statsNew):
    # Updating sinhala stats
    statsModel['totalLetters']  += statsNew['totalLetters']

    for key, value in statsNew['letterCounts'].items():
        statsModel['letterCounts'][key] += value

    statsModel['cvCount']  += statsNew['cvCount']
    statsModel['cvvCount']  += statsNew['cvvCount']
    
    for key, value in statsNew['cvcvvCount']['cv'].items():
        statsModel['cvcvvCount']['cv'][key] += value
    
    for key, value in statsNew['cvcvvCount']['cvv'].items():
        statsModel['cvcvvCount']['cvv'][key] += value
    
    with open(sinhalaStats, 'wb') as f:
        f.writelines("totalLetters- " + str(statsModel['totalLetters']))
        f.writelines("\nletterCounts- " + str(statsModel['letterCounts']))
        f.writelines("\ncvCount- " + str(statsModel['cvCount']))
        f.writelines("\ncvvCount- " + str(statsModel['cvvCount']))
        f.writelines("\ncvcvvCount- " + str(statsModel['cvcvvCount']))

    print("Model updated using new target file")


initialParams = sys.argv

targetStats = ''
sinhalaStats = ''
tamilStats = ''

if len(initialParams) != 4:
    print("Use python detector.py <TARGET STATS> <SINHALA STATS> <TAMIL STATS>")
    error = True
else:
    targetStats = initialParams[1]
    sinhalaStats = initialParams[2]
    tamilStats = initialParams[3]

    calculateDistributions(sinhalaStats, tamilStats, targetStats)
    calculateError()
    
    if meanAbsoluteError['sinhala'] < meanAbsoluteError['tamil']:
        print('Language detected: SINHALA')
        print('MAE: ' + str(meanAbsoluteError['sinhala']) + ' < ' + str(meanAbsoluteError['tamil']))
        detectedLanguage = 'SINHALA'
    elif meanAbsoluteError['sinhala'] > meanAbsoluteError['tamil']:
        print('Language detected: TAMIL')
        print('MAE: ' + str(meanAbsoluteError['tamil']) + ' < ' + str(meanAbsoluteError['sinhala']))
        detectedLanguage = 'TAMIL'
    else:
        error = True
        print('Language detection failed, please provide a larger data set for training/testing')

if not error:
    print('Was the prediction true and you need to update the stats? (Y/N) [N]')
    if input().lower() == 'y':
        if detectedLanguage == 'SINHALA':
            updateModel(statSinhala, statTarget)

        elif detectedLanguage == 'TAMIL':
            updateModel(statTamil, statTarget)