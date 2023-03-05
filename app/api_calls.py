import requests
from time import mktime

from secret_keys import flask_secret_key, Nasdaq_key, CCompare_key
from models import Fiat_curr, Crypto_curr, Commodity, db

CC_BASE_URL = 'https://min-api.cryptocompare.com/data'
# CC_ASSET_INFO = 'https://data-api.cryptocompare.com/asset/v1/data/by/symbol'


def create_fiat_currs():
    '''Add all fiat currencies from list to DB.\n
    Only needs to be ran once (fiat currs don't change).'''
    for fiat in fiat_currs_list:
        f = Fiat_curr(symbol=fiat[0], name=fiat[1],
                      country=fiat[2], icon=fiat[3])
        db.session.add(f)
    db.session.commit()


def update_crypto_data():
    '''Get top 100 cryptos by market cap.
    If any of those cryptos are not in the db, add them.'''

    resp = requests.get(f'{CC_BASE_URL}/top/mktcapfull', params={
        'api_key': CCompare_key,
        'limit': 100,
        'tsym': 'USD'})

    current_symbols = {  # Convert from list of tuples to set of strings
        sym[0] for sym in db.session.query(Crypto_curr.symbol).all()}

    for coin in resp.json()['Data']:
        info = coin['CoinInfo']
        if info['Name'] not in current_symbols:
            c = Crypto_curr(symbol=info['Name'], name=info['FullName'])
            db.session.add(c)

    db.session.commit()


fiat_currs_list = {
    ('ALL', 'Albanian lek', 'Albania', 'Lek'),
    ('AMD', 'Armenian dram', 'Armenia', '֏'),
    ('AOA', 'Angolan kwanza', 'Angola', 'Kz'),
    ('ARS', 'Argentine peso', 'Argentine', '$'),
    ('AUD', 'Australian Dollar', 'Australia', '$'),
    ('BAM', 'Bosnia and Herzegovina convertible mark', 'Bosnia and Herzegovina', 'KM'),
    ('BDT', 'Bangladeshi taka', 'Bangladesh', '৳'),
    ('BGN', 'Bulgarian lev', 'Bulgaria', 'Lev'),
    ('BHD', 'Bahraini dinar', 'Bahrain', 'BD'),
    ('BIF', 'Burundian franc', 'Burundi', 'Fr'),
    ('BRL', 'Brazilian real', 'Brazil', 'R$'),
    ('BWP', 'Botswana pula', 'Botswana', 'P'),
    ('BYN', 'Belarusian ruble', 'Belarus', 'Rbl'),
    ('CAD', 'Canadian dollar', 'Canada', '$'),
    ('CDF', 'Congolese franc', 'Democratic Republic of the Congo', 'Fr'),
    ('CHF', 'Swiss franc', 'Switzerland', 'Fr'),
    ('CLP', 'Chilean peso', 'Chile', '$'),
    ('CNY', 'Chinese yuan', 'China', '¥'),
    ('COP', 'Colombian peso', 'Colombia', '$'),
    ('CRC', 'Costa Rican colón', 'Costa Rica', '₡'),
    ('CZK', 'Czech koruna', 'Czech Republic', 'Kč'),
    ('DKK', 'Danish krone', 'Denmark', 'kr'),
    ('DZD', 'Algerian dinar', 'Algeria', 'DA'),
    ('EGP', 'Egyptian pound', 'Egypt', 'LE'),
    ('ETB', 'Ethiopian birr', 'Ethiopia', 'Br'),
    ('EUR', 'Euro', 'European Union', '€'),
    ('GBP', 'British pound', 'United Kingdom', '£'),
    ('GEL', 'Georgian lari', 'Georgia', '₾'),
    ('GHS', 'Ghanaian cedi', 'Ghana', '₵'),
    ('GTQ', 'Guatemalan quetzal', 'Guatemala', 'Q'),
    ('HKD', 'Hong Kong dollar', 'Hong Kong', '$'),
    ('HNL', 'Honduran lempira', 'Honduras', 'L'),
    ('HUF', 'Hungarian forint', 'Hungary', 'Ft'),
    ('IDR', 'Indonesian rupiah', 'Indonesia', 'Rp'),
    ('ILS', 'Israeli new shekel', 'Israel', '₪'),
    ('INR', 'Indian rupee', 'India', '₹'),
    ('IQD', 'Iraqi dinar', 'Iraq', 'ID'),
    ('IRR', 'Iranian rial', 'Iran', 'Rl'),
    ('ISK', 'Icelandic króna', 'Iceland', 'kr'),
    ('JMD', 'Jamaican dollar', 'Jamaica', '$'),
    ('JOD', 'Jordanian dinar', 'Jordania', 'JD'),
    ('JPY', 'Japanese yen', 'Japan', '¥'),
    ('KES', 'Kenyan shilling', 'Kenya', 'Sh'),
    ('KGS', 'Kyrgyz som', 'Kyrgyzstan', 'som'),
    ('KHR', 'Cambodian riel', 'Cambodia', 'CR'),
    ('KRW', 'South Korean won', 'South Korea', '₩'),
    ('KWD', 'Kuwaiti dinar', 'Kuwait', 'KD'),
    ('KZT', 'Kazakhstani tenge', 'Kazakhstan', '₸'),
    ('LBP', 'Lebanese pound', 'Lebanon', 'LL'),
    ('MAD', 'Moroccan dirham', 'Morocco', 'DH'),
    ('MDL', 'Moldovan leu', 'Moldova', 'leu'),
    ('MMK', 'Burmese kyat', 'Myanmar', 'K'),
    ('MOP', 'Macanese pataca', 'Macau', 'MOP$'),
    ('MUR', 'Mauritian rupee', 'Mauritius', 'Re'),
    ('MVR', 'Maldivian rufiyaa', 'Maldives', 'Rf'),
    ('MWK', 'Malawian kwacha', 'Malawi', 'K'),
    ('MXN', 'Mexican peso', 'Mexico', '$'),
    ('MYR', 'Malaysian ringgit', 'Malaysia', 'RM'),
    ('NAD', 'Namibian dollar', 'Namibia', '$'),
    ('NGN', 'Nigerian naira', 'Nigeria', '₦'),
    ('NOK', 'Norwegian krone', 'Norway', 'kr'),
    ('NPR', 'Nepalese rupee', 'Nepal', 'Re'),
    ('NZD', 'New Zealand dollar', 'New Zealand', '$'),
    ('OMR', 'Omani rial', 'Oman', 'RO'),
    ('PEN', 'Peruvian sol', 'Peru',  'S/'),
    ('PGK', 'Papua New Guinean kina', 'Papua New Guinea', 'K'),
    ('PHP', 'Philippine peso', 'Philippines', '₱'),
    ('PNL', 'Polish złoty', 'Poland', 'zł'),
    ('PYG', 'Paraguayan guaraní', 'Paraguay', '₲'),
    ('QAR', 'Qatari riyal', 'Qatar', 'QR'),
    ('RON', 'Romanian leu', 'Romania', 'leu'),
    ('RSD', 'Serbian dinar', 'Serbia', 'DIN'),
    ('RUB', 'Russian ruble', 'Russia', '₽'),
    ('RWF', 'Rwandan franc', 'Rwanda', 'Rr'),
    ('SAR', 'Saudi riyal', 'Saudi Arabia', 'Rl'),
    ('SEK', 'Swedish krona', 'Sweden', 'kr'),
    ('SGD', 'Singapore dollar', 'Singapore', '$'),
    ('STN', 'São Tomé and Príncipe dobra', 'São Tomé and Príncipe', 'Db'),
    ('SYP', 'Syrian pound', 'Syria', 'LS'),
    ('THB', 'Thai baht', 'Thailand', '฿'),
    ('TMT', 'Turkmenistani manat', 'Turkmenistan', 'm'),
    ('TND', 'Tunisian dinar', 'Tunisia', 'DT'),
    ('TOP', "Tongan pa'anga", 'Tonga', 'T$'),
    ('TRY', 'Turkish lira', 'Turkey', '₺'),
    ('TTD', 'Trinidad and Tobago dollar', 'Trinidad and Tobago', '$'),
    ('TWD', 'New Taiwan dollar', 'Taiwan', '$'),
    ('TZS', 'Tanzanian shilling', 'Tanzania', 'Sh'),
    ('UAH', 'Ukrainian hryvnia', 'Ukraine', '₴'),
    ('UGX', 'Ugandan shilling', 'Uganda', 'Sh'),
    ('USD', 'United States dollar', 'United States', '$'),
    ('UYU', 'Uruguayan peso', 'Uruguay', '$'),
    ('UZS', 'Uzbekistani sum', 'Uzbekistan', 'soum'),
    ('VES', 'Venezuelan sovereign bolívar', 'Venezuela', 'Bs.S'),
    ('VND', 'Vietnamese đồng', 'Vietnam', '₫'),
    ('VUV', 'Vanuatu vatu', 'Vanuatu', 'VT'),
    ('XAF', 'Central African CFA franc', 'Central Africa', 'Fr'),
    ('XOF', 'West African CFA franc', 'West Africa', 'Fr'),
    ('ZAR', 'South African rand', 'South Africa', 'R'),
    ('ZMW', 'Zambian kwacha', 'Zambia', 'K')}


def convert(date, from_sym, amount, to_sym) -> dict:
    '''Returns amount converted to to_sym and btc equivalent at date'''
    if 'com' in from_sym and 'com' in to_sym:
        return
    elif 'com' in from_sym:
        return
    elif 'com' in to_sym:
        return

    resp = requests.get(f'{CC_BASE_URL}/pricehistorical', params={
        'fsym': 'BTC',
        'tsyms': f'{from_sym},{to_sym}',
        'ts': mktime(date.timetuple())})
    rates = resp.json()['BTC']

    # | btc |  fsym  |  tsym  |
    # |  1  | r[f_s] | r[t_s] |
    # |  ?  |  amnt  |   ?    |
    btc_equiv = amount / rates[from_sym]
    tsym_equiv = rates[to_sym] * amount / rates[from_sym]

    return (btc_equiv, tsym_equiv)
