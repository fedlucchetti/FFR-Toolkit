from bin import FFR
import json, csv, sys
import numpy as np
import matplotlib.pyplot as plt
######################################
path2avgjson = sys.argv[1]
######################################
ffr = FFR.FFR()
######################################
axsize            = 18
patientmarkersize = 10
######################################
with open(path2avgjson) as data_file: data = json.load(data_file)
patient_number = int(data["MetaData"]["Patient"]["Number"])
f1             = int(data["MetaData"]["Stimulus"]["F1"])
f2             = int(data["MetaData"]["Stimulus"]["F2"])
level          = int(data["MetaData"]["Stimulus"]["Level[dB]"])
print(f1,f2,f2-f1,2*f1-f2)
try:
    ear            = data["MetaData"]["Patient"]["Oreille"]
except:
    ear            = data["MetaData"]["Patient"]["Oreille "]
######################################






def get_metric(SC,channel):
    with open(path2avgjson) as data_file: data = json.load(data_file)
    on   =  float(data["FFR"]['Channel-' +channel][SC]["Analysis"]["Latency"])
    off   = float(data["FFR"]['Channel-'+channel][SC]["Analysis"]["Lenght"])
    fc    = float(data["FFR"]['Channel-'+channel][SC]["Analysis"]["Frequency"])
    return on, off, fc



EFRVdata = get_metric("EFR","V")
EFRHdata = get_metric("EFR","H")

CDTVdata = get_metric("CDT","V")
CDTHdata = get_metric("CDT","H")

F1Hdata = get_metric("F1","H")
F1Vdata = get_metric("F1","V")

F2Vdata = get_metric("F2","V")
F2Hdata = get_metric("F2","H")

latEFRV = [EFRVdata[0],EFRVdata[1]]
latEFRH = [EFRHdata[0],EFRHdata[1]]
latF1H  = [max(0,F1Hdata[0]),F1Hdata[1]]
latF1V  = [F1Vdata[0],F1Vdata[1]]
latF2H  = [max(0,F2Hdata[0]),F2Hdata[1]]
latF2V  = [F2Vdata[0],F2Vdata[1]]
latCDTH = [CDTHdata[0],CDTHdata[1]]
latCDTV = [CDTVdata[0],CDTVdata[1]]
title = "20" + str(patient_number) + "\n EFR" + str(int(EFRVdata[2]))+ " " + str(level) + "dB SPL " + ear + "\n"

name,number,date,stim,_,level,path2json,code = ffr.list_all()
# print(path2json)
listpath = np.array(path2json)





def CDT(fc = 440):
    latencyH_list  = []
    latencyV_list  = []
    lengthH_list  = []
    lengthV_list  = []
    SC = 'CDT'
    for path in path2json:
        with open(path) as data_file:
            data = json.load(data_file)
        _latencyV   = data["FFR"]["Channel-V"][SC]["Analysis"]["Latency"]
        _latencyH   = data["FFR"]["Channel-H"][SC]["Analysis"]["Latency"]
        # print(data["FFR"]["Channel-V"][SC]["Analysis"])
        _lengthV    = data["FFR"]["Channel-V"][SC]["Analysis"]["Lenght"]
        _lengthH    = data["FFR"]["Channel-H"][SC]["Analysis"]["Lenght"]
        _frequency  = data["FFR"]["Channel-V"][SC]["Analysis"]["Frequency"]
        if _latencyV!="" and  _latencyH!="" and _frequency!="":
            if float(_frequency) in range(fc-20,fc+20):
                if float(_latencyV) > 6 and float(_latencyV)<15  and float(_latencyH) > 4 and float(_latencyH)<15 :
                    latencyV_list.append([float(_latencyV)-5])
                    latencyH_list.append([float(_latencyH)-5])

        if _lengthV!="" and  _lengthH!="" and _frequency!="":
            if float(_frequency) in range(fc-20,fc+20):
                if float(_lengthV) > 50 and float(_lengthV)<65  and float(_lengthH) > 50 and float(_lengthH)<65 :
                    lengthH_list.append([float(_lengthH)-2])
                    lengthV_list.append([float(_lengthV)])


    latencyV_list = np.array(latencyV_list)
    latencyH_list = np.array(latencyH_list)
    lengthH_list  = np.array(lengthH_list)
    lengthV_list  = np.array(lengthV_list)
    latencyV_list = latencyV_list.reshape(len(latencyV_list))
    latencyH_list = latencyH_list.reshape(len(latencyH_list))
    lengthH_list  = lengthH_list.reshape(len(lengthH_list))
    lengthV_list  = lengthV_list.reshape(len(lengthV_list))
    # fig1, ax = plt.subplots(2)
    plt.subplot(2, 1, 1)
    latdata = [latencyH_list,latencyV_list]
    print("latencyH_list shape",np.shape(latencyH_list))
    print("latencyV_list shape",np.shape(latencyV_list))
    print("latdata shape",np.shape(latdata))
    plt.title(title + "  --- " + SC + " " + str(fc) + " Hz ---  ")
    plt.boxplot(latdata,labels=[SC+'-H',SC+'-V'])
    if latCDTH[0]!=0: plt.plot(1,latCDTH[0],'b s',markersize=patientmarkersize,label='Patient')
    if latCDTV[0]!=0: plt.plot(2,latCDTV[0],'b s',markersize=patientmarkersize)
    plt.ylabel('Onset latency [ms]',fontsize=axsize)
    plt.xticks(ticks=[1,2],labels=['',''],fontsize=axsize)
    plt.yticks(fontsize=axsize)
    plt.xlim([0,3])
    plt.grid()
    plt.legend()

    plt.subplot(2, 1, 2)
    lengthdata = [lengthH_list,lengthV_list]
    print("lengthdata shape",np.shape(lengthdata))
    plt.boxplot(lengthdata,labels=[SC+'-H',SC+'-V'])
    if latCDTH[1]!=0: plt.plot(1,latCDTH[1],'b s',markersize=patientmarkersize)
    if latCDTV[1]!=0: plt.plot(2,latCDTV[1],'b s',markersize=patientmarkersize)
    plt.plot([0,3],[57,57],'r-',alpha=0.1,linewidth=8,label='stimulus duration')
    plt.ylabel('Response duration [ms]',fontsize=axsize)
    plt.xticks(ticks=[1,2],labels=[SC+'-H',SC+'-V'],fontsize=axsize)
    plt.ylim([20,60])
    plt.yticks(fontsize=axsize)
    plt.grid()
    plt.legend()
    plt.show()

def EFR(fc=220):
    latencyH_list  = []
    latencydiff_list  = []
    lengthH_list  = []
    lengthV_list  = []
    SC = 'EFR'
    for path in path2json:
        with open(path) as data_file:
            data = json.load(data_file)
        _latencyV   = data["FFR"]["Channel-V"][SC]["Analysis"]["Latency"]
        _latencyH   = data["FFR"]["Channel-H"][SC]["Analysis"]["Latency"]
        # print(data["FFR"]["Channel-V"][SC]["Analysis"])
        _lengthV    = data["FFR"]["Channel-V"][SC]["Analysis"]["Lenght"]
        _lengthH    = data["FFR"]["Channel-H"][SC]["Analysis"]["Lenght"]
        _frequency  = data["FFR"]["Channel-V"][SC]["Analysis"]["Frequency"]
        if _latencyV!="" and  _latencyH!="" and _frequency!="":
            if float(_frequency) in range(fc-20,fc+20):
                if float(_latencyV) > 6 and float(_latencyV)<15  and float(_latencyH) > 4 and float(_latencyH)<15 :
                    latencydiff_list.append([float(_latencyV)-float(_latencyH)])
                    latencyH_list.append([float(_latencyH)-5])

        if _lengthV!="" and  _lengthH!="" and _frequency!="":
            if float(_frequency) in range(fc-20,fc+20):
                if float(_lengthV) > 50 and float(_lengthV)<58  and float(_lengthH) > 50 and float(_lengthH)<58 :
                    lengthH_list.append([float(_lengthH)])
                    lengthV_list.append([float(_lengthV)+1.5])


    latencydiff_list = np.array(latencydiff_list)
    latencyH_list = np.array(latencyH_list)
    lengthH_list  = np.array(lengthH_list)
    lengthV_list  = np.array(lengthV_list)
    latencydiff_list = latencydiff_list.reshape(len(latencydiff_list))
    latencyH_list = latencyH_list.reshape(len(latencyH_list))
    lengthH_list  = lengthH_list.reshape(len(lengthH_list))
    lengthV_list  = lengthV_list.reshape(len(lengthV_list))
    # fig1, ax = plt.subplots(2)
    plt.subplot(2, 1, 1)
    latdata = [latencyH_list,latencydiff_list]
    print("latencyH_list shape",np.shape(latencyH_list))
    print("latencyV_list shape",np.shape(latencydiff_list))
    print("latdata shape",np.shape(latdata))
    plt.title(title + "  --- " + SC + " " + str(fc) + " Hz ---  ")
    plt.boxplot(latdata,labels=[SC+'-H',SC+'Diff V-H'])
    if latEFRH[0]!=0: plt.plot(1,latEFRH[0],'b s',alpha=0.4,markersize=patientmarkersize,label='Patient')
    if latEFRV[0]!=0: plt.plot(2,latEFRV[0]-latEFRH[0],'b s',alpha=0.4,markersize=patientmarkersize)
    plt.ylabel('Onset latency [ms]',fontsize=axsize)
    plt.xticks(ticks=[1,2],labels=[SC+'-H',SC+' $\Delta$ V-H'],fontsize=axsize)
    plt.yticks(fontsize=axsize)
    plt.xlim([0,3])
    plt.grid()
    plt.legend()

    plt.subplot(2, 1, 2)
    lengthdata = [lengthH_list,lengthV_list]
    print("lengthdata shape",np.shape(lengthdata))
    plt.boxplot(lengthdata,labels=[SC+'-H',SC+'Diff V-H'])
    if latEFRH[1]!=0: plt.plot(1,latEFRH[1],'b s',alpha=0.4,markersize=patientmarkersize)
    if latEFRV[1]!=0: plt.plot(2,latEFRV[1],'b s',alpha=0.4,markersize=patientmarkersize)
    plt.plot([0,3],[57,57],'r-',alpha=0.1,linewidth=8,label='stimulus duration')
    plt.ylabel('Response duration [ms]',fontsize=axsize)
    plt.ylim([50,60])
    plt.xticks(ticks=[1,2],labels=[SC+'-H',SC+'-V'],fontsize=axsize)
    plt.yticks(fontsize=axsize)
    plt.grid()
    plt.legend()
    plt.show()

def F1F2(f1 = 651, f2 = 868):
    latencyF1_list  = []
    latencyF2_list  = []
    lengthF1_list  = []
    lengthF2_list  = []
    SC1 = 'F1'
    SC2 = 'F2'
    for path in path2json:
        with open(path) as data_file:
            data = json.load(data_file)
        _latencyF1   = data["FFR"]["Channel-H"][SC1]["Analysis"]["Latency"]
        _latencyF2   = data["FFR"]["Channel-H"][SC2]["Analysis"]["Latency"]
        # print(data["FFR"]["Channel-V"][SC]["Analysis"])
        _lengthF1    = data["FFR"]["Channel-H"][SC1]["Analysis"]["Lenght"]
        _lengthF2    = data["FFR"]["Channel-H"][SC2]["Analysis"]["Lenght"]
        _frequency1  = data["FFR"]["Channel-H"][SC1]["Analysis"]["Frequency"]
        _frequency2  = data["FFR"]["Channel-H"][SC2]["Analysis"]["Frequency"]
        if _latencyF1!="" and  _latencyF2!="" and _frequency1!="" and _frequency2!="":
            if float(_frequency1) in range(f1-20,f1+20) and float(_frequency2) in range(f2-20,f2+20)  :
                if float(_latencyF1) > 5 and float(_latencyF1)<10  and float(_latencyF2) > 5 and float(_latencyF2)<10 :
                    latencyF1_list.append([float(_latencyF1)-5])
                    latencyF2_list.append([float(_latencyF2)-5])

        if _lengthF1!="" and  _lengthF2!="" and _frequency1!="" and _frequency2!="":
            if float(_frequency1) in range(f1-20,f1+20) and float(_frequency2) in range(f2-20,f2+20)  :
                if float(_lengthF1) > 50 and float(_lengthF1)<58  and float(_lengthF2) > 50 and float(_lengthF2)<58 :
                    lengthF1_list.append([float(_lengthF1)])
                    lengthF2_list.append([float(_lengthF2)])


    latencyF1_list = np.array(latencyF1_list)
    latencyF2_list = np.array(latencyF2_list)
    lengthF1_list  = np.array(lengthF1_list)
    lengthF2_list  = np.array(lengthF2_list)
    latencyF1_list = latencyF1_list.reshape(len(latencyF1_list))
    latencyF2_list = latencyF2_list.reshape(len(latencyF2_list))
    lengthF1_list  = lengthF1_list.reshape(len(lengthF1_list))
    lengthF2_list  = lengthF2_list.reshape(len(lengthF2_list))
    # fig1, ax = plt.subplots(2)
    plt.subplot(2, 1, 1)
    latdata = [latencyF1_list,latencyF2_list]

    plt.title(title + "  --- " + SC1+'-H ' +SC2 + "-H  " + str(662) + " & "+str(882) + " Hz ---  ")
    plt.boxplot(latdata,labels=[SC1+'-H',SC1+'H'])
    if latF1H[0]!=0: plt.plot(1,latF1H[0],'b s',alpha=0.4,markersize=patientmarkersize,label='Patient')
    if latF2H[0]!=0: plt.plot(2,latF2H[0],'b s',alpha=0.4,markersize=patientmarkersize)
    plt.ylabel('Onset latency [ms]',fontsize=axsize)
    plt.xticks(ticks=[1,2],labels=['',''],fontsize=axsize)
    plt.yticks(fontsize=axsize)
    plt.xlim([0,3])
    plt.grid()
    plt.legend()

    plt.subplot(2, 1, 2)
    lengthdata = [lengthF1_list,lengthF2_list]
    print("lengthdata shape",np.shape(lengthdata))
    plt.boxplot(lengthdata,labels=[SC1+'-H',SC2+'-H'])
    if latF1H[1]!=0: plt.plot(1,latF1H[1],'b s',alpha=0.4,markersize=patientmarkersize)
    if latF2H[1]!=0: plt.plot(2,latF2H[1],'b s',alpha=0.4,markersize=patientmarkersize)
    plt.plot([0,3],[57,57],'r-',alpha=0.1,linewidth=8,label='stimulus duration')
    plt.ylim([54,60])
    plt.ylabel('Response duration [ms]',fontsize=axsize)
    plt.xticks(ticks=[1,2],labels=[SC1+'-H',SC2+'-H'],fontsize=axsize)
    plt.yticks(fontsize=axsize)
    plt.grid()
    plt.legend()
    plt.show()

# if __name__=="__main__":
F1F2(f1,f2)
EFR(f2-f1)
CDT(2*f1-f2)
