from folium import Map, LayerControl, Marker
from folium.plugins import MarkerCluster
import pandas as pd
import sqlite3
from time import time
start = time()


"""
Takes map, filename (cleans ext automatically and puts the name as overlay
name) and the color of the points. Also, (latitude, longitude) rows
"""
def mupLoader(mapElement, fname, color):
    # open csv file and read coln
    initLen = len(data)
    print(initLen, len(data))
    markuster = MarkerCluster()
    for row in data.itertuples():
        markuster.add_child(Marker(
            location=[row[5], row[6]],
            popup=row[1]
        ))
    mapElement.add_child(markuster)


# for i in range
# plotDot(getLoc('', 'CHENNAI', 'TAMIL NADU', '600029'))

#create a map
main_map = Map(prefer_canvas=True)

#Connect with database
db_connection = sqlite3.connect(database='../db.sqlite3')
# db_connection = sql.connect(host='hostname', database='db_name', user='username', password='password')
df = pd.read_sql('SELECT lat, long FROM main_userprofile', con=db_connection)

#Load dataframe and cluster
mupLoader(main_map, df)

#Add LayerControl
LayerControl().add_to(main_map)

#Set the zoom to the maximum possible
main_map.fit_bounds(main_map.get_bounds())

#Save the map to an HTML file
main_map.save('MarkerMap.html')

print('Time Taken: {} secs'.format(time()-start))
