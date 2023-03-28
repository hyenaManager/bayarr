
#for making pure nested list for itemName id and quantity pice and post price own its user_id
def filt(data,userId,By='userID'):
    data_list = []
    for i in data:
        if i[By] == userId:
            data_list.append(i)
    return data_list

def update_data(request,id,data):
    dataUp = data.objects.get(id=id)
    dataUp.quantity = request.POST['quantity']
    dataUp.price = request.POST['price']
    dataUp.post_price = request.POST['post_price']
    return dataUp.save()

def delete_data(request,id,data):
    dataDel = data.objects.get(id=id)
    return dataDel.delete()

#for filtering the item names in the database
def itemName_filter(cleaned_data):
    itemName_list = []
    for i in cleaned_data:
        itemName_list.append(i['item_name'])
    return itemName_list

#for filtering the existing quatity
def fetch_idQ(data,item_name,type):
    listId = []
    listQ = []
    if type == 'id':  
        for j in item_name:  
            for i in data:
                if j ==i['item_name']:
                    listId.append(i['id'])
        return listId
    elif type == 'q':
        for j in item_name:  
            for i in data:
                if j ==i['item_name']:
                    listQ.append(i['quantity'])
        return listQ
#print(fetch_idQ(mainData1,['pepsi','lemon tea','cake'],'id'))
            
#for filtering each item property
def property_dict(cleaned_data):
    property_dict = {}
    name_list = itemName_filter(cleaned_data)
    for i in name_list:
        for j in cleaned_data:
            if j['item_name'] == i:
                property_dict.update({i:j['price']})
    return property_dict

#input listing funciton
def lister(data):
    data = data[:-1]
    data = data.replace('"','')
    data1 = data.split('+')
    return data1

#for graph data
def sellDate(data):
    dates = []
    for i in data:
        if i not in dates:
            dates.append(i)
    return dates

def sell_amount(data,dates):
    moneyBy_date = []
    amount_list = []
    for i in dates:
        amount_list = []
        for j in data:
            if i == j['date']:
                amount_list.append(int(j['O_price'])*int(j['Oquantity']))
        moneyBy_date.append(sum(amount_list))
    return moneyBy_date

def timeFilter(type):
    from datetime import date
    currentTime = str(date.today())
    currentTime = currentTime.split('-')
    if type == 'month':
        result = currentTime[1]
    elif type == 'day':
        result = currentTime[2]
    elif type == 'year':
        result = currentTime[0]
    return result

def code_generator(num):
    import random
    numCode = ""
    for i in range(int(num)):
        numCode+=str(random.randint(1,9))
    return numCode

def crypting(data,style):
    data = str(data)
    de_cryptor = {'a':'2','b':'3','j':'4','w':'5','l':'6','f':'9','m':'8','x':'7','&':'1','x':'0'}
    en_cryptor = {'2':'a','3':'b','4':'j','5':'w','6':'l','9':'f','8':'m','7':'x','1':'&','0':'x'}
    crypted_code = ''
    if style == 'en':
        for i in range(len(data)):
            crypted_code += en_cryptor[data[i]]
    else:
        for i in range(len(data)):
            crypted_code +=de_cryptor[data[i]]
    return crypted_code

def dictMaker(itemName,quantity,price,post_price,time):
    dictResult = []
    for i in range(len(itemName)):
        exDict = {'item_name':itemName[i],'quantity':quantity[i],'price':price[i],'post_price':post_price[i],'time':time[i]}
        dictResult.append(exDict)
    return dictResult

def dictMakerU(itemName,CitemName,quantity,Cquantity,price,Cprice,post_price,Cpost_price,time):
    dictResult = []
    for j in range(len(itemName)):
        exDict = [
            [itemName[j],CitemName[j]],
            [quantity[j],Cquantity[j]],
            [price[j],Cprice[j]],
            [post_price[j],Cpost_price[j]],
            time[j]
        ]
        checked_result = {}
        count = 0
        for i in exDict:
            if count == 0:
                if i[0] != i[1]:
                    checked_result.update({'item_name':i[0],'Citem_name':i[1]})
                else:
                    checked_result.update({'item_name':i[0]})
            elif count == 1:
                if i[0] != i[1]:
                    checked_result.update({'quantity':i[0],'Cquantity':i[1]})
            elif count == 2:
                if i[0] != i[1]:
                    checked_result.update({'price':i[0],'Cprice':i[1]})
            elif count == 3:
                if i[0] != i[1]:
                    checked_result.update({'post_price':i[0],'Cpost_price':i[1]})
                checked_result.update({'time':time[j]})
            # elif count == 4:
            #     checked_result.update({str(i)})
            count +=1
        count = 0
        dictResult.append(checked_result)
    return dictResult

#most of above modules(funcitons) are not used coz of pandas' cool functions
def dRemover(list):
    rList = []
    for i in list:
        if i in rList:
            pass
        else:
            rList.append(i)
    return rList

# def marking_data():
#     markerList1 = sellD[['item_marker']].to_dict('list')
#     markerList = markerList1['item_marker']
#     profit_withMarker = []
#     quantity_withMarker = []
#     item_nameWM = []
    
#     for i in np.unique(markerList):
#         sellN = mainData.objects.values()
#         sell_names_wm = pandas.DataFrame(sellN)
#         sellNames_wm = sell_names_wm.loc[sell_names_wm['id']==i]
#         namesWM = sellNames_wm[['item_name']].to_dict('list')
#         namesWM = dRemover(namesWM['item_name'])
#         print('ids',namesWM)
#         markerMonth = sellD.loc[sellD['item_marker']==i]
#         sellPQlist = markerMonth[['Opost_price','Oquantity']].to_dict('list')#for quantity and price with marker
#         sellQList = sum(sellPQlist['Oquantity'])
#         sellPList = sum(sellPQlist['Opost_price'])
#         profit_withMarker.append(sellPList)
#         quantity_withMarker.append(sellQList)
#         item_nameWM.append(namesWM[0])

