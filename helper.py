from ctypes.macholib.dyld import dyld_framework_path
from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter
import banglish_stopwords as bs
import emoji
import pandas as pd

geturl = URLExtract()
def fetch_stats(user_name,df):
    if user_name !='Overall':
        df = df[df['users'] == user_name]
    #if overall is called then all df is considered otherwise df is changed to a newer version where only the selected users info is available in it
    #thats why the code works even if its short

    #num of total words
    words = []
    for message in df['messages']:
        words.extend(message.split())
    #num of total messages
    num_messages = df.shape[0]
    #num of total media messages
    num_media=df[df['messages']=='<Media omitted>'].shape[0]
    #total number of links shared
    links = []
    for message in df['messages']:
        links.extend(geturl.find_urls(message))
    num_links=len(links)
    return num_messages, len(words),num_media,num_links

def fetch_most_busy(df):
    x=df['users'].value_counts().head()
    name=x.index
    count=x.values
    new_df = round((df['users'].value_counts() / df['users'].shape[0]) * 100, 2).reset_index().rename(
        columns={'users': 'Name', 'count': 'Percentage'})
    return name,count,new_df

def wordcloud(user_name,df):
    if user_name !='Overall':
        df = df[df['users'] == user_name]
    def remove_stopwords(message):
        y=[]
        stopwords = bs.BanglishStopwords()
        llist=stopwords.get_stopwords()
        for word in message.lower().split():
            if word not in llist and word.strip() not in ['-', '---------']:
                y.append(word)
        return " ".join(y)
    temp = df[df['messages'] != '<Media omitted>']
    temp['messages']=temp['messages'].apply(remove_stopwords)
    wc=WordCloud(width=800, height=600, min_font_size=10, background_color='white',)
    if user_name !='Overall':
        temp = temp[temp['users'] == user_name]
    df_wc=wc.generate(temp['messages'].str.cat(sep=''))
    return df_wc

def most_common_word(user_name,df):
    if user_name !='Overall':
        df = df[df['users'] == user_name]
    words = []
    stwd = bs.BanglishStopwords()
    llist = stwd.get_stopwords()
    temp = df[df['messages'] != '<Media omitted>']
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in llist and word.strip() not in ['-', '---------']:
                words.append(word)
    commonWordDf = pd.DataFrame(Counter(words).most_common(20))
    return commonWordDf

def emoji_extractor(selected_user,df):
    if selected_user !='Overall':
        df = df[df['users'] == selected_user]
    emojis=[]
    for message in df['messages']:
        found=([c for c in message if c in emoji.EMOJI_DATA])
        emojis.extend(found)
    emoji_df=pd.DataFrame(Counter(emojis).most_common(5),columns=['Emoji','Count'])
    return emoji_df

def timeline_maker(selected_user,df):
    if selected_user !='Overall':
        df = df[df['users'] == selected_user]
    df['month_number']=df['date'].dt.month
    timeline=df.groupby(['year','month_number','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_analysis(selected_user,df):
    if selected_user !='Overall':
        df = df[df['users'] == selected_user]
    df['only_date']=df['date'].dt.date
    daily_df=df.groupby(['only_date']).count()['messages'].reset_index()
    return daily_df

def day_analysis(selected_user,df):
    if selected_user !='Overall':
        df = df[df['users'] == selected_user]
    df['day_name']=df['date'].dt.day_name()
    day_df=df.groupby(['day_name']).count()['messages'].reset_index()
    return day_df

def month_analysis(selected_user,df):
    if selected_user !='Overall':
        df = df[df['users'] == selected_user]
    month_df=df['month'].value_counts().reset_index()
    return month_df

def heatmap_time(selected_user,df):
    if selected_user !='Overall':
        df = df[df['users'] == selected_user]
    period=[]
    for hour in df['hour']:
        if hour==23:
            period.append(str(hour)+'-'+str('00'))
        elif hour==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    df['period']=period
    heat=df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return heat