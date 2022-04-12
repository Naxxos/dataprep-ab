import copy
import backend.config
import xmltodict
import json

from pathlib import Path
from datetime import datetime

from .models import Annexe


def create_dict_from_xml(chemin_fichier: Path):
    start_time = datetime.now()
    with open(chemin_fichier, encoding='latin-1') as fd:
        doc = xmltodict.parse(fd.read(), dict_constructor=dict)
    end_time = datetime.now()
    print('Fichier {} ouvert en {}'.format(
        chemin_fichier, end_time - start_time))
    return doc


def parsing_infos_collectivite(dict_from_xml: dict):
    infos_dict = dict()
    dict_entete_doc = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]
    infos_dict["siret_coll"] = dict_entete_doc["IdColl"]["@V"]
    infos_dict["libelle_collectivite"] = dict_entete_doc["LibelleColl"]["@V"]
    infos_dict["nature_collectivite"] = dict_entete_doc["NatCEPL"]["@V"]
    infos_dict["departement"] = dict_entete_doc.get(
        "Departement", {}).get("@V", None)

    return infos_dict


def parsing_infos_etablissement(dict_from_xml: dict):
    infos_dict = dict()
    dict_entete_budget = dict_from_xml["DocumentBudgetaire"]["Budget"]["EnTeteBudget"]
    dict_bloc_budget = dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]

    infos_dict["siret_etablissement"] = dict_entete_budget["IdEtab"]["@V"]
    infos_dict["libelle"] = dict_entete_budget["LibelleEtab"]["@V"]
    infos_dict["code_insee"] = dict_entete_budget.get(
        "LibelleEtab", {}).get("@V", None)
    infos_dict["nomenclature"] = dict_entete_budget["Nomenclature"]["@V"]

    infos_dict["exercice"] = int(dict_bloc_budget["Exer"]["@V"])
    infos_dict["nature_dec"] = dict_bloc_budget["NatDec"]["@V"]
    infos_dict["NumDec"] = int(dict_bloc_budget.get(
        "NumDec", {}).get("@V", None) or 0)
    infos_dict["nature_vote"] = dict_bloc_budget["NatFonc"]["@V"]
    infos_dict["type_budget"] = dict_bloc_budget["CodTypBud"]["@V"]
    infos_dict["id_etabl_princ"] = dict_bloc_budget.get(
        "IdEtabPal", {}).get("@V", None)

    infos_dict["json_budget"] = generate_dict_budget(dict_from_xml)
    infos_dict["list_annexes"] = list(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"].keys())
    
    infos_dict["fk_siret_collectivite"] = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["IdColl"]["@V"]

    return infos_dict


def generate_dict_all_annexes(dict_from_xml: dict) -> dict:
    return dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]

def generate_dict_budget(dict_from_xml: dict) -> dict:
    budget_dict = copy.deepcopy(
        dict_from_xml["DocumentBudgetaire"]["Budget"]["LigneBudget"])

    for idx, row in enumerate(budget_dict):
        for field in backend.config.CHAMPS_LIGNE_BUDGET:
            if field in row:
                if "@V" in row[field]:
                    budget_dict[idx][field] = row[field]['@V']
    #erreur s'il y a qu'une seule ligne de budget
    return json.dumps(budget_dict)

def generate_dict_annexe(dict_from_xml: dict, nom_annexe: str, liste_champs_annexe: list) -> dict:
    annexe_dict = copy.deepcopy(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]
                                [nom_annexe][nom_annexe.split("_", 1)[1]])
    annexe_dict = [annexe_dict] if isinstance(
        annexe_dict, dict) else annexe_dict
    for idx, row in enumerate(annexe_dict):
        for field in liste_champs_annexe:
            if field in row:
                if "@V" in row[field]:
                    annexe_dict[idx][field] = row[field]['@V']
    return annexe_dict

def parsing_annexes(dict_from_xml: dict) -> dict:
    liste_annexe = dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"].keys()
    dict_annexes = dict()
    for annexe in liste_annexe:
        dict_annexes[annexe] = generate_dict_annexe(dict_from_xml, annexe, backend.config.CHAMPS_ANNEXES[annexe])

    return dict_annexes

def create_list_Annexe(dict_annexe: dict, id_doc: int):
    annexes = []
    infos_dict = dict()
    dict_temp = copy.deepcopy(dict_annexe)
    infos_dict["json_annexe"] = {}
    for annexe in  dict_annexe.keys():
        infos_dict["type_annexe"] = annexe
        infos_dict["json_annexe"] = json.dumps(dict_temp[annexe])
        infos_dict["fk_id_document_budgetaire"] = id_doc
        annexes.append(Annexe(**infos_dict))
    
    return annexes

