import plotly.express as px
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from Testfn import *
from streamlit_option_menu import option_menu
import plotly.graph_objects as go


# -------------------------------- Page Title --------------------------------------------
st.set_page_config(page_title = 'Cricket Analyze')

# -------------------------------- Add BackGround image  --------------------------------------------
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://st2.depositphotos.com/1001941/6345/v/600/depositphotos_63452319-stock-illustration-cricket-sports-concept-with-red.jpg");
             #background-image: url("https://cdn.dnaindia.com/sites/default/files/styles/full/public/2023/03/31/2582506-whatsapp-image-2023-03-31-at-5.07.51-pm.jpeg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

# -------------------------------- lottie bird animation -------------------------------------------- 

#st.markdown("<h1 style='text-align: center; color: black; background-color: white; '>Cricket Analyze</h1>", unsafe_allow_html=True)

def load_lottieURl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# lottie_bird = load_lottieURl("https://assets8.lottiefiles.com/packages/lf20_Hw1OgduFe1.json")

# st_lottie(lottie_bird, height=300, width=700, key='bird')

# -------------------------------- Streamlit Setups -------------------------------------------- 

menu = option_menu(
                    menu_title='Cricket Analyze',
                    options=['Live Score',
                            'Team Scorecard',
                            'Analysis'],
                    icons=['activity', 'back',
                            'back', 'pie-chart'],
                    default_index=0,
                    orientation = "horizontal"
                    )
#-----------------------------------------------LIVE SCORES-----------------------------------------------------------------

if menu == 'Live Score':
    #scrape = st.button("Cricket - LIVE SCORE")

    url = "https://www.cricbuzz.com/live-cricket-scores/66250/rr-vs-csk-17th-match-indian-premier-league-2023"
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")
    live_score = soup.find("div", {"class": "cb-min-bat-rw" })
    text = soup.find("div", {"class": "cb-text-inprogress" })
    # Find the live score element
    # live_score = soup.find("div", {"class": "cb-col cb-col-67 cb-nws-lft-col cb-comm-pg"}) # cb-col-100 cb-col cb-col-scores | "cb-col cb-col-67 cb-nws-lft-col cb-comm-pg" | "cb-col-100 cb-col cb-schdl"
    if live_score is not None:
        #print(live_score.text)
        live = live_score.text   
        # Split the text
        split_text = live.split()

        # Create a dictionary
        live_score_dict = {'Team': [split_text[0]], 'Score': [split_text[1:3]], 'CRR': [split_text[4]]}

        # Create the dataframe
        df_live = pd.DataFrame(live_score_dict)

        # Print the dataframe
        st.dataframe(df_live)
    else:
        print("Live score not found.")

    if text is not None:
        df_decision = pd.DataFrame([text.text], columns=['Decision'])
        st.dataframe(df_decision)
    else:
        print("text not found.")
        
    final_res = soup.find("div", {"class": "cb-col cb-col-100 cb-min-stts cb-text-complete" })
    if final_res is not None:
        df_final_res = pd.DataFrame([final_res.text], columns=['Result'])
        st.dataframe(df_final_res)
    else:
        pass

#-------------------------------------------------------------------------------------------#

#1st innings
df_innings1 = Team1()
batsmen_df_in1, extras_df_in1, total_df_in1, bowlers_df_in1 = innings1(df_innings1)

with open('scorecard_innings2.csv', 'w', newline='') as csvfile:
            
                writer = csv.writer(csvfile)
                
                # Write the header row
                writer.writerow(['Batsman', 'Dismissal', 'Runs', 'Balls', '4s', '6s', 'SR','',""])


# 2nd innings
df_innings2 = Team2()
batsmen_df_in2, extras_df_in2, total_df_in2, bowlers_df_in2 = innings2(df_innings2)


if menu == 'Team Scorecard':
    Teams = ["RR","CSK"]
    Team_Selection = st.selectbox('Select the Team:', options= Teams)

    if Team_Selection == 'RR':
        
        st.dataframe(batsmen_df_in1)
        st.dataframe(extras_df_in1)
        st.dataframe(total_df_in1)
        st.dataframe(bowlers_df_in1)

    if Team_Selection == 'CSK':
          
         st.dataframe(batsmen_df_in2)
         st.dataframe(extras_df_in2)
         st.dataframe(total_df_in2)
         st.dataframe(bowlers_df_in2)

#-----------------------------------------------------------------------------------------------#


if menu == 'Analysis':
            
        Teams = ["RR","CSK"]

        Team_Selection = st.selectbox('Select the Team:', options= Teams)

        if Team_Selection == "RR":

            Analyze = ["Top 5 Run Scorer",
                       "Top 5 Wicket Taker",
                       "Top Bowling Analyze",
                       "Team Strike Rate Analyze"]
            
            Analyze_Selection = st.selectbox('Select the Team:', options= Analyze)

            Runs_1 = batsmen_df_in1.sort_values('Runs',ascending = False).head()
            Runs_1 = Runs_1.sort_values('Runs')
            if bowlers_df_in2 is not None:
                Bowl_1 = bowlers_df_in2.sort_values('W',ascending = False).head()
                ECO_1 = bowlers_df_in2.sort_values(['W','ECO'],ascending = [False,True])

            if Analyze_Selection == "Top 5 Run Scorer":

                # Create a scatter plot of the number of balls vs. run rate
                bar_trace = go.Bar(x=Runs_1["Batsman"], y=Runs_1["Runs"],marker=dict(color='#e73895'))
                line_trace = go.Scatter(x=Runs_1["Batsman"], y=Runs_1["Runs"],line=dict(color='#254AA5'), yaxis='y2')

                layout = go.Layout(
                    title='Bar and Line Chart with Dual Axis',
                    yaxis=dict(title='Bar Data'),
                    yaxis2=dict(title='Line Data', overlaying='y', side='right')
                )

                fig = go.Figure(data=[bar_trace, line_trace], layout=layout)
                st.plotly_chart(fig)

            if Analyze_Selection == "Top 5 Wicket Taker":
                if bowlers_df_in2 is not None:
                    # Create a scatter plot of the number of balls vs. run rate
                    fig = px.bar(
                        Bowl_1,
                        x='Bowler',
                        y='W',
                        color_discrete_sequence=['#e73895'],
                        title='Bowling Analyze',
                        hover_data=['W','ECO','Bowler']
                    )
                    st.plotly_chart(fig)

            if Analyze_Selection == "Top Bowling Analyze":
                if bowlers_df_in2 is not None:
                    # Create a scatter plot of the number of balls vs. run rate
                    fig = px.bar(
                        ECO_1,
                        x='Bowler',
                        y='ECO',
                        color_discrete_sequence=['#e73895'],
                        title='Bowling Analyze',
                        hover_data=['W','ECO','Bowler']
                    )
                    st.plotly_chart(fig)

            if Analyze_Selection == "Team Strike Rate Analyze":

                fig = go.Figure(go.Scatter(x = batsmen_df_in1['Batsman'],
                                           y = batsmen_df_in1['SR'],
                                           line=dict(color='#e73895'),
                                           marker=dict(color='#254AA5'),
                                           mode = 'lines+markers'))
                st.plotly_chart(fig)
             

            #-----------------------------------------------------------------#

        if Team_Selection == "CSK":

            Analyze = ["Top 5 Run Scorer",
                       "Top 5 Wicket Taker",
                       "Top Bowling Analyze",
                       "Team Strike Rate Analyze"]
            
            Analyze_Selection = st.selectbox('Select the Team:', options= Analyze)
            if batsmen_df_in2 is not None:
                Runs_2 = batsmen_df_in2.sort_values('Runs',ascending = False).head()
                Runs_2 = Runs_2.sort_values('Runs')
            Bowl_2 = bowlers_df_in1.sort_values('W',ascending = False).head()
            ECO_2 = bowlers_df_in1.sort_values(['W','ECO'],ascending = [False,True])

            if Analyze_Selection == "Top 5 Run Scorer":
                if batsmen_df_in2 is not None:
                    # Create a scatter plot of the number of balls vs. run rate
                    bar_trace = go.Bar(x=Runs_2["Batsman"], y=Runs_2["Runs"], marker=dict(color='#FFD700'))
                    line_trace = go.Scatter(x=Runs_2["Batsman"], y=Runs_2["Runs"],line=dict(color='#1C2C5B'), yaxis='y2')

                    layout = go.Layout(
                        title='Bar and Line Chart with Dual Axis',
                        yaxis=dict(title='Bar Data'),
                        yaxis2=dict(title='Line Data', overlaying='y', side='right')
                    )

                    fig = go.Figure(data=[bar_trace, line_trace], layout=layout)
                    st.plotly_chart(fig)
    
            if Analyze_Selection == "Top 5 Wicket Taker":

                # Create a scatter plot of the number of balls vs. run rate
                fig = px.bar(
                    Bowl_2,
                    x='Bowler',
                    y='W', 
                    color_discrete_sequence=['#FFD700','#1C2C5B'],
                    title='Bowling Analyze',
                    hover_data=['W','ECO','Bowler']
                )
                st.plotly_chart(fig)

            if Analyze_Selection == "Top Bowling Analyze":

                # Create a scatter plot of the number of balls vs. run rate
                fig = px.bar(
                    ECO_2,
                    x='Bowler',
                    y='ECO',
                    color_discrete_sequence=['#FFD700','#1C2C5B'],
                    title='Bowling Analyze',
                    hover_data=['W','ECO','Bowler']
                )
                st.plotly_chart(fig)
                
            if Analyze_Selection == "Team Strike Rate Analyze":
                if batsmen_df_in2 is not None:
                    fig = go.Figure(go.Scatter(x = batsmen_df_in2['Batsman'],
                                            y = batsmen_df_in2['SR'],
                                            line=dict(color='#FFD700'),
                                            marker=dict(color='#1C2C5B'),
                                            mode = 'lines+markers'))
                    st.plotly_chart(fig)
 


