import plotly.graph_objs as go
from plotly.subplots import make_subplots

def candlestick(df, title = "stock_candlestick"):
  """
  df : pandas.DataFrame
    OHLCV data
  title : str
     Title of the chart
  """
  #Configures traces for prices and volume
  ohlc = go.Candlestick(x=df["date"],
                      open=df["open"],
                      high=df["high"],
                      low=df["low"],
                      close=df["close"])
  volume = go.Bar(x=df.date,y=df["volume"])

  #configure subplot with a grid of 4 rows and 1 column. OHLC will take 3 rows heigh
  fig = make_subplots(rows=4, cols=1,
                shared_xaxes=True,
                shared_yaxes=True,
                specs=[
                    [{'rowspan':3}],
                    [None],
                    [None],
                    [{}]
                  ]
                )
  #Add the 2 subplots
  fig.append_trace(ohlc, 1, 1)
  fig.append_trace(volume, 4, 1)

  fig['layout'].update(
            title=f'{title}',
            xaxis = dict(rangeslider = dict(visible = False))
            )

  fig.show()