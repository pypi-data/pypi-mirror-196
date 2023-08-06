import os
import json


def update_package(dependencies, path='./package.json'):
    if os.path.exists(path):
        with open(path, 'r+') as f:
            p_obj = json.load(f)
            for key in dependencies:
                p_obj['dependencies'][key] = dependencies[key]
            json_object = json.dumps(p_obj, indent=2)
            f.write(json_object)

