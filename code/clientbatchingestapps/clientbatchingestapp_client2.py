from pymongo import MongoClient
import sys
import csv
import json



def main():

    file_path = sys.argv[1]
    config_file_path = sys.argv[2]

    with open(config_file_path, 'r') as f:
        parsed_json = json.load(f)

    mongo_uri = parsed_json['mongo_uri']
    mongo_dbname = parsed_json['mongo_db_name']
    client = MongoClient(mongo_uri)
    db = client[mongo_dbname]
    json_dataset = []

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                # data to be sent to api
                year = row[0]
                length = row[1]
                title = row[2]
                subject = row[3]
                json_dataset.append({'Year': int(year), 'Length': length, 'Title': title, 'Subject': subject})
                line_count += 1

    res = db.films.insert_many(json_dataset)
    if (res):
        print('client2 ingestion done')


if __name__ == "__main__":
    main()
