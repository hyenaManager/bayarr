import pandas 
import io
import csv
import reportlab
from django.core.mail import send_mail
from twilio.rest import Client
from .models import historyData,mainData,userInfo

from.modules import *
from datetime import date,datetime
from json import dumps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse,FileResponse
from django.shortcuts import redirect, render
from reportlab.pdfgen import canvas
import numpy as np
@login_required(login_url='login')
def history(request):
    dateNow = str(date.today())
    if request.method == 'POST':
        dateNow = request.POST['date']
    hisData = list(historyData.objects.values())
    defaultDateD1 = pandas.DataFrame(hisData)
    defaultDateD = defaultDateD1.loc[defaultDateD1['date']==dateNow]  
    filtData1 = defaultDateD.loc[defaultDateD['userID1']==request.user.id]
    deletes = filtData1.loc[filtData1['historyFor']=='deleting']
    deletingD = deletes.to_dict(orient='list')
    addings = filtData1.loc[filtData1['historyFor']=='adding']
    addingD = addings.to_dict(orient='list')
    sellings = filtData1.loc[filtData1['historyFor']=='selling']
    sellingD = sellings.to_dict('list')
    updatings = filtData1.loc[filtData1['historyFor']=='updating']
    updatingD = updatings.to_dict(orient='list')
    added = dictMaker(addingD['item_name'],addingD['Oquantity'],addingD['O_price'],addingD['Opost_price'],addingD['actionTime'])
    updated = dictMakerU(
        updatingD['item_name'],
        updatingD['Citem_name'],
        updatingD['Oquantity'],
        updatingD['Cquantity'],
        updatingD['O_price'],
        updatingD['C_price'],
        updatingD['Opost_price'],
        updatingD['Cpost_price'],
        updatingD['actionTime']
        )
    updatedTo = dictMaker(updatingD['Citem_name'],updatingD['Cquantity'],updatingD['C_price'],updatingD['Cpost_price'],updatingD['actionTime'])
    deleted = dictMaker(deletingD['item_name'],deletingD['Oquantity'],deletingD['O_price'],deletingD['Opost_price'],deletingD['actionTime'])
    sold = dictMaker(sellingD['item_name'],sellingD['Oquantity'],sellingD['O_price'],sellingD['Opost_price'],sellingD['actionTime'])
    return render(request,'history.html',{
        'deleted':deleted,
        'added':added,
        'updated':updated,
        'updatedTo':updatedTo,
        'sold':sold,
        'storeName':request.user.username,
        'date':dateNow,
    })

def login_view(request):
    return render(request,'login.html')

def register_form(request):
     return render(request,'register.html')
@login_required(login_url='login')
def graph(request,monthInput):#monthInput default is current month and the user can change the month from UI
    hisData1 = list(historyData.objects.values())
    allD1 = pandas.DataFrame(hisData1)
    allD = allD1.loc[allD1['userID1']==request.user.id]#fetching data for current user
    sellD1 = allD.loc[allD['historyFor']=='selling']
        
    monthDate = {'January':31,'February':28,'March':31,'April':30,'May':31,'June':30,'July':31,'August':31,'September':30,'October':31,'November':30,'December':31}
    monthNum = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
    if monthInput == 'currentMonth':
        month=timeFilter('month')
        for key,value in monthNum.items():#for filtering the current month number using the timefilter
            if value == int(month):
                monthInput = key
                break
    
    sellD = sellD1.loc[sellD1['month']==int(monthNum[monthInput])]
    sellByD = sellD.loc[sellD['day']==int(timeFilter('day'))]#filtering the selling days
    totalP = sellByD[['C_price']].to_dict('list')#filtering the sell price list using the days
    N_Q = sellD[['item_name','Oquantity']].to_dict('list')#for sell rate
    # N_Q = sellD[['item_marker']].to_dict('list')#for detecting marker
    sell_date = sellD[['day']].to_dict(orient='list')#filtering for day list
    sell_dates = sellDate(sell_date['day'])#fetch the days list and deleting the duplicated days
    sellNames = sellDate(N_Q['item_name'])
    sellNames.sort()
    sellQuantity = []#for today UI
    profitList = []#for today UI
    #--testing for item marker--
    markerList1 = sellD[['item_marker']].to_dict('list')
    markerList = markerList1['item_marker']
    profit_withMarker = []
    quantity_withMarker = []
    item_nameWM = []
    
    for i in np.unique(markerList):
        sellN = mainData.objects.values()
        sell_names_wm = pandas.DataFrame(sellN)
        sellNames_wm = sell_names_wm.loc[sell_names_wm['id']==i]
        namesWM = sellNames_wm[['item_name']].to_dict('list')
        namesWM = dRemover(namesWM['item_name'])
        print('ids',namesWM)
        markerMonth = sellD.loc[sellD['item_marker']==i]
        sellPQlist = markerMonth[['Opost_price','Oquantity']].to_dict('list')#for quantity and price with marker
        sellQList = sum(sellPQlist['Oquantity'])
        sellPList = sum(sellPQlist['Opost_price'])
        profit_withMarker.append(sellPList)
        quantity_withMarker.append(sellQList)
        item_nameWM.append(namesWM[0])

    #--testing for item marker--
    #---------for sell rate per day---------
    perdayS = sellD[['C_price']].to_dict('list')
    perday = perdayS['C_price']
    sellRate_perDay = sum(perday)/monthDate[monthInput]
    #---------fro sell rate per day end------
    for j in sellNames:#for today UI
        nameS = sellD.loc[sellD['item_name']==j]
        nameS = nameS[['Oquantity','Opost_price']].to_dict('list')
        sellQuantity.append(sum(nameS['Oquantity']))
        profitList.append(sum(nameS['Opost_price']))
    totalBy_dates = []#for price graph line
    totalPp_dates = []
    rMonth = [x for x in range(1,int(monthDate[monthInput])+1)]
    for i in rMonth:#for total price graph line and post price line
        if i in sell_dates:
            forCurrentD = sellD.loc[sellD['day']==i]
            #for total price
            totalP = forCurrentD[['C_price']].to_dict(orient='list')
            totalP = sum(totalP['C_price'])
            totalBy_dates.append(totalP)
            #for post price
            totalPp = forCurrentD[['Opost_price']].to_dict('list')
            totalPp = sum(totalPp['Opost_price'])
            totalPp_dates.append(totalPp)
        else:
            totalBy_dates.append(0)
            totalPp_dates.append(0)
    graphData = []
    for i in range(len(item_nameWM)):
        exDict = {
                  'quantity':quantity_withMarker[i],
                  'profitWM':profit_withMarker[i],
                  'nameWM':item_nameWM[i],
                  }
        graphData.append(exDict)

    if request.method == 'POST':#for daySelling
        inputTime = request.POST['date']
        sellD2 = sellD1.loc[sellD1['date']==inputTime]
        markerList1 = sellD2[['item_marker']].to_dict('list')
        markerList = markerList1['item_marker']
        profit_withMarker = []
        quantity_withMarker = []
        item_nameWM = []
        
        for i in np.unique(markerList):
            
            sellN = mainData.objects.values()
            sell_names_wm = pandas.DataFrame(sellN)
            sellNames_wm = sell_names_wm.loc[sell_names_wm['id']==i]
            namesWM = sellNames_wm[['item_name']].to_dict('list')
            namesWM = dRemover(namesWM['item_name'])
            
            markerMonth = sellD2.loc[sellD2['item_marker']==i]
            sellPQlist = markerMonth[['Opost_price','Oquantity']].to_dict('list')#for quantity and price with marker
            sellQList = sum(sellPQlist['Oquantity'])
            sellPList = sum(sellPQlist['Opost_price'])
            profit_withMarker.append(sellPList)
            quantity_withMarker.append(sellQList)
            item_nameWM.append(namesWM[0])
        print(item_nameWM)
        graphData1 = []
        for i in range(len(item_nameWM)):
            exDict = {
                    'quantity':quantity_withMarker[i],
                    'profitWM':profit_withMarker[i],
                    'nameWM':item_nameWM[i],
                    }
            graphData1.append(exDict)
        return render(request,'graph.html',{
            'sell_dates':dumps(rMonth),
            'sell_amounts':dumps(totalBy_dates),
            'storeName':request.user.username,
            'sellProfit':totalPp_dates,
            'month':monthInput,
            'totalProfit':sum(profitList),
            #'totalSell':sum(totalBy_dates),
            'graphData':graphData1,
            'perDay':request.POST['date'],
    })
    return render(request,'graph.html',{
        'sell_dates':dumps(rMonth),
        'sell_amounts':dumps(totalBy_dates),
        'storeName':request.user.username,
        'sellProfit':totalPp_dates,
        'month':monthInput,
        'totalProfit':sum(profitList),
        #'totalSell':sum(totalBy_dates),
        'graphData':graphData,
    })

@login_required(login_url='login')
def home(request):
    #fetching all the data from database in list and dict form
    storage_data = list(mainData.objects.values())
    userId = request.user.id
    storage_dataC = pandas.DataFrame(storage_data)
    storage_dataC = storage_dataC.loc[storage_dataC['userID']==userId]
    marker_list = storage_dataC[['id']].to_dict(orient='list')
    name_list = storage_dataC[['item_name']].to_dict(orient='list')
    price_list = storage_dataC[['price']].to_dict(orient='list')
    itemName_list = name_list['item_name']
    itemPrice_list = price_list['price']
    itemMarker_list = marker_list['id']
    print(itemName_list)
    user_name = request.user.username
    return render(request,'homeCal.html',{
            'storeName':user_name,
            'name_list':dumps(itemName_list),
            'value_list':dumps(itemPrice_list),
            'marker_list':dumps(itemMarker_list)
    })
@login_required(login_url='login')
def data(request):
    storage_data = mainData.objects.values()
    user_id = request.user.id
    pandasD = pandas.DataFrame(storage_data)
    cleaned_data1 = pandasD.loc[pandasD['userID']==user_id]
    #with pandas sorted function
    sorted_Data = cleaned_data1.sort_values("item_name")
    s_cleaned_data = sorted_Data.to_dict('list')#extracted user data
    s_name = s_cleaned_data['item_name']
    s_quantity = s_cleaned_data['quantity']
    s_price = s_cleaned_data['price']
    s_post_price = s_cleaned_data['post_price']
    s_id = s_cleaned_data['id']
    s_data = []
    numberL = [x for x in range(1,len(s_name)+1)]
    for i in range(len(s_name)):
        exDict = {'number':numberL[i],
            'name':s_name[i],
            'price':s_price[i],
            'quantity':s_quantity[i],
            'post_price':s_post_price[i],
            'id':s_id[i]
        }
        s_data.append(exDict)
    print('-----this is sData')
    print(s_data)
    #----without pandas frame----
    # cleaned_data = cleaned_data1.to_dict('list')
    # itemNames = cleaned_data['item_name']
    # numberL = [x for x in range(1,len(itemNames)+1)]
    # itemNames.sort()
    # quantityL = []
    # priceL = []
    # postPriceL = []
    # idL = []
    # for i in itemNames:
    #     sName =  cleaned_data1.loc[cleaned_data1['item_name']==i]
    #     sName = sName.to_dict('list')
    #     quantityL.append(sName['quantity'][0])
    #     priceL.append(sName['price'][0])
    #     postPriceL.append(sName['post_price'][0])
    #     idL.append(sName['id'][0])
    # lastData = []
    # for i in range(len(itemNames)):
    #     exDict = {'number':numberL[i],
    #         'name':itemNames[i],
    #         'price':priceL[i],
    #         'quantity':quantityL[i],
    #         'post_price':postPriceL[i],
    #         'id':idL[i]
    #     }
    #     lastData.append(exDict)
    # print('-------> this is last Data')
    # print(lastData)
    return render(request,'Data.html',{
            'dataList':s_data,
            'storeName':request.user.username,
            'jsNum':dumps(numberL)
    })

def getStart(request):
    return render(request,'getStart.html')

def register_user(request):
    allUser = userInfo.objects.values()
    allUser = pandas.DataFrame(allUser)
    if len(allUser)>0:
        all_userNames = allUser[['user_name']].to_dict('list')
    else:
        all_userNames = {'user_name':[]}
    userName = request.POST['user_name']
    email_phone = request.POST['email_phone']
    password = request.POST['pswd']
    city = request.POST['city']
    township = request.POST['township']
    ward = request.POST['ward']
    street = request.POST['street']
    if userName in all_userNames['user_name'] :
        messages.add_message(request, messages.INFO, 'ဤနာမည်ကိုသုံး၍မရတော့ပါ အခြားပြောင်းရွေးပေးပါ')
        return render(request,'register.html',{
            'email':email_phone,
            'userName':'',
            'city':city,
            'township':township,
            'ward':ward,
            'street':street,
        })
    if password != request.POST['conPass']:
        message1 = 'လှူ့ဝှက်စာလုံး နှစ်ခုကိုက်ညီမှုမရှိပါ'
        messages.add_message(request, messages.INFO, 'လှူ့ဝှက်စာလုံး နှစ်ခုကိုက်ညီမှုမရှိပါ')
        return render(request,'register.html',{
            'email':email_phone,
            'userName':userName,
            'city':city,
            'township':township,
            'ward':ward,
            'street':street,
        })
    if len(password)<8:
        message1 = 'password နှစ်ခုကိုက်ညီမှုမရှိပါ'
        messages.add_message(request, messages.INFO, 'လှူ့ဝှက်စာလုံး အနည်းဆုံး၈လုံးထည့်ပေးပါ')
        return render(request,'register.html',{
            'email':email_phone,
            'userName':userName,
            'city':city,
            'township':township,
            'ward':ward,
            'street':street,
        })

    user = User.objects.create_user(userName,email_phone,password)
    user.save()
    user = authenticate(request, username=userName, password=password)
    login(request,user)
    userInfoA = userInfo(userPswd = password,user_name = userName,userId = request.user.id,email = email_phone,city = city,township = township,ward = ward,street=street)
    userInfoA.save()
    mainD = data = mainData(userID = request.user.id,item_name = 'l',quantity = 0,price=0,post_price=0)
    mainD.save()
    return redirect('home')
    # if int(inputCode) == int():
    #     try:
    #         user = User.objects.create_user(userName,email_phone,password)
    #         user.save()
    #         user = authenticate(request, username=userName, password=password)
    #         login(request,user)
    #         userInfoA = userInfo(user_name = userName,userId = request.user.id,email = email_phone,city = city,township = township,ward = ward,street=street)
    #         userInfoA.save()
    #         mainD = data = mainData(userID = request.user.id,item_name = 'l',quantity = 0,price=0,post_price=0)
    #         mainD.save()
    #         return redirect('home')
    #     except Exception as err:
    #         messages.add_message(request, messages.INFO, str(err))
    #         return render(request,'register.html',{
    #             'email':email_phone,
    #             'userName':userName,
    #             'password':password,
    #             'city':city,
    #             'township':township,
    #             'ward':ward,
    #             'street':street,
    #         })
    # messages.add_message(request, messages.INFO, 'The code is not correct')
    # return render(request,'emailCon.html',{
    #         'email':email_phone,
    #         'userName':userName,
    #         'password':password,
    #         'city':city,
    #         'township':township,
    #         'ward':ward,
    #         'street':street,
    #     })

def login_user(request):
    username = request.POST['username']
    password = request.POST['pswd']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.add_message(request, messages.INFO, 'Oopsss!!! your user name or password is not correct')
        return redirect('login')
def logout_user(request):
    logout(request)
    return redirect('login')

def addData(request):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    storage_data = list(mainData.objects.values())
    user_id = request.user.id
    cleaned_data1 = pandas.DataFrame(storage_data)
    cleaned_data = cleaned_data1.loc[cleaned_data1['userID']==user_id]
    itemNames = cleaned_data[['item_name']].to_dict(orient='list')
    item_name = request.POST['item_name']
    quantity = request.POST['quantity']
    price = request.POST['price']
    post_price = request.POST['post_price']
    # if item_name in itemNames['item_name']:
    #     updateData = mainData.objects.get(item_name = item_name)
    #     historyData_u = historyData(userID1=user_id,actionTime = current_time,O_price=updateData.price,C_price=price,Opost_price=updateData.post_price,Cpost_price=post_price,date=date.today(),Oquantity=updateData.quantity,Cquantity=quantity,item_name=item_name,historyFor='updating')
    #     historyData_u.save()
    #     updateData.quantity = quantity
    #     updateData.price = price
    #     updateData.post_price = post_price
    #     updateData.save()
    # else:
    user_id = request.user.id
    item_name = request.POST['item_name']
    quantity = request.POST['quantity']
    price = request.POST['price']
    post_price = request.POST['post_price']
    data = mainData(userID = user_id,item_name = item_name,quantity = quantity,price=price,post_price=post_price)
    historyData_a = historyData(userID1=user_id,O_price=price,actionTime = current_time,Opost_price=post_price,date=date.today(),Oquantity=quantity,item_name=item_name,historyFor='adding')
    historyData_a.save()
    data.save()
    return redirect('data')

def dataDel(request):
    now = datetime.now()
    idNum = request.POST['idNum']
    current_time = now.strftime("%H:%M:%S")
    dataFor_del = mainData.objects.get(id=idNum)
    delHistory = historyData(userID1=request.user.id,O_price=dataFor_del.price,Opost_price=dataFor_del.post_price,actionTime = current_time,date=date.today(),Oquantity=dataFor_del.quantity,item_name=dataFor_del.item_name,historyFor='deleting')
    delHistory.save()
    dataFor_del.delete()
    return redirect('data')

def dataToEdit(request,id):
    dataFor_ed = mainData.objects.get(id=id)
    listT = [dataFor_ed.item_name,dataFor_ed.quantity,dataFor_ed.price,dataFor_ed.post_price]
    print(dataFor_ed.item_name)
    # return render(
    #     request,'dataToEd.htm',{
    #         'dataToE':dumps(listT)
    #     }
    # )
    return render(
        request,'dataToEd.html',{
            # 'item_name':str(dataFor_ed.item_name),
            'quantity':dataFor_ed.quantity,
            'price':dataFor_ed.price,
            'post_price':dataFor_ed.post_price,
            'dataId':id,
            'dataToE':dumps(listT)
        }
    )
def dataToFill(request,id):
    dataFor_fill = mainData.objects.get(id=id)
    listT = [dataFor_fill.item_name,dataFor_fill.quantity,dataFor_fill.price,dataFor_fill.post_price]
    # print(dataFor_ed.item_name)
    # return render(
    #     request,'dataToEd.htm',{
    #         'dataToE':dumps(listT)
    #     }
    # )
    return render(
        request,'fillData.html',{
            'item_name5':(dataFor_fill.item_name),
            'quantity':dataFor_fill.quantity,
            'price':dataFor_fill.price,
            'post_price':dataFor_fill.post_price,
            'dataId':id,
            'dataToE':dumps(listT)
        }
    )
def dataFill(request):
    dataId = request.POST['dataId']
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    dataFor_fill = mainData.objects.get(id=dataId)
    #note as we import new quantity the current quantity and the import quantity is to sum...
    previous_quantity = dataFor_fill.quantity
    added_quantity = request.POST['quantity']
    dataFor_fill.quantity+=int(request.POST['quantity'])
    dataFor_fill.save()
    edithistory = historyData(
        userID1=request.user.id,
        actionTime = current_time,
        O_price=request.POST['price1'],
        Opost_price=request.POST['post_price1'],
        date=date.today(),
        Oquantity=request.POST['quantity'],
        item_name=request.POST['item_name1'],
        historyFor='adding',
        )
    edithistory.save()
    return redirect('data')

def dataEdit(request):
    dataId = request.POST['dataId']
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    dataFor_edit = mainData.objects.get(id=dataId)
    dataFor_edit.item_name = request.POST['item_name']
    dataFor_edit.price = request.POST['price']
    # dataFor_edit.quantity = request.POST['quantity']
    dataFor_edit.post_price = request.POST['post_price']
    dataFor_edit.save()
    edithistory = historyData(
        userID1=request.user.id,
        actionTime = current_time,
        O_price=request.POST['price1'],
        C_price=request.POST['price'],
        Opost_price=request.POST['post_price1'],
        Cpost_price=request.POST['post_price'],
        date=date.today(),
        # Oquantity=request.POST['quantity1'],
        # Cquantity=request.POST['quantity'],
        item_name=request.POST['item_name1'],
        Citem_name=request.POST['item_name'],
        historyFor='updating',
        )
    edithistory.save()
    return redirect('data')


def updateExData(request):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    now1 = str(date.today())
    now1 = now1.split('-')
    currentDay = now1[2]
    currentMonth = now1[1]
    currentYear = now1[0]
    if request.POST['quantity'] != '' and request.POST['item_name'] !='':
        allData = list(mainData.objects.values())
        user_id = request.user.id
        cleaned_data =pandas.DataFrame(allData)
        cleaned_datas = cleaned_data.loc[cleaned_data['userID']==user_id]
        input_quantity = request.POST['quantity']
        input_names = request.POST['item_name']
        inputQuantity = lister(input_quantity)
        inputNames = lister(input_names)
        idList = []
        existedQList = []
        for i in inputNames:
            fQ = cleaned_datas.loc[cleaned_datas['item_name']==i]
            QandId = fQ.to_dict(orient='list')
            existedQList.append(QandId['quantity'][0])
            idList.append(QandId['id'][0])
        for i in range(len(inputNames)):
            updateD = mainData.objects.get(id=idList[i])
            def sumP(price,quantity,loopI):
                result = 0
                for j in range(int(quantity[loopI])):
                    result +=price
                return result
            def find_marker(itemName):
                marker = mainData.objects.get(item_name=itemName)
                markerId  = marker.id
                return markerId
            print('this is id',find_marker(inputNames[i]))
            #find marker function is to find item's original id,fixing duplicate profits and item names
            historyData_e = historyData(item_marker=int(find_marker(inputNames[i])),userID1=user_id,month = currentMonth,year = currentYear,day = currentDay,O_price=updateD.price,C_price = sumP(updateD.price,inputQuantity,i),Opost_price=sumP(updateD.post_price,inputQuantity,i),date=date.today(),Oquantity=inputQuantity[i],item_name=inputNames[i],historyFor='selling',actionTime=current_time)
            historyData_e.save()
            updateD.quantity = int(existedQList[i])-int(inputQuantity[i])
            updateD.save()
    return redirect('home')

# def sendMail(request):
#     email_phone = request.POST['email_phone']
#     user_name = request.POST['user_name']
#     password = request.POST['pswd']
#     confirmPass = request.POST['conPass']
#     city = request.POST['city']
#     township = request.POST['township']
#     ward = request.POST['ward']
#     street = request.POST['street']
#     allUser = userInfo.objects.values()
#     allUser = pandas.DataFrame(allUser)

    # if len(allUser)>0:
    #     emails = allUser[['email']].to_dict('list')
    #     all_userNames = allUser[['user_name']].to_dict('list')
    # else:
    #     emails = {'email':[]}
    #     all_userNames = {'user_name':[]}
    
#     if user_name in all_userNames['user_name']:
#         messages.add_message(request, messages.INFO, 'user name is taken')
#         return render(request,'register.html',{
#             'email':email_phone,
#             'userName':'user name',
#             'city':city,
#             'township':township,
#             'ward':ward,
#             'street':street,
#         })
#     elif email_phone in emails['email']:
#         messages.add_message(request, messages.INFO, 'email already exist try another one')
#         return render(request,'register.html',{
#             'userName':user_name,
#             'city':city,
#             'email':'email',
#             'township':township,
#             'ward':ward,
#             'street':street,
#         })
#     elif password != confirmPass:
#         messages.add_message(request, messages.INFO, 'the passwords are not match')
#         return render(request,'register.html',{
#             'email':email_phone,
#             'userName':user_name,
#             'city':city,
#             'township':township,
#             'ward':ward,
#             'street':street,
#         })
#     code = code_generator(4)
#     # global systemCode
#     # systemCode = code
#     send_mail(
#         'Sending email verification code',
#         code,
#         'mesutkee8@gmail.com',
#         [f'{email_phone}'],
#     )
#     return render(request,'emailCon.html',{
#         'email':email_phone,
#         'user_name':user_name,
#         'password':password,
#         'city':city,
#         'township':township,
#         'ward':ward,
#         'street':street,
#     })

def reset_password(request):
    inputC = request.POST['codeSent']
    if int(inputC)==int():
        try:
            user_name = request.POST['userName']
            new_pswd = request.POST['passWord']
            u = User.objects.get(username=user_name)
            u.set_password(new_pswd)
            u.save()
            login(request,u)
            return redirect('home')
        except:
            #messages.add_message(request, messages.INFO, 'user name doesnt exist please enter the correct user name')
            return render(request,'resetPswd.html',{
                'error':'user name doesnt exist please enter the correct user name',
            })
    else:
        #messages.add_message(request, messages.INFO, 'the code is not correct')
        return render(request,'resetPswd.html',{'error':'the code is not correct'})
def idUser(request):
    return render(request,'identifyUser.html')

def addPswd(request):
    inputName = request.POST['userName']
    userData1 = userInfo.objects.values()
    userData = pandas.DataFrame(userData1)
    usernames = userData[['user_name']].to_dict('list')
    if inputName in usernames['user_name']:
        checkEmail = userInfo.objects.get(user_name=inputName)
        code = code_generator(4)
        # global systemCode
        # systemCode = code
        user_mail = checkEmail.email
        print(user_mail)
        print(code)
        send_mail(
            'Sending email verification code',
            code,
            'mesutkee8@gmail.com',
            [f'{user_mail}'],
        )
        return render(request,'resetPswd.html')
    else:
        return render(request,'identifyUser.html',{'error':'There is no such user name'})

def dataSave(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer,pagesize='letter')

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    textBox = p.beginText()
    textBox.setFont('Helvetica',14)
    textLines = [
        'this is one',
        'this is two',
        'this is three',
    ]
    for tline in textLines:
        textBox.textLines(tline)
    p.drawText(textBox)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

def csv_data(request):
    storage_data = mainData.objects.values()
    user_id = request.user.id
    pandasD = pandas.DataFrame(storage_data)
    cleaned_data1 = pandasD.loc[pandasD['userID']==user_id]
    sorted_cleanData = cleaned_data1.sort_values('item_name')
    cleaned_data = sorted_cleanData.to_dict('list')
    itemNames = cleaned_data['item_name']
    itemQ = cleaned_data['quantity']
    itemP = cleaned_data['price']
    itemPp = cleaned_data['post_price']

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="StoreData.csv"'},
    )
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['စဉ်','ပစ္စည်းအမည်', 'အရေအတွက်', 'တန်ဖိုး', 'ဈေးတင်နှုန်း'])
    for i in range(len(itemNames)):
        writer.writerow([i+1,itemNames[i],itemQ[i], itemP[i], itemPp[i]])

    return response

def devContact(request):
    id = request.user.id
    data = mainData.objects.values()
    item_names = []
    for i in data:
        if data.id_serializer(id) is not None:
            item_names.append(data.id_serializer(id))

    return render(request,'developerContact.html',{'itemNames':item_names})

def del_op(request,id):
    return render(request,'delOption.html',{'id':id})

