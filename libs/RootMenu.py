# -*- coding: utf-8 -*-

import os
import sys
from BaseMenu import BaseMenu
from InfoMenu import InfoMenu
from FonctionnalitiesMenu import FonctionnalitiesMenu


class RootMenu(BaseMenu):
    """Menu principal de l'outil.
    """
    title = 'Outil de gestion d\'un plugin'
    menu = ['Télécharger le plugin Template',
            'Modifier l\'identifiant du plugin',
            'Modifier les informations du plugin',
            'Ajouter des fonctionnalités']
    plugin_template_repo = \
        'https://github.com/Jeedom-Plugins-Extra/plugin-template.git'
    plugin_name = ''
    plugin_name_file_path = ''

    def __init__(self, plugin_name, plugin_name_file_path):
        """Constructeur
        Initialise le chemin vers le fichier qui stocke le nom du plugin.
        :params plugin_name:           Nom du plugin
        :params plugin_name_file_path: Chemin du fichier stockant le nom du
        plugin
        :type plugin_name:             str
        :type plugin_name_file_path:   str
        """
        if sys.version_info[0] < 3:
            super(RootMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name
        self.plugin_name_file_path = plugin_name_file_path

    def action_1(self):
        """Télécharge une copie du plugin Template
        """
        self.plugin_name = 'template'
        sys_return = os.system('git clone ' + self.plugin_template_repo +
                               ' 2> /dev/null')
        if sys_return == 0:
            self.print_success('Le plugin ' + self.plugin_name +
                               ' a été téléchargé')
        else:
            self.print_error('Le plugin ' + self.plugin_name +
                             ' est déjà téléchargé.')
        self.save_current_plugin_name()

    def action_2(self):
        """Renomme le plugin
        Modifie le nom des répertoires, des fichiers ainsi que le contenu
        des fichiers.
        """

        if 'plugin-'+self.plugin_name in os.listdir('.'):
            new_name = self.get_user_input('Nouveau nom du plugin : ')
            if 'plugin-'+new_name not in os.listdir('.'):
                # Renomme le répertoire racine du plugin
                os.rename('plugin-'+self.plugin_name, 'plugin-'+new_name)
                self.rename_plugin(
                    'plugin-'+new_name, self.plugin_name, new_name)
                self.print_success('Le plugin ' + self.plugin_name +
                                   ' a été renommé en ' + new_name)
                self.plugin_name = new_name
            else:
                self.print_error('Un plugin '+new_name+' existe déjà')
        else:
            self.print_error('Le plugin ' + self.plugin_name +
                             ' n\'a pas été trouvé')

    def action_3(self):
        """Lance le menu de modification des informations
        """
        info_menu = InfoMenu(self.plugin_name)
        info_menu.start()

    def action_4(self):
        """Lance le menu de modification des informations
        """
        fonctionnalities_menu = FonctionnalitiesMenu(self.plugin_name)
        fonctionnalities_menu.start()

    def save_current_plugin_name(self):
        """Ecrit le nom du plugin dans un fichier caché
        """
        with open(self.plugin_name_file_path, 'w') as plugin_name_file:
            plugin_name_file.write(self.plugin_name)
            plugin_name_file.close()

    def rename_plugin(self, current_path, old_name, new_name):
        """Remplace les occurences dans les noms des fichiers, les répertoires,
        et au sein des fichiers
        :param current_path: Répertoire courant
        :param old_name:     Ancien nom
        :param new_name:     Nouveau nom
        :type current_path:  str
        :type old_name:      str
        :type new_name:      str
        """
        if old_name != '' and new_name != '':
            # Remplacement des occurences dans les noms des fichiers et
            # des répertoires
            for item in os.listdir(current_path):
                # A enlever quand plugin-template sera renommé plugin-Template
                if 'core/template':
                    item = self.rename_item(current_path+os.sep,
                                            item,
                                            old_name,
                                            new_name)
                if os.path.isdir(current_path+os.sep+item):
                    self.rename_plugin(current_path+os.sep+item,
                                       old_name,
                                       new_name)
                else:
                    # Remplacement des occurences dans le fichier
                    self.replace_in_file(
                        current_path+os.sep+item, old_name, new_name)
            self.save_current_plugin_name()

    def replace_in_file(self, target_file, old_name, new_name):
        """Remplace l'ancien nom par le nouveau
        :param target_file: Fichier à traiter
        :param old_name:    Ancien nom du plugin
        :param new_name:    Nouveau nom du plugin
        :type target_file:  str
        :type old_name:     str
        :type new_name:     str
        """
        self.sed_replace(old_name, new_name, target_file)
        self.sed_replace(old_name.upper(), new_name.upper(), target_file)
        self.sed_replace(old_name.capitalize(),
                         new_name.capitalize(),
                         target_file)

    def rename_item(self, path, item, old_name, new_name):
        """Renomme un élément si besoin
        :param path:     Chemin courant
        :param item:     Fichier à tester
        :param old_name: Ancien nom du plugin
        :param new_name: Nouveau nom du plugin
        :type path:      str
        :type item:      str
        :type old_name:  str
        :type new_name:  str
        :return:         Fichier avec le nouveau nom si il a été renommé
        :rtype:          str
        """
        result = item
        # Cas simple
        if old_name in item:
            result = item.replace(old_name, new_name)
            os.rename(path+item, path+result)
        # En majuscule
        elif old_name.upper() in item:
            result = item.replace(old_name.upper(), new_name.upper())
            os.rename(path+item, path+result)
        # Avec une majuscule au début
        elif old_name.capitalize() in item:
            result = item.replace(old_name.capitalize(), new_name.capitalize())
            os.rename(path+item, path+result)
        return result