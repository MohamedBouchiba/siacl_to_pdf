# -*- coding: utf-8 -*-

##Parseur compliquer à expliquer veulleuz contacter Mohoamed Bouchiba au 0605803044


import json
import os
import sys

from odf import text, teletype
from odf.opendocument import load

BOOL = 0
PREFET = ""


def clean_phone_number(val):
    if 'Téléphone' in val[0]:
        splited = val[0].split("Téléphone")
        splited[1] = "Téléphone" + splited[1]
        val.pop(0)
        val = splited + val
    return val


def clean_all_space_start_and_end(val):
    for idx, value in enumerate(val):
        val[idx] = value.strip()
    return val


def split_number_and_mail(val):
    buffer = val[1].replace(" ", "")
    if "@" in val[1] and "Téléphone" in val[1]:
        index = buffer.index(":")
        mail = buffer[index + 11:]
        phone = buffer[:index + 11]
        val.pop(1)
        val.insert(1, phone)
        val.insert(2, mail)
    return val


def split_objet(val):
    if 'Objet' in val[-3] and 'l’attention d' in val[-3]:
        splited = val[-3].split("Objet")
        splited[1] = "Objet" + splited[1]
        val.pop(-3)
        val.insert(-4, splited[0])
        val.insert(-3, splited[1])
    return val


def extract(textdoc):
    global BOOL
    BOOL = 0
    allparas = textdoc.getElementsByType(text.P)
    list_entete = []
    for i in allparas:
        str_i = teletype.extractText(i)
        list_entete.append(str_i)
        if "Dossier suivi par" in str_i or "Affaire suivie par" in str_i:
            BOOL = 1
        if "PJ" in str_i or "P. J." in str_i:
            break

    buffer = ""
    list_entete2 = []
    if len(list_entete) < 5:
        return [None, None]
    for j in list_entete:
        buffer += (' ' + j)
        if j == "" or "Objet" in j or "Réf" in j or "PJ" in j or "P. J." in j:
            if buffer != " " and " DIRECTION GENERALE" not in buffer \
                    and "POLE INTERREGIONAL" not in buffer \
                    and "Le Directeur général des" not in buffer \
                    and " Le Responsable du Pôle" not in buffer \
                    and " Le responsable du Pôle Interrégional" not in buffer:
                list_entete2.append(buffer)
            buffer = ""
    if " à " in list_entete2:
        list_entete2.remove(" à ")

    for k in list_entete2:
        if k.strip() == "":
            list_entete2.remove(k)
    golabl_document = []
    for l in allparas:
        str_i = teletype.extractText(l)
        golabl_document.append(str_i)
    golabl_document = ' '.join(golabl_document)

    return list_entete2, golabl_document


def main(root_dir_files_extract, extention, nom_du_fichier_de_sauvegard):
    """
    root_dir_files_extract : (str) le dossier ou ce trouve les fichiers à extraire
    extention : (str) privilégier les fichiers du type "dot".
    nom_du_fichier_de_sauvegard : (str) le nom du fichier de sortie que l'on souhaite avoir
    -------------------------------------------------
    compteur : (int) est utile pour compter le nompbre totale de fichers total
    compteur2 : (int) est utile pour compter le nompbre totale de fichers un par un
    nom_fichier_sauvegard : util


    Cette fonction est la fonction central du scripte, elle fait appel à toute les autre fonction developer en amont.
    """
    compteur = 0
    compteur2 = 0
    nom_fichier_sauvegard = nom_du_fichier_de_sauvegard + ".json"
    data = []
    with open(nom_fichier_sauvegard, 'w') as outfile:
        json.dump(data, outfile)

    for path, subdirs, files in os.walk(root_dir_files_extract):
        if files:
            for f in files:
                if f.endswith(extention):
                    compteur = compteur + 1
    for path, subdirs, files in os.walk(root_dir_files_extract):
        if files:
            for f in files:
                if f.endswith(extention):
                    compteur2 = compteur2 + 1
                    PATH = os.path.join(path, f)
                    textdoc = load(os.path.join(path, f))
                    res, DOCUMENT = extract(textdoc)
                    if not BOOL:
                        continue

                    res = clean_all_space_start_and_end(res)
                    res = clean_phone_number(res)
                    res = split_number_and_mail(res)
                    res = split_objet(res)

                    # -----------------------OBJET---------------------------
                    try:
                        matchers = ["Objet\xa0", "Objet \xa0", " Objet:", "Objet:"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        OBJET = (value[0].split(":")[1]).strip()
                        res.remove(value[0])
                    except:
                        OBJET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # -----------------------NOM_REDACTEUR---------------------------
                    try:
                        matchers = ["Dossier suivi par", "Affaire suivie par"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        NOM_REDACTEUR = (value[0].split(":")[1]).strip()
                        res.remove(value[0])
                    except:
                        NOM_REDACTEUR = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # -------------------------TELEPHONE------------------------------

                    try:
                        matchers = ["Téléphone"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        TELEPHONE = (value[0].split(":")[1]).replace(" ", "")
                        res.remove(value[0])
                    except:
                        TELEPHONE = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # ---------------------------MAIL--------------------------------
                    try:
                        matchers = [".gouv.fr"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        if ":" in value[0]:
                            MAIL = (value[0].split(":")[1]).strip()
                            res.remove(value[0])
                        else:
                            MAIL = value[0]
                            res.remove(value[0])
                    except:
                        MAIL = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # ---------------------------REF_LY-------------------------------
                    try:
                        matchers = ["Réf.\xa0: LY"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        REF_LY = (value[0].split(":")[1]).strip()
                        res.remove(value[0])
                    except:
                        REF_LY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # ---------------------------DESTINATAIRE-------------------------------
                    try:
                        matchers = ["l’attention d"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        DESTINATAIRE = value[0]
                        res.remove(value[0])
                    except:
                        DESTINATAIRE = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # ---------------------------REF_DATE_TYPE-------------------------------
                    try:
                        matchers = ["Réf.\xa0:", "Réf\xa0:", " Réf.:", "Réf.:"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        REF_DATE_TYPE = (value[0].split(":")[1]).strip()
                        res.remove(value[0])
                    except:
                        REF_DATE_TYPE = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # --------------------------------PJ-------------------------------------
                    try:
                        matchers = ["PJ", "P.J", "P. J"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        PJ = (value[0].split(":")[1]).strip()
                        res.remove(value[0])
                    except:
                        PJ = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # --------------------------------DATE-------------------------------------
                    try:
                        matchers = ["Lyon, le"]
                        value = [s for s in res if any(xs in s for xs in matchers)]
                        DATE = (value[0].split("Lyon,")[1]).strip()
                        res.remove(value[0])
                    except:
                        DATE = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    # --------------------------------PREFET-------------------------------------
                    try:
                        matchers = ["madame la préfète", "monsieur le préfet", "monsieur le sous-préfet",
                                    "madame la sous-préfète", "monsieur le responsable du", "madame la responsable du"]
                        value = [s for s in res if any(xs in str(s).lower() for xs in matchers)]
                        PREFET = value[0]
                        res.remove(value[0])
                    except:
                        PREFET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

                    x = {
                        "nom_redacteur": NOM_REDACTEUR,
                        "telephone": TELEPHONE,
                        "mail": MAIL,
                        "referance_ly": REF_LY,
                        "referance_date_type": REF_DATE_TYPE,
                        "objet": OBJET,
                        "destinataire": DESTINATAIRE,
                        "pieces_joints": PJ,
                        "date_redaction": DATE,
                        "prefet": PREFET,
                        "doc": DOCUMENT,
                        "path": PATH
                    }

                    print( str(compteur2) + " / " + str(compteur))

                    ### Optimisation possible

                    with open(nom_fichier_sauvegard) as feedsjson:
                        feeds = json.load(feedsjson)

                    feeds.append(x)
                    with open(nom_fichier_sauvegard, mode='w') as f:
                        f.write(json.dumps(feeds, indent=2))


# ----------------------------------------------------------------------------------------------------------#



if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
