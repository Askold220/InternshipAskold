import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

symbol = "AAPL"
data = yf.download(symbol, start="2022-01-01", end="2022-12-31")

range_value = 15
short_boxes = []
long_boxes = []

for i in range(1, len(data)):
    structure_low = min(data['Low'][:i][-range_value:])
    
    if data['Low'][i] < structure_low:
        short_boxes.append((i - 1, i, data['Low'][i], structure_low))
    elif short_boxes and data['High'][i] > short_boxes[-1][3]:
        short_boxes[-1] = (short_boxes[-1][0], i, data['Low'][i], short_boxes[-1][3])

    elif short_boxes and data['Close'][i] > short_boxes[-1][2]:
        short_boxes.pop()

    if short_boxes and data['Close'][i] > short_boxes[-1][2]:
        long_boxes.append((i - 1, i, data['Close'][i], structure_low))
    elif long_boxes and data['Low'][i] < long_boxes[-1][3]:
        long_boxes[-1] = (long_boxes[-1][0], i, data['Close'][i], long_boxes[-1][3])

    elif long_boxes and data['Close'][i] < long_boxes[-1][2]:
        long_boxes.pop()

data['Date'] = data.index

fig = go.Figure()

fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'],
                             close=data['Close'], increasing_line_color='lime', decreasing_line_color='red',
                             name='Candlesticks'))

for box in short_boxes:
    fig.add_trace(go.Candlestick(x=[data['Date'][box[0]]], open=[box[2]], high=[box[2] + 0.1], low=[box[2]],
                                 increasing_line_color='red', decreasing_line_color='red'))

for box in long_boxes:
    fig.add_trace(go.Candlestick(x=[data['Date'][box[0]]], open=[box[2]], high=[box[2] + 0.1], low=[box[2]],
                                 increasing_line_color='green', decreasing_line_color='green'))

fig.update_layout(title='Технічний індикатор', xaxis_title='Дата', yaxis_title='Ціна закриття',
                  template="plotly_dark")  

fig.show()
