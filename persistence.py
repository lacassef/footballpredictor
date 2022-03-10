import csv
import os

import pandas as pd

from model.optimizedmodels import AwaitingResultsModel, AiTrainingModel


def check_already_awaiting(awaited: list) -> []:
    actual = []
    with open(file='persistence/awaited.csv', mode='r+', newline='') as file:
        writer = csv.DictReader(file)
        ids = [i['id'] for i in writer]
        for row in awaited:
            if not (str(row['id']) in ids):
                actual.append(row)
    return actual


def check_already_training(training: list) -> []:
    actual = []
    with open(file='persistence/training.csv', mode='r+', newline='') as file:
        writer = csv.DictReader(file)
        ids = [i['id'] for i in writer]
        for row in training:
            if not (str(row.id) in ids):
                actual.append(row)
    return actual


def save_awaiting_games(fields: [], awaited: list):
    actual = []
    with open(file='persistence/awaited.csv', mode='r+', newline='') as file:
        writer = csv.DictReader(file, fields)
        ids = [i['id'] for i in writer]
        for row in awaited:
            if not (str(row['id']) in ids):
                actual.append(row)
    with open(file='persistence/awaited.csv', mode='a+', newline='') as file:
        writer = csv.DictWriter(file, fields)
        if not file.tell():
            writer.writeheader()
        writer.writerows(actual)


def save_training_games(fields: [], training: list[dict]):
    actual = []
    with open(file='persistence/training.csv', mode='r+', newline='') as file:
        writer = csv.DictReader(file, fields)
        ids = [i['id'] for i in writer]
        for row in training:
            if not (str(row['id']) in ids):
                actual.append(row)
    with open(file='persistence/training.csv', mode='a+', newline='') as file:
        writer = csv.DictWriter(file, fields)
        if not file.tell():
            writer.writeheader()
        writer.writerows(actual)


def load_awaiting_games() -> list[AwaitingResultsModel]:
    ex: list[AwaitingResultsModel] = []
    with open(file='persistence/awaited.csv', mode='r+', newline='') as file:
        writer = csv.DictReader(file)
        for row in writer:
            awa = AwaitingResultsModel()
            awa.from_dict(row)
            ex.append(awa)
    return ex
