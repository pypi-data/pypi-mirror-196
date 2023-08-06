import abc
import requests
import json

class Verify(abc.ABC):
    """
    This class is a value verifier.
    It contains a method which verifies the variable type of the parameter
    and is called by all conversion methods from measurement units classes.
    """
    def checkValue(value):
        try:
            float(value)
            return True
        except ValueError:
            print('Invalid value. Numbers only.')
            return False

class Temperature(abc.ABC):
    '''
    This class represents the temperature measurement units: Celsius, Fahrenheit and Kelvin.
    It contains conversion methods between theses units and returns float number
    as the calculations results.
    '''

    # Celsius
    def celsius2fahrenheit(temp):
        if Verify.checkValue(temp):
            return temp * 9/5 + 32

    def celsius2kelvin(temp):
        if Verify.checkValue(temp):
            return temp + 273.15 
    
    # Fahrenheit
    def fahrenheit2celsius(temp):
        if Verify.checkValue(temp):
            return (temp - 32) * 5/9
    
    def fahrenheit2kelvin(temp):
        if Verify.checkValue(temp):
            return (temp - 32) * 5/9 + 273.15

    # Kelvin
    def kelvin2celsius(temp):
        if Verify.checkValue(temp):
            return temp - 273.15

    def kelvin2fahrenheit(temp):
        if Verify.checkValue(temp):
            return (temp - 273.15) * 9/5 + 32

class Length(abc.ABC):
    '''
    This class represents the length measurement units: nanometer, micrometer
    millimeter, centimeter, meter, kilometer, inch, yard, feet and mile.
    It contains conversion methods between theses units and returns float number
    as the calculations results.
    '''

    # Nanometer
    def nanometer2micrometer(length):
        if Verify.checkValue(length):
            return length / 1000
            
    def nanometer2millimeter(length):
        if Verify.checkValue(length):
            return length / 10**6
            
    def nanometer2centimeter(length):
        if Verify.checkValue(length):
            return length / 10**7
            
    def nanometer2meter(length):
        if Verify.checkValue(length):
            return length / 10**9
            
    def nanometer2kilometer(length):
        if Verify.checkValue(length):
            return length / 10**12
                
    def nanometer2inch(length):
        if Verify.checkValue(length):
            return length / 2.54*10**7
            
    def nanometer2feet(length):
        if Verify.checkValue(length):
            return length / 3.048*10**8
            
    def nanometer2yard(length):
        if Verify.checkValue(length):
            return length / 9.144*10**8
                
    def nanometer2mile(length):
        if Verify.checkValue(length):
            return length / 1.609*10**12
            
    # Micrometer
    def micrometer2nanometer(length):
        if Verify.checkValue(length):
            return length * 1000
                
    def micrometer2millimeter(length):
        if Verify.checkValue(length):
            return length / 1000
            
    def micrometer2centimeter(length):
        if Verify.checkValue(length):
            return length / 10000
                
    def micrometer2meter(length):
        if Verify.checkValue(length):
            return length / 10**6
            
    def micrometer2kilometer(length):
        if Verify.checkValue(length):
            return length / 10**9
            
    def micrometer2inch(length):
        if Verify.checkValue(length):
            return length / 25400
            
    def micrometer2feet(length):
        if Verify.checkValue(length):
            return length / 304800
                
    def micrometer2yard(length):
        if Verify.checkValue(length):
            return length / 914400
            
    def micrometer2mile(length):
        if Verify.checkValue(length):
            return length / 1.609*10**9
            
    # Millimeter
    def millimeter2nanometer(length):
        if Verify.checkValue(length):
            return length * 10**6

    def millimeter2micrometer(length):
        if Verify.checkValue(length):
            return length * 1000

    def millimeter2centimeter(length):
        if Verify.checkValue(length):
            return length / 10
    
    def millimeter2meter(length):
        if Verify.checkValue(length):
            return length / 1000

    def millimeter2kilometer(length):
        if Verify.checkValue(length):
            return length / 10**6

    def millimeter2inch(length):
        if Verify.checkValue(length):
            return length / 25.4

    def millimeter2feet(length):
        if Verify.checkValue(length):
            return length / 304.8

    def millimeter2yard(length):
        if Verify.checkValue(length):
            return length / 914.4

    def millimeter2mile(length):
        if Verify.checkValue(length):
            return length / 1609*10**6

    # Centimeter
    def centimeter2nanometer(length):
        if Verify.checkValue(length):
            return length * 10**7
    
    def centimeter2micrometer(length):
        if Verify.checkValue(length):
            return length * 10000

    def centimeter2millimeter(length):
        if Verify.checkValue(length):
            return length * 10

    def centimeter2meter(length):
        if Verify.checkValue(length):
            return length / 100
    
    def centimeter2kilometer(length):
        if Verify.checkValue(length):
            return length / 100000

    def centimeter2inch(length):
        if Verify.checkValue(length):
            return length / 2.54
    
    def centimeter2feet(length):
        if Verify.checkValue(length):
            return length / 30.48

    def centimeter2yard(length):
        if Verify.checkValue(length):
            return length / 91.44
    
    def centimeter2mile(length):
        if Verify.checkValue(length):
            return length / 160900

    # Meter
    def meter2nanometer(length):
        if Verify.checkValue(length):
            return length * 0.000000001
                
    def meter2micrometer(length):
        if Verify.checkValue(length):
            return length * 0.000001
                
    def meter2millimeter(length):
        if Verify.checkValue(length):
            return length * 1000
            
    def meter2centimeter(length):
        if Verify.checkValue(length):
            return length * 100
            
    def meter2kilometer(length):
        if Verify.checkValue(length):
            return length / 1000
                
    def meter2inch(length):
        if Verify.checkValue(length):
            return length * 3.28084
                
    def meter2feet(length):
        if Verify.checkValue(length):
            return length * 3.28084
            
    def meter2yard(length):
        if Verify.checkValue(length):
            return length * 109361
                
    def meter2mile(length):
        if Verify.checkValue(length):
            return length / 1609
            
    # Kilometer
    def kilometer2nanometer(length):
        if Verify.checkValue(length):
            return length * 10**12
    
    def kilometer2micrometer(length):
        if Verify.checkValue(length):
            return length * 10**9
    
    def kilometer2millimeter(length):
        if Verify.checkValue(length):
            return length * 10**6
    
    def kilometer2centimeter(length):
        if Verify.checkValue(length):
            return length * 100000
    
    def kilometer2meter(length):
        if Verify.checkValue(length):
            return length * 1000
    
    def kilometer2inch(length):
        if Verify.checkValue(length):
            return length * 39370
    
    def kilometer2feet(length):
        if Verify.checkValue(length):
            return length * 3281

    def kilometer2yard(length):
        if Verify.checkValue(length):
            return length * 1094
    
    def kilometer2mile(length):
        if Verify.checkValue(length):
            return length / 1609

    def inch2nanometer(length):
        if Verify.checkValue(length):
            return length * 2.54*10**7
    
    def inch2micrometer(length):
        if Verify.checkValue(length):
            return length * 25400

    # Inch
    def inch2millimeter(length):
        if Verify.checkValue(length):
            return length * 25.4

    def inch2centimeter(length):
        if Verify.checkValue(length):
            return length * 2.5

    def inch2meter(length):
        if Verify.checkValue(length):
            return length / 39.37

    def inch2kilometer(length):
        if Verify.checkValue(length):
            return length / 39370

    def inch2feet(length):
        if Verify.checkValue(length):
            return length / 12

    def inch2yard(length):
        if Verify.checkValue(length):
            return length / 36   

    def inch2mile(length):
        if Verify.checkValue(length):
            return length / 63360

    # Feet
    def feet2nanometer(length):
        if Verify.checkValue(length):
            return length * 3.048*10**8

    def feet2micrometro(length):
        if Verify.checkValue(length):
            return length * 304800
    
    def feet2millimeter(length):
        if Verify.checkValue(length):
            return length * 304.8

    def feet2centimeter(length):
        if Verify.checkValue(length):
            return length * 30.48

    def feet2meter(length):
        if Verify.checkValue(length):
            return length * 3.281
    
    def feet2kilometer(length):
        if Verify.checkValue(length):
            return length * 3281 

    def feet2inch(length):
        if Verify.checkValue(length):
            return length * 12

    def feet2yard(length):
        if Verify.checkValue(length):
            return length / 3
    
    def feet2mile(length):
        if Verify.checkValue(length):
            return length / 5280

    # Yard
    def yard2nanometer(length):
        if Verify.checkValue(length):
            return length * 9.144*10**8
    
    def yard2micrometer(length):
        if Verify.checkValue(length):
            return length * 914400
    
    def yard2millimeter(length):
        if Verify.checkValue(length):
            return length * 914.4
    
    def yard2centimeter(length):
        if Verify.checkValue(length):
            return length * 91.44

    def yard2meter(length):
        if Verify.checkValue(length):
            return length / 1.094
        
    def yard2kilometer(length):
        if Verify.checkValue(length):
            return length / 1094

    def yard2inch(length):
        if Verify.checkValue(length):
            return length * 36
    
    def yard2feet(length):
        if Verify.checkValue(length):
            return length * 3
    
    def yard2mile(length):
        if Verify.checkValue(length):
            return length / 1760

    # Mile
    def mile2nanometer(length):
        if Verify.checkValue(length):
            return length * 1.609*10**12

    def mile2micrometer(length):
        if Verify.checkValue(length):
            return length * 1.609*10**9

    def mile2millimeter(length):
        if Verify.checkValue(length):
            return length * 1.609*10**6

    def mile2centimeter(length):
        if Verify.checkValue(length):
            return length * 160900

    def mile2meter(length):
        if Verify.checkValue(length):
            return length * 1609

    def mile2kilometer(length):
        if Verify.checkValue(length):
            return length * 1.609

    def mile2inch(length):
        if Verify.checkValue(length):
            return length * 63660
    
    def mile2feet(length):
        if Verify.checkValue(length):
            return length * 5280
    
    def mile2yard(length):
        if Verify.checkValue(length):
            return length * 1760


class Mass(abc.ABC):
    '''
    This class represents the mass measurement units: microgram, milligram, gram,
    kilogram, ton, ounce and pound.
    It contains conversion methods between theses units and returns float number
    as the calculations results.
    '''

    # Microgram
    def microgram2milligram(mass):
        if Verify.checkValue(mass):
            return mass / 1000    
    
    def microgram2gram(mass):
        if Verify.checkValue(mass):
            return mass / 10**6
    
    def microgram2kilogram(mass):
        if Verify.checkValue(mass):
            return mass / 10**9

    def microgram2ton(mass):
        if Verify.checkValue(mass):
            return mass / 10**12

    def microgram2ounce(mass):
        if Verify.checkValue(mass):
            return mass / 2.835*10**10
    
    def microgram2pound(mass):
        if Verify.checkValue(mass):
            return mass / 1000
    
    # Milligram
    def milligram2microgram(mass):
        if Verify.checkValue(mass):
            return mass * 1000
    
    def milligram2gram(mass):
        if Verify.checkValue(mass):
            return mass / 1000
    
    def milligram2kilogram(mass):
        if Verify.checkValue(mass):
            return mass / 10**6

    def milligram2ton(mass):
        if Verify.checkValue(mass):
            return mass / 10**9

    def milligram2ounce(mass):
        if Verify.checkValue(mass):
            return mass / 28350

    def milligram2pound(mass):
        if Verify.checkValue(mass):
            return mass / 453600

    # Gram
    def gram2microgram(mass):
        if Verify.checkValue(mass):
            return mass * 1*10**6

    def gram2milligram(mass):
        if Verify.checkValue(mass):
            return mass * 1000

    def gram2kilogram(mass):
        if Verify.checkValue(mass):
            return mass / 1000
    
    def gram2ton(mass):
        if Verify.checkValue(mass):
            return mass / 1*10**6
    
    def gram2ounce(mass):
        if Verify.checkValue(mass):
            return mass / 28.35

    def gram2pound(mass):
        if Verify.checkValue(mass):
            return mass / 453.3

    # Kilogram
    def kilogram2microgram(mass):
        if Verify.checkValue(mass):
            return mass * 1*10**9

    def kilogram2milligram(mass):
        if Verify.checkValue(mass):
            return mass * 10**6
    
    def kilogram2gram(mass):
        if Verify.checkValue(mass):
            return mass * 1000
    
    def kilogram2ton(mass):
        if Verify.checkValue(mass):
            return mass / 1000
    
    def kilogram2ounce(mass):
        if Verify.checkValue(mass):
            return mass * 35.274

    def kilogram2pound(mass):
        if Verify.checkValue(mass):
            return mass * 2.205
    
    # Ton
    def ton2microgram(mass):
        if Verify.checkValue(mass):
            return mass * 2.205

    def ton2microgram(mass):
        if Verify.checkValue(mass):
            return mass * 10**12

    def ton2milligram(mass):
        if Verify.checkValue(mass):
            return mass * 10**9

    def ton2gram(mass):
        if Verify.checkValue(mass):
            return mass * 10**6
    
    def ton2kilogram(mass):
        if Verify.checkValue(mass):
            return mass * 1000

    def ton2ounce(mass):
        if Verify.checkValue(mass):
            return mass * 35270

    def ton2pound(mass):
        if Verify.checkValue(mass):
            return mass * 2205

    # Ounce
    def ounce2microgram(mass):
        if Verify.checkValue(mass):
            return mass * 2.835*10**7
    
    def ounce2milligram(mass):
        if Verify.checkValue(mass):
            return mass * 28350

    def ounce2gram(mass):
        if Verify.checkValue(mass):
            return mass * 28.35

    def ounce2kilogram(mass):
        if Verify.checkValue(mass):
            return mass / 35.274
    
    def ounce2ton(mass):
        if Verify.checkValue(mass):
            return mass / 35270
    
    def ounce2pound(mass):
        if Verify.checkValue(mass):
            return mass / 16

    # Pound
    def pound2microgram(mass):
        if Verify.checkValue(mass):
            return mass * 4.536*10**8
    
    def pound2milligram(mass):
        if Verify.checkValue(mass):
            return mass * 453600
    
    def pound2gram(mass):
        if Verify.checkValue(mass):
            return mass * 453.6
    
    def pound2kilogram(mass):
        if Verify.checkValue(mass):
            return mass / 2.205
    
    def pound2ton(mass):
        if Verify.checkValue(mass):
            return mass / 2205

    def pound2ounce(mass):
        if Verify.checkValue(mass):
            return mass * 16

class Time(abc.ABC):
    '''
    This class represents the time measurement units: nanosecond, microsecond
    second, minute, hour and day.
    It contains conversion methods between theses units and returns float number
    as the calculations results.
    '''

    # Nanosecond
    def nanosecond2microsecond(time):
        if Verify.checkValue(time):    
            return time / 1000

    def nanosecond2millisecond(time):
        if Verify.checkValue(time):    
            return time / 10**6

    def nanosecond2second(time):
        if Verify.checkValue(time):    
            return time / 10**9

    def nanosecond2minuto(time):
        if Verify.checkValue(time):    
            return time / 6*10**10
    
    def nanosecond2hour(time):
        if Verify.checkValue(time):    
            return time / 3.6*10**12

    def nanosecond2day(time):
        if Verify.checkValue(time):    
            return time / 8.64*10**13

    # Microsecond
    def microsecond2nanosecond(time):
        if Verify.checkValue(time):    
            return time * 1000

    def microsecond2millisecond(time):
        if Verify.checkValue(time):    
            return time / 1000

    def microsecond2second(time):
        if Verify.checkValue(time):    
            return time / 10**6
    
    def microsecond2minuto(time):
        if Verify.checkValue(time):    
            return time / 6*10**7
    
    def microsecond2hour(time):
        if Verify.checkValue(time):    
            return time / 3.6*10**9
    
    def microsecond2day(time):
        if Verify.checkValue(time):    
            return time / 8.64*10**10

    # Millisecond
    def microsecond2nanosecond(time):
        if Verify.checkValue(time):    
            return time * 10**6

    def millisecond2second(time):
        if Verify.checkValue(time):    
            return time / 1000
    
    def millisecond2minute(time):
        if Verify.checkValue(time):    
            return time / 60000
    
    def millisecond2hour(time):
        if Verify.checkValue(time):    
            return time / 3.6 * 10**6
    
    def millisecond2day(time):
        if Verify.checkValue(time):    
            return time / 8.64*10**7

    # Second
    def second2nanosecond(time):
        if Verify.checkValue(time):    
            return time * 10**9

    def second2millisecond(time):
        if Verify.checkValue(time):    
            return time * 1000

    def second2minute(time):
        if Verify.checkValue(time):    
            return time/60
    
    def second2hour(time):
        if Verify.checkValue(time):
            return time/3600
    
    def second2day(time):
        if Verify.checkValue(time):
            return time/86400
    
    # Minute
    def minute2nanosecond(time):
        if Verify.checkValue(time):    
            return time * 6*10**10

    def minute2millisecond(time):
        if Verify.checkValue(time):    
            return time * 60000

    def minute2second(time):
        if Verify.checkValue(time):
            return time*60

    def minute2hour(time):
        if Verify.checkValue(time):
            return time/60

    def minute2day(time):
        if Verify.checkValue(time):
            return time/1440
    
    # Hour
    def hour2nanosecond(time):
        if Verify.checkValue(time):    
            return time * 3.6*10**12

    def hour2millisecond(time):
        if Verify.checkValue(time):    
            return time * 3.6*10**6

    def hour2second(time):
        if Verify.checkValue(time):
            return time*3600
    
    def hour2minute(time):
        if Verify.checkValue(time):
            return time * 60
    
    def hour2day(time):
        if Verify.checkValue(time):
            return time/24
    
    # Day
    def microsecond2millisecond(time):
        if Verify.checkValue(time):    
            return time * 8.64*10*13

    def day2millisecond(time):
        if Verify.checkValue(time):    
            return time / 8.64*10**7

    def day2second(time):
        if Verify.checkValue(time):
            return time*86400
    
    def day2minute(time):
        if Verify.checkValue(time):
            return time*1440
    
    def day2hour(time):
        if Verify.checkValue(time):
            return time*24

class Currency(abc.ABC):
    '''
    This class represents the currency in different regions of the world.
    It contains conversion methods between theses currencies and returns float number
    as the calculations results and the data is collect by the 'requests' API.
    '''

    # Padrão de conversão de moedas sem registro na API
    # 1 libra = (1/1.20) dólar
    # 1 dólar = 0.0074 iene
    # 1 libra = ((1/1.20) * 0.0074) iene
    # 1 libra = 0.0061666667 iene (aproximando para 7 casas decimais)
    
    """
    Avaible coins:
    BRL (Real Brasileiro)
    USD (Dollar)
    EUR (Euro)
    JPY (Japanese Yen)
    GBP (Pound Sterling)
    Franco Suíço (CHF)
    CAD (Canadian Dollar) 
    AUD (Australian Dollar) 
    Yuan (CNY)
    """

    # Dollar
    def USD2BRL(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/USD-BRL")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['USDBRL']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
    
    def USD2JPY(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/USD-JPY")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['USDJPY']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def USD2GBP(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/USD-GBP")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['USDGBP']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def USD2CHF(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/USD-CHF")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['USDCHF']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def USD2CAD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/USD-CAD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['USDCAD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def USD2AUD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/USD-AUD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['USDAUD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def USD2CNY(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/USD-CNY")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['USDCNY']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def USD2EUR(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/USD-EUR")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['USDEUR']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
    
    # Euro
    def EUR2BRL(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/EUR-BRL")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['EURBRL']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    def EUR2USD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/EUR-USD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['EURUSD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    def EUR2JPY(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/EUR-JPY")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['EURJPY']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def EUR2GBP(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/EUR-GBP")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['EURGBP']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def EUR2CHF(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/EUR-CHF")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['EURCHF']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def EUR2CAD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/EUR-CAD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['EURCAD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def EUR2AUD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/EUR-AUD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['EURAUD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def EUR2CNY(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/EUR-CNY")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['EURCNY']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    # Real
    def BRL2USD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/BRL-USD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['BRLUSD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    def BRL2JPY(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/BRL-JPY")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['BRLJPY']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def BRL2GBP(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/BRL-GBP")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['BRLGBP']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def BRL2CHF(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/BRL-CHF")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['BRLCHF']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def BRL2CAD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/BRL-CAD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['BRLCAD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def BRL2AUD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/BRL-AUD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['BRLAUD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def BRL2CNY(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/BRL-CNY")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['BRLCNY']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
    
    def BRL2EUR(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/BRL-EUR")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['BRLEUR']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    # Japanese Iene
    def JPY2USD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['JPYUSD']['bid'])*amount/100
                    return f'{coin:.4f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        else:
            return "Bah"
        
    def JPY2EUR(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-EUR")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['JPYEUR']['bid'])*amount/100
                    return f'{coin:.4f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def JPY2BRL(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-BRL")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['JPYBRL']['bid'])*amount/100
                    return f'{coin:.4f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
            
    def JPY2GBP(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['JPYUSD']['bid'])/100
                    c2 = float((json.loads(c2.content))['GBPUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.4f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def JPY2CHF(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['JPYUSD']['bid'])/100
                    c2 = float((json.loads(c2.content))['CHFUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.4f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def JPY2CAD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['JPYUSD']['bid'])/100
                    c2 = float((json.loads(c2.content))['CADUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.4f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def JPY2AUD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['JPYUSD']['bid'])/100
                    c2 = float((json.loads(c2.content))['AUDUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.4f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def JPY2CNY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['JPYUSD']['bid'])/100
                    c2 = float((json.loads(c2.content))['CNYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.4f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    # Libra Esterlina
    def GBP2USD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['GBPUSD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    def GBP2EUR(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-EUR")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['GBPEUR']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def GBP2BRL(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-BRL")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['GBPBRL']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
            
    def GBP2JPY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['GBPUSD']['bid'])
                    c2 = float((json.loads(c2.content))['JPYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def GBP2CHF(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['GBPUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CHFUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def GBP2CAD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['GBPUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CADUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def GBP2AUD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['GBPUSD']['bid'])
                    c2 = float((json.loads(c2.content))['AUDUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def GBP2CNY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['GBPUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CNYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    # Franco Suiço
    def CHF2USD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CHFUSD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    def CHF2EUR(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-EUR")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CHFEUR']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CHF2BRL(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-BRL")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CHFBRL']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
            
    def CHF2GBP(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CHFUSD']['bid'])
                    c2 = float((json.loads(c2.content))['GBPUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def CHF2JPY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CHFUSD']['bid'])
                    c2 = float((json.loads(c2.content))['JPYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def CHF2CAD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CHFUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CADUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def CHF2AUD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CHFUSD']['bid'])
                    c2 = float((json.loads(c2.content))['AUDUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def CHF2CNY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CHFUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CNYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    # Dollar Canadense
    def CAD2USD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CADUSD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    def CAD2EUR(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-EUR")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CADEUR']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CAD2BRL(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-BRL")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CADBRL']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
            
    def CAD2GBP(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CADUSD']['bid'])
                    c2 = float((json.loads(c2.content))['GBPUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"  

    def CAD2CHF(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CADUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CHFUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CAD2JPY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CADUSD']['bid'])
                    c2 = float((json.loads(c2.content))['JPYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CAD2AUD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CADUSD']['bid'])
                    c2 = float((json.loads(c2.content))['AUDUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CAD2CNY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CADUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CNYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    # Dollar Australiano
    def AUD2USD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['AUDUSD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    def AUD2EUR(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-EUR")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['AUDEUR']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def AUD2BRL(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-BRL")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['AUDBRL']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
            
    def AUD2GBP(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['AUDUSD']['bid'])
                    c2 = float((json.loads(c2.content))['GBPUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def AUD2CHF(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['AUDUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CHFUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def AUD2CAD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['AUDUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CADUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def AUD2JPY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['AUDUSD']['bid'])
                    c2 = float((json.loads(c2.content))['JPYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    def AUD2CNY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['AUDUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CNYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR" 

    # Yuan
    def CNY2USD(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CNYUSD']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
        
    def CNY2EUR(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-EUR")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CNYEUR']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CNY2BRL(amount):
        if Verify.checkValue(amount):
            try:    
                coin = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-BRL")
                if coin.status_code == 200:
                    coin = json.loads(coin.content)
                    coin = float(coin['CNYBRL']['bid'])*amount
                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"
            
    def CNY2GBP(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/GBP-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CNYUSD']['bid'])
                    c2 = float((json.loads(c2.content))['GBPUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"  

    def CNY2CHF(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CHF-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CNYUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CHFUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CNY2CAD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/CAD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CNYUSD']['bid'])
                    c2 = float((json.loads(c2.content))['CADUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CNY2AUD(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/AUD-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CNYUSD']['bid'])
                    c2 = float((json.loads(c2.content))['AUDUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"

    def CNY2JPY(amount):
        if Verify.checkValue(amount):
            try:    
                c1 = requests.get("http://economia.awesomeapi.com.br/json/last/CNY-USD")
                c2 = requests.get("http://economia.awesomeapi.com.br/json/last/JPY-USD")
                if c1.status_code == 200 and c1.status_code == 200:
                    c1 = float((json.loads(c1.content))['CNYUSD']['bid'])
                    c2 = float((json.loads(c2.content))['JPYUSD']['bid'])

                    if c1 > 1 and c2 > 1 or c1 < 1 and c2 < 1:
                        coin = (c1/c2)*amount
                    elif c1 < 1 and c2 > 1:
                        coin = (c1*(1/c2))*amount
                    else:
                        coin = ((1/c1)*c2)*amount

                    return f'{coin:.2f}'
                else:
                    return "Connection ERROR"
            except:
                return "Conversion ERROR"