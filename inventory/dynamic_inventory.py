#!/usr/bin/env python3
import csv
from pprint import pprint
import json
import os

csv_filename = "dyninv_input.csv"


def main():

    if os.path.isfile(csv_filename):
        csv_path = csv_filename
    elif os.path.isfile("files/{}".format(csv_filename)):
        csv_path = "files/{}".format(csv_filename)
    elif os.path.isfile("../files/{}".format(csv_filename)):
        csv_path = "../files/{}".format(csv_filename)
    else:
        print("Can't find {}, exiting.".format(csv_filename))
        exit(0)

    with open(csv_path) as csvfile:
        # reader = csv.reader(csvfile, delimiter=',')
        reader = csv.DictReader(csvfile)

        model_hash = {}
        sitecode_hash = {}
        sitecode_model_hash = {}

        for row in reader:
            # print(row['model'], row['hostname'], row['hash'], row['version'])
            model_key = row["model"].split("/")[1]
            if model_key in model_hash:
                model_hash[model_key].append(row["hostname"])
            else:
                model_hash[model_key] = [row["hostname"]]

            sitecode_key = row["hostname"].split("-")[0]
            if sitecode_key in sitecode_hash:
                sitecode_hash[sitecode_key].append(row["hostname"])
            else:
                sitecode_hash[sitecode_key] = [row["hostname"]]

        for sitecode_k, sitecode_v in sitecode_hash.items():
            for model_k, model_v in model_hash.items():
                for host in sitecode_v:
                    if host in model_v:
                        # model/site intersection
                        sitecode_model_key = "{}_{}".format(sitecode_k, model_k)
                        if sitecode_model_key in sitecode_model_hash:
                            sitecode_model_hash[sitecode_model_key].append(host)
                        else:
                            sitecode_model_hash[sitecode_model_key] = [host]

    result = {}
    result.update(model_hash)
    result.update(sitecode_hash)
    result.update(sitecode_model_hash)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
