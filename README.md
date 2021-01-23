# RobinHoodTradingBot
This is a hypothetical trading bot that uses the Robinhood API to extract data about technical indicators. It plots technical analysis data to let the user know to buy or sell the security. The project was developed in PyCharm using python. There are three files that make the essential parts of the program.

The three files are the following:

1. main.py
2. tradestrategy.py
3. plots.py

The main.py file is used for the control flow of the application. 
The tradestrategy.py file is used to calculate tehcnical analysis on an equity and then make a decision on whether to buy or sell that equity.
The plots.py file is used to plot the technical indicators from the tradestrategy.py file.

# How the Program Works

1. The user must entire their robinhood account information into the console. The password won't be visible to the user for security reasons.
![Screenshot 2021-01-23 150933](https://user-images.githubusercontent.com/60039153/105613255-91a2bc80-5d8f-11eb-94e5-dbd3d1290b5f.jpg)

2. The user then inputs the ticker of a stock or asset when prompeted (in this case it will be "AAPL").
![Screenshot 2021-01-23 151016](https://user-images.githubusercontent.com/60039153/105613286-9a938e00-5d8f-11eb-843c-ed993ed3c9d4.jpg)

3. The program will then generate 3 graphs including the moving averages, the MACD, and Bollinger Bands. Each graph shows where the most recent crossover occurred. 
![Screenshot 2021-01-23 151406](https://user-images.githubusercontent.com/60039153/105613294-9e271500-5d8f-11eb-971b-555346e55a0f.jpg)

4. The console will display information on the stock as well and then provide the user with an overall decision.
![Screenshot 2021-01-23 151506](https://user-images.githubusercontent.com/60039153/105613298-a2ebc900-5d8f-11eb-8524-b7de45f15e49.jpg)

5. The user then has a choice to continue using the program by typing in another stock ticker or entering "Done"
![Screenshot 2021-01-23 151534](https://user-images.githubusercontent.com/60039153/105613302-a67f5000-5d8f-11eb-918a-b9d16c384853.jpg)
