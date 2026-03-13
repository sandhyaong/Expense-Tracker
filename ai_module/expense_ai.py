import pandas as pd


def detect_abnormal_expense(expenses):

    df = pd.DataFrame(expenses)

    avg = df['amount'].mean()

    abnormal = df[df['amount'] > avg * 2]

    return abnormal