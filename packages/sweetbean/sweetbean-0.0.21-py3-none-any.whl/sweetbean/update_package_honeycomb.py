import os
import json


def update_package(dependencies, path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            print(f)
            p_obj = json.load(f)
            print(p_obj)
            for key in dependencies:
                p_obj['dependencies'][key] = dependencies[key]
            json_object = json.dumps(p_obj, indent=2)
            with open(path, 'w') as f_out:
                f.write(json_object)

