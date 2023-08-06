import json
import pandas as pd
import sys

# output_file = sys.argv[1]
sheet_name = "Sheet1"

def txt_writer_lst(output_file, res):
    with open(output_file,"w",encoding= "utf-8") as fp:
        for line in res:
            fp.write("{}\n".format(line))


def jsonl_writer_lst(output_file, res):
    with open(output_file,"w") as fp:
        for line in res:
            fp.write(json.dumps(i, ensure_ascii=False)+"\n")

def json_writer_lst(output_file, res):
    with open(output_file,"w") as fp:
        json.dump(res, fp, indent=2, ensure_ascii=False)


def excel_writer_dic(output_file, res):
    df = pd.DataFrame(res) #res为字典
    df.to_excel(output_file,index=False)


def csv_writer_dic(output_file, res):
    df = pd.DataFrame(res)
    df.to_csv(output_file, index=False)