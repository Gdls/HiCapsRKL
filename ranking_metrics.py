import os
import sys
import codecs
import pdb
import math

dir = sys.argv[1]
class ranking(object):
  def __init__(self):
    print ("init")
  def output(self):
    fw = codecs.open(dir+"/output.txt","w","utf-8")
    f = codecs.open("./SampleData/medical_literature_retrieval_test_data/test.tsv","r","utf-8")
    datalist =f.read().splitlines()[1:]
    fresult = codecs.open(dir+"/test_results.tsv","r","utf-8")
    resultlist= fresult.read().splitlines()
    assert len(datalist)==len(resultlist)
    for i in range(len(resultlist)):
      fw.write(datalist[i].split("\t")[0]+"\t"+datalist[i].split("\t")[2]+"\t"+resultlist[i].strip()+"\n")
    f.close()
    fresult.close()
  def ranking_file(self):
    print ("ranking_file")
    f = codecs.open(dir+"/output.txt","r","utf-8")
    triple_dict = {}
    datalist = f.read().splitlines()
    for line in datalist:
      kg = line.split("\t")[1]
      if kg not in triple_dict.keys():
        triple_dict[kg] = []
        triple_dict[kg].append(line)
      else:
        triple_dict[kg].append(line)
    fw = codecs.open(dir+"/rank_result.txt","w","utf-8")
    for k in triple_dict.keys():
      triple_value_dict = {}
      for data in triple_dict[k]:
        values = [float(x) for x in data.split("\t")[2:7]]
        maxvalue =max(values)
        maxindex = values.index(maxvalue)
        if maxindex == 0:
          floatv = 5+maxvalue
        elif maxindex == 1:
          floatv = 4+maxvalue
        elif maxindex == 2:
          floatv = 3+maxvalue
        elif maxindex == 3:
          floatv = 2+maxvalue
        elif maxindex == 4:
          floatv = 1+maxvalue
        triple_value_dict[data] = floatv
      output = list(sorted(triple_value_dict.items(),key=lambda asd:asd[1],reverse= True))
      for elem in output:
        fw.write(elem[0]+"\t"+str(elem[1])+"\n")
    fw.close()  
    f.close()
  def p_k(self):
    print ("2.P@k")
    f = codecs.open(dir+"/rank_result.txt","r","utf-8")
    datalist = f.read().splitlines()
    triple_dict = {}
    for line in datalist:
      kg = line.split("\t")[1]
      if kg not in triple_dict.keys():
        triple_dict[kg] = []
        triple_dict[kg].append(line)
      else:
        triple_dict[kg].append(line)
    P_1_mostrel = 0.0
    P_5_mostrel = 0.0
    P_10_mostrel = 0.0    
    P_1_rel = 0.0
    P_5_rel = 0.0
    P_10_rel = 0.0
    for key in triple_dict.keys():
      data = triple_dict[key]
      top_1 =data[0:1]
      top_5 = data[0:5]
      top_10 = data[0:10]
      top_1_cnt = 0.0
      top_1_cnt_rel = 0.0
      top_5_cnt = 0.0
      top_5_cnt_rel = 0.0
      top_10_cnt = 0.0
      top_10_cnt_rel = 0.0
      for line in top_1:
        label = line.split("\t")[0]
        if label == "2":
          top_1_cnt +=1
          top_1_cnt_rel += 1
        elif label == "1":
          top_1_cnt_rel += 1
      P_1_mostrel += top_1_cnt/1.0
      P_1_rel += top_1_cnt_rel/1.0
      for line in top_5:
        label = line.split("\t")[0]
        if label == "2":
          top_5_cnt+=1
          top_5_cnt_rel+=1
        elif label == "1":
          top_5_cnt_rel+=1
      P_5_mostrel += top_5_cnt/5.0
      P_5_rel += top_5_cnt_rel/5.0
      for line in top_10:
        label = line.split("\t")[0]
        if label == "2":
          top_10_cnt+=1
          top_10_cnt_rel+=1
        elif label == "1":
          top_10_cnt_rel+=1
      P_10_mostrel += top_10_cnt/10.0
      P_10_rel += top_10_cnt_rel/10.0
    N = len(triple_dict.keys())
    P_at_1_mostrel = P_1_mostrel/N
    P_at_5_mostrel = P_5_mostrel/N
    P_at_10_mostrel = P_10_mostrel/N
    P_at_1_rel = P_1_rel/N
    P_at_5_rel = P_5_rel/N
    P_at_10_rel = P_10_rel/N
    print ("\tMost_relevant P@1",P_at_1_mostrel,"P@5",P_at_5_mostrel,"P@10",P_at_10_mostrel)
    print ("\tRrelevant P@1",P_at_1_rel,"P@5",P_at_5_rel,"P@10",P_at_10_rel)
  def ndcg_k(self):
    print ("4.NDCG@k")
    f = codecs.open(dir+"/rank_result.txt","r","utf-8")
    datalist = f.read().splitlines()
    triple_dict = {}
    for line in datalist:
      kg = line.split("\t")[1]
      if kg not in triple_dict.keys():
        triple_dict[kg] = []
        triple_dict[kg].append(line)
      else:
        triple_dict[kg].append(line)
    DCG_1 = 0.0
    DCG_5 = 0.0
    DCG_10 = 0.0
    IDCG_1 = 0.0
    IDCG_5 = 0.0
    IDCG_10 = 0.0
    NDCG_1=0.0
    NDCG_5=0.0
    NDCG_10=0.0
    for k in triple_dict.keys():
      DCG_1 = 0.0
      DCG_5 = 0.0
      DCG_10 = 0.0
      IDCG_1 = 0.0
      IDCG_5 = 0.0
      IDCG_10 = 0.0
      data = triple_dict[k]
      top_1 = data[0:1]
      top_5 = data[0:5]
      idealD_5 = [int(line.split("\t")[0]) for line in top_5]
      idealD_5.sort(reverse=True)
      if len(data)>=10:
        top_10 = data[0:10]
      else:
        top_10 = data
      idealD_10 = [int(line.split("\t")[0]) for line in top_10]
      idealD_10.sort(reverse=True)

      for i in range(1):
        label = top_1[i].split("\t")[0]
        DCG_1 += (2**int(label)-1)/(math.log(i+1+1,2))
        IDCG_1 += (2**int(2)-1)/(math.log(i+1+1,2))
      NDCG_1 += DCG_1/IDCG_1
      for i in range(5):
        label = top_5[i].split("\t")[0]
        ilabel = idealD_5[i]
        DCG_5 += (2**int(label)-1)/math.log(i+1+1,2)
        IDCG_5 += (2**int(ilabel)-1)/math.log(i+1+1,2)
      NDCG_5 += DCG_5/(IDCG_5+0.00001)
      for i in range(len(top_10)):
        label = top_10[i].split("\t")[0]
        ilabel = idealD_10[i]
        DCG_10 += (2**int(label)-1)/math.log(i+1+1,2)
        IDCG_10 += (2**int(ilabel)-1)/math.log(i+1+1,2)
      NDCG_10 += DCG_10/(IDCG_10+0.00001)
    N = len(triple_dict.keys())
    _NDCG_1 = NDCG_1/N
    _NDCG_5 = NDCG_5/N
    _NDCG_10 = NDCG_10/N
    print ("\tNDCG@1",_NDCG_1,"NDCG@5",_NDCG_5,"NDCG@10",_NDCG_10)
  def mrr(self):
    f = codecs.open(dir+"/rank_result.txt","r","utf-8")
    print ("1.MRR")
    datalist = f.read().splitlines()
    triple_dict = {}
    for line in datalist:
      kg = line.split("\t")[1]
      if kg not in triple_dict.keys():
        triple_dict[kg] = []
        triple_dict[kg].append(line)
      else:
        triple_dict[kg].append(line)
    RR_mostrelevant = 0.0
    RR_relevant = 0.0
    for k in triple_dict.keys():
      data = triple_dict[k]
      i = 1
      mostrel_flag = False
      rel_flag =False
      for item in data:
        label = item.split("\t")[0]
        if label == "2" and mostrel_flag==False:
          RR_mostrelevant += 1/i
          mostrel_flag =True
        if (label == "2" or label == "1") and rel_flag==False:
          RR_relevant += 1/i
          rel_flag = True
        i = i+1
    N = len(triple_dict.keys())
    MRR_mostrelevant = RR_mostrelevant/N
    MRR_relevant = RR_relevant/N
    print ("\tMRR_mostrelevant",MRR_mostrelevant,"MRR_relevant",MRR_relevant,"N", N)
    f.close()
  def map(self):
    print ("3.MAP")
    f = codecs.open(dir+"/rank_result.txt","r","utf-8")
    datalist = f.read().splitlines()
    triple_dict = {}
    for line in datalist:
      kg = line.split("\t")[1]
      if kg not in triple_dict.keys():
        triple_dict[kg] = []
        triple_dict[kg].append(line)
      else:
        triple_dict[kg].append(line)
    AP_mostrel = 0.0
    AP_rel = 0.0
    for k in triple_dict.keys():
      data = triple_dict[k]
      R = len(data)
      cnt_mostrel = 0.0
      cnt_rel = 0.0
      P_mostrel = 0.0
      P_rel = 0.0
      for i in range(R):
        label = data[i].split("\t")[0]
        if label == "2":
          cnt_mostrel +=1
          cnt_rel += 1
        if label == "1":
          cnt_rel += 1
        P_mostrel += cnt_mostrel/(i+1.0)
        P_rel += cnt_rel/(i+1.0)
      AP_mostrel += P_mostrel/R
      AP_rel += P_rel/R
    N = len(triple_dict.keys())
    MAP_mostrel = AP_mostrel/N
    MAP_rel = AP_rel/N
    print ("\tMAP_mostrelevant",MAP_mostrel,"MAP_relevant",MAP_rel)
if __name__=="__main__":
  obj = ranking()
  obj.output()
  obj.ranking_file()
  obj.mrr() # 
  obj.p_k() # 
  obj.map() # 
  obj.ndcg_k() # 
