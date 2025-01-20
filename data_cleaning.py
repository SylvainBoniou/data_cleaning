# Importer les bibliothèques
import pandas as pd
from tkinter import filedialog
import re

seuil_null = 20
seuil_boolean = 50

#Selection du fichier source
file_path = filedialog.askopenfilename(title="Sélectionner un fichier CSV",filetypes=(("csv","*.csv"),("all files","*.*")))

if  not file_path:
    print("Sélectionner un fichier")
    exit()

# Lire le fichier csv dans un dataframe pandas
df = pd.read_csv(file_path)

print("")
print("######################### Synthèse #########################")
print("Nom du fichier csv = " + file_path)
print("Nombre de lignes = " + str(len(df)))
print("Nombre de colonnes = " + str(len(df.columns)))
print("Listes des colonnes : "+str(df.columns.tolist()))
print("Nombre de lignes en doublons : "+str(len(df)-len(df.drop_duplicates())))

print("")
print("######################### Echantillon du fichier #########################")
print(df.head(5))

print("")
print("######################### Analyse des colonnes #########################")
column_types = {}

#boucle sur chaque colonne
for column_name in df.columns:
    print("----- Colonne : "+column_name+" -----")

    nb_lignes = df[column_name].isnull().sum()
    pourcentage_null = nb_lignes/len(df)*100

    if pourcentage_null>seuil_null:
        print("Nombre de valeurs NULL = " + str(nb_lignes) + " ("+str(round(pourcentage_null))+"% de valeurs NULL)" )
    else:
        print("Nombre de valeurs NULL = "+  str(nb_lignes))

    #si colonne est de type numérique alors afficher les valeurs min/max
    if ((df[column_name].dtype=="float64" or df[column_name].dtype=="int64") and pourcentage_null<100):
        print("Valeur MIN = " + str(int(df[column_name].min())))
        print("Valeur MAX = " + str(int(df[column_name].max())))

    #vérification si la colonne est au format datetime
    is_datetime = all(re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', str(value)) for value in df[column_name])

    #vérification si la colonne est au format date
    is_date = all(re.match(r'\d{4}-\d{2}-\d{2}', str(value)) for value in df[column_name])

    #si colonne est de type date alors afficher les valeurs min/max
    if is_datetime or is_date:
        print(df[column_name].agg(['min', 'max']))

    #si colonne est un booleen (le nombre de valeurs doit être supérieur au seuil) alors afficher valeurs min/max
    df_boolean = df[df[column_name].isin(['Oui', 'Non','UNK'])]
    pourcentage_boolean = round(len(df_boolean)/len(df)*100)
    if  pourcentage_boolean>seuil_boolean:
        print("Distribution des valeurs :")
        value = df_boolean.value_counts(subset=column_name)
        print(value)

    print("")





