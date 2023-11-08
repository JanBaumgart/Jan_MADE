import pandas as pd
from sqlalchemy import create_engine

# URL in Variable speichern
url = 'https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv'

# Den lokalen Dateipfad und Name für die Datenbank definieren (hier im selben Verzeichnis)
db_path = 'airports.sqlite'

# Die Daten von der URL abrufen und mit Pandas Funktion lesen. WICHTIG: Anmerken dass es mit Semikolon getrent wird! (https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas-read-csv)
data = pd.read_csv(url, sep=';')

# Eine Verbindung mit einer lokalen SQLite-Datenbank herstellen. (https://docs.sqlalchemy.org/en/20/core/engines.html)
engine = create_engine('sqlite:///' + db_path)

# Die Daten in die Datenbank einfügen (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html)
data.to_sql('airports', engine, if_exists='replace', index=False)

# Datenbankverbindung beenden
engine.dispose()