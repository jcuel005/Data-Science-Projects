#Neccessary Python Libraries
from matplotlib import pyplot
from matplotlib.pyplot import figure, title
import pandas as pd
import numpy as np
import statistics
import math
import datetime
import yahoo_fin.stock_info as yahoo_fin
from bs4 import BeautifulSoup
import requests
import scipy.stats
import pylab
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
from statsmodels.graphics.gofplots import qqplot
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])

#The neccessary propriety functions for data wrangling-------------------------------------------------------

#Gets the string format for Dates
def Dates(date):
    dateString = ''
    for val in str(date):
        if(val == ' '):
            break
        elif(val == '-'):
            dateString = dateString + '/'   
        else:
            dateString = dateString + val
            
    return dateString

#Gets the soup for the link provided
def SoupGetter(searchVar):
    source = requests.get(searchVar,allow_redirects=False).text
    soup = BeautifulSoup(source,'lxml')
    return soup

#converts strings into floats for financial statements
def locator(data_array):
    desired_array2 = []
    desired_array3 = []
            
    # Converts the data that is negative into a readable negative strings            
    for value in data_array:
        if(value.startswith('(') == True):
            value = value[1:-1]
            value = '-'+ value
        else:
            pass
        desired_array2.append(value)
        
    # Converts the into useable numerical values        
    for item in desired_array2:
        if(str(item[-1]) == 'B'):
            item = float(item[0:-1]) * 1000000000
        elif(str(item[-1]) == 'M'):
            item = float(item[0:-1]) * 1000000
        elif(str(item[-1]) == 'T'):
            item = float(item[0:-1]) * 1000000000000
        elif(str(item[-1]) == 'K'):
            item = float(item[0:-1]) * 1000
        elif(str(item) == '-'):
            item = np.NaN
        else:
            temp = ''
            for char in item:
                item = item.split(',')
                for i in item:
                    temp += i
                item = float(temp)
        desired_array3.append(item)
            
    return desired_array3

#Transform nan to zero for the SaleGains variable
def NaNZero(array):
    x = []
    for i in array:
        if(i is np.nan):
            x.append(0)
        else:
            x.append(i)
    return x

#This Function is for the 3 valuation ratios
def ValuationRatios(soup):
    finder = []
    holder = []
    holder2 = []
    holder3 = []
    
    for value in soup.find_all('td',style = 'text-align:center;'):
        finder.append(value.text)
      
    #Gets the PE Ratios
    for index in range(7,len(finder),4):
        holder.append(float(finder[index]))
        
    #Gets the date of the PE Ratios  
    for index in range(4,len(finder),4):
        holder2.append(str(finder[index]))
        
    for index in range(6,len(finder),4):
        i = finder[index][1:]
        holder3.append(float(i))
        
        
        
    #Gets the dataframe for the PEs
    PEdataframe = pd.DataFrame({'Dates': holder2,
                               'PEs':holder,
                               'EPS':holder3})
        
    return PEdataframe

#Function for plotting 1 line on a plot
def pyplot1plot(name,x,y,yaxe = '$',user_stock = 'pep',color1 = '',color2 = ''):

    layout = go.Layout(
    title = f"{user_stock}'s {name} Time Series",
    font = dict(family="Arial",size=18, color="white"),
    yaxis = dict(
        title = yaxe
    ),
    xaxis = dict(
        title = 'Date'
        ),
    paper_bgcolor='#3F3B3A',
    plot_bgcolor = color1

    )

    trace1 = go.Scatter(
        x = x,
        y = y,
        mode = 'lines+markers',
        name = name,
        line = dict(
                shape = 'linear'
        ),
        marker = dict(
                size = 10,
                color = color2
        )
    )

    fig = go.Figure(data = [trace1],layout = layout)
    return fig

#Function for plotting two lines on a plot
def pyplot2plots(name1,array1x,array1y,name2,array2x,array2y,user_stock,color1, color2,color3):
    layout = go.Layout(
    font = dict(family="Arial",size=18, color="white"),
    title = f"Yearly {user_stock}'s {name1} V. {name2}",
    yaxis = dict(
        title = "$"
        ),
    xaxis = dict(
        title = 'Date'
        ),
    paper_bgcolor='#3F3B3A',
    plot_bgcolor = color1
    )

    trace1 = go.Scatter(
        x = array1x,
        y = array1y,
        mode = 'lines+markers',
        name = name1,
        line = dict(
                shape = 'linear'
        ),
        marker = dict(
                size = 10,
                color = color2
        )

    )

    trace2 = go.Scatter(
        x = array2x,
        y = array2y,
        mode = 'lines+markers',
        name = name2,
        line = dict(
                shape = 'linear'
        ),
        marker = dict(
                size = 10,
                color = color3
        )
    )

    fig = go.Figure(data = [trace1,trace2],layout = layout)
    return fig

def pyplot1dash(x1,y1,name1,y2,colorDash,user_stock,color1,color2):
    layout = go.Layout(
    title = f"{user_stock}'s {name1} Timeseries",
    font = dict(family="Arial",size=18, color="white"),
    yaxis = dict(
        title = name1
    ),
    xaxis = dict(
        title = 'Date'
        ),
    paper_bgcolor='#3F3B3A',
    plot_bgcolor = color1,
    showlegend = False
    )

    trace1 = go.Scatter(
        x = x1,
        y = y1,
        mode = 'lines+markers',
        name = name1,
        line = dict(
                shape = 'linear'
        ),
        marker = dict(
                size = 10,
                color = color2
        )

    )

    trace2 = go.Scatter(
        x = x1,
        y = [y2,y2,y2,y2,y2],
        mode = 'lines',
        line = dict(
                shape = 'hv',
                dash = 'dash',
                color = colorDash
        )
    )

    fig = go.Figure(data = [trace1,trace2],layout = layout)

    return fig

def pyplotBar(x,y,xaxe,yaxe,main):
    layout = go.Layout(
    title = main,
    font = dict(family="Arial",size=18, color="white"),
    yaxis = dict(
        title = yaxe
        ),
    xaxis = dict(
        title = xaxe
        ),
    paper_bgcolor='#3F3B3A',
    plot_bgcolor = "rgb(230,245,201)"
    )
    
    trace1 = go.Bar(
        x = x,
        y = y,
        marker_color = "rgb(102,166,30)"
        
    )
    
    fig = go.Figure(data = [trace1],layout = layout)
    return fig

def pyplotScatter(name,x,y,xaxe,yaxe,user_stock):
    layout = go.Layout(
    title = f"{user_stock}'s Correlation w/ {name}",
    font = dict(family="Arial",size=18, color="white"),
    yaxis = dict(
        title = yaxe
        ),
    xaxis = dict(
        title = xaxe
        ),
        paper_bgcolor='#3F3B3A',
        plot_bgcolor = "rgb(230,245,201)"
    )

    trace1 = go.Scatter(
        x = x,
        y = y,
        mode = 'markers',
        marker = dict(
                size = 10,
                color = 'rgb(102,166,30)'
        )

    )

    fig = go.Figure(data = [trace1],layout = layout)
    return fig

#Gets stock price over a certain of time the user wants------------------------------------------

#Gets today's date
today_time = datetime.datetime.now()
today_date = str(Dates(pd.to_datetime(today_time,yearfirst = True)))

#Gets the date 20 Years ago
twentyYr_date = Dates(datetime.datetime.now() - datetime.timedelta(days = 20 * 365))

#Gets the years for the financial graphs
year = int(datetime.datetime.now().year) - 1
years = [year,year-1,year-2,year-3,year-4]
years = [str(i) + '/12/31' for i in years]
years = np.flip(years)
ffoX = datetime.datetime.strptime(str(datetime.datetime.now().year) + '/12/31','%Y/%m/%d')

#Styles the Sidebar------------------------------------------------------------------------------
SIDEBAR_STYLE = {
    "position":"fixed",
    "width":"16rem",
    "padding":"2rem 1rem",
    "background-color":"#3F3B3A"
}

CONTENT_STYLE = {
    "margin-left":"18rem",
    "margin-right":"2rem",
    "padding":"1rem 1rem"
}

sidebar = html.Div(
    [
        html.H2("Analytics Choices",className="display-4",style={"color":"yellow"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home",href="/",active="exact"),
                dbc.NavLink("Balance Sheet",href="/Balance-Sheet",active="exact"),
                dbc.NavLink("Income Statement",href="/Income-Statement",active="exact"),
                dbc.NavLink("Cashflow Statement",href="/Cashflow-Statement",active="exact"),
                dbc.NavLink("Profitability Ratios",href="/Profitablility-Ratios",active="exact"),
                dbc.NavLink("Liquidity Ratios",href="/Liquidity-Ratios",active="exact"),
                dbc.NavLink("Solvency Ratios",href="/Solvency-Ratios",active="exact"),
                dbc.NavLink("Financial Risk Ratios",href="/Financial-Risk-Ratios",active="exact"),
                dbc.NavLink("Dividend Charts",href="/Dividend-Charts",active="exact"),
                dbc.NavLink("Valuation Ratio Charts",href="/Valuation-Ratio-Charts",active="exact"),
                dbc.NavLink("Macro Economic Charts",href="/Macro-Economic-Charts",active="exact"),
                dbc.NavLink("Insider Trading Chart",href="/Insider-Trading-Chart",active="exact")
            ],
            vertical = True,
            pills = True
        ),
    ],
    style = SIDEBAR_STYLE,
)

content = html.Div(id="page-content",children=[],style=CONTENT_STYLE)

#Gets the App Layout-------------------------------------------------------------------------
app.layout = html.Div([
    sidebar,
    html.Div('Dividend Analytica',style = {'textAlign':'center', "fontsize":1000,"color":"yellow"}),

    dbc.Row(
        dbc.Col(
            dcc.Input(
                id="Ticker_Symbol",
                type= "text",
                placeholder="Input Ticker Symbol",
                debounce = True,
                pattern = r"^[A-Za-z].*",
                value = 'pep'
            ),
            width = {'offset':10,'size':6}
        )
    ),

    dcc.Location(id="url"),
    content,

    dcc.Store(id="store-data",data = '',storage_type='memory'),
    dcc.Store(id="Stock_Prices",data = {},storage_type = 'memory'),
    dcc.Store(id="Balance_Sheet",data={},storage_type='memory'),
    dcc.Store(id="Sector",data=[],storage_type="memory"),
    dcc.Store(id = "Income_Statement",data = {},storage_type="memory"),
    dcc.Store(id = "Cashflow_Statement", data = {}, storage_type = "memory"),
    dcc.Store(id = "Insider_Data", data = {},storage_type = "memory"),
    dcc.Store(id = "Dividend_Data", data = [], storage_type = "memory"),
    dcc.Store(id = "Valuation_Data", data = {}, storage_type = "memory" ),
    dcc.Store(id = "Earnings_Data",data = [], storage_type = "memory")
    
])

#Gets the string Connect with webscraping & creates the neccessary dataset functions-----------------------------------------------------------------------

#Gets the ticker symbol in order to webscrape different sources
@app.callback(
    Output('store-data','data'),
    Input('Ticker_Symbol','value')
)
def inputTicker(ticker):
    user_stock = ticker
    return user_stock

#Gets the stock price data
@app.callback(
    Output('Stock_Prices','data'),
    Input('store-data','data')
)
def stockPriceDict(user_stock):
    #Gets the neccessary Stonk Data Prices
    stonkPrices = yahoo_fin.get_data(user_stock,start_date = str(twentyYr_date),end_date = today_date)
    stonkPrices['dates'] = pd.to_datetime(stonkPrices.index)

    #Converts it a dictionary so it can properly be 
    stonkPrices = {
        'close':stonkPrices['close'],
        'dates':stonkPrices['dates'],
        'ticker':stonkPrices['ticker']
    }
    return stonkPrices

#Gets the stock's sector, needed to properly webscrape
@app.callback(
    Output("Sector",'data'),
    Input('store-data','data')
)
def Sector(user_stock):
    #webscrapes the stock's sector
    sectors = SoupGetter(f"https://www.marketwatch.com/investing/stock/{user_stock}/company-profile?mod=mw_quote_tab")

    #gets & return the stock's sector
    sectorList = []
    for value in sectors.find_all('span', class_ = 'primary'):
        sectorList.append(value.text)
        
    sector = sectorList[7]
    industry = sectorList[6]

    #Corrects for false sector designation
    if(industry == 'Consumer Finance'):
        sector = 'Technology'
    else:
        pass

    return [sector,industry]

#Gets the balance sheet data
@app.callback(
    Output("Balance_Sheet","data"),
    [Input('store-data','data'),
    Input("Sector",'data')]
)
def balanceSheetData(user_stock,sector):
    #Gets Essential Balance Sheet data 
    BalanceSoup = SoupGetter(searchVar = f'https://www.marketwatch.com/investing/stock/{user_stock}/financials/balance-sheet')

    index = 0

    #Puts all BalanceSheet data in a array
    BalanceData = []
    for i in BalanceSoup.find_all('div',class_ = 'cell__content'):
        BalanceData.append(str(i.text))
        
    #Gets balance sheet data from real estate companies
    if(sector[0] == 'Real Estate/Construction'):
        
        #For loop to work through balance sheet data
        desiredBalance = ['Total Assets','Total Debt','Total Liabilities','Total Equity',"Total Shareholders' Equity"]
        
        #For loop to work through balance sheet data
        SortedBalanceSheet = []
        for item in desiredBalance: 
            for index in range(0,len(BalanceData),1):
                if((BalanceData[index - 1] ==  item) and (BalanceData[index] == item)):
                    for number in range(1,6,1):
                        SortedBalanceSheet.append(BalanceData[index + number])
                else:
                    pass
            
        #Makes balance sheet into a pandas dataframe
        BalanceSheetDataFrame = {'Years': years,
                                'Total_Assets':locator(list(SortedBalanceSheet[0:5])),
                                'Total_Debt':locator(list(SortedBalanceSheet[5:10])),
                                'Total_Liabilities':locator(list(SortedBalanceSheet[10:15])),
                                'Total_Equity':locator(list(SortedBalanceSheet[15:20])),
                                "Shareholder's_Equity":locator(list(SortedBalanceSheet[20:25])),
                                'Total_Current_Assets':[np.nan,np.nan,np.nan,np.nan,np.nan],
                                'Total_Current_Liabilities':[np.nan,np.nan,np.nan,np.nan,np.nan]}

    #Gets balance sheet data from financial services companies
    elif(sector[0] == 'Financial Services'):
        
        #For loop to work through balance sheet data
        desiredBalance = ['Total Assets','Total Debt','Total Liabilities','Total Equity',"Total Shareholders' Equity"]
        
        #For loop to work through balance sheet data
        SortedBalanceSheet = []
        for item in desiredBalance: 
            for index in range(0,len(BalanceData),1):
                if((BalanceData[index - 1] ==  item) and (BalanceData[index] == item)):
                    for number in range(1,6,1):
                        SortedBalanceSheet.append(BalanceData[index + number])
                else:
                    pass
            
        #Makes balance sheet into a pandas dataframe
        BalanceSheetDataFrame = {'Years': years,
                                'Total_Assets':locator(list(SortedBalanceSheet[0:5])),
                                'Total_Debt':locator(list(SortedBalanceSheet[5:10])),
                                'Total_Liabilities':locator(list(SortedBalanceSheet[10:15])),
                                'Total_Equity':locator(list(SortedBalanceSheet[15:20])),
                                "Shareholder's_Equity":locator(list(SortedBalanceSheet[20:25])),
                                'Total_Current_Assets':[np.nan,np.nan,np.nan,np.nan,np.nan],
                                'Total_Current_Liabilities':[np.nan,np.nan,np.nan,np.nan,np.nan]}

    else:
        
        #List of desired lines of a balance sheet 
        desiredBalance = ['Total Current Assets','Total Assets','Total Current Liabilities','Total Liabilities',
                        'Long-Term Debt','Total Equity',"Total Shareholders' Equity",'Inventories',
                        'Interest Expense','Income Tax']
        
        #For loop to work through balance sheet data
        SortedBalanceSheet = []
        for item in desiredBalance: 
            for index in range(0,len(BalanceData),1):
                if((BalanceData[index - 1] ==  item) and (BalanceData[index] == item)):
                    for number in range(1,6,1):
                        SortedBalanceSheet.append(BalanceData[index + number])
                else:
                    pass
                
        #Makes balance sheet into a pandas dataframe
        BalanceSheetDataFrame = pd.DataFrame({'Years':years,
                                'Total_Current_Assets':locator(list(SortedBalanceSheet[0:5])),
                                'Total_Assets':locator(list(SortedBalanceSheet[5:10])),
                                'Total_Current_Liabilities':locator(list(SortedBalanceSheet[10:15])),
                                'Total_Liabilities':locator(list(SortedBalanceSheet[15:20])),
                                'Total_Debt':locator(list(SortedBalanceSheet[20:25])),
                                'Total_Equity':locator(list(SortedBalanceSheet[25:30])),
                                "Shareholder's_Equity":locator(list(SortedBalanceSheet[30:35])),
                                'Inventories':locator(list(SortedBalanceSheet[35:40]))})

        BalanceSheetDataFrame.fillna(0,inplace = True)

        #Convert dataframe to dictionary since fillna doesn't work on dictionaries
        BalanceSheetDataFrame = {'Years':BalanceSheetDataFrame['Years'],
                                "Total_Current_Assets":BalanceSheetDataFrame['Total_Current_Assets'],
                                "Total_Assets":BalanceSheetDataFrame['Total_Assets'],
                                'Total_Current_Liabilities':BalanceSheetDataFrame['Total_Current_Liabilities'],
                                'Total_Liabilities':BalanceSheetDataFrame['Total_Liabilities'],
                                'Total_Debt':BalanceSheetDataFrame['Total_Debt'],
                                'Total_Equity':BalanceSheetDataFrame['Total_Equity'],
                                "Shareholder's_Equity":BalanceSheetDataFrame["Shareholder's_Equity"],
                                'Inventories':BalanceSheetDataFrame['Inventories']
                                }

    return BalanceSheetDataFrame

#Gets the Income Statement data
@app.callback(
    Output("Income_Statement","data"),
    [Input('store-data','data'),
    Input("Sector",'data')]
)
def incomeStatementData(user_stock,sector):
    IncomeSoup = SoupGetter(searchVar = 'https://www.marketwatch.com/investing/stock/{0}/financials/income'.format(user_stock))

    #Puts all Income Statement data in a array
    IncomeData = []
    for i in IncomeSoup.find_all('div',class_ = 'cell__content'):
        IncomeData.append(str(i.text))
        
    # For Reits
    if(sector[0] == 'Real Estate/Construction'):
        #List of desired lines of a Income Statement
        desiredIncome = ['Net Income','Sales/Revenue','Depreciation & Amortization Expense',
                        'Extra Items & Gain/Loss Sale Of Assets','Basic Shares Outstanding','Total Interest Expense',
                        'Income Taxes']

        #For loop to work through Income Statement data
        SortedIncome = []
        for item in desiredIncome: 
            for index in range(0,len(IncomeData),1):
                if((IncomeData[index - 1] ==  item) and (IncomeData[index] == item)):
                    for number in range(1,6,1):
                        SortedIncome.append(IncomeData[index + number])
                else:
                    pass 

        if(len(SortedIncome) < 10):
            for i in range(0,5,1):
                SortedIncome.append('0')
        else:
            pass
        

        #Makes Income Statement into a pandas dataframe
        IncomeDataFrame = pd.DataFrame({'Years': years,
                                            'Net_Income': locator(list(SortedIncome[0:5])),
                                            'Revenue': locator(list(SortedIncome[5:10])),
                                            'Depreciation&Amortization': locator(list(SortedIncome[10:15])),
                                            'SaleGains': NaNZero(locator(list(SortedIncome[15:20]))),
                                            'Shares':locator(list(SortedIncome[20:25])),
                                            'Interest_Expense':locator(list(SortedIncome[25:30])),
                                            'Income_Tax':locator(list(SortedIncome[30:35]))
                                            })

        IncomeDataFrame['FFO'] = (IncomeDataFrame['Net_Income'] + IncomeDataFrame['Depreciation&Amortization'] - IncomeDataFrame['SaleGains']) / IncomeDataFrame['Shares']

        IncomeDataFrame = {'Years':IncomeDataFrame['Years'],
                        'Net_Income':IncomeDataFrame['Net_Income'],
                        'Revenue':IncomeDataFrame['Revenue'],
                        'Depreciation&Amortization':IncomeDataFrame['Depreciation&Amortization'],
                        'SaleGains':IncomeDataFrame['SaleGains'],
                        'Shares':IncomeDataFrame['Shares'],
                        'Interest_Expense':IncomeDataFrame['Interest_Expense'],
                        'Income_Tax':IncomeDataFrame['Income_Tax'],
                        'FFO':IncomeDataFrame['FFO']
        
        }

    elif(sector[0] == 'Financial Services'):
        #List of desired lines of a Income Statement
        desiredIncome = ['Net Income','Sales/Revenue','Total Internest Expense','Income Taxes','Basic Shares Outstanding']

        #For loop to work through Income Statement data
        SortedIncome = []
        for item in desiredIncome: 
            for index in range(0,len(IncomeData),1):
                if((IncomeData[index - 1] ==  item) and (IncomeData[index] == item)):
                    for number in range(1,6,1):
                        SortedIncome.append(IncomeData[index + number])
                else:
                    pass        

        if(len(SortedIncome) < 10):
            for i in range(0,5,1):
                SortedIncome.append('0')
        else:
            pass

        #Makes Income Statement into a pandas dataframe
        IncomeDataFrame = pd.DataFrame({'Years': years,
                                        'Net_Income': locator(list(SortedIncome[0:5])),
                                        'Revenue':locator(list(SortedIncome[5:10])),
                                        'Shares':locator(list(SortedIncome[10:15]))
                                            })

        IncomeDataFrame = {'Years':IncomeDataFrame['Years'],
                        'Net_Income':IncomeDataFrame['Net_Income'],
                        'Revenue':IncomeDataFrame['Revenue'],
                        'Shares':IncomeDataFrame['Shares']
        }

    else:
        #List of desired lines of a Income Statement
        desiredIncome = ['Net Income','Sales/Revenue','Depreciation & Amortization Expense',
                        'Extra Items & Gain/Loss Sale Of Assets','Basic Shares Outstanding','Interest Expense',
                        'Income Tax']

        #For loop to work through Income Statement data
        SortedIncome = []
        for item in desiredIncome: 
            for index in range(0,len(IncomeData),1):
                if((IncomeData[index - 1] ==  item) and (IncomeData[index] == item)):
                    for number in range(1,6,1):
                        SortedIncome.append(IncomeData[index + number])
                else:
                    pass 

        if(len(SortedIncome) < 10):
            for i in range(0,5,1):
                SortedIncome.append('0')
        else:
            pass
        

        #Makes Income Statement into a pandas dataframe
        IncomeDataFrame = pd.DataFrame({'Years': years,
                                            'Net_Income': locator(list(SortedIncome[0:5])),
                                            'Revenue': locator(list(SortedIncome[5:10])),
                                            'Depreciation&Amortization': locator(list(SortedIncome[10:15])),
                                            'SaleGains': NaNZero(locator(list(SortedIncome[15:20]))),
                                            'Shares':locator(list(SortedIncome[20:25])),
                                            'Interest_Expense':locator(list(SortedIncome[25:30])),
                                            'Income_Tax':locator(list(SortedIncome[30:35]))
                                            })

        IncomeDataFrame['FFO'] = (IncomeDataFrame['Net_Income'] + IncomeDataFrame['Depreciation&Amortization'] - IncomeDataFrame['SaleGains']) / IncomeDataFrame['Shares']

        IncomeDataFrame = {'Years':IncomeDataFrame['Years'],
                        'Net_Income':IncomeDataFrame['Net_Income'],
                        'Revenue':IncomeDataFrame['Revenue'],
                        'Depreciation&Amortization':IncomeDataFrame['Depreciation&Amortization'],
                        'SaleGains':IncomeDataFrame['SaleGains'],
                        'Shares':IncomeDataFrame['Shares'],
                        'Interest_Expense':IncomeDataFrame['Interest_Expense'],
                        'Income_Tax':IncomeDataFrame['Income_Tax'],
                        'FFO':IncomeDataFrame['FFO']}

    return IncomeDataFrame

#Gets the Cashflow statement
@app.callback(
    Output('Cashflow_Statement','data'),
    Input('store-data','data')
)
def cashflowData(user_stock):
    #Gets the Yearly Cashflow Statement
    CashSoup = SoupGetter(searchVar = 'https://www.marketwatch.com/investing/stock/{0}/financials/cash-flow'.format(user_stock))

    #Puts all Income Statement data in a array
    CashData = []
    for i in CashSoup.find_all('div',class_ = 'cell__content'):
        CashData.append(str(i.text))

    #List of desired lines of a Income Statement
    desiredCash = ['Net Investing Cash Flow','Cash Dividends Paid - Total','Free Cash Flow','Net Operating Cash Flow']

    #For loop to work through Income Statement data
    SortedCash = []
    for item in desiredCash: 
        for index in range(0,len(CashData),1):
            if((CashData[index - 1] ==  item) and (CashData[index] == item)):
                for number in range(1,6,1):
                    SortedCash.append(CashData[index + number])
            else:
                pass        
    
    #Makes Income Statement into a pandas dataframe
    CashFlowDataFrame = {'Net_Investing_Cashflow': locator(list(SortedCash[0:5])),\
                                    'Dividends': locator(list(SortedCash[5:10])),
                                    'Free_Cash_Flow': locator(list(SortedCash[10:15])),
                                    'Net_Operating_Cashflow' : locator(list(SortedCash[15:20]))
                                    }
    return CashFlowDataFrame

@app.callback(
    Output("Earnings_Data", "data"),
    Input('store-data',"data")
)
def earningsData(user_stock):
    #Gets the earnings data
    epsHistory = yahoo_fin.get_earnings_history(user_stock)

    #Gets the eps Surprise Percent from estimate and actual
    actualEPS = []
    estimateEPS = []
    dateEPS = []
    for frame in epsHistory:
        tempFrame = pd.DataFrame([frame])
        actualEPS.append(tempFrame['epsactual'][0])
        estimateEPS.append(tempFrame['epsestimate'][0])
        dateEPS.append(tempFrame['startdatetime'][0][0:10])
            

            
    epsDataFrame = pd.DataFrame({'EPS_Actual':actualEPS,
                                'EPS_Estimate':estimateEPS,
                                'Date':dateEPS})

    #Gets the Ananlyst Estimate
    rowz = 0
    while (np.isnan(epsDataFrame['EPS_Estimate'][rowz]) == True):
        rowz += 1
            
    estimate = epsDataFrame['EPS_Estimate'][rowz + 0] + epsDataFrame['EPS_Estimate'][rowz + 1] + epsDataFrame['EPS_Estimate'][rowz + 2] + epsDataFrame['EPS_Estimate'][rowz + 3]

    #This eps dataframe is for EPS correction estimation
    epsDataFrame.dropna(inplace = True)
    epsDataFrame.reset_index(inplace = True)

    #Checks for repeating dates to remove that row form the epsDataFrame
    droppables = []
    for row in range(1,len(epsDataFrame['Date']),1):
        if(epsDataFrame['Date'][row] == epsDataFrame['Date'][row-1]):
            droppables.append(row)
        else:
            pass

    epsDataFrame.drop(droppables,inplace = True)
    epsDataFrame.reset_index(inplace = True)

    #Now to calculate the trailing Yearly EPS, (used in the PE Boxplot) & compare difference with trailing estimate EPS
    EPSAct = []
    EPSEst = []
    EPSdiff = []
    EPSper = []
    EPSdate = []

    for row in range(4,len(epsDataFrame),1):
        trailingAct = epsDataFrame['EPS_Actual'][row] + epsDataFrame['EPS_Actual'][row-1] + epsDataFrame['EPS_Actual'][row-2] + epsDataFrame['EPS_Actual'][row-3]
        trailingEst = epsDataFrame['EPS_Estimate'][row] + epsDataFrame['EPS_Estimate'][row-1] + epsDataFrame['EPS_Estimate'][row-2] + epsDataFrame['EPS_Estimate'][row-3]
        EPSdifference = trailingAct - trailingEst
            
        if(trailingEst == 0):
            EPSpercent = 0
        else:
            EPSpercent = ((trailingAct - trailingEst) / trailingEst) * 100
            
        EPSAct.append(trailingAct)
        EPSEst.append(trailingEst)
        EPSdiff.append(EPSdifference)
        EPSper.append(EPSpercent)
        EPSdate.append(epsDataFrame['Date'][row-4])
            

    trailingEPS = {'Trailing_EPS_Act':EPSAct,
                        'Trailing_EPS_Est':EPSEst,
                        'Trailing_EPS_Diff':EPSdiff,
                        'Trailing_EPS_Per':EPSper,
                        'Trailing_EPS_Date':EPSdate}

    return [trailingEPS,estimate]

#Gets the Insider Trading Data
@app.callback(
    Output("Insider_Data","data"),
    Input('store-data','data')
)
def InsiderData(user_stock):
    ## Gets the Insider Trading Data from openinsider.com
    insiderSoup = SoupGetter(searchVar = f'http://openinsider.com/search?q={user_stock}')

    #Puts all Insider data in a array
    insiderData = []
    for i in insiderSoup.find_all('td',align = 'right'):
        insiderData.append(str(i.text))
        
    #Removes all of the unneccessary tags & empty spaces from array
    insiderData = insiderData[20:] 
    inData = []
    for val in insiderData:
        if((val == '') or (val == 'D') or (val == 'A') or (val == 'E') or (val == 'M') or (val == 'DM') 
        or (val == 'DE')):
            pass
        else:
            inData.append(val)

    #Gets the dates for insider trading
    inDates = []
    for num in range(1,len(inData),7):
        inDates.append(inData[num])
        
    #Gets the Value of Stock Bought or sold
    inSale = []
    for num in range(6,len(inData),7):
        inSale.append(inData[num])
        
    insiderSale = []
    for string in inSale:
        temp = ''
        for char in string:
            if((char == '$') or (char == ',') or (char == '%')):
                pass
            else:
                temp += char
        insiderSale.append(float(temp))

    insiderSale = np.flip(insiderSale)
        
    #Creates the dataframe for insider trading info
    insiderDF = pd.DataFrame({'Date':inDates,
                            'Exchange':insiderSale
                            })

    aggregation_functions = {'Exchange': 'sum','Date': 'first'}
    insiderDF = insiderDF.groupby(insiderDF['Date']).aggregate(aggregation_functions)

    #Gets the colors for Insider Trading
    inColors = []
    for num in insiderDF['Exchange']:
        if(num <= 0):
            inColors.append('red')
        else:
            inColors.append('green')
            
    insiderDF['Color'] = inColors

    insiderDF = {"Date":insiderDF['Date'],
                "Exchange":insiderDF['Exchange'],
                "Color": insiderDF["Color"]
    }

    return insiderDF

@app.callback(
    Output("Dividend_Data",'data'),
    Input('store-data','data')
)
def dividendData(user_stock):
    #Gets the dividend data and the percent changes
    dividends = yahoo_fin.get_dividends(user_stock,start_date = '2000-01-01' ,end_date = '2021-01-01',index_as_date = False)
    trailYield = dividends['dividend'][len(dividends['dividend']) - 1] + dividends['dividend'][len(dividends['dividend']) - 2] + dividends['dividend'][len(dividends['dividend']) - 3] + dividends['dividend'][len(dividends['dividend']) - 4]

    #Gets dividends by the year
    if(len(dividends) > 0):
        divX = dividends.groupby(dividends.date.dt.year)
        divPays = []
        divYears = []
        for key, item in divX:
            divPays.append(sum(item['dividend']))
            divYears.append(key)

        dividendData = pd.DataFrame({'Years': divYears,
                                    'Dividends': divPays})
        
    else:
        dividendData = pd.DataFrame({'Years': [np.nan],
                                    'Dividends': [np.nan]})

    dividendData = {"Years":dividendData['Years'],
                    "Dividends":dividendData['Dividends']}

    return [dividendData,trailYield]

@app.callback(
    Output("Valuation_Data",'data'),
    [Input('store-data','data'),
    Input("Sector",'data'),
    Input("Income_Statement","data"),
    Input("Earnings_Data", "data")]
)
def valuationData(user_stock,sector,incomeData,earningsData):

    IncomeDataFrame = pd.DataFrame(incomeData)

    ##Gets the Book Values for the stock
    if(sector[0] == 'Financial Services'):
        
        #Webscrapes for the name of stock
        name_soup = SoupGetter(searchVar = 'https://www.cnbc.com/quotes/{0}?qsearchterm={0}'.format(user_stock))

        #Gets the company name we need to webscrape
        CompanyName = name_soup.find(class_ = 'QuoteStrip-quoteTitle').text.lower()
        splitName = CompanyName.split(' ')

        compName = ''
        for char in splitName[0]:
            if(char == "'") or (char == "-"):
                pass
            else:
                compName += char

        #Webscrapes for pb ratios
        PBs = ValuationRatios(SoupGetter(searchVar = 'https://www.macrotrends.net/stocks/charts/{0}/{1}/price-book'.format(user_stock,compName)))

        BookValue = np.flip(PBs['EPS'])
        neoBookDates = np.flip(PBs['Dates'])

        neoPBs = pd.DataFrame({'Dates':neoBookDates,
                            'BookValues':BookValue})

        neoPBs.reset_index(inplace = True)

        compName2 = ''
        if(len(PBs) == 0):
            for string in splitName:

                if(string == f'{user_stock.lower()}:nyse'):
                    pass
                else:

                    newChar = ''

                    for char in string:
                        if(char == "'") or (char == "-"):
                            pass
                        else:
                            newChar += char

                    compName2 += f'{newChar}-'

            #Webscrapes for pb ratios again
            PBs2 = ValuationRatios(SoupGetter(searchVar = 'https://www.macrotrends.net/stocks/charts/{0}/{1}/price-book'.format(user_stock,compName2[0:-1])))

            BookValue = np.flip(PBs2['EPS'])
            neoBookDates = np.flip(PBs2['Dates'])

            neoPBs = pd.DataFrame({'Dates':neoBookDates,
                                'BookValues':BookValue})

            neoPBs.reset_index(inplace = True)
            PBs = PBs2

        else:
            pass

        compName3 = ''
        if(len(PBs2) == 0):
            for string in splitName:

                if((string == 'corp') or (string == 'inc') or (string == f'{user_stock.lower()}:nyse') or (string == '&') or (string == 'co')):
                    pass
                else:

                    newChar = ''

                    for char in string:
                        if(char == "'") or (char == "-"):
                            pass
                        else:
                            newChar += char

                    compName3 += f'{newChar}-'

            #Webscrapes for pb ratios again
            PBs3 = ValuationRatios(SoupGetter(searchVar = 'https://www.macrotrends.net/stocks/charts/{0}/{1}/price-book'.format(user_stock,compName3[0:-1])))

            BookValue = np.flip(PBs3['EPS'])
            neoBookDates = np.flip(PBs3['Dates'])

            neoPBs = pd.DataFrame({'Dates':neoBookDates,
                                'BookValues':BookValue})

            neoPBs.reset_index(inplace = True)
            PBs = PBs3
            
            #Get the prices divided by the book value to get P/B ratios
            PBdates = yahoo_fin.get_data(user_stock, start_date = PBs['Dates'][len(PBs) - 1], end_date = PBs['Dates'][0])

            PBdates.reset_index(inplace = True)
            PBdates['Date'] = PBdates['index']
            del PBdates['index']

            #Convert neoPBs into date type array
            PByears = [datetime.datetime.strptime(neoPBs['Dates'][i],'%Y-%m-%d') for i in range(0,len(neoPBs['Dates']),1)]

            #Gets the PB ratios by date
            meter = 0
            pbs = []
            bookValues = []
            for i in range(0,len(PBdates['Date']),1):
                if(PBdates['Date'][i] > PByears[meter+1]):
                    pb = PBdates['close'][i]/neoPBs['BookValues'][meter]
                    pbs.append(pb)
                    bookValues.append(neoPBs['BookValues'][meter])
                    meter += 1
                elif(meter == len(PByears)):
                    break
                else:
                    pb = PBdates['close'][i]/neoPBs['BookValues'][meter]
                    pbs.append(pb)
                    bookValues.append(neoPBs['BookValues'][meter])

            #assigns ttm PBs & BookValues per trading date
            PBdates['PB'] = pbs
            PBdates['BookValues'] = bookValues
            valuationData = {"close":PBdates['close'],
                    "PB":PBdates['PB'],
                    "BookValues": PBdates['BookValues']
            }

        else:
            pass

    elif(sector[0] == 'Real Estate/Construction'):
        
        #Gets the prices for FFO Dates to have a FFO Boxplot
        FFOdates = yahoo_fin.get_data(user_stock,start_date = str(IncomeDataFrame['Years'][0]) ,
                                        end_date = ffoX,index_as_date = False)

            #Convert the Years in income statement into timestamp
        datesFFO = [datetime.datetime.strptime(IncomeDataFrame['Years'][i],'%Y/%m/%d') for i in range(0,len(IncomeDataFrame['Years']),1)]
        datesFFO.append(ffoX)

        meter = 0
        pFFO = []
        for i in range(0,len(FFOdates),1):
            if(FFOdates['date'][i] > datesFFO[meter+1]):
                pffo = FFOdates['close'][i]/IncomeDataFrame['FFO'][meter]
                pFFO.append(pffo)
                meter += 1
            #The meter increment stops if it's 5
            elif(meter == 5):
                break
            else:
                pffo = FFOdates['close'][i]/IncomeDataFrame['FFO'][meter]
                pFFO.append(pffo)
                    
        FFOdates['pffo'] = pFFO

        valuationData = {"close":FFOdates['close'],
                        "pffo":FFOdates['pffo']}

    else:
        ###This gets the PE ratios

        #Gets the earnings dataframe
        trailingEPS = pd.DataFrame(earningsData[0])

        #This is where we get the TTM PE ratios for all closing prices
        PEdates = yahoo_fin.get_data(user_stock,start_date = str(trailingEPS['Trailing_EPS_Date'][len(trailingEPS) - 1]),
                                    end_date = str(trailingEPS['Trailing_EPS_Date'][0]))

        PEdates.reset_index(inplace = True)
        PEdates['Date'] = PEdates['index']
        del PEdates['index']

        #Convert trailingEPS dates into date type array
        PEyears = np.flip([datetime.datetime.strptime(trailingEPS['Trailing_EPS_Date'][i],'%Y-%m-%d') for i in range(0,len(trailingEPS['Trailing_EPS_Date']),1)])
        PEeps = np.flip([float(i) for i in trailingEPS['Trailing_EPS_Act']])

        #Gets the PE ratios by date
        meter = 0
        pes = []
        earningsShare = []
        for i in range(0,len(PEdates['Date']),1):
            if(PEdates['Date'][i] > PEyears[meter+1]):
                pe = PEdates['close'][i]/PEeps[meter]
                pes.append(pe)
                earningsShare.append(PEeps[meter])
                meter += 1
            elif(meter == len(PEyears)):
                break
            else:
                pe = PEdates['close'][i]/PEeps[meter]
                pes.append(pe)
                earningsShare.append(PEeps[meter])
                
        #assigns ttm PEs & EPS per trading date
        PEdates['PE'] = pes 
        PEdates['EPS'] = earningsShare
        
        valuationData = {"close":PEdates['close'],
                        "PE":PEdates['PE'],
                        "EPS":PEdates['EPS'],
                        'Date':PEdates['Date']
        }        
    
    return valuationData

#Creates the graphs-------------------------------------------------------------------------------------------- 
@app.callback(
    Output("page-content",'children'),
    [Input('Stock_Prices','data'),
    Input('url','pathname'),
    Input("Balance_Sheet","data"),
    Input("Income_Statement","data"),
    Input("Cashflow_Statement","data"),
    Input("Sector",'data'),
    Input("Insider_Data","data"),
    Input("Dividend_Data","data"),
    Input("Valuation_Data",'data'),
    Input("Earnings_Data", "data")]
)
def StockPriceGraph(stonkPricesDict,pathname,balanceSheetData,incomeStatementData,cashflowData,sector,insiderData,divData,valData,earningsData):

    #reconverts dictionary to pandas dataframe
    priceDataFrame = pd.DataFrame(stonkPricesDict)

    if(pathname == '/'):
        valRatio = pd.DataFrame(valData)

        if(list(valRatio.columns)[1] == 'PB'):
            #Assigns today's current PB Ratio
            denom = float(valRatio['BookValues'][len(valRatio['BookValues']) - 1])
            valuation = priceDataFrame['close'][len(priceDataFrame['close']) - 1]/ denom
        elif(list(valRatio.columns)[1] == 'pffo'):
            valuation = valRatio['pffo'][len(valRatio['pffo']) - 1]
        else:
            valuation = priceDataFrame['close'][len(priceDataFrame['close'])-1]/valRatio['EPS'][len(valRatio['EPS'])-1]

        #Gets the Bernoulli Probability of the Stock to go up 
        priceChanges = [100*i for i in priceDataFrame['close'].pct_change()]

        bernoulli = []
        for price in priceChanges[1:]:
            if(price >= 0):
                bernoulli.append(1)
            else:
                bernoulli.append(0)
                
        bernoulli = sum(bernoulli)/len(bernoulli)

        #Gets the Stock Price Volatilility
        volatility = statistics.stdev(priceChanges[1:])

        #Produces the Graph
        layout = go.Layout(
            title = f"{priceDataFrame['ticker'][0]}'s Price Time Series",
            font = dict(family="Arial",size=18, color="white"),
            yaxis = dict(
                title = "Stock Price",
                color = "#FFFFFF"
            ),
            xaxis = dict(
                title = 'Date',
                color = "#FFFFFF"
                ),
            plot_bgcolor = 'rgb(230,245,201)',
            paper_bgcolor='#3F3B3A'
            )   

        trace1 = go.Scatter(
            x = priceDataFrame['dates'],
            y = priceDataFrame['close'],
            mode = 'lines',
            name = "Stonk Price Time Series",
            line = dict(
                shape = 'spline'
            ),
            marker = dict(
                color = 'rgb(102,166,30)'
            )
        )

        fig = go.Figure(data = [trace1],layout = layout)
        
        return [

            dcc.Graph(id="StockPriceHist",
                    figure = fig
            ),
            html.Hr(style = {"color":"yellow"}),
            dbc.Row(
                [dbc.Col(
                    html.Div(f"Previous Close: ${round(priceDataFrame['close'][len(priceDataFrame['close']) - 1],2)}"),
                    width = {'size' : True}
                ),
                dbc.Col(
                    html.Div(f"{list(valRatio.columns)[1]} (TTM): {round(valuation,4)}"),
                    width = {'size': True}
                ),
                dbc.Col(
                    html.Div(f'Sector: {sector[0]}'),
                    width = {'size': True}
                )]
            ),
            dbc.Row(
                [dbc.Col(
                    html.Div(f'Bernoulli: {round(bernoulli,3)}'),
                    width = {'size': True}
                ),
                dbc.Col(
                    html.Div(f"Div. Yield (TTM): {round(100 * (divData[1]/priceDataFrame['close'][len(priceDataFrame['close']) - 1]),3)}%"),
                    width = {'size': True}
                ),
                dbc.Col(
                    html.Div(f"Industry: {sector[1]}"),
                    width = {'size': True}
                )]
            ),
            dbc.Row(
                [dbc.Col(
                    html.Div(f"Volatility: {round(volatility,3)}%"),
                    width = {'size': True}
                ),
                dbc.Col(
                    html.Div('Credit Rating (S&P): '),
                    width = {'size': True}
                ),
                dbc.Col(
                    html.Div("Market Cap: "),
                    width = {'size': True}
                )]
            ),
            html.Hr(style = {"color":"yellow"})
        ]

    elif(pathname == '/Balance-Sheet'):
        BalanceSheetDataFrame = pd.DataFrame(balanceSheetData)
        TAssets = pyplot1plot('Total Assets',BalanceSheetDataFrame['Years'],BalanceSheetDataFrame['Total_Assets'],
                   user_stock = priceDataFrame['ticker'][0],color1="rgb(230,245,201)", color2="rgb(102,166,30)")

        TLiabilities = pyplot1plot('Total Liabilities',BalanceSheetDataFrame['Years'],BalanceSheetDataFrame['Total_Liabilities'],
                   user_stock = priceDataFrame['ticker'][0],color1="rgb(230,245,201)", color2="rgb(102,166,30)")

        CAssets = pyplot1plot('Current Assets',BalanceSheetDataFrame['Years'],BalanceSheetDataFrame['Total_Current_Assets'],
                   user_stock = priceDataFrame['ticker'][0],color1="rgb(230,245,201)", color2="rgb(102,166,30)")

        CLiabilities = pyplot1plot('Current Liabilities',BalanceSheetDataFrame['Years'],BalanceSheetDataFrame['Total_Current_Liabilities'],
                   user_stock = priceDataFrame['ticker'][0],color1="rgb(230,245,201)", color2="rgb(102,166,30)")

        totalDebt = pyplot1plot('Total Debt',BalanceSheetDataFrame['Years'],BalanceSheetDataFrame['Total_Debt'],
                   user_stock = priceDataFrame['ticker'][0],color1="rgb(230,245,201)", color2="rgb(102,166,30)")
        
        return[
            dcc.Graph(id = 'TotalAssetsPlot',
                    figure = TAssets
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = 'TotalLiabilities',
                    figure = TLiabilities
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = 'CurrentAssets',
                    figure = CAssets 
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = 'Current Liabilities',
                    figure = CLiabilities
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "TotalDebt",
                    figure = totalDebt
            )
        ]
    
    elif(pathname == '/Income-Statement'):
        incomeDataframe = pd.DataFrame(incomeStatementData)
        trailingEPS = pd.DataFrame(earningsData[0])

        totalRevenue = pyplot1plot('Total Revenue',incomeDataframe['Years'],incomeDataframe['Revenue'],
                        user_stock = priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        shares = pyplot1plot('Shares Outstanding',incomeDataframe['Years'],incomeDataframe['Shares'],yaxe = 'Shares',
                        user_stock = priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        netIncome = pyplot1plot('Net Income',incomeDataframe['Years'],incomeDataframe['Net_Income'],user_stock = priceDataFrame['ticker'][0],
                            color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        eps = pyplot1plot('Quarterly EPS',trailingEPS['Trailing_EPS_Date'],trailingEPS['Trailing_EPS_Act'],yaxe = 'EPS (Quarterly)',
                        user_stock = priceDataFrame['ticker'][0], color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')
        
        return[
            dcc.Graph(id = 'TotalRevenue',
                    figure = totalRevenue
                    ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "netIncome",
                    figure = netIncome
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id ='shares',
                figure = shares
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(
                id = 'eps',
                figure = eps
            )
        ] 

    elif(pathname == '/Cashflow-Statement'):
        cashflowDataframe = pd.DataFrame(cashflowData)
        incomeDataframe = pd.DataFrame(incomeStatementData)
        freeCash = pyplot1plot('Free Cashflow',incomeDataframe['Years'],cashflowDataframe['Free_Cash_Flow'],
                    user_stock = priceDataFrame['ticker'][0], color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        invCash = pyplot1plot('Net Investing Cashflow',years,cashflowDataframe['Net_Investing_Cashflow'],
                    user_stock = priceDataFrame['ticker'][0], color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        ICashOCash = pyplot2plots('Net Investing Cashflow',years,abs(cashflowDataframe['Net_Investing_Cashflow']),
                   'Net Operating Cashflow',years,cashflowDataframe['Net_Operating_Cashflow'],priceDataFrame['ticker'][0],
                   color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)',color3="#FFD700")

        return[
            dcc.Graph(id = "freeCashflow",
                    figure = freeCash
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "investingCashflow",
                        figure = invCash
                ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "IOCash",
                    figure = ICashOCash
            )
        ]

    elif(pathname == '/Profitablility-Ratios'):
        #Gets the Net Profit Margin Year over Year
        IncomeDataFrame = pd.DataFrame(incomeStatementData)
        BalanceSheetDataFrame = pd.DataFrame(balanceSheetData)

        profitMargins = [100 * (IncomeDataFrame['Net_Income'][i] / IncomeDataFrame['Revenue'][i]) for i in range(0,len(IncomeDataFrame['Revenue']),1)]
        profitsMarg = pyplot1plot('Profit Margins',IncomeDataFrame['Years'],profitMargins,yaxe = '%',user_stock = priceDataFrame['ticker'][0],
                        color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        #Gets the Timeseries of the ROE for the stock
        roe = []
        for val in range(0,len(IncomeDataFrame['Net_Income']),1):
            numerator = BalanceSheetDataFrame["Shareholder's_Equity"][val]
            denominator = IncomeDataFrame['Net_Income'][val]
            roe.append((numerator/denominator))
    
        #Plots the ROE
        ROE = pyplot1plot('ROE',BalanceSheetDataFrame['Years'],roe,user_stock = priceDataFrame['ticker'][0],
                        color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        #Gets the Return on Assets timeseries for the stock
        roa = []
        for val in range(0,len(BalanceSheetDataFrame['Total_Assets']),1):
            numerator = BalanceSheetDataFrame['Total_Assets'][val]
            denominator = IncomeDataFrame['Net_Income'][val]
            roa.append((numerator/denominator))
    
        #Plots the ROA
        ROA = pyplot1plot('ROA',BalanceSheetDataFrame['Years'],roa,user_stock = priceDataFrame['ticker'][0],
                        color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')
            
        return[
            dcc.Graph(id="ProfitMargins",
                    figure = profitsMarg
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "ROE",
                    figure = ROE
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "ROA",
                    figure = ROA
            )
        ]

    elif(pathname == '/Liquidity-Ratios'):
        
        BalanceSheetDataFrame = pd.DataFrame(balanceSheetData)

        #Gets the Total & Current Ratios Graph
        TotalRatios = BalanceSheetDataFrame['Total_Liabilities']/BalanceSheetDataFrame['Total_Assets']
        CurrentRatios = BalanceSheetDataFrame['Total_Current_Liabilities']/BalanceSheetDataFrame['Total_Current_Assets']

        TAssetLiabilities =  pyplot1dash(BalanceSheetDataFrame['Years'],TotalRatios,'Total Ratios',1,'red',
                            priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        #Gets the Current Ratio
        CAssetLiabilities =  pyplot1dash(BalanceSheetDataFrame['Years'],CurrentRatios,'Current Ratios',1,'red',
                            priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        #Timeseries Graph for Quick Ratio
        if((sector[0] == 'Financial Services') or (sector[0] == 'Real Estate/Construction')):
            return[
                dcc.Graph(id = 'TotalRatioPlot',
                        figure = TAssetLiabilities
                ),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(id = "CurrentRatio",
                        figure = CAssetLiabilities
                )
            ]
        else:
            Acid = []
            for val in range(0,len(BalanceSheetDataFrame['Total_Current_Assets']),1):
                numerator = BalanceSheetDataFrame['Total_Current_Assets'][val] - BalanceSheetDataFrame['Inventories'][val]
                denominator = BalanceSheetDataFrame['Total_Current_Liabilities'][val]
                Acid.append(numerator/denominator)
                
            quickRatio = pyplot1dash(BalanceSheetDataFrame['Years'],Acid,'Quick Ratio',1,'green',
                            priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')
        
            return[
                dcc.Graph(id = 'TotalRatioPlot',
                        figure = TAssetLiabilities
                ),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(id = "CurrentRatio",
                        figure = CAssetLiabilities

                ),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(id = "quickRatio",
                    figure = quickRatio
                )
            ]

    elif(pathname == '/Solvency-Ratios'):

        IncomeDataFrame = pd.DataFrame(incomeStatementData)
        BalanceSheetDataFrame = pd.DataFrame(balanceSheetData)

        #Debt to Assets Ratio
        DebtAssets = []
        for val in range(0,len(BalanceSheetDataFrame['Total_Assets']),1):
            numerator = BalanceSheetDataFrame['Total_Debt'][val]
            denominator = BalanceSheetDataFrame['Total_Assets'][val]
            DebtAssets.append(numerator/denominator)

        debtAssets = pyplot1dash(BalanceSheetDataFrame['Years'],DebtAssets,'Debt-to-Assets Ratio',1,'red',
                        priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        #Gets the Equity Ratio Timeseries
        equityRatio = []
        for val in range(0,len(BalanceSheetDataFrame['Total_Assets']),1):
            numerator = BalanceSheetDataFrame["Shareholder's_Equity"][val]
            denominator = BalanceSheetDataFrame['Total_Assets'][val]
            equityRatio.append((numerator/denominator))

        #Plots the Equity Ratio
        equityRatio = pyplot1dash(BalanceSheetDataFrame['Years'],equityRatio,'Equity Ratio',0.5,'green',
                        priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        #Gets the Interest Coverage Ratio Timeseries
        if(sector[0] == 'Financial Services'):
            return[
                dcc.Graph(
                    id = "debtAssetsPlot",
                    figure = debtAssets
                ),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(
                    id = "equityRatio",
                    figure = equityRatio
                )
            ] 
        else:
            
            coverageRatio = []
            for val in range(0,len(IncomeDataFrame['Years']),1):
                numerator = IncomeDataFrame["Net_Income"][val] + IncomeDataFrame["Income_Tax"][val] + IncomeDataFrame["Interest_Expense"][val]
                denominator = IncomeDataFrame['Interest_Expense'][val]
                coverageRatio.append((numerator/denominator))

            #Plots the coverage ratio
            covRatio = pyplot1dash(IncomeDataFrame['Years'],coverageRatio,'Coverage Ratio',1.5,'green',
                        priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

            return[
                dcc.Graph(
                    id = "coverageRatio",
                    figure = covRatio
                ),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(id = "debtAssetsPlot",
                    figure = debtAssets
                ),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(
                    id = "equityRatio",
                    figure = equityRatio
                )
            ]
        

    elif(pathname == '/Financial-Risk-Ratios'):
        BalanceSheetDataFrame = pd.DataFrame(balanceSheetData)

        #Debt-to-Capital  Ratio Timeseries, should be below 1 to show they're under leveraged
        DebtCap = []
        for val in range(0,len(BalanceSheetDataFrame['Total_Debt']),1):
            numerator = BalanceSheetDataFrame['Total_Debt'][val]
            denominator = BalanceSheetDataFrame['Total_Debt'][val] + BalanceSheetDataFrame['Total_Equity'][val]
            DebtCap.append((numerator/denominator))
    
        #Plots Debt to Capital Timseseries
        debtCapitol = pyplot1plot('Debt-to-Capital Ratio',BalanceSheetDataFrame['Years'],DebtCap,yaxe = 'Debt-to-Capital Ratio',
                        user_stock = priceDataFrame['ticker'][0], color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')

        #Gets the Debt to Equity Ratio Timeseries
        DebtEquity = []
        for val in range(0,len(BalanceSheetDataFrame['Total_Debt']),1):
            numerator = BalanceSheetDataFrame['Total_Debt'][val]
            denominator = BalanceSheetDataFrame['Total_Equity'][val]
            DebtEquity.append((numerator/denominator))
    
        #Plots Debt to Equity Timseseries
        debtEquity = pyplot1dash(BalanceSheetDataFrame['Years'],DebtEquity,'Debt-to-Equity',2,'red',
                        priceDataFrame['ticker'][0],color2 = 'rgb(102,166,30)',color1='rgb(230,245,201)')
        
        return[
            dcc.Graph(id="DebtCapitol",
                    figure = debtCapitol
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "DebtEquity",
                    figure= debtEquity
            )
        ]

    elif(pathname == '/Dividend-Charts'):
        dividendData = pd.DataFrame(divData[0])
        CashFlowDataFrame = pd.DataFrame(cashflowData)

        #Plots the Dividend Data
        divPlot = pyplotBar(dividendData['Years'],dividendData['Dividends'],'Year','Dividends',f"{priceDataFrame['ticker'][0]} Dividend History")
        
        divPercent = pyplotBar(dividendData['Years'],[100* i for i in dividendData['Dividends'].pct_change()],
                       'Year','%',' Dividend % Change History')

        divPercs = statistics.mean([100* i for i in dividendData['Dividends'].pct_change()][-5:])

        # Shows the payout ratio over time
        payoutRatios = (abs(CashFlowDataFrame['Dividends']) / CashFlowDataFrame['Free_Cash_Flow'] ) * 100

        layout = go.Layout(
            title = " Payout Ratio Timeseries",
            font = dict(family="Arial",size=18, color="white"),
            yaxis = dict(
                title = "Payout Ratio"
                ),
            xaxis = dict(
                title = 'Date'
                ),
            showlegend = False,
            paper_bgcolor='#3F3B3A',
            plot_bgcolor = "rgb(230,245,201)"

            )

        trace1 = go.Scatter(
            x = years,
            y = payoutRatios,
            name = 'Payout Ratio',
            mode = 'lines+markers',
            line = dict(
                    shape = 'linear'
            ),
            marker = dict(
                    size = 10,
                    color = 'rgb(102,166,30)'
                )
            )

        trace2 = go.Scatter(
            x = years,
            y = [100,100,100,100,100],
            name = '100% Payout Ratio',
            mode = 'lines',
            line = dict(
                    shape = 'linear',
                    dash = 'dash'
                )
            )
            
        trace3 = go.Scatter(
            x = years,
            y = [75,75,75,75,75],
            name = '75% Payout Ratio',
            mode = 'lines',
            line = dict(
                    shape = 'linear',
                    color = 'orange',
                    dash = 'dash'
                )
            
            )

        payouts = go.Figure(data = [trace1,trace2,trace3],layout = layout)

        return[
            dbc.Row(
                [dbc.Col(
                    html.Div(f"Div. Yield (TTM): {round(100 * (divData[1]/priceDataFrame['close'][len(priceDataFrame['close']) - 1]),3)}% "),
                    width = {'size': True}
                ),
                dbc.Col(
                    html.Div(f"Div. Amount (TTM): {divData[1]}"),
                    width = {'size': True}
                ),
                dbc.Col(
                    html.Div(f"Payout Ratio (Yearly): {round(payoutRatios[4],3)}%"),
                    width = {'size': True}
                ),
                dbc.Col(
                    html.Div(f"5yr Div CAGR: {round(divPercs,3)}%"),
                    width = {'size': True}
                )]
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(
                id = "DividendGraph",
                 figure = divPlot
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "divPercent",
                    figure = divPercent
            ),
            html.Hr(style = {"color":"yellow"}),
            dcc.Graph(id = "payouts",
                    figure = payouts
            )
        ]

    elif(pathname == '/Valuation-Ratio-Charts'):
        #Turns Valuation data into a dataframe
        valuationData = pd.DataFrame(valData)

        if(sector[0] == 'Real Estate/Construction'):
            pffo = valuationData['pffo'][len(valuationData['pffo']) - 1]
            pFFO = [x for x in valuationData['pffo'] if math.isnan(x) == False]
            
            #Plots the P/FFO Boxplot
            layout = go.Layout(
            title = f"{priceDataFrame['ticker'][0]}'s P/FFO Boxplot",
            paper_bgcolor='#3F3B3A',
            plot_bgcolor = "rgb(230,245,201)",
            font = dict(family="Arial",size=18, color="white")
            )

            trace1 = go.Scatter(
                name = 'P/FFOs',
                x = pFFO,
                y = ['P/FFOs' for i in pFFO],
                marker = dict(
                    size = 10
                )

            )
            
            trace2 = go.Violin(
            x = pFFO,
            meanline_visible=True,
            name = 'P/FFOs',
            box_visible=True,
            marker_color = 'rgb(102,166,30)'

            )
            
            trace3 = go.Scatter(
            name = 'Current P/FFO(ttm)',
            x = [pffo],
            y = ['P/FFOs'],
            marker = dict(
                color = 'red',
                size = 10
                )
            )
            
            fig = go.Figure(data = [trace1,trace2,trace3],layout = layout)

            #Gets the 5 Number Summary
            
            fivNumeSum = pd.Series(pFFO[1:]).describe()

            return[
                dcc.Graph(id = 'p/ffo_boxplot',
                figure = fig
                ),
                html.Div("P/FFO Ratio 5 Number Summary:"),
                html.Div(f'Count: {round(fivNumeSum[0],3)}'),
                html.Div(f"The Mean P/FFO Ratio: {np.nanmean(pFFO[1:])}"),
                html.Div(f"Std: {round(fivNumeSum[2],3)}"),
                html.Div(f"Min: {round(fivNumeSum[3],3)}"),
                html.Div(f"Q1: {round(fivNumeSum[4],3)}"),
                html.Div(f"Median:{round(fivNumeSum[5],3)}"),
                html.Div(f"Q3: {round(fivNumeSum[6],3)}"),
                html.Div(f"Max: {round(fivNumeSum[7],3)}"),
                html.Div(f"The Current P/FFO is: {pffo}")

            ]

        elif(sector[0] == 'Financial Services'):
            pbs = [x for x in valuationData['PB'] if math.isnan(x) == False]

            #Assigns today's current PB Ratio
            denom = float(valuationData['BookValues'][len(valuationData['BookValues']) - 1])
            currPB = priceDataFrame['close'][len(priceDataFrame['close']) - 1]/ denom

            #BoxPlot for PB ratios
            layout = go.Layout(
            title = f"{priceDataFrame['ticker'][0]}'s PB Boxplot",
            paper_bgcolor='#3F3B3A',
            plot_bgcolor = "rgb(230,245,201)",
            font = dict(family="Arial",size=18, color="white")
            )

            trace1 = go.Scatter(
                name = 'PBs',
                x = pbs,
                y = ['PBs' for i in pbs],
                marker = dict(
                    size = 15
                )

            )
            
            trace2 = go.Violin(
            x = pbs,
            meanline_visible=True,
            name = 'PBs',
            box_visible=True,
            marker_color = 'rgb(102,166,30)'

            )
            
            trace3 = go.Scatter(
            name = 'Current PB(ttm)',
            x = [currPB],
            y = ['PBs'],
            marker = dict(
                color = 'red',
                size = 10
                
                )
            
            )
            
            fig = go.Figure(data = [trace1,trace2,trace3],layout = layout)
            fivNumeSum = pd.Series(pbs).describe()

            return[
                dcc.Graph(
                    id = "PB_Boxplot",
                    figure = fig
                    ),
                html.Div("P/B Ratio 5 Number Summary:"),
                html.Div(f'Count: {round(fivNumeSum[0],3)}'),
                html.Div(f"The Mean P/B Ratio: {statistics.mean(pbs)}"),
                html.Div(f"Std: {round(fivNumeSum[2],3)}"),
                html.Div(f"Min: {round(fivNumeSum[3],3)}"),
                html.Div(f"Q1: {round(fivNumeSum[4],3)}"),
                html.Div(f"Median:{round(fivNumeSum[5],3)}"),
                html.Div(f"Q3: {round(fivNumeSum[6],3)}"),
                html.Div(f"Max: {round(fivNumeSum[7],3)}"),
                html.Div(f"The Current P/B is: {currPB}")
            ]

        else:
            #Gets the EPS dataframe and estimate
            trailingEPS = pd.DataFrame(earningsData[0])
            estimate = earningsData[1]

            #Gets the current PE
            currPE = priceDataFrame['close'][len(priceDataFrame['close'])-1]/valuationData['EPS'][len(valuationData['EPS'])-1]

            #Creates Histogram, Rig Graph, & Density Plot for EPS differences
            kEPS = 0
            while 2**kEPS < len(trailingEPS['Trailing_EPS_Per']):
                kEPS += 1
            binsizeEPS = (max(trailingEPS['Trailing_EPS_Per'])-min(trailingEPS['Trailing_EPS_Per']))/kEPS

            ogEPS = ff.create_distplot([trailingEPS['Trailing_EPS_Per']],['distplot'],colors = ['green'],bin_size = binsizeEPS)

            #Conducts Bootstrapping to get a Confidence Interval for the Mean
            bootMeans = []
            for boot in range(5000):
                
                #Gets N random numbers from the Percents off
                bootSample = np.random.choice(trailingEPS['Trailing_EPS_Per'],replace = True, 
                                            size = 100)
                
                #Gets the Mean for the BootStrapped Sample
                bootMean = np.mean(bootSample)
                
                #Collects the Mean of the BootStrapped Mean
                bootMeans.append(bootMean)

            #Assuming we got a normal distribution, this block will get the 95% confidence interval of difference in EPS
            #create 95% confidence interval for population mean weight

            lowerConf = np.percentile(bootMeans,2.5)
            upperConf = np.percentile(bootMeans,97.5)

            #Gets the lower bound & upper bound of the confidence interval as a range of optimistic and pessimistic outlooks on
            #Earnings per Share

            estimatePes = ((lowerConf/100) + 1) * estimate
            estimateOpt = ((upperConf/100) + 1) * estimate
            newEstimate = ((statistics.mean(bootMeans)/100)+1) * estimate

            #This is the Bootstrapped Mean Distribution

            #Gets the number of Bins
            kBoot = 0
            while 2**kBoot < len(bootMeans):
                kBoot += 1
                
            binsizeBoot = (max(bootMeans)-min(bootMeans))/kBoot

            booties = ff.create_distplot([bootMeans],['distplot'],colors = ['green'],bin_size = binsizeBoot)
            
            #PE Box plot

            #Gets the 10yr range for PEs
            tenYr_date = Dates(datetime.datetime.now() - datetime.timedelta(days = 10 * 365))
            dataPE = valuationData[valuationData['Date'] >= tenYr_date]['PE']
            newPEs = [x for x in dataPE if math.isnan(x) == False]

            layout = go.Layout(
                title = f"{priceDataFrame['ticker'][0]}'s PE Boxplot",
                paper_bgcolor='#3F3B3A',
                font = dict(family="Arial",size=18, color="white"),
                plot_bgcolor = "rgb(230,245,201)"
                )

            trace1 = go.Scatter(
                name = 'PEs',
                x = newPEs,
                y = ['PEs' for i in newPEs],
                marker = dict(
                    size = 5
                )

            )

            trace2 = go.Scatter(
                name = 'Current PE (ttm)',
                x = [currPE],
                y = ['PEs'],
                marker = dict(
                    color = 'red',
                    size = 10
                
                )

            )

            trace3 = go.Scatter(
                name = 'Forward PE',
                x = [(priceDataFrame['close'][len(priceDataFrame['close']) - 1])/newEstimate],
                y = ['PEs'],
                marker = dict(
                    color = 'purple',
                    size = 10
                    
                    )
                
                )

            trace4 = go.Scatter(
                name = 'Optimistic Forward PE',
                x = [priceDataFrame['close'][len(priceDataFrame['close']) - 1]/estimateOpt],
                y = ['PEs'],
                marker = dict(
                    color = 'orange',
                    size = 10
                    
                    )
                
                )

            trace5 = go.Scatter(
                name = 'Pessimistic Forward PE',
                x = [priceDataFrame['close'][len(priceDataFrame['close'])-1]/estimatePes],
                y = ['PEs'],
                marker = dict(
                    color = 'orange',
                    size = 10
                    
                    )
                
                )

            trace6 = go.Violin(
                x = newPEs,
                meanline_visible=True,
                name = 'PEs',
                box_visible=True,
                marker_color = 'rgb(102,166,30)'

            )
            fivNumeSum = pd.Series(newPEs).describe()

            fig = go.Figure(data = [trace1, trace2,trace3,trace4,trace5,trace6],layout = layout)

            return[
                dcc.Graph(
                id = "EPSDifferenceDistribution",
                figure = ogEPS
                ),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(
                    id = "BootstrappedMeans",
                    figure = booties
                ),
                html.Hr(style = {"color":"yellow"}),
                html.Div(f"The Shapiro-Wilk Test for Bootstrpped Means' P-Value: {scipy.stats.shapiro(bootMeans)[1]}"),
                html.Hr(style = {"color":"yellow"}),
                html.Div(f'The Optimistic Estimate Correction: {estimateOpt}'),
                html.Div(f'The Expected Estimate Correction: {newEstimate}'),
                html.Div(f'The Pessimistic Estimate Correction: {estimatePes}'),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(
                    id = "PE_Boxplot",
                    figure = fig
                ),
                html.Hr(style = {"color":"yellow"}),
                html.Div('PE Ratio 5 Number Summary:', style={"color":"yellow"}),
                html.Div(f'Count: {round(fivNumeSum[0],3)}'),
                html.Div(f"Mean: {round(statistics.mean(newPEs),3)}"),
                html.Div(f"Std: {round(fivNumeSum[2],3)}"),
                html.Div(f"Min: {round(fivNumeSum[3],3)}"),
                html.Div(f"Q1: {round(fivNumeSum[4],3)}"),
                html.Div(f"Median:{round(fivNumeSum[5],3)}"),
                html.Div(f"Q3: {round(fivNumeSum[6],3)}"),
                html.Div(f"Max: {round(fivNumeSum[7],3)}"),
                html.Div(f"The current PE ttm Ratios is: {round(currPE,3)}"),
                html.Div(f"The Forward PE Ratio is: {round((priceDataFrame['close'][len(priceDataFrame['close'])-1])/newEstimate,3)}")
            ]

    #Produces the Macro-Economic Charts and Spearman Correlations
    elif(pathname == '/Macro-Economic-Charts'):

        #SP500 Correlation Data
        sp500 = yahoo_fin.get_data('^GSPC',start_date = str(priceDataFrame['dates'][0]),end_date = today_date)
        circPlot = pyplotScatter('S&P 500',priceDataFrame['close'],sp500['close'],'Stock Price','S&P 500 Price',priceDataFrame['ticker'][0])

        #Gets the EPS correlation data
        trailingEPS = pd.DataFrame(earningsData[0])
        trailingEPS['Trailing_EPS_Date'] = [datetime.datetime.strptime(date,'%Y-%m-%d') for date in trailingEPS['Trailing_EPS_Date']]

        earnX = trailingEPS.groupby(trailingEPS.Trailing_EPS_Date.dt.year)
        earnPays = []
        earnYears = []
        for key, item in earnX:
            earnPays.append(sum(item['Trailing_EPS_Act']))
            x = list(item['Trailing_EPS_Date'])
            earnYears.append(str(x[0])[:4])

        earnData = pd.DataFrame({'Years': earnYears,
                                'Earnings': earnPays})

        #Gets the Stock's End Year Prices
        priceDataFrame['dates'] = [datetime.datetime.strptime(date[:10],'%Y-%m-%d') for date in priceDataFrame['dates']]
        priceX = priceDataFrame.groupby(priceDataFrame.dates.dt.year)

        pricePays = []
        priceYears = []
        for key, item in priceX:
            x = list(item['dates'])
            y = list(item['close'])
            
            priceYears.append(str(x[-1])[0:4])
            pricePays.append(y[-1])
            
        priceYearly = pd.DataFrame({'Years':priceYears,
                                'Close':pricePays})

        epsPrice = pd.merge(earnData,priceYearly,on = 'Years')

        #Gets the Federal Reserve Balance Sheet buy back by end year
        fedBalanceSheet = pd.read_csv('WALCL-2.csv')
        fedBalanceSheet['DATE'] = [datetime.datetime.strptime(date[:10],'%Y-%m-%d') for date in fedBalanceSheet['DATE']]
        fedBalanceSheetX = fedBalanceSheet.groupby(fedBalanceSheet.DATE.dt.year) 
        
        balancePays = []
        balanceYears = []
        for key, item in fedBalanceSheetX:
            x = list(item['DATE'])
            y = list(item['WALCL'])
            
            balanceYears.append(str(x[-1])[0:4])
            balancePays.append(y[-1])
            
        balanceYearly = pd.DataFrame({'Years':balanceYears,
                                'Balance':balancePays})

        balancePrice = pd.merge(priceYearly,balanceYearly,on = 'Years')

        #Gets the SP500 by end year
        sp500 = sp500.reset_index()
        sp500['date'] = sp500['index']
        del sp500['index']

        sp500X = sp500.groupby(sp500.date.dt.year)
        sp500Pays = []
        sp500Years = []
        for key, item in sp500X:
            
            x = list(item['date'])
            y = list(item['close'])
            sp500Years.append(str(x[-1])[0:4])
            sp500Pays.append(y[-1])
            
        sp500Yearly = pd.DataFrame({'Years':sp500Years,
                                'S&P':sp500Pays})

        sp500Price = pd.merge(priceYearly,sp500Yearly,on = 'Years')

        #Now scatter plot for the data & rank sum correlation for the Balance Sheet, EPS
        epsCorr = pyplotScatter('Yearly EPS',epsPrice['Close'],epsPrice['Earnings'],'Yearly Stock Price',
                    'EPS (Yearly)',priceDataFrame['ticker'][0])

        balanceCorr = pyplotScatter('Yearly Fed Balance Sheet',balancePrice['Close'],balancePrice['Balance'],'Yearly Stock Price',
                    'Balance Sheet Amount (Yearly)',priceDataFrame['ticker'][0])

        sp500Corr = pyplotScatter('Yearly S&P 500 Price',sp500Price['Close'],sp500Price['S&P'],'Yearly Stock Price',
                    'S&P 500 Price (Yearly)',priceDataFrame['ticker'][0])

        return[
                dcc.Graph(
                    id = "epsCorr",
                    figure = epsCorr
                ),
                html.Div(f"The Spearman Rank Sum Correlation is: {scipy.stats.spearmanr(epsPrice['Close'],epsPrice['Earnings'])[0]}"),
                html.Div(f"The Spearman Rank Sum P-Value is: {scipy.stats.spearmanr(epsPrice['Close'],epsPrice['Earnings'])[1]}"),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(
                    id = "FedBalanceCorr",
                    figure = balanceCorr
                ),
                html.Div(f"The Spearman Rank Sum Correlation is: {scipy.stats.spearmanr(balancePrice['Close'],balancePrice['Balance'])[0]}"),
                html.Div(f"The Spearman Rank Sum P-Value is: {scipy.stats.spearmanr(balancePrice['Close'],balancePrice['Balance'])[1]}"),
                html.Hr(style = {"color":"yellow"}),
                dcc.Graph(
                    id = 'SP500Corr',
                    figure = sp500Corr
                ),
                html.Div(f"The Spearman Rank Sum Correlation is: {scipy.stats.spearmanr(sp500Price['Close'],sp500Price['S&P'])[0]}"),
                html.Div(f"The Spearman Rank Sum P-Value is: {scipy.stats.spearmanr(sp500Price['Close'],sp500Price['S&P'])[1]}")
            ]

    elif(pathname == '/Insider-Trading-Chart'):
        #Makes the dates workable
        insiderDF = pd.DataFrame(insiderData)
        neoDate = []
        for val in insiderDF['Date']:
            newDate = val[8]+val[9]+'/'+val[5]+val[6]+'/'+val[0]+val[1]+val[2]+val[3]
            neoDate.append(newDate)
            
        #Plots the Insider Trading Bar Chart
        layout = go.Layout(
            title = f"{priceDataFrame['ticker'][0]}'s Insider Trading Time Series",
            font = dict(family="Arial",size=18, color="white"),
            yaxis = dict(
                title = '$'
            ),
            xaxis = dict(
                title = 'Date'
                ),
            paper_bgcolor='#3F3B3A',
            plot_bgcolor = "rgb(230,245,201)"
            )

        trace1 = go.Bar(
            x = neoDate,
            y = insiderDF['Exchange'],
            marker_color = insiderDF['Color']
            )

        #Plots the Insider Trading Bar Chart

        fig = go.Figure(data = [trace1],layout = layout)

        return[
            dcc.Graph(
                id = "InsiderPlot",
                figure = fig
            )
        ]

    else:
        pass

#---------------------------------------------------------------------------------------------------------------
if(__name__ == '__main__'):
    app.run_server(debug=True)
