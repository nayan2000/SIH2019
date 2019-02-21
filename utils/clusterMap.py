import folium
from folium.plugins import FastMarkerCluster
import pandas as pd
import sqlite3
from time import time
start = time()


"""
Takes map, filename (cleans ext automatically and puts the name as overlay
name) and the color of the points. Also, (latitude, longitude) rows
"""
def mupLoader(mapElement, data, color):
    # query latitude and longitude
    initLen = len(data)
    print(data)
    # Cleaned Name
    cname = 'UserList'
    # Change Colors here (js callback string)
    callback = ('function (row) {'
                'var circle = L.circle(new L.LatLng(row[0], row[1]), {color: "' + color + '",  radius: 100});'
                'return circle};')
    # Add Clusters
    Fm = FastMarkerCluster(
        data.values,
        callback=callback,
        name=cname,
        overlay=True)
    mapElement.add_child(Fm)


# for i in range
# plotDot(getLoc('', 'CHENNAI', 'TAMIL NADU', '600029'))

#create a map
main_map = folium.Map(prefer_canvas=True)

#Connect with database
db_connection = sqlite3.connect(database='../db.sqlite3')
# db_connection = sql.connect(host='hostname', database='db_name', user='username', password='password')
df = pd.read_sql('SELECT lat, long FROM main_userprofile', con=db_connection)

#Load dataframe and cluster
mupLoader(main_map, df, 'blue')

#Add LayerControl
folium.LayerControl().add_to(main_map)

#Set the zoom to the maximum possible
main_map.fit_bounds(main_map.get_bounds())

#Save the map to an HTML file
main_map.save('CustomerMap.html')

print('Time Taken: {} secs'.format(time()-start))
