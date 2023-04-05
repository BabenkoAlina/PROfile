from pathlib import Path
import pandas as pd
import re
import unicodedata

dot = Path("./")
GOALS_PATH = dot / "data" / "goals.csv"
LISTS_PATH = dot / "data" / "lists.csv"

def get_lists_by_user_id(user_id):
    list_data = pd.read_csv(LISTS_PATH, delimiter=',')
    results = list_data.loc[list_data['user_id'] == user_id].to_dict('records')
    return results

def get_list_by_name(user_id, name):
    list_data = pd.read_csv(LISTS_PATH, delimiter=',')
    list = list_data.loc[(list_data['list_url'] == name) & (list_data['user_id'] == user_id)].to_dict('records')
    return list[0]

def delete_particular_list(user_id, list_id):
    # delete all goals in the list to be deleted
    print('deleting', user_id, list_id)
    goals_data = pd.read_csv(GOALS_PATH, delimiter=',')
    goals_in_list = goals_data[(goals_data['user_id'] == user_id) & (goals_data['list_id'] == list_id)].index
    goals_data.drop(goals_in_list, inplace=True)
    goals_data.to_csv(GOALS_PATH, mode='w', index=False, header=True)

    # delete the desired list
    lists_data = pd.read_csv(LISTS_PATH, delimiter=',')
    list_to_be_deleted = lists_data[(lists_data['user_id'] == user_id) & (lists_data['list_id'] == list_id)].index
    lists_data.drop(list_to_be_deleted, inplace=True)
    lists_data.to_csv(LISTS_PATH, mode='w', index=False, header=True)

def create_list_by_user_id(user_id, name):
    list_data = pd.read_csv(LISTS_PATH, delimiter=',')
    last_id = list_data['list_id'].max()

    list_exists = len(list_data.loc[(list_data['list_name'] == name) & (list_data['user_id'] == user_id)].to_dict('records'))

    if list_exists < 1: 
        df = pd.DataFrame({
            'list_id': [last_id + 1],
            'list_name': [name],
            'list_url': [slugify(name)],
            'user_id': [user_id]
        })
        df.to_csv(LISTS_PATH, mode='a', index=False, header=False)
    else:
        print('ERROR!')
 
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower()).strip()
    return re.sub(r'[-\s]+', '-', value)
