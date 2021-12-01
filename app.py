import finviz

tickers = [
    'MSFT', 'AAPL' 
]

ok = finviz.get_stock('MSFT')
print(ok['P/S'])