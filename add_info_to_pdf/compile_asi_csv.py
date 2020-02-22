import pandas as pd

username_list = pd.read_csv('info.csv', dtype={'Numero civico': object, 'CAP': object})

columns = [
    "STAGIONE",
    "DISCIPLINA",
    "QUALIFICA",
    "TIPO TESSERA",
    "NOME",
    "COGNOME",
    "CODICE FISCALE",
    "COMUNE RESIDENZA",
    "INDIRIZZO RESIDENZA",
    "CAP",
    "EMAIL",
    "CODICE TESSERA",
    "CODICE AFFILIAZIONE"
]

global_df = pd.DataFrame(columns=columns)
for index, user in username_list.iterrows():
    box = ''.join(c.lower() for c in user["Box di provenienza"] if not c.isspace())

    if box != "crossfittorino":
        global_df = global_df.append({
            columns[0]: "2020",
            columns[1]: "FITNESS",
            columns[2]: "ATLETA",
            columns[3]: "B",
            columns[4]: user["Nome"].upper(),
            columns[5]: user["Cognome"].upper(),
            columns[6]: user["Codice Fiscale"].upper(),
            columns[7]: user["Residente a"].upper(),
            columns[8]: user["Indirizzo"].upper() + " " + user["Numero civico"],
            columns[9]: user["CAP"].upper(),
            columns[10]: user["Email"].upper(),
            columns[11]: None,
            columns[12]: "PIE-TO1076",
        }, ignore_index=True)
        # print(global_df)
    # break
global_df.to_csv("tessere.csv", index=False, sep=";")
