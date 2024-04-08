import re
import pandas as pd
import numpy as np

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:[ap]m\s)?-\s'

    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    for i in range(len(dates)):
        dates[i] = dates[i][:-3]

    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M')
    df.rename(columns={'message_date':'date'},inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(':\s+', message, maxsplit=1)
        if len(entry) == 2:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'],inplace=True)

    df['message'] = df['message'].apply(lambda x: x[:-1])
    
    
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()
    df.rename(columns={'day': 'day_name'}, inplace=True)
    df['dat'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month

    period = []

    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period

    return df