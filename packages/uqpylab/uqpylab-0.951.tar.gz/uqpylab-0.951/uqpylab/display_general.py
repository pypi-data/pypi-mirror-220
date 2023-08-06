""" Plotting utility for the abstract functionalities """
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import uqpylab.display_util as display_util
from collections import OrderedDict

def display_bar(data, VarNames=None, xaxis_title='', yaxis_title='', yaxis_ticks=None, title=None, legend_title='', showlegend=False, grid=True, color=None, width=None):

    # Process data
    if type(data) == dict:
        df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        msg = "Accepted data type is dict or pandas DataFrame"
        raise RuntimeError(msg)
    if VarNames is not None:
        df.index = VarNames

    # Prepare color scheme
    subset = list(data.keys())
    if color is None:
        color = display_util.colorOrder(len(data))
    if type(color) == str:
        color = [color]
    
    # Bar plot
    if len(data)==1:
        fig = px.bar(
            df,
            color_discrete_map=dict(zip(subset, color)))
    else:
        fig = px.bar(
            df, 
            barmode='group', 
            color_discrete_map=dict(zip(subset, color))
        )

    if grid:
        fig.update_xaxes(mirror=True)
        fig.update_yaxes(mirror=True)

    fig.update_layout(
        xaxis_title= xaxis_title,
        yaxis_title= yaxis_title,
        legend_title= legend_title,
        showlegend=showlegend,    
    ) 

    if width is None and showlegend==True:
        fig.update_layout(
            width=800
        )
    else:
        fig.update_layout(
            width=width
        )

    if yaxis_ticks is not None:
        yaxis_range = yaxis_ticks[:2]
        fig.update_layout(
            yaxis_range=yaxis_range,
        )

        if len(yaxis_ticks) == 3:
            dtick = yaxis_ticks[2]
            fig.update_layout(
                yaxis = dict(
                    tickmode = 'linear',
                    dtick = dtick
            )
        ) 

    if title is not None:
        fig.update_layout(title=dict(text=title,y=0.95))  

    return fig


def morris_plot(data, VarNames=None, xaxis_title='', yaxis_title='', legend_title='', showlegend=False, grid=True):


    cm = display_util.colorOrder(len(data['MU']))

    traces = [
        go.Scatter(
            x=[2*data['minMU'], 2*data['maxMU']], 
            y=[0, 0], 
            mode='lines',
            showlegend=False,
            line=dict(
                color='black',
                width=2
            )
        ),
        go.Scatter(
            x=[0, 0],
            y=[2*data['minMSTD'], 2*data['maxMSTD']],
            mode='lines',
            showlegend=False,            
            line=dict(
                color='black',
                width=2
            )
        ),
    ]

    for i in range(len(data['MU'])):
        traces.append(
            go.Scatter(
                x=[data['MU'][i]], 
                y=[data['MSTD'][i]],
                text=[VarNames[i]],
                customdata= [[[xaxis_title], [yaxis_title]]],
                mode='markers', 
                marker_color=cm[i], 
                textposition='top center',
                textfont_color=cm[i],
                name=VarNames[i],
                hovertemplate =
                '<b>Input Variable: %{text}</b>'+
                '<br><b>%{customdata[0]}</b>: %{x:.5g}'+
                '<br><b>%{customdata[1]}</b>: %{y:.5g}<br>',
            )
        )

    fig = go.Figure(data=traces)

    if grid:
        fig.update_xaxes(mirror=True)
        fig.update_yaxes(mirror=True)

    # fig.update_xaxes(showspikes=True)
    # fig.update_yaxes(showspikes=True)

    if showlegend is None:
        showlegend=True if len(data['MU'])<10 else False

    fig.update_layout(
        xaxis_title= xaxis_title,
        yaxis_title= yaxis_title,
        legend_title= legend_title,
        showlegend=showlegend,
        xaxis_range=[np.amin([data['minMU'], 0-0.1*data['minMU']]), data['maxMU']],
        yaxis_range=[data['minMSTD'], data['maxMSTD']]
    ) 

    return fig


def display_bar_errors(data, xaxis_title='', yaxis_title='',  yaxis_ticks=None, legend_title='', showlegend=False, grid=True, color=None, width=None):

    if not any(isinstance(i, list) for i in data['x_bar']):
        data['x_bar'] = [data['x_bar']]
        data['y_bar'] = [data['y_bar']] 
        data['lb'] = [data['lb']]
        data['ub'] = [data['ub']]    
        if 'trace_name' in data:
            data['trace_name'] = [data['trace_name']]

    numOutputs = len(data['x_bar'])

    if color is None:
        color = display_util.colorOrder(numOutputs)

    if 'trace_name' not in data:
        data['trace_name'] = []
        for i in range(numOutputs):
            data['trace_name'].append(f'dataset #{i}')

    traces = []

    for i in range(numOutputs):
        traces.append(
                go.Bar(
                    x=data['x_bar'][i], 
                    y=data['y_bar'][i],
                    marker={'color': color[i]},
                    name=data['trace_name'][i],
                error_y=dict(
                    type='data',
                    symmetric=False,
                        array=data['ub'][i],
                        arrayminus=data['lb'][i],
                    color='black'
                )
            )
        )

    fig = go.Figure(data=traces)

    if grid:
        fig.update_xaxes(mirror=True)
        fig.update_yaxes(mirror=True)

    fig.update_layout(
        xaxis_title= xaxis_title,
        yaxis_title= yaxis_title,
        legend_title= legend_title,
        showlegend=showlegend,
    ) 

    if showlegend==True and width is None:
        fig.update_layout(
            width=800
        )
    else:
        fig.update_layout(
            width=width
        )

    if yaxis_ticks is not None:
        yaxis_range = yaxis_ticks[:2]
        fig.update_layout(
            yaxis_range=yaxis_range,
        )

        if len(yaxis_ticks) == 3:
            dtick = yaxis_ticks[2]
            fig.update_layout(
                yaxis = dict(
                    tickmode = 'linear',
                    dtick = dtick
            )
        )         

    return fig

def pie_chart(data, VarNames): 
    # Process data
    df = pd.DataFrame(data)
    if VarNames is not None:
        df.index = VarNames 


    fig = px.pie(
        df, 
        values='Values', 
        names=VarNames,
    )

    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        showlegend=False,
    )

    return fig


def convergence_curve(yvalue, LB, UB, xvalue=None, BatchSize=None, xaxis_title=None, yaxis_title=None):

    # prepare data
    if xvalue is None:
        iter = np.size(yvalue)
        xvalue = np.arange(1,iter+1)
    if BatchSize is None:
        BatchSize = 1
    xvalue *= BatchSize

    blue_color = display_util.colorOrder(1)[0]

    fig = go.Figure()

    # lower bound
    fig.add_trace(go.Scatter(
        x=xvalue, 
        y=LB, 
        fill=None,
        mode='lines', 
        line_width = 0.5,
        line_color='black',
        showlegend=False
        )
    )

    # confidence interval
    fig.add_trace(go.Scatter(
        x=xvalue, 
        y=UB, 
        fill='tonexty',
        fillcolor='rgba(0,0,0,0.1)',
        mode='lines', 
        line_width = 0.5,
        line_color='white',
        name='CI'
        )
    )

    # upper bound
    fig.add_trace(go.Scatter(
        x=xvalue, 
        y=UB, 
        fill=None,
        fillcolor='rgba(0,0,0,0.1)',
        mode='lines', 
        line_width = 0.5,
        line_color='black',
        showlegend=False
        )
    )

    # probability of failure
    fig.add_trace(go.Scatter(
        x=xvalue, 
        y=yvalue,
        fill=None,
        mode='lines',
        line_color=blue_color,
        name=yaxis_title
        )
    )

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_x=0.99,
        legend_xanchor='right',
        legend_y=0.99,
        legend_yanchor='top'
    )

    return fig


def sample_points(Samples, LSF, title=None):

    colorOrder = display_util.colorOrder(2)

    traces = [
        go.Scatter(
            x=Samples[LSF<=0,0] if len(Samples[LSF<=0,0])!=0 else [None], 
            y=Samples[LSF<=0,1] if len(Samples[LSF<=0,1])!=0 else [None],
            mode='markers',
            marker_symbol='circle',
            marker_color=colorOrder[0],
            name='g(X) ≤ 0'
            ),
        go.Scatter(
            x=Samples[LSF>0,0] if len(Samples[LSF>0,0])!=0 else [None],
            y=Samples[LSF>0,1] if len(Samples[LSF>0,1])!=0 else [None],
            mode='markers',
            marker_symbol='circle',
            marker_color=colorOrder[1],
            name='g(X) > 0'
            ),                       
    ]

    layout = go.Layout(
        xaxis_title_text='x<sub>1',
        yaxis_title_text='x<sub>2',
        showlegend=True,
        legend_x=0.99,
        legend_xanchor='right',
        legend_y=0.99,
        legend_yanchor='top'
    )

    fig = go.Figure(data=traces, layout=layout)

    if title:
        fig.update_layout(
            title=title
        )
    
    return fig


def display_histogram(data, VarNames=None, xaxis_title='', yaxis_title='', yaxis_ticks=None, title=None, legend_title='', showlegend=False, grid=True, color=None, width=None):

    # histogram properties
    nbins=15
    bin_size = (max(data[list(data.keys())[0]])-min(data[list(data.keys())[0]]))/nbins

    # Prepare color scheme
    subset = list(data.keys())
    if color is None:
        color = display_util.colorOrder(len(data))
    if type(color) == str:
        color = [color]
    
    # Histogram plot    
    fig = go.Figure()
    count = 0
    for key, value in data.items():
        fig.add_trace(
            go.Histogram(
                x=value, 
                name=key, 
                marker_color=color[count],
                xbins_size=bin_size
            )
        )
        count+=1

    if grid:
        fig.update_xaxes(mirror=True)
        fig.update_yaxes(mirror=True)

    fig.update_layout(
        xaxis_title= xaxis_title,
        yaxis_title= yaxis_title,
        legend_title= legend_title,
        showlegend=showlegend,    
    ) 

    if len(data) > 1:
        fig.update_layout(barmode='overlay')
        fig.update_traces(opacity=0.8)

    if width is not None:
        fig.update_layout(
            width=900
        )

    if yaxis_ticks is not None:
        yaxis_range = yaxis_ticks[:2]
        fig.update_layout(
            yaxis_range=yaxis_range,
        )

        if len(yaxis_ticks) == 3:
            dtick = yaxis_ticks[2]
            fig.update_layout(
                yaxis = dict(
                    tickmode = 'linear',
                    dtick = dtick
            )
        ) 

    # revert order of histograms
    # fig.data = fig.data[::-1]

    if title is not None:
        fig.update_layout(title=title)   

    return fig


def plot_line(xvalue, yvalue, line_color=None, xaxis_title=None, yaxis_title=None):

    # prepare data
    if xvalue is None:
        iter = np.size(yvalue)
        xvalue = np.arange(1,iter+1)

    if line_color is None:
        line_color = display_util.colorOrder(1)[0]

    fig = go.Figure()

    # plot line
    fig.add_trace(go.Scatter(
        x=xvalue, 
        y=yvalue,
        mode='lines',
        line_color=line_color,
        showlegend=False
        )
    )

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
    )

    return fig
    

def limitState(obj, outIdx, theInterface, myInput=None, myMetamodel=None):
    # validate input
    myAnalysis=obj
    myAnalysisMethodName = myAnalysis['Options']['Method']

    if myAnalysis['Class'] != 'uq_analysis':
        raise RuntimeError('Input needs to be a UQ_ANALYSIS object.')

    if myAnalysis['Type'] != 'uq_reliability':
        raise RuntimeError('Analysis needs to be a reliability analysis.')

    if not myAnalysis['Options']['Method'].lower() in ['sser','activelearning','alr','akmcs']:
        raise RuntimeError('Reliability analysis needs to be metamodel-based.')

    if type(myAnalysis['Internal']['Input']) == str:
        myInput = theInterface.getInput(obj['Internal']['Input'])
    else:
        myInput = obj['Internal']['Input']
    if len(myInput['nonConst']) != 2:
        raise RuntimeError('Works only for 2-dimensional problems.')

    # extract results
    Results = obj['Results']

    # extract metamodel and history
    if myAnalysis['Options']['Method'].lower() == 'sser':
        if type(obj['Results']['SSER']) == str:
            myMetamodel = theInterface.getModel(obj['Results']['SSER'])
            MetaModelName = myMetamodel['Options']['MetaType']
        else:
            raise ValueError('Unsupported type of Model!')

    elif myAnalysis['Options']['Method'].lower() == 'akmcs':
        MetaModelName = obj['Internal']['AKMCS']['MetaModel']
        parentName = obj["Name"]
        objPath = "Results." + MetaModelName 
        myMetamodel = theInterface.extractFromAnalysis(parentName=parentName,objPath=objPath)
        if type(myMetamodel) == list:
            myMetamodel = myMetamodel[outIdx]
    elif myAnalysis['Options']['Method'].lower() == 'alr':
        myAnalysisMethodName = "Active learning"
        MetaModelName = obj['Internal']['ALR']['MetaModel']
        parentName = obj["Name"]
        objPath = "Results.Metamodel" 
        myMetamodel = theInterface.extractFromAnalysis(parentName=parentName,objPath=objPath)
        if type(myMetamodel) == list:
            myMetamodel = myMetamodel[outIdx]

    else:
        raise RuntimeError("Not yet implemented!")

    if myAnalysis['Options']['Method'].lower() == 'sser':
        # get extremes
        minX = []
        maxX = []
        # UQLab uses a table with 11 columns to store data for Nodes in myMetamodel['SSE']['Graph']['Nodes'], namely: 
        # neighbours, bounds, inputMass, ref, level, idx, expansions, refineScore, Pf, History, and PfRepl
        numnodes = int(len(myMetamodel['SSE']['Graph']['Nodes'])/11)
        for dd in range(numnodes):
            Ucurr = np.array(myMetamodel['SSE']['Graph']['Nodes'][9*numnodes+dd]['U'])
            if Ucurr.size > 0:
                myInput1 = theInterface.getInput(myMetamodel['SSE']['Input']['Original'])
                Xcurr = theInterface.invRosenblattTransform(Ucurr, myInput1['Marginals'], myInput1['Copula'])
                if type(minX) == list:
                    minX = np.amin(Xcurr, axis=0, keepdims=True)
                    maxX = np.amax(Xcurr, axis=0, keepdims=True)
                else:
                    minX = np.amin(np.concatenate((minX, Xcurr), axis=0), axis=0, keepdims=True)
                    maxX = np.amax(np.concatenate((maxX, Xcurr), axis=0), axis=0, keepdims=True)

    elif myAnalysis['Options']['Method'].lower() == 'akmcs':
        minX = np.amin(np.array(Results['History']['MCSample']), axis=0, keepdims=True)  # from uq_akmcs_display
        maxX = np.amax(np.array(Results['History']['MCSample']), axis=0, keepdims=True)  # from uq_akmcs_display
    
    elif myAnalysis['Options']['Method'].lower() == 'alr':
        minX = np.amin(np.array(Results['History']['ReliabilitySample']), axis=0, keepdims=True)
        maxX = np.amax(np.array(Results['History']['ReliabilitySample']), axis=0, keepdims=True)

    else:
        raise RuntimeError("Not yet implemented!")

    # extract experimental design
    X = np.array(myMetamodel['ExpDesign']['X'])
    G = np.array(myMetamodel['ExpDesign']['Y'])

    # init
    colorOrder = display_util.colorOrder(2)

    # compute grid
    NGrid = 200
    [xx, yy] = np.meshgrid(np.linspace(minX[0,0], maxX[0,0], NGrid),
                           np.linspace(minX[0,1], maxX[0,1], NGrid))
    XGrid = np.stack((xx.flatten('F'), yy.flatten('F'))).T
    zz = theInterface.evalModel(myMetamodel, XGrid)
    zz = np.reshape(zz, xx.shape, order='F')

    traces = [
            go.Contour(
                x=xx.flatten(),
                y=yy.flatten(),
                z=zz.flatten(),
                contours_coloring='lines',
                line_width=2,
                contours_start=0,
                contours_end=0,
                colorscale=[[0, 'rgb(0,0,0)'], [1, 'rgb(0,0,0)']],
                name='g(X) = 0',
                showlegend=True,
                showscale=False,
                coloraxis=None
            )
    ]

    if np.any(X[G<=0,0]):
        traces.append(go.Scatter(
            x=X[G<=0,0] if len(X[G<=0,0])!=0 else [None], 
            y=X[G<=0,1] if len(X[G<=0,1])!=0 else [None],
            mode='markers',
            marker_symbol='square',
            marker_color=colorOrder[0],
            name='g(X) ≤ 0'
            ))

    if np.any(X[G>0,0]):
        traces.append(go.Scatter(
            x=X[G>0,0] if len(X[G>0,0])!=0 else [None], 
            y=X[G>0,1] if len(X[G>0,1])!=0 else [None],
            mode='markers',
            marker_symbol='cross',
            marker_color=colorOrder[1],
            name='g(X) > 0'
            ))

    layout = go.Layout(
        xaxis_title_text=myInput['Marginals'][0]['Name'],
        yaxis_title_text=myInput['Marginals'][1]['Name'],
        showlegend=True,
        legend_x=0.99,
        legend_xanchor='right',
        legend_y=0.99,
        legend_yanchor='top',
        title=f"{myAnalysisMethodName} - Limit state approximation"
    )

    fig = go.Figure(data=traces, layout=layout)

    fig.update_xaxes(range=[minX[0,0], maxX[0,0]])
    fig.update_yaxes(range=[minX[0,1], maxX[0,1]])
    return fig

