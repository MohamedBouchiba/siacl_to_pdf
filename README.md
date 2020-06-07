# Instalation

1. git clone https://gitlab.com/MohamedBouchiba/siacl_to_pdf

2. cd siacl_to_pdf

3. virtualenv venv

4. source venv/bin/activate 

5. pip install -r requirements.txt


# Configuration

Mettre le dossier contentant tous les documents du PIACL du projet à la racine


# Utilisation

```bash

python extraction_et_parsing.py ./chemin_relatif_des_docs .extentions nom_de_sauegarde_du_ficher

```

- - - -


Variables  | Descriptions
------------- | -------------
./chemin_relatif_des_docs  | le dossier où se trouvent les fichiers à extraire
.extentions  | privilégier les fichiers du type ".dot"
nom_de_sauegarde_du_ficher | le nom du fichier de sortie que l'on souhaite avoir