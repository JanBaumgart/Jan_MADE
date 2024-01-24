import zipfile
import os
import urllib.request
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Wichtige Variablen definieren
url = "https://gtfs.rhoenenergie-bus.de/GTFS.zip"
zip_file_path = "GTFS.zip"
file = 'stops.txt'

# Auf die URL zugreifen und nur die stops.txt datei laden.
urllib.request.urlretrieve(url, zip_file_path)
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract(file)
    

# Benötigten Spalten in einer Liste und ihre Datentypen in einem Dictionary speichern
columns = ["stop_id", "stop_name", "stop_lat", "stop_lon", "zone_id"]
data_types = {
    'stop_id': sqlalchemy.types.INTEGER,
    'stop_name': sqlalchemy.types.TEXT,
    'stop_lat': sqlalchemy.types.FLOAT,
    'stop_lon': sqlalchemy.types.FLOAT,
    'zone_id': sqlalchemy.types.INTEGER 
    }

# Nur die Spalten die von stops.txt gebraucht werden in einem Pandas-DataFrame speichern
# Nur die Stops von Zone 2001 behalten
df = pd.read_csv(file, usecols = columns)
df = df[df["zone_id"] == 2001]


# Nach Überprüfung: 'stop_name' behält bereits die deutschen Umlaute.
# Zur Sicherheit: Spalte "stop_name" auf jeden Fall als string lesen.
df["stop_name"] = df["stop_name"].astype(str)

# Die Spanne der validen Daten festlegen und auf die Spalten anwenden 
valid_coordinate_range = (-90, 90)
df = df[df['stop_lat'].between(*valid_coordinate_range) & df['stop_lon'].between(*valid_coordinate_range)]

# Die Datenbank am angegebenen Ort erstellen und verbinden.
db_path = 'gtfs.sqlite'
engine = create_engine('sqlite:///' + db_path)

# Den Dataframe in die Tabelle 'stops' in der Datenbank speichern
df.to_sql('stops', engine, index=False, if_exists='replace', dtype = data_types)

# Die Verbindung mit der Datenbank schliessen und nicht mehr benötigte Dateien löschen
engine.dispose()
os.remove(zip_file_path)
os.remove(file)