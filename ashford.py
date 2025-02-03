import os
import csv
import shutil
import datetime
import pysftp as sftp
import warnings as war
from connection.Connection import Connection




objConnect = Connection()
host = "sftp.waitingmed.com"
user = "ashfordh"
file_path = ["./server/", './compare/', './nocompare/','./compare/get2colums/', "./compare/processed/"]
password = "SAz2HTQHx7f7EB4"
cnopts = sftp.CnOpts()
cnopts.hostkeys = None
conn = objConnect.Connect(user,password,host,cnopts)

try:
  if(conn):
    print("connected")
    conn.get_d("upload",file_path[0], preserve_mtime=True)
    for p in conn.listdir_attr("upload"):
       print(p.filename, p)
except:
  print("Error connection", conn)
  

today = datetime.datetime.now().strftime("%Y%m%d")
oneday = datetime.timedelta(days=1)
last = datetime.date.today() - oneday 
combinaciones = []
all_files = os.listdir(file_path[0])
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
to_day = datetime.datetime.now().strftime("%Y%m%d")
one_day = datetime.timedelta(days=1)
lastday = datetime.date.today() - one_day



def getFiles(path):
   f = []
   for file in os.listdir(path):
      if os.path.isfile(os.path.join(path, file)):
         f.append(file)
   return f

def getCompareF(path):
   lista =  []
   lista_compare = []
   count = 0

   
   directory_compare = os.path.dirname(file_path[1]);
   nocompare = os.path.dirname(file_path[2])
   getcolumn = os.path.dirname(file_path[3])
   processed = os.path.dirname(file_path[4])

   if not os.path.exists(directory_compare):
    os.makedirs(directory_compare)
    
   
   
   if not os.path.exists(nocompare):
      os.makedirs(nocompare)
   

   if not os.path.exists(getcolumn):
        os.makedirs(getcolumn)
   
   if not os.path.exists(processed):
       os.makedirs(processed)
   
   for file in csv_files:
      if os.path.isfile(os.path.join(path, file)) and not os.path.isfile(os.path.join(file_path[4], file)):
         if(file.split("-")[-1] == "LabHeaderData.csv"):
           lista_compare.append(file_path[1]+file)
           shutil.copy2(os.path.join(file_path[0],file),file_path[1])
         else:
            shutil.copy2(os.path.join(file_path[0],file),file_path[2])

   name = slice(10,50)

   for x in lista_compare:
      with open(x,'r') as check_file:
               reader_new = csv.reader(check_file)
               with open(file_path[3]+x[name], 'w', newline='') as result:
                 writer_new = csv.writer(result)
                 for r in reader_new:
                    writer_new.writerow((r[1],r[2]))
    
   for z in getFiles(file_path[3]):
      lista.append(file_path[3]+z)
   for i in range(len(lista)):
      for j in range(i+1, len(lista)):
         count = count+1
         combinaciones.append([lista[i], lista[j]])
   return combinaciones  

lista = getCompareF(file_path[0])
x = slice(13)
file_list = lista
file_new = []
file_old = []
x = slice(21,60)
count = 0
for i in file_list:
   file_new = i[0]
   file_old = i[1]
   print(i[0][x],' > ',i[1][x])
   with open(file_new, 'r') as f1, open(file_old, 'r') as f2:
    new_csv = f1.readlines()
    old_csv = f2.readlines()
    count = 0
    for row2 in old_csv:
       if row2 in new_csv:
          count +=1
          print(row2) 
    print(count-1)
count_exist = 0
for x in getFiles(file_path[1]):
   
      if(x.split("-")[-1] == "LabHeaderData.csv"):
         if(x.split("-")[0] == lastday.strftime("%Y%m%d") or x.split("-")[0] == to_day):
        
            print(x)
         else:
            shutil.move(os.path.join(file_path[1],x),file_path[4])

