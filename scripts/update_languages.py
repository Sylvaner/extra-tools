#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Met à jour les fichiers de traduction d'un plugin
"""

import json
import os
import sys

from libs.File import File  # pylint: disable= import-error
from libs.IO import IO  # pylint: disable= import-error
from libs.Jeedom import Jeedom  # pylint: disable= import-error

# Gestion des accents pour python 2
if sys.version_info[0] < 3:
    reload(sys)  # pylint: disable=undefined-variable
    sys.setdefaultencoding('utf8')  # pylint: disable=no-member


def update_languages(plugin_path):
    """
    Ajoute la classe pour traiter les requêtes AJAX
    :param plugin_path: Chemin du plugin
    :param plugin_name: Nom du plugin
    :type plugin_path:  str
    :type plugin_name:  str
    """
    i18n_path = Jeedom.get_i18n_path(plugin_path)
    if os.path.exists(i18n_path):
        i18n_list = os.listdir(i18n_path)
        if i18n_list:
            scan_data = Jeedom.scan_for_strings(plugin_path)
            for i18n in i18n_list:
                json_data = {}
                try:
                    with open(i18n_path + os.sep + i18n) as i18n_content:
                        json_data = json.loads(i18n_content.read())
                except ValueError:
                    pass
                json_data = Jeedom.merge_i18n_json(plugin_path, json_data,
                                                   scan_data)
                # Json retire le \ avant les / à la lecture
                parsed_json_data = {}
                for key in json_data.keys():
                    parsed_json_data[key.replace('/', '\\/')] = json_data[key]
                File.write_json_file(i18n_path + os.sep + i18n,
                                     parsed_json_data)
        else:
            IO.print_error('Aucune traduction')
    else:
        IO.print_error('Aucun répertoire pour les traductions')


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        update_languages(sys.argv[1])
