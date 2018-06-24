import matplotlib.pyplot as plt
import pandas as pd

import seaborn.apionly as sns
import numpy as np


def save(filename, param, metric):
    return plt.savefig("plot_" + filename + "_" + param + "_" + metric + ".png")


def ultimateGraphCreator(filename, someParameters, someMetrics):
    data = pd.read_csv(filename, index_col=False)
    augmentTicksIdlePercent(data)
    data['lazyTicks'] = (data['nrOfLazy'] / data['numTaxis']) * data['ticks']
    data['ticksNonlazyTaxisSpentIdle'] = data['ticksTaxiSpentIdle'] - data['lazyTicks']
    data['ticksNonlazyTaxisSpentIdlePercent'] = data['ticksNonlazyTaxisSpentIdle'] / (data['ticks'] - data['lazyTicks'])
    
    data['passengersDeliveredPerNonlazyTaxi'] = data['passengersDelivered'] / (data['numTaxis'] - data['nrOfLazy'])
    
    parameters = findVariatingParameters(data, someParameters)
    
    if(parameters.__contains__('commRange')):
        # it is a commRange graph!
        for param in parameters:
            for metric in someMetrics:
                #drawNormalGraph(data, param, metric)
                print("TODO functionality for commRange graphs")
    elif(len(parameters) == 1):
        # draw 2 line graph
        for metric in someMetrics:
            drawTwoLineGraph(data, parameters[0], metric)
            save(filename, parameters[0], metric)
            plt.close()
            # plt.show()
    elif(len(parameters) == 2):
        # draw heatmap
        for metric in someMetrics:
            print(metric)
            print(parameters)
            drawHeatMap(data, parameters[0], parameters[1], metric)
    else:
        for param in parameters:
            for metric in someMetrics:
                drawTwoLineGraph(data, param, metric)
                save(filename, param, metric)
                plt.close()
                # plt.show()
    

def findVariatingParameters(data, someParameters):
    variatingParameters = []
    for p in someParameters:
        if (data[p].unique().size > 1):
            variatingParameters.append(p)
            
    # special case: commRange is also being varied, more than just usual 2 values
    if(len(data['commRange'].unique())>2):
        variatingParameters.append('commRange')
    
    return variatingParameters

def augmentTicksIdlePercent(data):
    data['ticksIdlePercent'] = data['ticksTaxiSpentIdle'].div(data['ticks'])

def drawNormalGraph(data, x, y='passengersDelivered'):
    # if there are configurations with same parameters keeping only the mean
    data = data.groupby(['runTime', 'commRange', 'commReliability', 'numTaxis', 'numCustomers', 'newCustomerProb', 'seeRange', 'lazyProb'], as_index=False).mean()
    
    ax = plt.gca()
    data.plot(loglog=True, x=x, y=y, ax=ax)
    plt.show()


def drawTwoLineGraph(data, x, y='passengersDelivered'):
    ax = plt.gca()
    data[data['commRange'] > 100].plot.scatter(loglog=True, x=x, y=y, ax=ax, color='red')
    data[data['commRange'] <= 100].plot.scatter(loglog=True, x=x, y=y, ax=ax, color='blue')
    # if there are configurations with same parameters keeping only the mean
    data = data.groupby(['runTime', 'commRange', 'commReliability', 'numTaxis', 'numCustomers', 'newCustomerProb', 'seeRange', 'lazyProb'], as_index=False).mean()
    
    # with and without communication
    data[data['commRange'] > 100].plot(loglog=True, x=x, y=y, ax=ax, color='red')
    data[data['commRange'] <= 100].plot(loglog=True, x=x, y=y, ax=ax, color='blue')
    ax.legend(['data[\'commRange\'] > 100', 'data[\'commRange\'] <= 100'])


def drawHeatMap(data, x, y, z='passengersDelivered', name="", filename=""):
    # if there are configurations with same parameters keeping only the mean
    data = data.groupby(['runTime', 'commRange', 'commReliability', 'numTaxis', 'numCustomers', 'newCustomerProb', 'seeRange', 'lazyProb'], as_index=False).mean()
    piv = pd.pivot_table(data, values=z, index=[x], columns=[y], fill_value=0)
    ax = sns.heatmap(piv, square=True)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
    plt.tight_layout()
    plt.title(z)
    # plt.savefig("plt_" + filename[-40:] + name + x + y + z + ".png")
    save(filename, x + '_' + y, z)
    plt.close()
   # plt.show()


def plotCommImprove(data, x, y, z='passengersDelivered', filename=""):
    # data = data.groupby(['runTime', 'commRange', 'commReliability', 'numTaxis', 'numCustomers', 'newCustomerProb', 'seeRange', 'lazyProb'], as_index=False).mean()
    
    dataComm = data[data['commRange'] > 100]
    dataNoComm = data[data['commRange'] <= 100]
    
    xValues = data[x].unique()
    yValues = data[y].unique()
    
    xs = []
    ys = []
    diffs = []
    
    for xValue in xValues:
        for yValue in yValues:
            
            # filter to only get rows with the specific x and y value. This should be only one row. Get from that row the value z.
            zComm = dataComm[(dataComm[x] == xValue) & (dataComm[y] == yValue)][z].values[0]
            zNoComm = dataNoComm[(dataNoComm[x] == xValue) & (dataNoComm[y] == yValue)][z].values[0]
            
            xs.append(xValue)
            ys.append(yValue)
            diffs.append(zComm - zNoComm) 
    
    newDataComm = pd.DataFrame.from_dict(data={x: xs, y: ys, 'commImprove':diffs})
    piv = pd.pivot_table(newDataComm, values='commImprove', index=[x], columns=[y], fill_value=0)
    ax = sns.heatmap(piv, square=True)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
    plt.tight_layout()
    plt.title(z)
    save(filename, x + '_' + y, z + '_commImprove')
    plt.close()
    # plt.show()
    

someParameters = ['runTime', 'commReliability', 'numTaxis', 'numCustomers', 'newCustomerProb', 'seeRange', 'lazyProb']
someMetrics = ['passengersDelivered', 'ticksTaxiSpentIdle', 'ticksBetweenSeenAndPickedAverage', 'ticksIdlePercent']

filename = "mas_taxi_delivery_data16_runtime10000000_trials40.csv"
ultimateGraphCreator(filename, someParameters, someMetrics)

filename = "mas_taxi_delivery_data2_runtime10000000_trials10.csv"
ultimateGraphCreator(filename, someParameters, someMetrics)

filename = "mas_taxi_delivery_data3_runtime10000000_trials5.csv"
ultimateGraphCreator(filename, someParameters, someMetrics)


#data = pd.read_csv("mas_taxi_delivery_data2_runtime10000000_trials10.csv", index_col=False)
#augmentTicksIdlePercent(data)
#for m in someMetrics:
#    drawTwoLineGraph(data, 'seeRange', m)
#    plt.show()

#data = pd.read_csv("mas_taxi_delivery_data10_runtime10000000_trials1.csv", index_col=False)
#drawTwoLineGraph(data[data['numTaxis']==2], 'newCustomerProb')
#drawTwoLineGraph(data[data['numTaxis']==5], 'newCustomerProb')
#drawTwoLineGraph(data[data['numTaxis']==10], 'newCustomerProb')
#plt.show()


#data = pd.read_csv("mas_taxi_delivery_data9_runtime10000000_trials10.csv", index_col=False)
#drawTwoLineGraph(data, 'seeRange')
#plt.show()
 
#data = pd.read_csv("mas_taxi_delivery_data10_runtime10000000_trials1.csv", index_col=False)
#drawHeatMap(data, 'newCustomerProb', 'numTaxis')
