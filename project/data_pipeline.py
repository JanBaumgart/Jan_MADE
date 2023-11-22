import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Liste der URLs in der 'sources' Liste speichern um sie später nacheinander abzurufen.
sources = [
    # Impfungen nach Bundesländern:
    'https://github.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/raw/main/Deutschland_Bundeslaender_COVID-19-Impfungen.csv',
    
    # Impfungen nach Landkreisen:
    'https://github.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/raw/main/Deutschland_Landkreise_COVID-19-Impfungen.csv', 
    
    # Covid Fälle nach Schultypen:
    'https://opendata.schleswig-holstein.de/dataset/08263e93-6e2c-4034-888a-31ac33c91bfe/resource/eddd721d-1789-4d89-85a1-a43ac6e1fd7f/download/data.csv', 
    
    # Kreisfreie Städte und Landkreise nach Fläche, Bevölkerung und Bevölkerungsdichte
    'https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.xlsx?__blob=publicationFile', 
    
    # Schüleranzahl in SH nach Schularten.
    'data/pupil_count.csv'
]

# Namen für die Tabellen deklarieren um sie später in der SQL Tabelle mit diesem Namen zu speichern.
table_names = [
    'Impfungen_Bundeslaender',
    'Impfungen_Landkreise',
    'Covid_Faelle_Schultypen',
    'Kreisfreie_Staedte_Landkreise',
    'Schueleranzahl_SH'
]

# Deklaration der Datentypen der Spalten für jede Datenquelle.
data_types = [
    {'Impfdatum': sqlalchemy.types.Date,'Impfstoff': sqlalchemy.types.TEXT, 'Impfserie': sqlalchemy.types.INTEGER, 'Anzahl': sqlalchemy.types.BIGINT},
    
    {'Impfdatum': sqlalchemy.types.Date, 'Altersgruppe': sqlalchemy.types.TEXT, 'Impfschutz': sqlalchemy.types.INTEGER, 'Anzahl': sqlalchemy.types.BIGINT},
    
    {'Datum': sqlalchemy.types.Date, 'Schulart': sqlalchemy.types.TEXT, 'Gruppe': sqlalchemy.types.TEXT, 'Anzahl': sqlalchemy.types.BIGINT},
    
    {'Schlüssel-nummer': sqlalchemy.types.INTEGER, 'Regionale Bezeichnung': sqlalchemy.types.TEXT, 'Kreis / Landkreis': sqlalchemy.types.TEXT, 
     'NUTS3': sqlalchemy.types.TEXT, 'Fläche in km2': sqlalchemy.types.FLOAT, 'insgesamt': sqlalchemy.types.BIGINT,
     'männlich': sqlalchemy.types.BIGINT,'weiblich': sqlalchemy.types.BIGINT,'je km2': sqlalchemy.types.INTEGER},
    
    {'Bundeslaender': sqlalchemy.types.TEXT, 'Schulart': sqlalchemy.types.TEXT, 'Klassenstufe': sqlalchemy.types.TEXT,  
     'maennlich19/20': sqlalchemy.types.BIGINT, 'weiblich19/20': sqlalchemy.types.BIGINT, 'insgesamt19/20': sqlalchemy.types.BIGINT, 
     'maennlich20/21': sqlalchemy.types.BIGINT, 'weiblich20/21': sqlalchemy.types.BIGINT, 'insgesamt20/21': sqlalchemy.types.BIGINT, 
     'maennlich21/22': sqlalchemy.types.BIGINT, 'weiblich21/22': sqlalchemy.types.BIGINT, 'insgesamt21/22': sqlalchemy.types.BIGINT, 
     'maennlich22/23': sqlalchemy.types.BIGINT, 'weiblich22/23': sqlalchemy.types.BIGINT, 'insgesamt22/23': sqlalchemy.types.BIGINT}
]


# Das Verzeichnis für die SQLLite Datenbank festlegen, hier also unter dem Ordner 'data'.
db_path = 'data/data.sqlite'


# Mithilfe von SQLalchemy eine Verbindung zu der Datenbank aufbauen.
engine = create_engine('sqlite:///' + db_path)


# HAUPTBEREICH: Eine Schleife, die durch die Datenquellen geht und die Daten in den Tabellen in der bereitgestellten Datenbank speichert.
for index, source in enumerate(sources): 

    # Überprüfen, ob die Quelle eine URL ist (ausschliesen der lokalen Quelle)  
    if source.startswith('http'):  
    
        
        # Excel-Quelle (destatis)
        if '.xlsx' in source: 
            
            # Die Daten von der URL als Excel-Datei abrufen und lesen
            data = pd.read_excel(source, sheet_name='Kreisfreie Städte u. Landkreise', skiprows=7, na_filter=False)
            
            # Header werden selbst definiert, weil der richtige Header nicht festgelegt werden kann, weil er über zwei Zeilen verteilt ist.
            data.columns = ['Schlüssel-nummer', 'Regionale Bezeichnung', 'Kreis / Landkreis', 'NUTS3', 'Fläche in km2',
                               'insgesamt', 'männlich', 'weiblich', 'je km2']
            
            # Filtert die Daten nach SH, weil nur diese gebraucht werden.
            # WICHTIG: '.astype' wird genutzt damit Nullwerte auch als Leere Strings eingelesen und übersprungen werden können (sonst Type Error).
            data = data[data['Schlüssel-nummer'].astype(str).str.startswith('01')] 
            
        # 'Impfungen_Bundeslaender' Quelle abrufen und nach SH filtern.
        elif source.endswith('Bundeslaender_COVID-19-Impfungen.csv'):
            data = pd.read_csv(source, sep=',', on_bad_lines='skip', skip_blank_lines=True, dtype={'BundeslandId_Impfort': str})
            data = data[data['BundeslandId_Impfort'] == '01']            
            
        # 'Impfungen_Landkreise' Quelle abrufen und nach SH filtern.
        elif source.endswith('Landkreise_COVID-19-Impfungen.csv'):
            data = pd.read_csv(source, sep=',', on_bad_lines='skip', skip_blank_lines=True, dtype={'LandkreisId_Impfort': str})
            data = data[data['LandkreisId_Impfort'].str[:2] == '01']    
            
        # 'Covid_Faelle_Schultypen' einlesen (besteht nur aus SH Daten, deshalb keine Filterung).
        else:
            data = pd.read_csv(source, sep=',', on_bad_lines='skip', skip_blank_lines=True)
       
            
    # lokale Quelle, mit den Schülerzahlen in SH, einlesen.
    else:
        data = pd.read_csv(source, sep=';', on_bad_lines='skip', skip_blank_lines=True)


    # die Tabelle des aktuellen Index korrekt benennen (wie zurvor definiert).
    table_name = table_names[index]
    
    
    # Konvertierung der Datums-Spalten, weil sie sonst nicht von der 'to_sql' funktion als DATETIME type gespeichert werden können ( -> type error).
    if 'Impfdatum' in data.columns:
        data['Impfdatum'] = pd.to_datetime(data['Impfdatum'], errors='coerce')

    if 'Datum' in data.columns:
        data['Datum'] = pd.to_datetime(data['Datum'], errors='coerce')


    # Die Daten in die Datenbank einfügen, bzw. erweitern. Zudem wird eine Nachricht ausgegeben die bestätigt dass eine Quelle erfolgreich in SQL eingelesen wurde.
    data.to_sql(table_name, engine, if_exists='append', index=False, dtype=data_types[index])
    print(f'Datenquelle: {index}: {table_name} erfolgreich eingelesen')

# Datenbankverbindung beenden
engine.dispose()
