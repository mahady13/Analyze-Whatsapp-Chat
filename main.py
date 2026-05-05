
import streamlit as st
import seaborn as sns
import preprocessor as pp
import helper
from matplotlib import pyplot as plt

st.sidebar.title('Analyze Whatsapp Chat(24hours format)')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=pp.preprocess(data)

    #fetch unique user
    user_list=df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox('Show analysis with',user_list)

    if st.sidebar.button('Analyze'):
        st.title('TOP STATISTICS')



        num_messages,num_words,num_media,num_links=helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(num_words)
        with col3:
            st.header('Total Media shared')
            st.title(num_media)
        with col4:
            st.header('Total links shared')
            st.title(num_links)
#monthly message analysis
        st.header('Monthly Messages Analysis')
        timeline = helper.timeline_maker(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'],color='teal')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


#day analysis
        st.title('Activity Map')
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            day_df = helper.day_analysis(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(day_df['day_name'],day_df['messages'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            month_df=helper.month_analysis(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(month_df['month'],month_df['count'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
    #daily timeline
        st.header('Daily Message Analysis')
        daily_timeline=helper.daily_analysis(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['messages'],color='pink')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    #find the busiest users in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            name,count,new_df=helper.fetch_most_busy(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:

                ax.bar(name, count,color='teal')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #busy time of the day
        st.title('Busiest Time Of The Day')
        heat=helper.heatmap_time(selected_user,df)
        fig,ax2=plt.subplots()
        ax2=sns.heatmap(heat)
        st.pyplot(fig)
        plt.yticks(rotation='horizontal')
        plt.show()
        #wordcloud
        st.title('WordCloud')
        fig,ax=plt.subplots()
        df_wc=helper.wordcloud(selected_user,df)
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title('Most Common Words')
        newdf2=helper.most_common_word(selected_user,df)
        fig2,ax2=plt.subplots()
        ax2.barh(newdf2[0],newdf2[1],color='teal')
        plt.xticks(rotation='vertical')
        st.pyplot(fig2)

        #most emojis used
        emojis_df=helper.emoji_extractor(selected_user, df)

        st.title('Emoji Analysis')
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emojis_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emojis_df[1],labels=emojis_df[0],startangle=90,autopct='%1.2f%%')
            st.pyplot(fig)
