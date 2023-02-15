# Project proposal

You often hear “It’s too late to get into Bitcoin now.” or “I missed out when Bitcoin was accessible.”, but is that really the case? This website will allow users to compare the price of commodities and other currencies to the price of Bitcoin at a chosen point in time (from Bitcoin’s inception , and their current exchange rate.

The targeted audience is anyone old enough to remember 2008, and interested in cryptocurrencies, so they can compare their past trades’ performance to Bitcoin.
The APIs the app will use are API for Commodity Data - Nasdaq Data Link Blog for commodities and CryptoCompare API for currency prices. They need to go back as far as possible, preferably before 2012 at least.

The rough draft of the database will look like this:  
![3rd DB schema](/Proposal/3rd_DB_schema.png)

I may run into several issues with the APIs:

- They may be offline, although they usually aren’t
- It may be hard to determine which commodities to include (including them all would be time consuming)
- The same may be the case for cryptocurrencies, although it would be easier to include them all

I will need to secure the API keys in a separate file, and exclude the file from git.

The website will allow users to enter a trade they did, or one they thought of, and see how well it fared, or would have fared, against Bitcoin. Also, there will be a little description for commodities and cryptocurrencies. This is how it will work:

1. The user creates and account (or signs in)
2. The user then searches for fiat, crypto and commodities by their symbol, name or description.
3. They add the ones they like to their list of assets
4. Then they can click any of those which will take them to a form to add a trade, which asks for:
   - The trade date
   - The amount of from asset
   - The asset they traded it for
   - Whether they want to add another trade or are done
5. Once done, they are shown a table of all the trades they entered, along with how much Bitcoin it would have been, and its current USD equivalent.
   There, they can add more trades, or edit or delete them
