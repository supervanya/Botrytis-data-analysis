# caching impolementation for the API requests
import requests
import json

# trurn this off to remove debugginf print statements
DEBUG = False
CACHING = True


# <----- PICKLING TO FILE ----->
# # pickling implementation
# I am trying to 'cache' the instances of class directly
# since BeautifulSoup is very slow in execusion and stores
# large unnecerray amount information on the HDD
CACHE_FNAME = 'cache.json'

def cache_init():
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
        if DEBUG == True:
            print("found JSON cache")
        return CACHE_DICTION

    # if there was no file, no worries. There will be soon!
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

    # A helper function that accepts 2 parameters
    # and returns a string that uniquely represents the request
    # that could be made with this info (url + params)


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        k.replace(" ","+")
        res.append("{}={}".format(k, params[k]))
    return baseurl + "?" + "&".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)


def cached_reqest(baseurl, params, auth=None):
    unique_ident = params_unique_combination(baseurl, params)
#     print(unique_ident)
#     print(CACHE_DICTION)

    # first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION and CACHING:
        if DEBUG == True:
            print("Getting cached data...")
            print(unique_ident)
        return CACHE_DICTION[unique_ident]

    # if not, fetch the data afresh, add it to the cache,
    # then write the cache to file
    else:
        # Make the request and cache the new data
        if auth == None:
            resp = requests.get(baseurl, params)
        else:
            resp = requests.get(baseurl, params=params, auth=auth)

        if DEBUG == True:
            print("Making a request for new data...")
            print(resp.url)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()  # Close the open file
        return CACHE_DICTION[unique_ident]


CACHE_DICTION = cache_init()
