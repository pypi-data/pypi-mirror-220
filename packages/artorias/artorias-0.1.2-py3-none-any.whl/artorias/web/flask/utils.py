from typing import List

from click import Command, Group
from flask import Blueprint

from artorias.utils import walk_module


def find_blueprints(blueprints_package: str) -> List[Blueprint]:
    blueprints = []
    for module in walk_module(blueprints_package):
        for obj_name in dir(module):
            obj = getattr(module, obj_name)
            if isinstance(obj, Blueprint):
                blueprints.append(obj)
    return blueprints


def find_commands(commands_package: str) -> List[Command | Group]:
    commands = []
    for module in walk_module(commands_package):
        for obj_name in dir(module):
            obj = getattr(module, obj_name)
            if isinstance(obj, (Command, Group)):
                commands.append(obj)
    return commands
