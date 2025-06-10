from flask import Flask, send_file, jsonify
import pyodbc
import os

app = Flask(__name__)

server=os.getenv('nazwaserwera')
database=os.getenv('nazwabazy')
username=os.getenv('nazwauzytkownika')
password=os.getenv('danehasla')

driver = '{ODBC Driver 18 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
conn = pyodbc.connect(conn_str)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/ile-niemiecki")
def ile_niemiecki():
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(CAST(REPLACE(liczbaUczniow, ' ', '') AS INT)) FROM [dbo].[tabelaJezyki] WHERE jezykObcy = 'niemiecki'")
    result = cursor.fetchone()
    return jsonify({"count": result[0] if result and result[0] is not None else 0})

@app.route("/ile-hiszpanski-dolnoslaskie-licea")
def ile_hiszpanski_dolnoslaskie_licea():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(CAST(REPLACE(liczbaUczniow, ' ', '') AS INT)) FROM [dbo].[tabelaJezyki] WHERE jezykObcy = 'hiszpanski' AND Wojewodztwo = 'DOLNOSLASKIE' AND typpODMIOTU = 'Liceum ogólnoksztalcace'
    """)
    result = cursor.fetchone()
    return jsonify({"count": result[0] if result else 0})

if __name__ == "__main__":
    app.run(debug=True)
