import lib

def _(book, var, lang="EN"):
    if book in lib.Trads.Dictionnaire["EN"]:
        if var in lib.Trads.Dictionnaire["EN"][book]:
            if lang not in lib.Trads.Dictionnaire:
                lang = "EN"
            else:
                if book not in lib.Trads.Dictionnaire[lang]:
                    lang = "EN"
                if var not in lib.Trads.Dictionnaire[lang][book]:
                    lang = "EN"
            translation = lib.Trads.Dictionnaire[lang][book][var]
        else:
            translation = "No Text Available"
    else:
        translation = "No Text Available"
    
    return translation