import copy
import backend.config
import xmltodict

from pathlib import Path
from datetime import datetime


def create_dict_from_xml(chemin_fichier: Path):
    start_time = datetime.now()
    with open(chemin_fichier, encoding='latin-1') as fd:
        doc = xmltodict.parse(fd.read(), dict_constructor=dict)
    end_time = datetime.now()
    print('Fichier {} ouvert en {}'.format(chemin_fichier, end_time - start_time))
    return doc

def parsing_infos_collectivite(dict_from_xml: dict):
    infos_dict = dict()
    infos_dict["siret_coll"] = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["IdColl"]["@V"]
    infos_dict["libelle_collectivite"] = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["LibelleColl"]["@V"]
    infos_dict["nature_collectivite"] = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["NatCEPL"]["@V"]
    if "Departement" in dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]:
        infos_dict["departement"] = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["Departement"]["@V"]

    return infos_dict

def parsing_infos_etablissement(dict_from_xml: dict):
    infos_dict = dict()
    infos_dict["siret_etablissement"] = dict_from_xml["DocumentBudgetaire"]["Budget"]["EnTeteBudget"]["IdEtab"]["@V"]
    infos_dict["libelle"] = dict_from_xml["DocumentBudgetaire"]["Budget"]["EnTeteBudget"]["LibelleEtab"]["@V"]
    if "LibelleEtab" in dict_from_xml["DocumentBudgetaire"]["Budget"]["EnTeteBudget"]:
        infos_dict["code_insee"] = dict_from_xml["DocumentBudgetaire"]["Budget"]["EnTeteBudget"]["LibelleEtab"]["@V"]
    infos_dict["nomenclature"] = dict_from_xml["DocumentBudgetaire"]["Budget"]["EnTeteBudget"]["Nomenclature"]["@V"]
    infos_dict["exercice"] = int(dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]["Exer"]["@V"])
    infos_dict["nature_dec"] = dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]["NatDec"]["@V"]
    if "NumDec" in dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]:
        infos_dict["NumDec"] = int(dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]["NumDec"]["@V"])
    infos_dict["nature_vote"] = dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]["NatFonc"]["@V"]
    infos_dict["type_budget"] = dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]["CodTypBud"]["@V"]
    if "IdEtabPal" in dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]:
        infos_dict["id_etabl_princ"] = dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]["IdEtabPal"]["@V"]
    infos_dict["fk_id_collectivite"] = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["IdColl"]["@V"]
    
    return infos_dict

def generate_dict_all_annexes(dict_from_xml: dict):
    return copy.deepcopy(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"])


def generate_dict_annexe(dict_from_xml: dict, nom_annexe: str, liste_champs_annexe: list):
    annexe_dict = copy.deepcopy(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]
                                    [nom_annexe][nom_annexe.split("_")[1]])
    annexe_dict = [annexe_dict] if isinstance(annexe_dict, dict) else annexe_dict
    for idx, row in enumerate(annexe_dict):
        for field in liste_champs_annexe:
            if field in row:
                if "@V" in row[field]:
                    annexe_dict[idx][field] = row[field]['@V']
    return annexe_dict

def generate_dict_budget(dict_from_xml: dict):
    budget_dict = copy.deepcopy(dict_from_xml["DocumentBudgetaire"]["Budget"]["LigneBudget"])

    for idx, row in enumerate(budget_dict):
        for field in backend.config.CHAMPS_LIGNE_BUDGET:
            if field in row:
                if "@V" in row[field]:
                    budget_dict[idx][field] = row[field]['@V']

    return budget_dict
    
