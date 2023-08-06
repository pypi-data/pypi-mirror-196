#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil
import difflib
from pathlib import Path

from slpkg.configs import Configs


class NewConfig(Configs):

    def __init__(self):
        super(Configs).__init__()
        self.slpkg_config = Path(self.etc_path, f'{self.prog_name}.toml')
        self.blacklist_config = Path(self.etc_path, 'blacklist.toml')
        self.slpkg_config_new = Path(self.etc_path, f'{self.prog_name}.toml.new')
        self.blacklist_config_new = Path(self.etc_path, 'blacklist.toml.new')

        self.color = self.colour()

        self.bold: str = self.color['bold']
        self.green: str = self.color['green']
        self.yellow: str = self.color['yellow']
        self.bgreen: str = f'{self.bold}{self.green}'
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.endc: str = self.color['endc']
        self.choice = None

    def check(self):
        """ Checks for .new files. """
        print('Checking for NEW configuration files...')
        if self.slpkg_config_new.is_file() or self.blacklist_config_new.is_file():
            print('There are NEW files:\n')

            if self.slpkg_config_new.is_file():
                print(f"  {self.bgreen}{self.slpkg_config_new}{self.endc}")

            if self.blacklist_config_new.is_file():
                print(f"  {self.bgreen}{self.blacklist_config_new}{self.endc}")

            print(f'\nWhat would you like to do ({self.byellow}K{self.endc}/{self.byellow}O{self.endc}/'
                  f'{self.byellow}R{self.endc}/{self.byellow}P{self.endc})?\n')

            print(f"  ({self.byellow}K{self.endc})eep the old files and consider '.new' files later.\n"
                  f"  ({self.byellow}O{self.endc})verwrite all old files with the new ones.\n"
                  f"     The old files will be stored with the suffix '.orig'.\n"
                  f"  ({self.byellow}R{self.endc})emove all '.new' files.\n"
                  f"  ({self.byellow}P{self.endc})rompt K, O, R, D selection for every single file.\n")

            self.menu()

        elif not self.slpkg_config_new.is_file() and not self.blacklist_config_new.is_file():
            print("\n  No '.new' files found.\n")

    def menu(self):
        """ Menu of choices. """
        choice = input('Choice: ')

        choice = choice.lower()

        arguments: dict = {
            'k': self.keep,
            'o': self.overwrite,
            'r': self.remove,
            'p': self.prompt
        }

        try:
            arguments[choice]()
        except KeyError:
            self.keep()

    @staticmethod
    def keep():
        print("\nNo changes were made.\n")

    def overwrite(self):
        """ Copy tne .new files and rename the olds to .orig.  """
        if self.slpkg_config_new.is_file():
            self.overwrite_config_file()

        if self.blacklist_config_new.is_file():
            self.overwrite_blacklist_file()
        print()  # new line

    def overwrite_config_file(self):
        """ Copy tne slpkg.toml.new file and rename the old to .orig. """
        if self.slpkg_config.is_file():
            shutil.copy(self.slpkg_config, f"{self.slpkg_config}.orig")
            print(f"\ncp {self.slpkg_config} -> {self.slpkg_config}.orig")

        shutil.move(self.slpkg_config_new, self.slpkg_config)
        print(f"mv {self.slpkg_config_new} -> {self.slpkg_config}")

    def overwrite_blacklist_file(self):
        """ Copy tne blacklist.toml.new file and rename the old to .orig. """
        if self.blacklist_config.is_file():
            shutil.copy(self.blacklist_config, f"{self.blacklist_config}.orig")
            print(f"\ncp {self.blacklist_config} -> {self.blacklist_config}.orig")

        shutil.move(self.blacklist_config_new, self.blacklist_config)
        print(f"mv {self.blacklist_config_new} -> {self.blacklist_config}")

    def remove(self):
        """ Removes the .new files. """
        print()  # new line
        self.remove_config_file()
        self.remove_blacklist_file()
        print()  # new line

    def remove_config_file(self):
        """ Remove slpkg.toml.new file. """
        if self.slpkg_config_new.is_file():
            self.slpkg_config_new.unlink()
            print(f"rm {self.slpkg_config_new}")

    def remove_blacklist_file(self):
        """ Remove blacklist.toml.new file. """
        if self.blacklist_config_new.is_file():
            self.blacklist_config_new.unlink()
            print(f"rm {self.blacklist_config_new}")

    def prompt(self):
        """ Prompt K, O, R selection for every single file. """
        print(f"\n  ({self.byellow}K{self.endc})eep, ({self.byellow}O{self.endc})verwrite, "
              f"({self.byellow}R{self.endc})emove, ({self.byellow}D{self.endc})iff\n")
        if self.slpkg_config_new.is_file():
            make = input(f'{self.bgreen}{self.slpkg_config_new}{self.endc} - '
                         f'({self.byellow}K{self.endc}/{self.byellow}O{self.endc}/'
                         f'{self.byellow}R{self.endc}/{self.byellow}D{self.endc}): ')

            if make.lower() == 'k':
                pass
            if make.lower() == 'o':
                self.overwrite_config_file()
                print()  # new line
            if make.lower() == 'r':
                print()  # new line
                self.remove_config_file()
                print()  # new line
            if make.lower() == 'd':
                self.diff_files(self.slpkg_config_new, self.slpkg_config)

        if self.blacklist_config_new.is_file():
            make = input(f'{self.bgreen}{self.blacklist_config_new}{self.endc} - '
                         f'({self.byellow}K{self.endc}/{self.byellow}O{self.endc}/'
                         f'{self.byellow}R{self.endc}/{self.byellow}D{self.endc}): ')

            if make.lower() == 'k':
                pass
            if make.lower() == 'o':
                self.overwrite_blacklist_file()
                print()  # new line
            if make.lower() == 'r':
                print()  # new line
                self.remove_blacklist_file()
                print()  # new line
            if make.lower() == 'd':
                self.diff_files(self.blacklist_config_new, self.blacklist_config)

    @staticmethod
    def diff_files(file1, file2):
        """ Diff the .new and the current file. """
        with open(file1, 'r') as f1:
            with open(file2, 'r') as f2:
                diff = difflib.context_diff(
                    f1.readlines(),
                    f2.readlines(),
                    fromfile=str(file1),
                    tofile=str(file2)
                )
                for line in diff:
                    print(line, end='')
