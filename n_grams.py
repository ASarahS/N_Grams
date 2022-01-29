import pm4py
import pandas as pd

from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics
from collections import Counter
from collections import defaultdict


#Import event log data
log = xes_importer.apply('event_log.xes')


#Get event sequence details out of log
total_variants = case_statistics.get_variant_statistics(log)
variants_count = {i['variant']:i['count']for i in total_variants} #Which variant occurs how many times?
variants_list = list(variants_count.keys()) #List of events in variants
get_trace_lengths = [len(i['variant'].split(',')) for i in total_variants]
max_trace_length = max(get_trace_lengths) #Longest sequence in event log


#Get counts for all possible gram sequences
ngrams = [] #initialize list for ngrams (it will contain 2 to n gram sequences with their count)

for gram_length in range(2, max_trace_length):
  temp_gram = []
  grams = Counter()
  
  for variant in variants_list:
    trace_list = variant.split(',') #Getting trace list for n grams (from 2 to n)
    n_gram_trace_list = [trace_list[j:] for j in range(gram_length)]
    temp_gram.append(dict(Counter(list(zip(*(n_gram_trace_list)))))) #Count sequence (of length 2 to n) in each unique variant.
  
  for i, j in zip(temp_gram, variants_count.values()):
    for k in i.keys():
      i[k] = i[k] * j #Multiply sequence count with variant count (gives sequence count in variant)
  
  for i in temp_gram:
    for j in i.keys():
      grams[j] += i[j] #Get count of a sequence in whole log
  ngrams.append(dict(grams))


#Calculate probabilities to make predictions
def get_predictions(pattern, ngrams):
  pattern = tuple(pattern.split(','))
  probs = defaultdict(list) #Will contain probabilities of next states and gram number
  gram2 = ngrams[0]

  #Calculate probabilities for 1 gram
  total_occurences = sum(gram2.values()) #total occurences of 2 grams
  [probs[i[-1]].append(j/total_occurences) for i,j in gram2.items() if i[0]==pattern[-1]] #get probability of next activity
  probs['grams'].append('1-gram')
  
  #Calculate probabilities for 2 to n gram
  for i in range(1, len(pattern)):
    probs['grams'].append(str(i+1)+'-gram') #
    gram_n = ngrams[i]
    total_occurences_n = sum(gram_n.values())
    for j,k in gram_n.items():
      if j[0:i+1]==pattern[-i-1:]:
        probs[j[-1]].append(k/total_occurences_n)
  
  df = pd.DataFrame.from_dict(probs, orient='index').transpose().fillna(0)
  print(df)
  return df




get_predictions("Accepted,Accepted", ngrams)


