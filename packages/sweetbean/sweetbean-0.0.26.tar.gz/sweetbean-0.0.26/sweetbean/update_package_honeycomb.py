import os
import json

def update_package(dependencies, path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            p_obj = json.load(f)
            for key in dependencies:
                p_obj['dependencies'][key] = dependencies[key]
            json_object = json.dumps(p_obj, indent=2)
            with open(path, 'w') as f_out:
                f_out.write(json_object)


def get_import(dependency):
    for k in dependency:
        for k_ in dependency[k]:
            return f"import {k} from \'{k_}\'\n"


