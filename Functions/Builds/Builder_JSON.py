import lib

def get_names_json(lang="EN"):
    if lang == "FR":
        with lib.urllib.request.urlopen("https://www.dauntless-builder.fr/map/names.json") as url:
            data = lib.json.loads(url.read().decode())
        return data
    elif lang == "EN":
        with lib.urllib.request.urlopen("https://www.dauntless-builder.com/map/names.json") as url:
            data = lib.json.loads(url.read().decode())
        return data 

def get_data_json(lang="EN"):
    if lang == "FR":
        with lib.urllib.request.urlopen("https://dauntless-builder.fr/data.json") as url:
            data = lib.json.loads(url.read().decode())
        return data    
    elif lang =="EN":
        with lib.urllib.request.urlopen("https://www.dauntless-builder.com/data.json") as url:
            data = lib.json.loads(url.read().decode())
        return data 

def get_hash(lien):
    BuildSplit = lien.split('/')
    BuildHash = BuildSplit[len(BuildSplit) - 1]
    BuildInfos = lib.hashids.decode(BuildHash)
    return BuildInfos