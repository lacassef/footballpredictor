import time
from datetime import datetime

import requests

from model.football import Match, TeamPerformance


def get_today_matches() -> list:
    # print('getting...')
    req = requests.get(f'http://localhost:8081/api/matches/schedules/{round(time.time() * 1000)}')
    if req.status_code == 200:
        return req.json()
    else:
        return []


def get_matches_from_date(year, month, day) -> list:
    # print('getting...')
    date = datetime(year=year, month=month, day=day, hour=12, minute=30)
    req = requests.get(f'http://localhost:8081/api/matches/schedules/{round(date.timestamp() * 1000)}')
    return req.json()


def get_match(mId: int) -> Match:
    # print('getting...')
    req = requests.get(f'http://localhost:8081/api/matches/{mId}')
    # print(mId)
    match = req.json()
    matchw = Match(id=match['id'], league=match['tournament']['id'], custom=match['customId'],
                   season=match['tournament']['season'], home=match['home']['id'],
                   away=match['away']['id'], status=match['status'], scoreHome=match['home']['score'],
                   scoreAway=match['away']['score'], awayName=match['away']['name'], homeName=
                   match['home']['name'], time= match['time'])
    return matchw


def get_performance(team: int, season: int, tournament: int) -> TeamPerformance:
    # http://localhost:8081/api/team/2829/7/36886/statistics
    req = requests.get(f'http://localhost:8081/api/team/{team}/{tournament}/{season}/statistics')
    performance = req.json()
    performancw = TeamPerformance(
        accurateCrosses=performance['accurateCrosses'],
        accurateFinalThirdPassesAgainst=performance['accurateFinalThirdPassesAgainst'],
        accurateLongBalls=performance['accurateLongBalls'],
        accurateOppositionHalfPasses=performance['accurateOppositionHalfPasses'],
        accurateOppositionHalfPassesAgainst=performance['accurateOppositionHalfPassesAgainst'],
        accurateOwnHalfPasses=performance['accurateOwnHalfPasses'],
        accurateOwnHalfPassesAgainst=performance['accurateOwnHalfPassesAgainst'],
        accuratePasses=performance['accuratePasses'],
        accuratePassesAgainst=performance['accuratePassesAgainst'],
        aerialDuelsWon=performance['aerialDuelsWon'],
        assists=performance['assists'],
        averageBallPossession=performance['averageBallPossession'],
        avgRating=performance['avgRating'],
        awardedMatches=performance['awardedMatches'],
        bigChances=performance['bigChances'],
        bigChancesAgainst=performance['bigChancesAgainst'],
        bigChancesCreated=performance['bigChancesCreated'],
        bigChancesCreatedAgainst=performance['bigChancesCreatedAgainst'],
        bigChancesMissed=performance['bigChancesMissed'],
        bigChancesMissedAgainst=performance['bigChancesMissedAgainst'],
        cleanSheets=performance['cleanSheets'],
        clearances=performance['clearances'],
        clearancesAgainst=performance['clearancesAgainst'],
        clearancesOffLine=performance['clearancesOffLine'],
        corners=performance['corners'],
        cornersAgainst=performance['cornersAgainst'],
        crossesSuccessfulAgainst=performance['crossesSuccessfulAgainst'],
        crossesTotalAgainst=performance['crossesTotalAgainst'],
        dribbleAttempts=performance['dribbleAttempts'],
        dribbleAttemptsTotalAgainst=performance['dribbleAttemptsTotalAgainst'],
        dribbleAttemptsWonAgainst=performance['dribbleAttemptsWonAgainst'],
        duelsWon=performance['duelsWon'],
        errorsLeadingToGoal=performance['errorsLeadingToGoal'],
        errorsLeadingToGoalAgainst=performance['errorsLeadingToGoalAgainst'],
        errorsLeadingToShot=performance['errorsLeadingToShot'],
        errorsLeadingToShotAgainst=performance['errorsLeadingToShotAgainst'],
        fastBreakGoals=performance['fastBreakGoals'],
        fastBreakShots=performance['fastBreakShots'],
        fastBreaks=performance['fastBreaks'],
        fouls=performance['fouls'],
        freeKickGoals=performance['freeKickGoals'],
        freeKickShots=performance['freeKickShots'],
        goalsConceded=performance['goalsConceded'],
        goalsFromInsideTheBox=performance['goalsFromInsideTheBox'],
        goalsFromOutsideTheBox=performance['goalsFromOutsideTheBox'],
        goalsScored=performance['goalsScored'],
        groundDuelsWon=performance['groundDuelsWon'],
        headedGoals=performance['headedGoals'],
        hitWoodwork=performance['hitWoodwork'],
        hitWoodworkAgainst=performance['hitWoodworkAgainst'],
        interceptions=performance['interceptions'],
        interceptionsAgainst=performance['interceptionsAgainst'],
        keyPassesAgainst=performance['keyPassesAgainst'],
        lastManTackles=performance['lastManTackles'],
        leftFootGoals=performance['leftFootGoals'],
        longBallsSuccessfulAgainst=performance['longBallsSuccessfulAgainst'],
        longBallsTotalAgainst=performance['longBallsTotalAgainst'],
        matches=performance['matches'],
        offsides=performance['offsides'],
        offsidesAgainst=performance['offsidesAgainst'],
        oppositionHalfPassesTotalAgainst=performance['oppositionHalfPassesTotalAgainst'],
        ownGoals=performance['ownGoals'],
        ownHalfPassesTotalAgainst=performance['ownHalfPassesTotalAgainst'],
        penaltiesCommited=performance['penaltiesCommited'],
        penaltiesTaken=performance['penaltiesTaken'],
        penaltyGoals=performance['penaltyGoals'],
        penaltyGoalsConceded=performance['penaltyGoalsConceded'],
        possessionLost=performance['possessionLost'],
        redCards=performance['redCards'],
        redCardsAgainst=performance['redCardsAgainst'],
        rightFootGoals=performance['rightFootGoals'],
        saves=performance['saves'],
        shots=performance['shots'],
        shotsAgainst=performance['shotsAgainst'],
        shotsBlockedAgainst=performance['shotsBlockedAgainst'],
        shotsFromInsideTheBox=performance['shotsFromInsideTheBox'],
        shotsFromInsideTheBoxAgainst=performance['shotsFromInsideTheBoxAgainst'],
        shotsFromOutsideTheBox=performance['shotsFromOutsideTheBox'],
        shotsFromOutsideTheBoxAgainst=performance['shotsFromOutsideTheBoxAgainst'],
        shotsOffTarget=performance['shotsOffTarget'],
        shotsOffTargetAgainst=performance['shotsOffTargetAgainst'],
        shotsOnTarget=performance['shotsOnTarget'],
        shotsOnTargetAgainst=performance['shotsOnTargetAgainst'],
        successfulDribbles=performance['successfulDribbles'],
        tackles=performance['tackles'],
        tacklesAgainst=performance['tacklesAgainst'],
        totalAerialDuels=performance['totalAerialDuels'],
        totalCrosses=performance['totalCrosses'],
        totalDuels=performance['totalDuels'],
        totalFinalThirdPassesAgainst=performance['totalFinalThirdPassesAgainst'],
        totalGroundDuels=performance['totalGroundDuels'],
        totalLongBalls=performance['totalLongBalls'],
        totalOppositionHalfPasses=performance['totalOppositionHalfPasses'],
        totalOwnHalfPasses=performance['totalOwnHalfPasses'],
        totalPasses=performance['totalPasses'],
        totalPassesAgainst=performance['totalPassesAgainst'],
        yellowCards=performance['yellowCards'],
        yellowCardsAgainst=performance['yellowCardsAgainst'],
        yellowRedCards=performance['yellowRedCards'],
    )
    return performancw
