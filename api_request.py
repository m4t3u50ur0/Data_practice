
#importing all necessary libraries
import requests as rq
import pymongo  as mongo

# connecting to database
ip = str(input("Please input your ID for database"))
client = mongo.MongoClient(f"mongodb://localhost:{ip}/")

# selecting the database
db = client["crypto_prices"]

#singular api call
response = rq.get("https://api.coindesk.com/v1/bpi/currentprice.json")

# checking if the request was successful
print(response.status_code)
    # if 200 means the request was successful
    # if not 200 then debug error

# checking if the request was successful
def do_call(url):
    # sending the GET request to the API
    response = rq.get(url)
    if response.status_code == 200:
        # parsing the JSON response and printing it
        print(response.json())
        return response.json()
    else:
        # printing the error message if the request was not successful
        print(f"Error occurred: {response.status_code}")




# removes collection if it exists
def remove_collection(collection):
    try:
        if db[collection] != None:
            db[collection].drop()
            print("Removed " + collection)
    except:
        print('Unable to drop collection')


# checks if collection is there if not it creates collection
def create_collection_bitcoin(collection):
    try:
        if db[collection] != None: 
            remove_collection(collection)
    except:
        print('Unable to delete collection')
    finally:        
        db.create_collection(collection)
        print(f'{collection} created successfully')
    


# loops through all pages and does api call whilst printing their values

def api_call_all():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = rq.get(url)
    bitcoin_info = ''
    
    try:
        while response.json() != None:

            for current_prices in response.json():
                bitcoin_info += current_prices

    except:
        print("ERROR unable to parse JSON response")
    
    
    print(bitcoin_info)
    return bitcoin_info

# inserts into collection all pilots with their corresponding ids
def insert_into_collection():
    
    client = mongo.MongoClient("mongodb://localhost:27017/")
    db = client["crypto_prices"]
    
    create_collection_bitcoin(collection='Bitcoin')
    create_collection_bitcoin(collection='Ethereum')



    #add all prices into the database
    if api_call_all() != None:
        current_price = api_call_all()
        db['Bitcoin'].insert_one(current_price)
        print(f"Added {current_price} price to Bitcoin collection")

'''
    #add_all_prices
    for price in api_call_all():
        print(price)
        if price['bpi']:
            for currency in price['bpi']:
                db['Bitcoin'].insert_one(currency)
                print(f"Added {currency} price to Bitcoin collection")          
        print(f"Bitcoin price inserted: {price}")        
    '''
    

# Running all the functions from within the main function
def main():
    # getting the current Bitcoin price data

    bitcoin_price_data = do_call("https://api.coindesk.com/v1/bpi/currentprice.json")
    print(bitcoin_price_data)
    api_call_all()
    insert_into_collection()

# Calling main function
main()