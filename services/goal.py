from pathlib import Path
import pandas as pd
from services.list import *

dot = Path("./")
GOALS_PATH = dot / "data" / "goals.csv"
LISTS_PATH = dot / "data" / "lists.csv"

def get_goals_by_user_id(user_id, name):
    """
    Get goals from goals.csv for a specific user.
    """
    #folders = pd.read_csv(LISTS_PATH, delimiter=',')
    #if name in set(folders['list_name']):
    goals_data = pd.read_csv(GOALS_PATH, delimiter=',')
    current_list = get_list_by_name(user_id, name)

    # if list exists

    goal_exists = goals_data.loc[(goals_data['user_id'] == user_id) & (goals_data['list_id'] == current_list['list_id'])].to_dict('records')
    return goal_exists

def create_goal_by_user_id(user_id, goal, list_name):
    goals_data = pd.read_csv(GOALS_PATH, delimiter=',')
    current_list = get_list_by_name(user_id, list_name)
    last_goal_id = goals_data['goal_id'].max()

    df = pd.DataFrame({
        'goal_id': [last_goal_id + 1],
        'list_id': [current_list['list_id']],
        'description': [goal],
        'status': ['in_progress'],
        'user_id': [user_id]
    })
    df.to_csv(GOALS_PATH, mode='a', index=False, header=False)

def change_goal_status(user_id, goal_id, new_status):
    goals_data = pd.read_csv(GOALS_PATH, delimiter=',')

    if new_status == 'deleted':
        indexes = goals_data[ (goals_data['user_id'] == user_id) & (goals_data['goal_id'] == goal_id) ].index
        goals_data.drop(indexes, inplace=True)
        goals_data.to_csv(GOALS_PATH, index=False, header=True)

    elif new_status == 'completed':
        goals_data.at[goal_id,'status']='completed'
    
    goals_data.to_csv(GOALS_PATH, index=False, header=True)
