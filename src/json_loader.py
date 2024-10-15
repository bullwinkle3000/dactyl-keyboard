import json
import os


def load_json(filepath, save_path='../things'):
    with open('./src/run_config.json') as fid:
        main_json = json.load(fid)

    with open(filepath, mode='r') as fid:
        first_data = json.load(fid)

    for key in first_data:
        value = str(first_data[key])
        if value.startswith("file:"):
            new_file_path = os.path.join(".", "src", "json", value[5:])
            print("Loading child json file: ", new_file_path)

            with open(new_file_path, mode='r') as nfid:
                to_merge = json.load(nfid)
                for new_key in to_merge:
                    main_json[new_key] = to_merge[new_key]

    print("Overriding values from main override file into new merged file")

    for key in first_data:
        main_json[key] = first_data[key]

    return main_json



