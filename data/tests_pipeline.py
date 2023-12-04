import os
import requests
import sqlite3
import pytest
from data_pipeline import run_data_pipeline, sources, table_names



# TEST1: ob die Verbindungen mit den 5 Datenquellen funktionieren
def test_datasources_connection():
    for index, source in enumerate(sources):
        response = requests.get(source)
        
        # Prüft, ob die HTTP-Anfrage erfolgreich war (Code 200), ansonsten gibt es einen Fehler mit dem jeweiligen Fehlercode aus.
        assert response.status_code == 200, f"Fehler beim Abrufen der Datenquelle {index + 1}: {table_names[index]}, Statuscode {response.status_code}"
        
        # Falls der Test der jeweiligen Quelle erfolgreich ist wird zudem eine Nachricht ausgegeben, um es dem Nutzer wiederzugeben.
        print(f'\n Datenquelle {index + 1}: {table_names[index]} ist erreichbar')



#------------
# TEST2 ob die sqllite Datenbank erstellt wurde / existiert.
# Dependency zum ersten Test, um das Pipeline-Skript nicht auszuführen, wenn etwas mit den Verbindungen zu den Datenquellen nicht funktioniert.
@pytest.mark.dependency(depends=["test_datasources_connection"])
def test_ensure_outputfile_exist():
    
    # Führt das Pipeline Skript einmal komplett aus.
    run_data_pipeline()

    # Überprüfen ob die Datenbank (data.sqlite) im Ordner 'data' existiert.
    output_file_path = 'data/data.sqlite'
    assert os.path.exists(output_file_path), f"Ausgabedatei {output_file_path} existiert nicht."
    
    print('\n Die Datenbank existiert')



#------------
# TEST3 ob die nötigen Tabellen in der Datenbank erstellt wurden.
# Dependency zum zweiten Test herstellen, weil es keinen Sinn macht die Tabellen in der Datenbank zu prüfen, wenn die Datenbank nicht existiert.
@pytest.mark.dependency(depends=["test_ensure_outputfile_exist"])
def test_data_in_database():
    
    conn = sqlite3.connect('data/data.sqlite')
    cursor = conn.cursor()
    
    expected_tables = ['Impfungen_SH', 'Impfungen_SH_LandKreise', 'Covid_Faelle_nach_Schultypen',
                       'Bewohneranzahl_SH_LandKreise', 'Schueleranzahl_SH_21_22']
    
    for table_name in expected_tables:
        cursor.execute(f'PRAGMA table_info({table_name})')
        table_info = cursor.fetchall()
        assert table_info, f'Tabelle {table_name} existiert nicht in der Datenbank.'
        print(f'\n Die Tabelle {table_name} existiert in den Datenbank')
    
    conn.close()  