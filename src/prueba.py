import pandas as pd
'''
df = pd.read_csv('engProlog30CSV\wn_s.csv', index_col=[0])

df = df.sort_values('Tag Count', ascending=False)

df1 = pd.read_csv('spa\PrologCSV\wn_s.csv', index_col=[0])

print(df1[df1['Tag Count'] != 0])

df1 = df1.sort_values('Tag Count', ascending=False)

print(df[df['Type' ]== 'n'].head(20))
print(df1.head(20))

def media_geometrica(na,nw,Na,Nw,N):
    return round((na*Na/N) + (nw*Nw/N))

print(media_geometrica(1135,7838,10031,16857,26000))'''

dfSynsets16 = pd.read_csv('spa/PrologCSV/Tag_Count_WikiCorpus.csv', index_col = [0], dtype = {'Synset16':'string'})

dfSynsets16 = dfSynsets16.sort_values(by = ['TagCount'], ascending=False)
dfSynsets16 = dfSynsets16.reset_index(drop = True)
print(dfSynsets16.head(10))