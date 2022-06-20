import copy
import backend.config
import xmltodict
import json

from pathlib import Path
from datetime import datetime

from .models import Annexe

from .timer import timed, logger

class Parsing():
    @timed
    def create_dict_from_xml(self, chemin_fichier: Path):
        with open(chemin_fichier, encoding='latin-1') as fd:
            doc = xmltodict.parse(fd.read(), dict_constructor=dict)
            logger.debug(chemin_fichier)
        return doc


    def parsing_infos_collectivite(self, dict_from_xml: dict):
        infos_dict = dict()
        dict_entete_doc = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]
        infos_dict["siret_coll"] = dict_entete_doc["IdColl"]["@V"]
        infos_dict["libelle_collectivite"] = dict_entete_doc["LibelleColl"]["@V"]
        infos_dict["nature_collectivite"] = dict_entete_doc["NatCEPL"]["@V"]
        infos_dict["departement"] = dict_entete_doc.get(
            "Departement", {}).get("@V", None)

        return infos_dict


    def parsing_infos_etablissement(self, dict_from_xml: dict):
        infos_dict = dict()
        dict_entete_budget = dict_from_xml["DocumentBudgetaire"]["Budget"]["EnTeteBudget"]
        dict_bloc_budget = dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]

        infos_dict["siret_etablissement"] = dict_entete_budget["IdEtab"]["@V"]
        infos_dict["libelle"] = dict_entete_budget["LibelleEtab"]["@V"]
        infos_dict["code_insee"] = dict_entete_budget.get(
            "CodInseeColl", {}).get("@V", None)
        infos_dict["nomenclature"] = dict_entete_budget["Nomenclature"]["@V"]

        infos_dict["exercice"] = int(dict_bloc_budget["Exer"]["@V"])
        infos_dict["nature_dec"] = dict_bloc_budget["NatDec"]["@V"]
        infos_dict["NumDec"] = int(dict_bloc_budget.get(
            "NumDec", {}).get("@V", None) or 0)
        infos_dict["nature_vote"] = dict_bloc_budget["NatFonc"]["@V"]
        infos_dict["type_budget"] = dict_bloc_budget["CodTypBud"]["@V"]
        infos_dict["id_etabl_princ"] = dict_bloc_budget.get(
            "IdEtabPal", {}).get("@V", None)

        infos_dict["json_budget"] = self.generate_dict_budget(dict_from_xml)
        if isinstance(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"], dict):
            infos_dict["list_annexes"] = list(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"].keys())
        
        infos_dict["fk_siret_collectivite"] = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["IdColl"]["@V"]

        return infos_dict


    def generate_dict_all_annexes(self, dict_from_xml: dict) -> dict:
        return dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]

    def generate_dict_budget(self, dict_from_xml: dict) -> dict:
        budget_dict = copy.deepcopy(
            dict_from_xml["DocumentBudgetaire"]["Budget"]["LigneBudget"])
        
        if isinstance(budget_dict, dict):
            for field in backend.config.CHAMPS_LIGNE_BUDGET:
                if field in budget_dict:
                    if "@V" in budget_dict[field]:
                        budget_dict[field] = budget_dict[field]['@V']
            return json.dumps([budget_dict])
        for idx, row in enumerate(budget_dict):
            for field in backend.config.CHAMPS_LIGNE_BUDGET:
                if field in row:
                    if "@V" in row[field]:
                        budget_dict[idx][field] = row[field]['@V']
        #erreur s'il y a qu'une seule ligne de budget
        return json.dumps(budget_dict)



    def generate_dict_annexe(self, dict_from_xml: dict, nom_annexe: str, liste_champs_annexe: list) -> dict:
        annexe_dict = copy.deepcopy(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]
                                    [nom_annexe][nom_annexe.split("_", 1)[1]])
        if annexe_dict == None:
            return {}
        annexe_dict = [annexe_dict] if isinstance(
            annexe_dict, dict) else annexe_dict
        # Cette étape précédente peut être évité en ajoutant force_list=('Annexes',) lors de l'utilis 
        for idx, row in enumerate(annexe_dict):
            for field in liste_champs_annexe:
                if row:
                    if field in row:
                        if "@V" in row[field]:
                            annexe_dict[idx][field] = row[field]['@V']
        return annexe_dict

    def parsing_annexes(self, dict_from_xml: dict) -> dict:
        dict_annexes = dict()
        if isinstance(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"], dict):
            liste_annexe = list(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"].keys())
            if "FLUX_CROISES" in liste_annexe: 
                liste_annexe.remove("FLUX_CROISES")
                keys = dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"].keys()
                logger.warning(f"\"{keys}\" ")
                
            if "DATA_MEMBRESASA" in liste_annexe: 
                liste_annexe.remove("DATA_MEMBRESASA")
                logger.warning(f"\"DATA_MEMBRESASA\" in annexe ")
        
            if liste_annexe:
                for annexe in liste_annexe:
                    dict_annexes[annexe] = self.generate_dict_annexe(dict_from_xml, annexe, backend.config.CHAMPS_ANNEXES[annexe])

        return dict_annexes

    def create_list_Annexe(self, dict_annexe: dict, id_doc: int):
        annexes = []
        infos_dict = dict()
        dict_temp = copy.deepcopy(dict_annexe)
        infos_dict["json_annexe"] = {}
        for annexe in  dict_annexe.keys():
            infos_dict["type_annexe"] = annexe
            infos_dict["json_annexe"] = json.dumps(dict_temp[annexe], ensure_ascii=False).encode('utf8')
            infos_dict["fk_id_document_budgetaire"] = id_doc
            annexes.append(Annexe(**infos_dict))
        
        return annexes

