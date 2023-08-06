import yaml
import json
from jsonpath_ng import parse


def paths(tree, cur=()):
    # get all nested strings from the yml file
    if not tree:
        yield cur
    else:
        try:
            for n, s in tree.items():
                for path in paths(s, cur + (n,)):
                    yield path
        except:
            yield tree


def query_dictionary(target_dict: dict, query: str):

    # if the query is invalid this will raise an error, catch this
    # and return an "invalid query" output instead
    try:
        # query is parsed here
        jpath = parse(query)
        # output is list -> list
        output = [match.value for match in jpath.find(target_dict)]
    except:
        # if invalid query -> error message to user
        output = f"shplat error - invalid query:'{query}'"

    # output is one value -> value
    if len(output) == 1:
        output = output[0]

    # output is not found -> None
    elif len(output) == 0:
        output = None

    return output


def get_nested_data(data, location_string):
    # get value out of dict using dot notation string
    location_list = location_string.split(".")

    nested = data
    for l in location_list:
        nested = nested[l]

    return nested


def update_dict(d: dict, curvalue: str, newvalue):
    # if shplat config is empty, return null
    if d == None:
        return None
    for k, v in d.items():
        if v == curvalue:
            d.update({k: newvalue})
        elif hasattr(v, "items"):
            update_dict(v, curvalue, newvalue)


def shplat(
    data: dict,
    shplat_config: dict,
    yml_output: bool = False,
    yml_output_path: str = "outgoing.shplat.yml",
    json_output: bool = False,
    json_output_path: str = "outgoing.json",
):

    # get all the string location formats from the config file
    shplat_refs = list(paths(shplat_config))

    # get all the corresponding data from the datadict
    shplat_data = [query_dictionary(data, x) for x in shplat_refs]

    # replace the location indicators with the data
    for shplat_table in zip(shplat_refs, shplat_data):
        update_dict(shplat_config, shplat_table[0], shplat_table[1])

    if yml_output:
        with open(yml_output_path, "w") as f:
            data = yaml.safe_dump(shplat_config)
            f.write(data)

    if json_output:
        with open(json_output_path, "w") as f:
            data = json.dumps(shplat_config)
            f.write(data)

    return shplat_config


def main():
    import os
    import argparse
    parser = argparse.ArgumentParser(
        prog="shplat",
        description="The shplat CLI",
        epilog="Happy shplatting!"
    )
    parser.add_argument("input_file")
    parser.add_argument("config_file")
    parser.add_argument("output")
    args = parser.parse_args()

    with open(args.config_file, "r") as f:
        config = yaml.safe_load(f)

    with open(args.input_file, "r") as f:
        inputdata = json.load(f)

    if not os.path.exists("output/"):
        os.mkdir("output")
    # shplat the document
    shplat(
        inputdata,
        config,
        json_output=True,
        json_output_path=f"output/{args.output}.json",
        yml_output=True,
        yml_output_path=f"output/{args.output}.yml",
    )

if __name__ == "__main__":
    main()
