# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import persistence

import matchservices
from model.optimizedmodels import AwaitingResultsModel, AiTrainingModel


def update_awaited_matches():
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
        m = matchservices.get_match(l.id)
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


if __name__ == '__main__':
    print('Realizando check-ups')
    update_awaited_matches()
    update_results()
    while True:
        print('Escolha a sua operação (zero para sair):')
        ok = int(input('Esc: \n '))
        if ok == 0:
            break

    pass
