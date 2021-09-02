import os
import sys
import pdb
import codecs
dir = sys.argv[1]

fgold = codecs.open("SampleData/relevance_prediction_test_data/test.tsv","r","utf-8")
datalist = fgold.read().splitlines()[1:]
goldlist= [line.split("\t")[0] for line in datalist]
fgold.close()

fpred = codecs.open("./"+dir+"/test_results.tsv","r","utf-8")
predlist = fpred.read().splitlines()
predoutput = []
labellist = ["0","1","2","3","4"] # most-rel rel, weak-irrel, neutral, irrel
for line in predlist:
  prediction = [float(value) for value in line.split("\t")]
  pred = str(prediction.index(max(prediction))) 
  predoutput.append(pred)
totalf1 = 0.0
totalacc = 0.0
for each_c in labellist:
  tp = 0.0
  allp = 0.0
  allt = 0.0
  for i in range(1050):
    #print (each_c, predlist[i], )
    if predoutput[i] == each_c:
      allt = allt +1
    if goldlist[i] == each_c:
      allp = allp+1
    if predoutput[i] == each_c and goldlist[i]==predoutput[i]:
      tp = tp +1
  totalacc = totalacc+tp
  recall = tp/(allp+0.000001)
  precision = tp/(allt+0.000001)
  f1 = 2*recall*precision/(recall+precision+0.000001)
  totalf1 = totalf1 + f1
  print ("Label ",each_c,"P:",precision,"R:",recall,"F1:",f1)
  #pdb.set_trace()
macrof1 = totalf1/5
acc = totalacc/1050
print ("Macro-F1:",macrof1,"Micro-F1:",acc)
fpred.close()
