import pandas as pd
from .config import get_param

from . import utils


########################################################################
# PARCELLES
########################################################################


def parcelles(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
    catpro3=None,
    ctpdl=None,
    dcntarti_min=None,
    dcntarti_max=None,
    dcntnaf_min=None,
    dcntnaf_max=None,
    dcntpa_min=None,
    dcntpa_max=None,
    idcomtxt=None,
    jannathmin_min=None,
    jannathmin_max=None,
    nlocal_min=None,
    nlocal_max=None,
    nlogh_min=None,
    nlogh_max=None,
    slocal_min=None,
    slocal_max=None,
    sprincp_min=None,
    sprincp_max=None,
    stoth_min=None,
    stoth_max=None,
):
    """Retourne les parcelles issues des Fichiers fonciers pour le périmètre demandé sous forme d'un dataframe

    Args:
        **code_insee (str or list, optional)**: Codes INSEE communaux ou des arrondissements municipaux. Defaults to None.

        **coddep (str or list, optional)**: Codes INSEE des départements. Defaults to None.

        **in_bbox (list, optional)**: Emprise rectangulaire sous la forme d'une liste [longitude_min, latitude_min, longitude_min, latitude_max]. Defaults to None.

        **lon_lat (list, optional)**: Coordonnée du point au sein de la ou des friches renvoyées [longitude, latitude]. Defaults to None.

        **fields (str, optional)**: Mettre à "all" pour obtenir tous les champs associés. Defaults to None.

        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.

        **catpro3 (str, optional)**: Chaîne(s) de caractères contenue dans le code de catégorie de
          propriétaire (il est possible de ne specifier que les premiers niveaux et
          de séparer par une virgule). Defaults to None.

        **ctpdl (str, optional)**: Type de pdl (type de copropriété). Defaults to None.

        **dcntarti_min (int, optional)**: Surface artificialisée minimale de la parcelle (m2). Defaults to None.

        **dcntarti_max (int, optional)**: Surface artificialisée maximale de la parcelle (m2). Defaults to None.

        **dcntnaf_min (int, optional)**: Surface NAF minimale de la parcelle (m2). Defaults to None.

        **dcntnaf_max (int, optional)**: Surface NAF maximale de la parcelle (m2). Defaults to None.

        **dcntpa_min (int, optional)**: Surface minimale de la parcelle (m2). Defaults to None.

        **dcntpa_max (int, optional)**: Surface maximale de la parcelle (m2). Defaults to None.

        **idcomtxt (str, optional)**: Chaine de caractères contenue dans le libellé de la commune. Defaults to None.

        **jannathmin_min (int, optional)**: Année minimale de construction du local le plus ancien. Defaults to None.

        **jannathmin_max (int, optional)**: Année maximale de construction du local le plus ancien. Defaults to None.

        **nlocal_min (int, optional)**: Nombre de locaux minimal sur la parcelle. Defaults to None.

        **nlocal_max (int, optional)**: Nombre de locaux maximal sur la parcelle. Defaults to None.

        **nlogh_min (int, optional)**: Nombre de logements minimal sur la parcelle. Defaults to None.

        **nlogh_max (int, optional)**:Nombre de logements maximal sur la parcelle. Defaults to None.

        **slocal_min (int, optional)**: Surface minimale des parties d'évaluation (m2). Defaults to None.

        **slocal_max (int, optional)**: Surface maximale des parties d'évaluation (m2). Defaults to None.

        **sprincp_min (int, optional)**:Surface minimale des pièces principales professionnelles (m2). Defaults to None.

        **sprincp_max (int, optional)**: Surface maximale des pièces principales professionnelles (m2). Defaults to None.

        **stoth_min (int, optional)**:Surface minimale des pièces d'habitation (m2). Defaults to None.

        **stoth_max (int, optional)**: Surface maximale des pièces d'habitation (m2). Defaults to None.

    Returns:
        dataframe: données sur les parcelles issues des Fichiers fonciers

    Examples:
        >>> import apifoncier.ff as ff
        >>> ff.parcelles(code_insee="59350", dcntpa_min=3000)
        >>> ff.parcelles(in_bbox=[3,50,3.01,50.01])
    """
    result = utils.Resultat("/ff/parcelles/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def geoparcelles(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
    catpro3=None,
    ctpdl=None,
    dcntarti_min=None,
    dcntarti_max=None,
    dcntnaf_min=None,
    dcntnaf_max=None,
    dcntpa_min=None,
    dcntpa_max=None,
    idcomtxt=None,
    jannathmin_min=None,
    jannathmin_max=None,
    nlocal_min=None,
    nlocal_max=None,
    nlogh_min=None,
    nlogh_max=None,
    slocal_min=None,
    slocal_max=None,
    sprincp_min=None,
    sprincp_max=None,
    stoth_min=None,
    stoth_max=None,
):
    """TEMP"""
    result = utils.Resultat("/ff/geoparcelles/", use_token=True, **locals())
    gdf = result.get_geodataframe()
    return gdf


def parcelle(idpar=None):
    """TEMP"""
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/ff/parcelles/{idpar}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict(response)


########################################################################
# TUPS
########################################################################


def tups(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """TEMP"""
    result = utils.Resultat("/ff/tups/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def geotups(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """TEMP"""
    result = utils.Resultat("/ff/geotups/", use_token=True, **locals())
    gdf = result.get_geodataframe()
    return gdf


def tup(idtup=None):
    """TEMP"""
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/ff/parcelles/{idtup}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict(response)


########################################################################
# LOCAUX
########################################################################


def locaux(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """TEMP"""
    result = utils.Resultat("/ff/locaux/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def local(idlocal=None):
    """TEMP"""
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/ff/locaux/{idlocal}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict(response)


########################################################################
# PROPRIOS
########################################################################


def proprios(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """TEMP"""
    result = utils.Resultat("/ff/proprios/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def proprio(idprodroit=None):
    """TEMP"""
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/ff/proprios/{idprodroit}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict(response)
