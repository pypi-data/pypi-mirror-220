import json


def write(file_path,data):
  with open(file_path,"w",encoding="utf8") as f:
    json.dump(data,f,indent=2,ensure_ascii=False)
 

def read(file_path):
  with open(file_path,"r") as d:
    data = json.load(d)
    return data


def reads(string):
    data = json.loads(string)
    return data
     
def writes(data):
  json.dumps(data,indent=2,ensure_ascii=False)

