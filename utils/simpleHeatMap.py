# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sih.settings')
# import django
# django.setup()
import folium
from folium.plugins import HeatMap
# from models import UserProfile
# import mysql.connector as sql
import sqlite3
import pandas as pd



from time import time
start = time()

db_connection = sqlite3.connect(database='../db.sqlite3')
# db_connection = sql.connect(host='hostname', database='db_name', user='username', password='password')
df = pd.read_sql('SELECT lat, long FROM main_userprofile', con=db_connection)
# df = pd.DataFrame(list(UserProfile.objects.all().values('lat', 'lan')))
print(df)
main_map = folium.Map(prefer_canvas=True)
# Heatmap of current address data
df = df.dropna(axis=1, how='any').values
main_map.add_child(HeatMap(df, radius=10))

# Save Map
main_map.save('basicHeatmap.html')
print('Time Taken: {} secs'.format(time()-start))
