import requests,json
import pickle

#getting data from website
url = 'https://tickets.fifa.com/API/WCachedL1/en/BasicCodes/GetBasicCodesAvailavilityDemmand?currencyId=USD'
r = requests.get(url)
response=r.json()
res=response["Data"]["Availability"]
data={'IMT61':0,'IMT62':0,'IMT64':0}
result=[]
for i in res:
  if i['p'] in data.keys() and data[i['p']]<3:
    i['n']=data[i['p']]+1
    result.append(i)
    data[i['p']]+=1

#checking availability
avil=False
for i in result:
  if i['a']==0:
    avil=True
    break

final={}


if avil:
  #getting previous stored data
  try:
    file=open('data.txt','rb')
    unpickler = pickle.Unpickler(file)
    dt=unpickler.load()
    file.close()
    #now checking
    for i,j in zip(result,dt):
      if i['a']==0 and j['a']==0: #change here 1 and 0 for real result
        if i['p'] not in final.keys():
          final[i['p']]=[str(i['n'])]
        else:
          temp=final[i['p']]
          temp.append(str(i['n']))
          final[i['p']]=temp
  except:
    for i in result:
      if i['a']==0: #change here 1 for real result
        if i['p'] not in final.keys():
          final[i['p']]=[str(i['n'])]
        else:
          temp=final[i['p']]
          temp.append(str(i['n']))
          final[i['p']]=temp
else:
  print("Nothing")


st=''
for i in final:
  cat=' & '.join(final[i])
  st+="Match "+i[3:]+" Cat "+cat+"\n"
print(st)

#send mail here



#End mail

#saving updated file
file=open('data.txt','wb+')
pickle.dump(result,file)
#print(dt)
