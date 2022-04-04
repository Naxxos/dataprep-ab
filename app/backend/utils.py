import copy


def generate_dict_annexe(doc_xml, nom_annexe: str, liste_champs_annexe: list):
    temp_doc = copy.deepcopy(doc_xml["DocumentBudgetaire"]["Budget"]["Annexes"]
                                    [nom_annexe][nom_annexe.split("_")[1]])
    
    temp_doc = [temp_doc] if isinstance(temp_doc, dict) else temp_doc
    for idx, row in enumerate(temp_doc):
        for field in liste_champs_annexe:
            if field in row:
                if "@V" in row[field]:
                    temp_doc[idx][field] = row[field]['@V']
        temp_doc[idx]["SIRET_etablissement"] = doc_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["IdColl"]["@V"]
    return temp_doc