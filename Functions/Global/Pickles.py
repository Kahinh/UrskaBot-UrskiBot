import lib

def LoadPickle(FileName):
    try:
        with open(FileName, 'rb') as picklefile:
            data = lib.pickle.load(picklefile)
            picklefile.close()
    except:
        data = []
    
    return data

def DumpPickle(FileName, data):
    with open(FileName, 'wb') as picklefile:
        lib.pickle.dump(data, picklefile)
        picklefile.close()