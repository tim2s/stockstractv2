## Welcome to Stockstract v2
This is the Stockstract App v2.
You can use it to donwload stock data form freely available sources and run 
simple analytics on it.

##### Gathering data
Run the App and launch (http://localhost:5000/extract/all) to extract stock data into the 
local `/data` folder. The app will be delivered with a specific data set you can use 
right away but it won't be up to date. 
Data will be stored in a specific JSON format, using the ISIN as a file name.

##### Analysing data
Data in your `/data` folder will be analysed using standard mechanisms:
* Price to Earning (P/E Ratio).
* Price to Book (P/B Ratio).
* Dividend Yield.
* Graham Number. A number from the book 'The Intelligent Investor' used to evaluate
the maximum price to be paid for a stock.
* Graham Number Ratio. Ratio between the current price and the Graham Number. 
If it is below 100 % that hints to an 'undervalued' stock.

##### Using the Analysis
Open your Web Browser on (http://localhost:5000/results/) to view the result data. 
You can use the following request parameters to find the stocks you are interested in.
* __sort__ Can be set to the following values
   * `sort=dividend-yield` Sorts by Dividend Yield Descending (highest value first)
   * `sort=price-to-book` Sorts by Price to Book Ascending, lowest value first
   * `sort=price-to-earnings` Sorts by Price to Earnings Ascending, lowest value first
   * `sort=graham_to_price` Sorts by Graham Number to Price, lowest value first
* __filter__ Can be set as follows (multiple filters work additive)
   * `min_pe=0.1` Filters P/E Ratio above 0.1
   * `max_pe=25` Filters P/E Ratio below 25
   * `min_pb=0.5` Filters P/B Ratio above 1
   * `max_pb=2` Filters P/B Ratio below 2
   * `min_dy=0.03` Filters Dividend Yield above 3.0 %
   * `max_dy=0.12` Filters Dividend Yield below 12.0 %
   * `min_gnp=0.1` Filters Graham Number to Price Ratio above 10.0 %
   * `max_gnp=1.25` Filters Graham Number to Price Ratio below 125.0 %
   * `sector=Energie` Limits to Companies from specific Sector %
   
   
##### Data Display
Colors indicate specific warnings which relate to unhealthy conditions.
* Red Earnings field - The company has an average earning below dividend. 
This is a sign that the company won't be able to pay the dividend in that height for 
long without running out of money.
* Green Dividend Yield - Yield above 4.0 %
* Yellow Dividend Yield - Yield between 3.0 % and 4.0 % 
* Green Dividend Field - Dividend is growing > 3.0 %
* Red Dividend Field - Dividend is declining
