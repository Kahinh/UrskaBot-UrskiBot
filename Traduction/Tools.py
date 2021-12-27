import lib

def _(var, lang="EN"):
    if lang not in lib.Trads.Dictionnaire:
        lang = "EN"
    
    if var not in lib.Trads.Dictionnaire[lang]:
        lang = "EN"

    translation = lib.Trads.Dictionnaire[lang][var]

    return translation