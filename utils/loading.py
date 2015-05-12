# Copyright (C) 2014 Federico (phretor) Maggi

import importlib
import logging

logger = logging.getLogger(__name__)

def load_by_name(name):
    """Load a class or method by module path"""
    modules = name.split('.')
    module, func = '.'.join(modules[0:-1]), modules[-1]

    logger.debug('Loading %s from %s', func, module)

    try:
        module_object = importlib.import_module(module)
        logger.debug('Found module object of %s: %s', module, module_object)
    except ImportError:
        return None

    try:
        return getattr(module_object, func, None)
    except AttributeError:
        return None


