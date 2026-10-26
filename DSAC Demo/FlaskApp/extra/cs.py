import csv
import re
from pandas import read_csv

df = read_csv('/Users/baharehzarei/Dropbox/FlaskApp/model/concepts.csv', sep=';')
df.columns=['word','no','emp']
df.drop(['no'], axis=1 , inplace = True)
df.drop(['emp'], axis=1, inplace = True )
df
df.to_csv('/Users/baharehzarei/Dropbox/FlaskApp/model/concepts.csv')


f=open('/Users/baharehzarei/Dropbox/FlaskApp/model/concepts.csv','r')
filedata=f.read()
f.close()
newdata=re.sub(r'[1|2|3|4|5|6|7|8|9|0|,]', r'', filedata)
f=open('/Users/baharehzarei/Dropbox/FlaskApp/model/concepts.csv','w')
f.write(newdata)
f.close()
