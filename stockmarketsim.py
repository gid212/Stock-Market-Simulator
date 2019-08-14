from bs4 import BeautifulSoup as BS
import requests
import random
import datetime

# Difficulty: 6
class Stock:
    '''
    Create a Stock class. 
    The class can take in a paramter called ticker, which is the name of the stock (Example: 'AAPL')
    If a ticker is not inputted, the user will be prompted to enter in the ticker. 

    Using beautiful soup, you will scrape stock data from the nasdaq site. You can use google and the bs4 documentation
    to figure out how to do this. 

    Your Stock class should support a method that returns the recent prices of the given stock in a clean format (perhaps an array)

    You also need a gradients method, which calculates the daily change in stock price each day. 

    '''
    def __init__(self, ticker=None):
        '''
        

        '''
        if not ticker:
            ticker = str(input('Please enter a stock ticker: '))
        self.name = ticker
        self.link = f'https://www.nasdaq.com/aspx/historical_nocp.aspx?symbol={ticker}&selected={ticker}'

        self.response = requests.get(self.link, 'html.parser')
        self.soup = BS(self.response.content, 'html.parser')
        self.price = 0
        self.clean_data
        self.gradients
        

    @property
    def raw_data(self):
        '''
        This function gets the raw data of the stock prices.
        Scrape a table from the website, removing any unnecessary white spaces.
        '''
        div = self.soup.find('div', id='historicalContainer')
        table = [data.text.strip() for data in div.findAll('td')]
        return [data for data in table if data]

    def __str__(self):
        return self.name.upper()
    
    __repr__ = __str__
    
    # Originally, I had self.raw_data in place of every 'A', but I found out that I could increase efficiency 
    # if I just stored the raw data in a variable.
    @property
    def clean_data(self):
        '''
        This function takes the raw data and cleans it up, making all the numbers
        into floats and overall just making it easier to work with. 
        '''
        A = self.raw_data
        prices  = [float(A[i].replace(',','')) for i in range(1, len(A)-1,2)]
        self.price = prices[-1]
        return prices
    
    @property
    def gradients(self):
        '''
        Input: nothing

        Output: Return a list that shows the daily change in stock price from the previous day.
        This will later be used to simulate stock changes randomly. 
        '''
        prices = self.clean_data 
        changes = [prices[i] - prices[i-1] for i in range(1,len(prices))]
        return changes

# Difficulty: 9
class Market:
    '''
    the Market class simulates a basic stock market. 

    '''
    def __init__(self):
        '''
        Make sure to have an instance attribute to keep track of the stocks in the market.
        '''
        self.stocks = {}

    def __add__(self, stock):
        '''
        NOTE: you don't need to write this function if you don't want to. 
        This is just to make the regular add function simple to write. 
        '''
        if not isinstance(stock, Stock):
            try:
                stock = Stock(stock)
            except: 
                return 'error: input is not of type Stock'

        self.stocks[stock] = stock.price

    def add(self, stock):
        '''
        Input: stock
        Add the stock to the market. 
        Output: display that it was successfully added
        '''
        self += stock

    def remove(self, stock):
        '''
        Input: stock to be removed from the market. 
        Remove the stock from the market. 
        Output: Tell them whether or not it was successfully removed. 
        '''
        for s in self.stocks:
            if str(s) == str(stock):
                self.stocks.pop(s)
                print(f'{str(stock)} successfully removed from market.')
                return
        print(f'{str(stock)} not in the market.')

    def simulate(self, days = None):
        '''
        Input: the number of days to simulate. 
        
        Simulate the action of the stock market, where prices increse or
        decrease. They should increase or decrease based on a randomly
        selected daily change from the previous daily changes (you calculated
        this in the gradients method.)

        Output: output the days simulated and then display the table for all prices of stocks (this 
        should be made in the __str__ special method.)

        '''
        if days == None:
            try:
                days = int(input('How many days would you like to simulate? Maximum of 365 per simulation: '))
            except:
                'error, not a valid input of days'
        if days < 0:
            return 'Not a valid input of days. No changes will be made.'
        
        for _ in range(days):
            for stock in self.stocks:
                next_price = round((stock.price + random.choice(stock.gradients)), 2)
                stock.clean_data.append(next_price)
                stock.price = next_price
                self.stocks[stock] = stock.price
       
        for stock in self.stocks:
            self.stocks[stock] = round(stock.price*(1 + days*.00005479452055),2)

        print(f'Days simulated: {days}')
        print(self)
    
    def __str__(self):
        '''
        Return the stocks and their prices in a nicely formatted table.
        '''
        rstring = 'MARKET:\n'
        rstring += '{:7} | {:7}'.format('Ticker', 'Price')
        for stock in self.stocks:
            rstring += '\n{:7} | ${:7}'.format(str(stock), self.stocks[stock])
        return rstring
   
    __repr__ = __str__    

    def display_price(self, stock):
        '''
        Input: stock

        Output: display the price per share of the stock. 
        '''
        return f'Price per share for {str(stock)}: {stock.price}'



# Difficulty: 4
class Trader:
    def __init__(self, money=None):
        '''
        The trader should have a balance, and should also have an instance attribute
        to keep track of all the stocks they possess. 
        '''
        if money == None:
            while True:
                try:
                    money = float(input('Please enter how much money you have: '))
                    break
                except:
                    'Invalid input of money.\n'
       
        self.money = money
        self.assets = {}

    def buy(self, market=None, stock=None, qty=1):
        '''
        Input: the market, stock, and quantity of which to buy. 

        Simulate the transaction of buying the stock. Make sure to add the stock to the trader's
        assets.

        Output: Let user know if the transaction was successfully completed. Be detailed about
        how many shares were purchased and of what stock. 
        '''
        if Market == None or Stock == None:
            return f"error, {('market', 'stock')[Market != None]} not specified"
      
        for s in market.stocks:
            if str(s) == str(stock):
                if market.stocks.get(s)*qty > self.money:
                    print('Not enough money to buy.')
                    return
                self.money -= market.stocks.get(s)*qty
                self.assets[s] = (qty, market)
                print(f"Successfully purchased {qty} share{['s', ''][qty == 1]} of {str(s)}.")
                return
       
        print('Market does not contain given stock.')
        return

    def deposit(self, money):
        '''
        Input: amount of money to deposit.
        
        Add money to the trader. Make sure they can't deposit negative money. 

        Output: print a message that shows the new balance. 
        '''
        if money < 0:
            print('Not a valid amount.')
            return
        self.money += money
        print(f'New balance: {round(self.money,2)}')
        return 

    def sell(self, market=None, stock=None, qty=1):
        '''
        Input: the market, stock, and quantity to sell (default 1)

        The trader should be able to sell their stock. 

        Output: Either tell them the transaction was successful, or if they have insufficient assets, 
        tell them the transaction wasn't successful. 
    
        '''
        if Market == None or Stock == None:
            print(f"error, {('market', 'stock')[Market != None]} not specified")
            return
        
        if str(stock) not in self.assets.keys():
            print(f'{str(stock)} not in assets.')
            return
        
        for s in market.stocks:
            if str(s) == str(stock):
                if qty > self.assets[s][0]:
                    print('Not enough stock to sell.')
                    return

                self.money += round(market.stocks.get(s)*qty,2)
                
                if qty == self.assets[s][0]: 
                    self.assets.pop(s)
                else: 
                    self.assets[s][0] -= qty
                
                print(f"Successfully sold {qty} share{['s', ''][qty == 1]} of {str(s)}.")
                return
    @property
    def net_worth(self):
        '''
        Input: Nothing

        Calculate the net worth of the trader including their current
        money and the worth of all of the stocks they own. 
        
        Should be a property method. 
        
        Output: Return a string that is formatted in terms of money: '$68.00'

        '''
        total = 0
        for stock in self.assets:
            total += self.assets[stock][1].stocks.get(stock, stock.price)*self.assets[stock][0]
        return f'${round(self.money + total, 2)}'

    def __str__(self):
        rstring = 'Net worth: {}\nAssets:\n{:7}{:10}'.format(self.net_worth, 'Name', '# of Shares')
        for stock in self.assets:
            rstring += '\n{:7}{:10}'.format(str(stock), str(self.assets[stock][0]))
        return rstring
    
    __repr__ = __str__

# Difficulty: 4
class Manager(Trader):
    '''
    The class manager should inherit from trader. Manager has all the functions of the trader, 
    but they can add and remove stocks from a market. 

    ''' 
    def __init__(self, money=None):
        super().__init__(money)

    def remove(self, market=None, stock=None):
        '''
        Input: A market and stock. 

        The manager should remove the stock from the specified market. 
        Print a message that it was successfully added. 
        
        You don't have to return anything. 
        '''

        if Market == None or Stock == None:
            print(f"error, {('market', 'stock')[Market != None]} not specified")
            return
        market.remove(stock)
        print(f'{str(stock)} removed from the market')
        return

    def add(self, market=None, stock=None):
        '''
        Input: a Market class object and a Stock class object. 

        The manager should add the specified stock to the specified market. 
        Print a message that it was successfully added. 

        You don't have to return anything. 
        '''
        if Market == None or Stock == None:
            print(f"error, {('market', 'stock')[Market != None]} not specified")
            return
        market.add(stock)
        print(f'{str(stock)} added to the market')
        return    


