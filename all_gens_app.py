import pandas as pd
import streamlit as st
import uuid
import re
from pathlib import Path

st.set_page_config(layout="wide")

def find_game(column,dataframe):
    series = []
    for col in column:
        indices = [i for i in range(len(dataframe)) 
                   if str(dataframe[col].iloc[i]).replace('\n','') not in ['Trade','Unobtainable','Pokémon Bank','Pokémon HOME']
                   and not dataframe[col].str.contains('Trade, |Trade Version|Time Capsule|Pokémon HOME Version|Poké Transfer|Global Link').iloc[i]]
        series = series + indices
    series = list(set(series))
    return dataframe[['No.','Caught?',*column]].iloc[series].sort_values(by='No.')
    
def find_game_nan(column,dataframe):
    series = []
    for col in column:
        indices = [i for i in range(len(dataframe)) 
                   if str(dataframe[col].iloc[i]).replace('\n','') not in ['Trade','Unobtainable','Pokémon Bank','Pokémon HOME']
                   and not dataframe[col].str.contains('Trade, |Trade Version|Time Capsule|Pokémon HOME Version|Poké Transfer|Global Link').iloc[i]]
        series.append(dataframe[col].iloc[indices])
    combined = pd.concat(series,axis=1)
    combined[['No.','Caught?']] = dataframe[['No.','Caught?']].loc[combined.index]
    combined = combined[['No.','Caught?']+column]
    return combined.sort_values(by='No.')

def get_dif(columns,dataframe):
    dummy = find_game_nan(columns,dataframe)
    indexes = []
    for column in columns:
        data = dummy[column]
        index = list(data[pd.isna(data)].index)
        indexes.append(index)
    indexes_flat = list(set([x for y in indexes for x in y]))
    return dummy.loc[indexes_flat].sort_values(by='No.')

def get_intersection(columns,dataframe):
    return find_game_nan(columns,dataframe).dropna()

def one_game_exclusive(one,others,dataframe):
    if type(one) == str:
        dummy = get_dif([one]+others,dataframe)
    else:
        dummy = get_dif(one+others,dataframe)
    one_each = []
    for i in range(len(dummy)):
        pokemon = dummy.iloc[i]
        if pd.isna(pokemon[others].unique()).all():
            one_each.append(i)
    return dummy[['No.','Caught?']+one].iloc[one_each].dropna()

def one_game_inclusive(one,others,dataframe):
    if type(one) == str:
        dummy = get_dif([one]+others,dataframe)
    else:
        dummy = get_dif(one+others,dataframe)
    one_each = []
    for i in range(len(dummy)):
        pokemon = dummy.iloc[i]
        if pd.isna(pokemon[others].unique()).all():
            one_each.append(i)
    indices = [list(dummy.index)[x] for x in one_each]
    # return dummy[['No.','Caught?']+one].iloc[one_each]
    return dataframe[['No.','Caught?']+one].loc[indices]

def searching(dataframe,columns,search_term):
    series = []
    for col in columns:
        indices = list(dataframe[col][dataframe[col].apply(
            lambda z: any(
                [all([bool(re.search(r'\b' + x +r's?\b',y.lower())) for x in search_term.lower().split()])
                 for y in re.split(r', (?=[A-Z])|& (?=[A-Z])',' ' + str(z))]))].index)
        series = series + indices
    series = list(set(series))
    return dataframe[['No.','Caught?',*columns]].loc[series].sort_values(by='No.')

def update_value():
    """
    Located on top of the data editor.
    """
    st.session_state.df = pd.read_csv(st.session_state.gen + " pokedex.csv",index_col="Pokemon")
    st.session_state.dek = str(uuid.uuid4())  # triggers reset

def save_caught(): 
    st.session_state.df.loc[st.session_state.caught.index,'Caught?'] = st.session_state.caught
    st.session_state.csv = st.session_state.df.to_csv()


def main():
    
    # Initialize session_state variables
    
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv("Generation I pokedex.csv",index_col="Pokemon")
    if 'caught' not in st.session_state:
        st.session_state.caught = st.session_state.df['Caught?']
    if 'file' not in st.session_state:
        st.session_state.file = True
    if 'dek' not in st.session_state:
        st.session_state.dek = str(uuid.uuid4())      
    if 'gen' not in st.session_state:
        st.session_state.gen = 'Generation I'
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Generation I'
    if 'csv' not in st.session_state:
        st.session_state.csv = st.session_state.df.to_csv()
    st.title('Gotta Catch \'Em All!')
    generations = ['Generation I',
               'Generation II',
               'Generation III',
               'Generation IV',
               'Generation V',
               'Generation VI',
               'Generation VII',
               'Generation VIII',
               'Generation IX']
    
    #Define buttons and options
    with st.sidebar:
        st.session_state.gen = st.selectbox('Select Generation:',generations)
        if st.session_state.gen != st.session_state.mode:
            st.session_state.df = pd.read_csv(st.session_state.gen + " pokedex.csv",index_col="Pokemon")
            st.session_state.mode = st.session_state.gen
            
    games_list = list(pd.read_csv(st.session_state.gen + " pokedex.csv",index_col="Pokemon").columns[2:])
    
    with st.sidebar.form('search_form'):
        button = st.radio('Get Pokemon that are in',['all of','at least one of'],horizontal=True)
        game = st.multiselect(
            "",
            games_list,
            label_visibility='collapsed'
        )    
        game_not = st.multiselect(
            "But not in:",
            games_list,
        )
        
        search_bar = st.text_input('Keywords')        
        st.form_submit_button("Search",on_click = save_caught)

    #Load Dataframe based on options
    if game and game_not and button == 'all of':
        search_df = one_game_exclusive(game,game_not,st.session_state.df)
        
    elif game and game_not and button == 'at least one of':
        search_df = one_game_inclusive(game,game_not,st.session_state.df)
        
    elif game and button == 'all of':
        search_df = get_intersection(game,st.session_state.df)
        
    elif game and button == 'at least one of':
        search_df = find_game(game,st.session_state.df)
        
    else:
        search_df = st.session_state.df

    #Report back the dataframe
    
    if search_bar:
        if game:
            search_df = searching(search_df,game,search_bar)
        else:
            search_df = searching(search_df,games_list,search_bar)

    st.write(f'Total Pokemon found: {len(search_df)}')
    editor = st.data_editor(
        search_df,
        key = st.session_state.dek,
        column_config = {
                "Caught?":st.column_config.CheckboxColumn(
                None,
                help="Select which Pokemon you've already caught",
                default=False,
            )
        },
        disabled = ('Pokemon','No.',*games_list)       
    )
    #Record the changes to the dataframe
    st.session_state.caught = pd.Series(
        [x['Caught?'] for x in list(st.session_state[st.session_state.dek]["edited_rows"].values())],
        index=editor.index[list(st.session_state[st.session_state.dek]["edited_rows"].keys())])
    with st.sidebar:
        download_button = st.sidebar.download_button(
        label="Download Pokedex",
        data=editor.to_csv(),
        file_name= st.session_state.gen + " pokedex.csv",
        mime="text/csv",
        on_click = save_caught
        )
        uploaded_file = st.file_uploader("Load a Previous Tracker")

    clear_button = st.button('Clear \"Caught?\" Column',on_click=update_value)
    
    #Get uploaded file, if available 
    if uploaded_file is not None and st.session_state.file:
        if Path(uploaded_file.name).suffix != '.csv':
            st.write(f'File type is {Path(uploaded_file.name).suffix}, needs to be .csv!')
        else:
            uploaded_df = pd.read_csv(uploaded_file,index_col="Pokemon")
            if any(uploaded_df.columns != st.session_state.df.columns) or any(uploaded_df.index != st.session_state.df.index):
                st.write('Columns and/or rows do not match current Pokedex')
            else:
                update_value()
                st.session_state.df = uploaded_df
                st.session_state.file = False
                st.rerun()
    elif uploaded_file is None:
        st.session_state.file = True

if __name__ == "__main__":
    main()
