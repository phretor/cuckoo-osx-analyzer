# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

def choose_package(file_type, file_name):
    """Choose analysis package due to file type and file extension.
    @param file_type: file type.
    @param file_name: file name.
    @return: package name or None.
    """
    if not file_type:
        return None

    file_name = file_name.lower()

    if "Mach-O" in file_type:
        return "macho"
    elif "Zipped App Bundle" in file_type:
        return "zipped_app"
    elif file_name.endswith(".macho"):
        return "macho"
    elif file_name.endswith(".app.zip"):
        return "zipped_app"
    else:
        return "generic"
