# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from numpy import mean, asarray, std

import bothtoscore
import persistence

import matchservices
import training
from model.optimizedmodels import AwaitingResultsModel, AiTrainingModel, AiPredictionModel, AiPredictionResult, \
    AiBothScoreModel


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
    oka = persistence.check_already_both_score(loads)
    training = []
    both = []
    fields: [] = None
    fields_btts: [] = None
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
    for l in oka:
        # print('Executed')
        try:
            m = matchservices.get_match(l.id)
        except:
            print(f'Jogo {l.id} sem match')
            continue
        if m.status == 100 or m.status == 120 or m.status == 110:
            i = AiBothScoreModel()
            i.build_model(m, l)
            # print(i)
            both.append(i.__dict__)
            if fields_btts is None:
                fields_btts = [*i.__dict__.keys()]
    persistence.save_training_games(fields, training)
    persistence.save_both_score_games(fields_btts, both)
    if len(training) > 0 or len(both) > 0:
        print('Resultados atualizados!')
    else:
        print('Sem novos resultados!')


def predict_today():
    print('Começou a predição')
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
            predbtts = bothtoscore.make_prediction(wi.__dict__)
            result = AiPredictionResult(home=ma.homeName, away=ma.awayName,
                                        time=ma.time, homeWin=('%.2f%%' % (float(pred[0]) * 100)),
                                        awayWin=('%.2f%%' % (float(pred[2]) * 100)),
                                        draw=('%.2f%%' % (float(pred[1]) * 100)),
                                        date=ma.date, bothToScore=('%.2f%%' % (float(predbtts[0]) * 100)))
            results.append(result)
    if len(results) > 0:
        with pd.ExcelWriter('predicoes.xlsx',
                            mode='a', if_sheet_exists="replace") as writer:
            df = pd.DataFrame(results)
            df.to_excel(writer, sheet_name=results[0].date.replace('/', '-'),
                        index=False)


def predict_date():
    date = int(input('Insira o dia\n'))
    month = int(input('Insira o mes\n'))
    year = int(input('Insira o ano\n'))
    tod = matchservices.get_matches_from_date(year, month, date)
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
            predbtts = bothtoscore.make_prediction(wi.__dict__)
            result = AiPredictionResult(home=ma.homeName, away=ma.awayName,
                                        time=ma.time, homeWin=('%.2f%%' % (float(pred[0]) * 100)),
                                        awayWin=('%.2f%%' % (float(pred[2]) * 100)),
                                        draw=('%.2f%%' % (float(pred[1]) * 100)),
                                        date=ma.date, bothToScore=('%.2f%%' % (float(predbtts[0]) * 100)))
            results.append(result)
    if len(results) > 0:
        with pd.ExcelWriter('predicoes.xlsx',
                            mode='a', if_sheet_exists="replace") as writer:
            df = pd.DataFrame(results)
            df.to_excel(writer, sheet_name=results[0].date.replace('/', '-'),
                        index=False)


def evaluate_model():
    X, y = training.get_training_data()
    results = training.evaluate_model(X, y)
    print('Average accuracy: %.2f%% \nStandart deviation: %.2f%%' % ((mean(results)) * 100, (std(results) * 100)))


def evaluate_btts_model():
    X, y = bothtoscore.get_training_data()
    results = bothtoscore.evaluate_model(X, y)
    print('Average accuracy: %.2f%% \nStandart deviation: %.2f%%' % ((mean(results)) * 100, (std(results) * 100)))


if __name__ == '__main__':
    print('Realizando check-ups')
    update_awaited_matches()
    update_results()
    while True:
        print('Escolha a sua operação (zero para sair):')
        try:
            ok = int(
                input('1 -> Avaliar os modelos\n2 -> Obter predições de hoje\n3 -> Obter predições de outra data\n'))
        except:
            continue
        if ok == 0:
            break
        elif ok == 2:
            predict_today()
        elif ok == 1:
            print('Vencedor do jogo')
            evaluate_model()
            print('Ambas marcam')
            evaluate_btts_model()
        elif ok == 3:
            predict_date()

    pass
