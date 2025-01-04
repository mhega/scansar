from .ListTables import printList

class Lookup:
    # For allowing storing and looking up variables using variable sets of key pairs.
    # Each key pair is a key-value pair tuple.
    # The entire set of key pair tuples uniquely stores and retreives a variable value.
    # frozenset is used to achieve the benifit of a set while ensuring immutability, so it can be hashed for use as a dictionary key.
    lookupDictionary = {}
    def put(*, keyPairs, value):
        Lookup.lookupDictionary[frozenset(keyPairs)] = value
    def get(*, keyPairs, default, matchWildcard = False): # No substring searching. only '*' can be used for searching for an entire string
        if matchWildcard and True in [bool(x) for x in [(y[1] == '*') for y in keyPairs]]:
            # If we are here, we need to match using wildcard. 
            valuedKeyPairs = set([y for y in keyPairs if not y[1] == '*'])  # Separating value pairs from wildcard pairs
            starKeyPairs = set(keyPairs) - valuedKeyPairs
            starKeyPairNames = [x[0] for x in starKeyPairs]
            return [Lookup.lookupDictionary[i] for i in Lookup.lookupDictionary.keys() if set(valuedKeyPairs).issubset(i) and sorted(starKeyPairNames) == sorted([x[0] for x in i-valuedKeyPairs])]
        return Lookup.lookupDictionary.get(frozenset(keyPairs), default)
    def getAllValues(*, keyPairs):
        # Returrns all qualifying values to part or all of the key pairs
        return [Lookup.lookupDictionary[i] for i in set(Lookup.lookupDictionary.keys()) if set(keyPairs).issubset(i)]
    def printAllItems(*, keyPairs):
        printList(('',''), [(set(i[0]), i[1]) for i in list(Lookup.lookupDictionary.items()) if set(keyPairs).issubset(set(i[0]))]) 
class utils:
    def setCacheEntry(*, zipFileName, functionName, value):
        Lookup.put(keyPairs = [('__zipFileName__',zipFileName),('__functionName__',functionName)],value=value)

    def getCacheEntry(*, zipFileName, functionName, default):
        return Lookup.get(keyPairs = [('__zipFileName__',zipFileName),('__functionName__',functionName)],default=default)
