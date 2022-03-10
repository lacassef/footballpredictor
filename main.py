# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import persistence


import matchservices
from model.optimizedmodels import AwaitingResultsModel

if __name__ == '__main__':
    tod = matchservices.get_today_matches()
    notDup = persistence.check_already_awaiting(tod)
    awaited = []
    fields: [] = None
    # print(notDup)
    for mat in notDup:
        if mat['status'] == 0:
            ma = matchservices.get_match(mat['id'])
            perfH = matchservices.get_performance(ma.home, ma.season, ma.league)
            perfA = matchservices.get_performance(ma.away, ma.season, ma.league)
            awai = AwaitingResultsModel()
            awai.build_from_data(ma, perfH, perfA)
            awaited.append(awai.__dict__)
            if fields is None:
                fields = [*awai.__dict__.keys()]
    persistence.save_awaiting_games(fields, awaited)
    ok = persistence.load_awaiting_games()
