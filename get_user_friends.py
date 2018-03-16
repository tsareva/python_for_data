import pandas as pd
import networkx as nx
import time
import numpy as np

import os
os.chdir(r"C:\Users\ATsareva\Desktop\Students") #work folder

import vk_api

def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device

login = input("login: ") 
password = input("password: ")
vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler  
    )

vk_session.auth()

tools = vk_api.VkTools(vk_session)
vk = vk_session.get_api()

def get_friends_for_sure(user):        
    while True:
        try:
            my_friends = get_all_friends(user)
            return my_friends
        except:
            print('sleep')
            time.sleep(1)
            continue
            
def get_all_friends(user_id):
	user_id = int(user_id)
	all_friends = tools.get_all('friends.get', 5000, 
								{'user_id': user_id, 
								'fields': 'sex,bdate,city,country,education'})
	all_friends = all_friends['items']
	for item in all_friends:
		item['country'] = item.get('country', {}).get('title', None)
		item['city'] = item.get('city', {}).get('title', None)
	friends_df = pd.DataFrame.from_dict(all_friends)
	if 'bdate' in friends_df.columns:
		friends_df['bdate'] = pd.to_datetime(friends_df['bdate'], errors='coerce')
	return friends_df

def get_all_members(group):
	members = tools.get_all('groups.getMembers', 500, 
                           {'group_id': str(group),
                            'fields': 'sex,bdate,city,country,education'})
	members = members['items']
	for member in members:
		member['city_id'] = member.get('city', {}).get('id', None)
		member['city'] = member.get('city', {}).get('title', None)
		member['country'] = member.get('country', {}).get('title', None)
	return members

def get_age_from_profile(df_profiles):
    if 'bdate' in df_profiles.columns:
        df_profiles['datenow'] = pd.to_datetime(time.strftime("%Y-%m-%d"))
        df_profiles['age'] = (df_profiles['datenow']-df_profiles['bdate']) / np.timedelta64(1, 'Y')
        del df_profiles['datenow']
        df_profiles['age'] = df_profiles['age'].apply(np.floor)
    return df_profiles

def add_edges_for_friends(G, friends):
    n = 1
    ego_friends = list(friends.id.values)
    for user in ego_friends:
        my_friends = get_friends_for_sure(user)
        if 'bdate' in my_friends.columns:
            my_friends['bdate'] = pd.to_datetime(my_friends['bdate'], errors='coerce')
            my_friends = get_age_from_profile(my_friends)
        if len(my_friends) > 0:
            add_info_from_friends(friends, user, my_friends)
            list_of_friends = my_friends.id.values
            for friend in list_of_friends:
                if friend in ego_friends:
                    G.add_edge(user, friend)
        print('Обработано %s из %s' % (n, len(ego_friends)))
        n+=1
        
def add_info_from_friends(df, user_id, user_friends):
    user_index = df[df.id==user_id].index[0]
    df.loc[user_index, 'number_of_friends'] = len(user_friends)
    if 'age' in user_friends.columns: 
        df.loc[user_index, 'age_by_friends'] = user_friends.age.median()
    if 'graduation' in user_friends.columns: 
        df.loc[user_index, 'graduation_by_friends'] = user_friends[user_friends.graduation>0].graduation.median()
    if 'university_name' in user_friends.columns: 
        if len(user_friends[user_friends.university>0].university_name.mode()) > 0:
            university = user_friends[user_friends.university>0].university_name.mode()[0]
            if len(user_friends[user_friends.university_name==university]) > 5:
                df.loc[user_index, 'university_by_friends'] = university
                
def add_nodes_with_labels(G, friends):
    ego_friends = list(friends.id.values)
    for user_id in ego_friends:
        city = friends[friends.id==user_id].city.fillna("").values[0]
        country = friends[friends.id==user_id].country.fillna("").values[0]
        graduation = friends[friends.id==user_id].graduation.fillna("").values[0]
        name = friends[friends.id==user_id].last_name.values[0] + " " + friends[friends.id==user_id].first_name.values[0]
        if friends[friends.id==user_id].sex.fillna("").values[0] == 1:
            sex = 'женский'
        if friends[friends.id==user_id].sex.fillna("").values[0] == 2:
            sex = 'мужской'
        university_name = friends[friends.id==user_id].university_name.fillna("").values[0]
        age = friends[friends.id==user_id].age.fillna("").values[0]
        faculty_name = friends[friends.id==user_id].faculty_name.fillna("").values[0]
        G.add_node(user_id, city=str(city), country=str(country), graduation=str(graduation),
                  name=name, sex=sex, university_name=university_name, age=str(age), faculty_name=str(faculty_name))
				  
user = -143617633
if user > 0: 
    friends = get_friends_for_sure(user)
if user < 0: friends = pd.DataFrame.from_dict(get_all_members(user*-1))
    
friends['bdate'] = pd.to_datetime(friends['bdate'], errors='coerce')
friends = get_age_from_profile(friends)
friends.to_excel("user"+str(user)+".xlsx")

user_G = nx.Graph()
add_nodes_with_labels(user_G, friends)
add_edges_for_friends(user_G, friends)
nx.write_graphml(user_G, "user"+str(user)+".graphml")