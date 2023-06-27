# Banan-asset

Live at https://banan-asset.up.railway.app


What if you'd bought Bitcoin and not another asset? This app answers with how much BTC a trade was worth at its date, and how much USD that is equivalent to today.  
The home page allows you to enter a trade, by chosing origin, destination and date. You can chose from fiat currencies, common cryptocurrencies, and common commodities.

It also allows you to log in. Once authenticated, there isn't any more to do, as it is still being worked on.  
There is a little Bitcoin price too at the top right of the page at all times.

The APIs used are the [Nasdaq commodity data](https://blog.data.nasdaq.com/api-for-commodity-data) and the [Cryptocompare API](https://min-api.cryptocompare.com/documentation). To clone this app you must get your own API keys.

This app runs on Render, using a Flask backend (Python). The database is in SQL. Some notable packages used are Flask-Login, WTForms, SQLAlchemy, and Boostrap for the CSS.
