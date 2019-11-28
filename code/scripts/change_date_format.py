from datetime import datetime
import sys
import csv



def main():

    file_path = sys.argv[1]
    out_path =  sys.argv[2]
    with open(out_path, 'a') as out_file:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    # data to be sent to api
                    t0 = row[0]
                    t1 = row[1]
                    t2 = row[2]
                    t3 = row[3]
                    t4 = row[4]
                    t5 = row[5]
                    a = datetime.strptime(t0, "%m/%d/%Y %I:%M:%S %p")
                    b = datetime(1970, 1, 1)
                    res = int((a - b).total_seconds())
                    out_file.write(str(res)+"," + t1 +"," +t2+"," +t3+"," +t4+"," +t5+"\n")



if __name__ == "__main__":
    main()
