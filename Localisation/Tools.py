import lib

def _(var, lang="EN"):
    if var in lib.Trads.Dictionnaire["EN"]:
        if lang not in lib.Trads.Dictionnaire:
            lang = "EN"
        else:
            if var not in lib.Trads.Dictionnaire[lang]:
                lang = "EN"
        translation = lib.Trads.Dictionnaire[lang][var]
    else:
        translation = "No Text Available"
    
    return translation