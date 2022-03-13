# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd

import persistence

import matchservices
import training
from model.optimizedmodels import AwaitingResultsModel, AiTrainingModel, AiPredictionModel, AiPredictionResult


def update_awaited_matches():
    tod = matchservices.get_today_matches()
    notDup = persistence.check_already_awaiting(tod)
    awaited = []
    fields: [] = None
    # print(notDup)
    for mat in notDup:
        if mat['status'] == 0:
            ma = matchservices.get_match(mat['id'])
            try:
                perfH = matchservices.get_performance(ma.home, ma.season, ma.league)
                perfA = matchservices.get_performance(ma.away, ma.season, ma.league)
            except:
                print(f'Jogo {ma.id} sem dados')
                continue
            awai = AwaitingResultsModel()
            awai.build_from_data(ma, perfH, perfA)
            awaited.append(awai.__dict__)
            if fields is None:
                fields = [*awai.__dict__.keys()]
    persistence.save_awaiting_games(fields, awaited)
    if len(awaited) > 0:
        print('Jogos adicionados!')
    else:
        print('Sem novos jogos!')


def update_results():
    loads = persistence.load_awaiting_games()
    okw = persistence.check_already_training(loads)
    training = []
    fields: [] = None
    for l in okw:
        # print('Executed')
        try:
            m = matchservices.get_match(l.id)
        except:
            print(f'Jogo {l.id} sem match')
            continue
        if m.status == 100 or m.status == 120 or m.status == 110:
            i = AiTrainingModel()
            i.build_model(m, l)
            # print(i)
            training.append(i.__dict__)
            if fields is None:
                fields = [*i.__dict__.keys()]
    persistence.save_training_games(fields, training)
    if len(training) > 0:
        print('Resultados atualizados!')
    else:
        print('Sem novos resultados!')


def predict_today():
    tod = matchservices.get_today_matches()
    results = []
    for i in tod:
        if i['status'] == 0:
            try:
                ma = matchservices.get_match(i['id'])
            except:
                continue
            try:
                perfH = matchservices.get_performance(ma.home, ma.season, ma.league)
                perfA = matchservices.get_performance(ma.away, ma.season, ma.league)
            except:
                print(f'Jogo {ma.id} sem dados')
                continue
            awai = AwaitingResultsModel()
            awai.build_from_data(ma, perfH, perfA)
            wi = AiPredictionModel()
            wi.build_model(awai)
            pred = training.make_prediction(wi.__dict__)
            result = AiPredictionResult(home=ma.homeName, away=ma.awayName,
                                        time=ma.time, homeWin=('%.2f%%' % (float(pred[0]) * 100)),
                                        awayWin=('%.2f%%' % (float(pred[2]) * 100)), draw=('%.2f%%' % (float(pred[1]) * 100)),
                                        date=ma.date)
            results.append(result)
    if len(results) > 0:
        with pd.ExcelWriter('predicoes.xlsx',
                            mode='a', if_sheet_exists="replace") as writer:
            df = pd.DataFrame(results)
            df.to_excel(writer, sheet_name=results[0].date.replace('/', '-'),
                        index=False)


if __name__ == '__main__':
    print('Realizando check-ups')
    update_awaited_matches()
    update_results()
    while True:
        print('Escolha a sua operação (zero para sair):')
        ok = int(input('1 -> Obter predições de hoje: \n '))
        if ok == 0:
            break
        elif ok == 1:
            predict_today()

    pass
