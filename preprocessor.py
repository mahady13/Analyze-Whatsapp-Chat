import re
import pandas as pd
def preprocess(data):
    pattern=r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':messages,'date':dates})
    df['date']=pd.to_datetime(df['date'],format='%m/%d/%y, %H:%M - ')
    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    users = []
    msg_list = []

    for message in df['user_message']:
        parts = message.split(': ', 1)

        if len(parts) > 1:
            users.append(parts[0].strip())
            msg_list.append(parts[1].strip())
        else:
            users.append('group_notification')
            msg_list.append(parts[0].strip())

    df['users'] = users
    df['messages'] = msg_list

    df.drop(columns=['user_message'], inplace=True)
    df = df.drop(df[df['users'] == 'group_notification'].index).reset_index(drop=True)

    return df