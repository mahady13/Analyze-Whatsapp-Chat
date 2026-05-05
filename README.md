WhatsApp Chat Analyzer
This is a Python based web application that allows users to analyze their WhatsApp chat exports. It provides various insights such as message statistics, most active users, word clouds, emoji analysis, and activity heatmaps.

Key Features
Overall and User-level Analysis: View statistics for the entire group or a specific person.

Top Statistics: Total messages, words, media shared, and links shared.

Monthly and Daily Activity: Visual timelines showing when the chat was most active.

Activity Map: Identify the busiest days of the week and months.

Weekly Activity Heatmap: A detailed grid showing the busiest hours of each day.

Most Active Users: Graphical representation of users who message the most.

WordCloud: Visual representation of the most frequently used words.

Most Common Words: A bar chart showing frequently used words after removing stop words.

Emoji Analysis: Breakdown of the most used emojis in the conversation.

How to run this project
Clone this repository to your local machine.

Install the required libraries using: pip install -r requirements.txt.

Run the application using: streamlit run main.py.

Export your WhatsApp chat(Time=24hours format) as a .txt file (without media) and upload it to the app.
