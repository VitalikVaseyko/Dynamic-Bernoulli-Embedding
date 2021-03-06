import glob
import numpy as np
import pandas as pd
import re
import os

# Change this to the name of the folder where your dataset is
dataset_name = "data_mining_data"
# Change this to the number of words you want in the vocabulary
V = 10000

files = glob.glob('../'+dataset_name + '/New_Data_stopwords/*.txt')
dictionary = {}
count = {}
N = len(files)

if not os.path.exists('train_temp'):
    os.mkdir('train_temp')
if not os.path.exists('train'):
    os.mkdir('train')

for f_number, fn in enumerate(files):
    #print(str(f_number)+" out of "+str(N))
    with open(fn, 'r') as myfile:
        words = re.sub(r'[^a-zA-Z ]',r' ', myfile.read().replace('-\n','').replace('\n',' ')).lower().split()
    data = np.zeros(len(words))
    for idx, word in enumerate(words):
        if word not in dictionary:
            count[len(dictionary)] = 1
            dictionary[word] = len(dictionary)
        data[idx] = dictionary[word]
        count[data[idx]] += 1

    np.save(fn.replace('.txt','.npy').replace('New_Data_stopwords\\','train_temp/'), data.astype('int32'))

#pickle.dump( dictionary, open( 'raw/dict.pkl', "a+" ) )
#pickle.dump( count, open( 'raw/counts.pkl', "a+" ) )

df = pd.DataFrame.from_dict(dictionary, orient='index')
cf = pd.DataFrame.from_dict(count, orient='index')
df.columns = ['idx']
cf.columns = ['cnt']
uni = df.join(cf, on = 'idx')

unig = uni.sort_values(by='cnt', ascending = False).reset_index().reset_index()

unig.columns = ['new_idx', 'word', 'old_idx', 'cnt']

old_idx = unig.old_idx.values

files = glob.glob('../'+dataset_name +'/train_temp/*.npy')
for fname in files:
    print(str(f_number)+" out of "+str(N))
    dat = np.load(fname)
    new_dat = np.zeros_like(dat) + 2*V
    
    for ni, oi in enumerate(old_idx[:V]):
        new_dat[dat == oi] = ni
    new_dat = new_dat[new_dat < V].astype('int32')

    new_fname = fname.replace('train_temp\\','train/')

    np.save(new_fname, new_dat)

unig.head(V).to_csv('./unigram.txt', header=False, index=False, sep='\t', columns=['word', 'new_idx', 'cnt'])

print('step_1_count_words has ended\n\n')