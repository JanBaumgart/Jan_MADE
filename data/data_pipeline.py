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
    
    # Schüleranzahl in SH nach Schularten 2022/23.
    'https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bildung-Forschung-Kultur/Schulen/Publikationen/Downloads-Schulen/statistischer-bericht-allgemeinbildende-schulen-2110100227005.xlsx?__blob=publicationFile',
    
    # Covid Fälle an Schulen nach Landkreisen
    'https://opendata.schleswig-holstein.de/dataset/acd37a65-b4ad-4abd-b318-a39fc37838f7/resource/5c7d0685-5ec2-441c-ab9e-dc5a691bef29/download/data.csv'
]


# Namen für die Tabellen deklarieren um sie später in der SQL Tabelle mit diesem Namen zu speichern.
table_names = [
    'Impfungen_SH',
    'Impfungen_SH_LandKreise',
    'Covid_Faelle_nach_Schultypen',
    'Bewohneranzahl_SH_LandKreise',
    'Schueleranzahl_SH_21_22',
    'Covid_Faelle_an_Schulen_nach_Landkreisen'
]


# Deklaration der Datentypen der Spalten für jede Datenquelle.
data_types = [
    {'Impfdatum': sqlalchemy.types.Date,'Impfstoff': sqlalchemy.types.TEXT, 'Impfserie': sqlalchemy.types.INTEGER, 'Anzahl': sqlalchemy.types.BIGINT},
    
    {'Impfdatum': sqlalchemy.types.Date, 'Altersgruppe': sqlalchemy.types.TEXT, 'Impfschutz': sqlalchemy.types.INTEGER, 'Anzahl': sqlalchemy.types.BIGINT},
    
    {'Datum': sqlalchemy.types.Date, 'Schulart': sqlalchemy.types.TEXT, 'Gruppe': sqlalchemy.types.TEXT, 'Anzahl': sqlalchemy.types.BIGINT},
    
    {'Schlüssel-nummer': sqlalchemy.types.INTEGER, 'Regionale Bezeichnung': sqlalchemy.types.TEXT, 'Kreis / Landkreis': sqlalchemy.types.TEXT, 
     'NUTS3': sqlalchemy.types.TEXT, 'Fläche in km2': sqlalchemy.types.FLOAT, 'insgesamt': sqlalchemy.types.BIGINT,
     'männlich': sqlalchemy.types.BIGINT,'weiblich': sqlalchemy.types.BIGINT,'je km2': sqlalchemy.types.INTEGER},
    
    {'Statistik_Code': sqlalchemy.types.INTEGER, 'Statistik_Label': sqlalchemy.types.TEXT, 'Schuljahr': sqlalchemy.types.TEXT, 'Bundesland': sqlalchemy.types.TEXT, 
     'Schulbereich': sqlalchemy.types.TEXT, 'Schulart': sqlalchemy.types.TEXT, 'Bildungsbereich': sqlalchemy.types.TEXT, 'Geschlecht': sqlalchemy.types.TEXT,
     'Schueler_innen_Anzahl': sqlalchemy.types.BIGINT, 'Geschlechtsverteilung_Prozent': sqlalchemy.types.FLOAT, 'Verteilung_Schulart_Prozent': sqlalchemy.types.FLOAT, 
     'Verteilung_Schulbereich_Prozent': sqlalchemy.types.FLOAT},
    
    {'Datum': sqlalchemy.types.Date, 'Kreis': sqlalchemy.types.TEXT, 'Gruppe': sqlalchemy.types.TEXT, 'Anzahl': sqlalchemy.types.INTEGER}
]


# Das Verzeichnis für die SQLLite Datenbank festlegen, hier also unter dem Ordner 'data'.
db_path = 'data/data.sqlite'

# Mithilfe von SQLalchemy eine Verbindung zu der Datenbank aufbauen.
engine = create_engine('sqlite:///' + db_path)



# HAUPTBEREICH:
# Infonachricht an den Nutzer Senden dass der Datenabruf aus den Quellen startet.
print('Der Datenabruf wird gestartet...')

# Ausführung des Hauptteil des Skripts in einer Funktion, um es auch anderswo wieder aufzurufen (z.B. im Test-Skript)
def run_data_pipeline():
    
    # Es wird zum start die Info an den Nutzer ausgegeben, dass der Datenabruf aus den Quellen erfolgreich gestartet hat.
    # Eine Schleife, die durch die Datenquellen geht und die Daten in den passenden Tabellen in der bereitgestellten Datenbank speichert.
    for index, source in enumerate(sources): 


        #---------------------------------------
        # Excel 'Bewohneranzahl_SH_LandKreise' einlesen  
        if '04-kreise.xlsx' in source: 
                
            # Die Daten von der URL als Excel-Datei abrufen und lesen
            data = pd.read_excel(source, sheet_name='Kreisfreie Städte u. Landkreise', skiprows=7, na_filter=False)
                
            # Header werden selbst definiert, weil der richtige Header nicht festgelegt werden kann, weil er über zwei Zeilen verteilt ist.
            data.columns = ['Schlüssel-nummer', 'Regionale Bezeichnung', 'Kreis / Landkreis', 'NUTS3', 'Fläche in km2',
                            'insgesamt', 'männlich', 'weiblich', 'je km2']
            
            # Filtert die Daten nach SH, weil nur diese gebraucht werden.
            # WICHTIG: '.astype' wird genutzt damit Nullwerte auch als Leere Strings eingelesen und übersprungen werden können (sonst Type Error).
            data = data[data['Schlüssel-nummer'].astype(str).str.startswith('01')]
            data = data.drop(columns=['Regionale Bezeichnung', 'NUTS3', 'Fläche in km2'])
            
            
        #---------------------------------------
        # Excel 'Schueleranzahl_SH_21/22'einlesen.
        elif '2110100227005.xlsx' in source: 
                
            # Die Daten von der URL als Excel-Datei abrufen und lesen
            data = pd.read_excel(source, sheet_name='csv-21111-03', na_filter=False)
            
            # Nur nach den Daten aus SH filtern
            data = data.loc[data['Bundesland'] == 'Schleswig-Holstein']
            
            # Zeilen löschen die nach Schulart differenzieren und nur die gesamten Zahlen behalten, die hier für uns wichtig sind.
            data = data.loc[data['Status'] == 'Insgesamt']
            
            # Ebenso Zeilen die nach Geschlecht differenzieren entfernen.
            data = data.loc[data['Geschlecht'] == 'Insgesamt']
            
            # Und auch nur die Daten die sich auf alle Bildungsbereicht innerhalb der Schule beziehen behalten.
            data = data.loc[data['Bildungsbereich'] == 'Alle Bildungsbereiche']
            
            # Zuletzt alle für uns unbrauchbare Spalten löschen, da nur Schule und Anzahl gebraucht wird. 
            data = data.drop(columns=['Statistik_Code', 'Statistik_Label','Bundesland', 'Bildungsbereich', 'Schuljahr', 'Status', 'Geschlecht', 'Staatsangehoerigkeit' ])



        #---------------------------------------        
        # CSV 'Impfungen_Bundeslaender' Quelle abrufen und nach SH filtern (unwichtige Spalten dropen).
        elif source.endswith('Bundeslaender_COVID-19-Impfungen.csv'):
            data = pd.read_csv(source, sep=',', on_bad_lines='skip', skip_blank_lines=True, dtype={'BundeslandId_Impfort': str})
            data = data[data['BundeslandId_Impfort'] == '01']  
            data = data.drop(columns=['BundeslandId_Impfort', 'Impfstoff', 'Impfserie'])
                
                
                
        #---------------------------------------        
        # CSV 'Impfungen_Landkreise' Quelle abrufen und nach SH filtern (unwichtige Spalten dropen).
        elif source.endswith('Landkreise_COVID-19-Impfungen.csv'):
            data = pd.read_csv(source, sep=',', on_bad_lines='skip', skip_blank_lines=True, dtype={'LandkreisId_Impfort': str})
            data = data[data['LandkreisId_Impfort'].str.startswith('01')]  
            data = data.loc[data['Altersgruppe'].isin(['05-11', '12-17'])]
            data = data.drop(columns=['Impfschutz'])    
        
                
        
        #---------------------------------------        
        # CSV 'Covid_Faelle_Schultypen' und 'Covid_Faelle_an_Schulen_nach_Landkreisen' einlesen (besteht nur aus SH Daten und haben gleiche Strucktur).
        else:
            data = pd.read_csv(source, sep=',', on_bad_lines='skip', skip_blank_lines=True)
            
            # Nur Schüler und Schülerinnen beachten und Lehrkräfte rausrechnen.
            data = data[data['Gruppe'] == 'Schülerinnen / Schüler']
            
            # Gruppen Spalten entfernen, weil sie nicht mehr gebraucht wird, weil nur noch Schüler darin sind
            data = data.drop(columns=['Gruppe'])

        #---------------------------------------
        # die Tabelle des aktuellen Index korrekt benennen (wie zurvor definiert).
        table_name = table_names[index]
        
        
        #--------------------------------------- 
        # Konvertierung der Datums-Spalten (falls vorhanden),
        # weil sie sonst nicht von der 'to_sql' funktion als DATETIME type gespeichert werden können ( -> type error).
        if 'Impfdatum' in data.columns:
            data['Impfdatum'] = pd.to_datetime(data['Impfdatum'], errors='coerce')

        if 'Datum' in data.columns:
            data['Datum'] = pd.to_datetime(data['Datum'], errors='coerce')



        #--------------------------------------- 
        # Die Daten in die Datenbank einfügen, bzw. falls möglich ersetzen mit neuen Daten. 
        data.to_sql(table_name, engine, if_exists='replace', index=False, dtype=data_types[index])
        
        #--------------------------------------- 
        # Zudem wird eine Nachricht ausgegeben die bestätigt dass eine Quelle erfolgreich in die Datenbank eingelesen wurde.
        print(f'\n Datenquelle {index + 1}: {table_name} erfolgreich eingelesen')



        # Datenbankverbindung beenden
        engine.dispose()


if __name__ == "__main__":
    run_data_pipeline()