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
                part_id = row[0]
                ts_date = row[1]
                ts_time = row[2]
                room = row[3]
                json_dataset.append({'part_id': int(part_id), 'ts_date': ts_date, 'ts_time': ts_time, 'room': room})
                line_count += 1

    res = db.indoorLocalization.insert_many(json_dataset)
    if (res):
        print('client1 ingestion done')


if __name__ == "__main__":
    main()

