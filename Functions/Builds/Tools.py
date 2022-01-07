import lib

def get_link(data, criterias):
    build_link = ""
    for row in data:
        respected_criterias = 0
        for i in range(len(criterias)):
            if row[i] == criterias[i]:
                respected_criterias += 1
        
        if respected_criterias == len(criterias):
            build_link = row[len(criterias)]
            return build_link, True

    return build_link, False

def update_build_link(data, link, omnicellule, arme, élément):
    for row in data:
        if row[0] == omnicellule and row[1] == arme and row[2] == élément:
            row[3]= link
            return data

def get_GoogleData(type, workbook, sheet, range, file):
    data = lib.GSheet.getData(type, workbook, sheet, range)
    lib.Pickles.DumpPickle(file, data)
    datalist = lib.Pickles.LoadPickle(file)
    return datalist

def get_trialsheetdata():

    #D'abord, on get la liste des sheets = trials
    SheetListe = lib.GSheet.get_trialsheetlist(lib.BuildsDict.Trials_Workbook)

    TrialSheetListe = {}
    for Behemoth in SheetListe:

        TrialSheetListe[Behemoth] = []
        
        res = lib.GSheet.getData("Meta", lib.BuildsDict.Trials_Workbook, Behemoth, lib.BuildsDict.Trials_Range)

        for row in res:
            
            for item in row:

                if "=HYPERLINK" in item or "=LIEN_HYPERTEXTE" in item:
                    link = item.replace('=HYPERLINK("', '')
                    link = link.replace('=LIEN_HYPERTEXTE("', '')
                    link = link.split('"')[0]

                    TrialSheetListe[Behemoth].append(link)

    return TrialSheetListe

def get_metasheetdata():
    MetaSheetListe = {}
    for omniFR in lib.BuildsDict.trad_Omni:
        omniEN = lib.BuildsDict.trad_Omni[omniFR]
        MetaSheetListe[omniEN] = []
        
        res = lib.GSheet.getData("Meta", lib.BuildsDict.Meta_Workbook, omniEN, lib.BuildsDict.Meta_Range)

        for row in res:
            
            for item in row:

                if "=HYPERLINK" in item or "=LIEN_HYPERTEXTE" in item:
                    link = item.replace('=HYPERLINK("', '')
                    link = link.replace('=LIEN_HYPERTEXTE("', '')
                    link = link.split('"')[0]

                    MetaSheetListe[omniEN].append(link)

    return MetaSheetListe

def create_build_embed(lang, buildlist, names_json, data_json, count, type, weapon, element):

    #Check que le build existe
    build_link, build_exist = lib.Builds_Tools.get_link(buildlist, [type, weapon, element])
    if build_link != "":
        
        #On change le lien si FR ou EN
        if lang == "EN":
            build_link = build_link.replace(".fr", ".com")
        elif lang == "FR":
            build_link = build_link.replace(".com", ".fr")

        BuildInfos = lib.Builder_JSON.get_hash(build_link)

        #On récupère les effets
        try:
            Effects = lib.get_Effects.getEffects(build_link, names_json, data_json, BuildInfos)
        except: 
            Effects = lib._("CantCalculateEffects", lang)

        #On calcule la thumbnail
        Weapon = names_json["Weapons"][str(BuildInfos[lib.Builder_Config.weapons[BuildInfos[0]]])]
        thumbnail = "https://dauntless-builder.com/" + data_json["weapons"][Weapon]["icon"]

        #On calcule la color
        if type in lib.BuildsDict.OmniColor:
            embedcolor = lib.BuildsDict.OmniColor[type]
        else:
            embedcolor = lib.BuildsDict.OmniColor['Standard']
        
        if lang == "FR":
            type = reversed_trad(lib.BuildsDict.trad_Omni, type)
            weapon = reversed_trad(lib.BuildsDict.trad_Weapon, weapon)
            element = reversed_trad(lib.BuildsDict.trad_Element, element)

        #description
        description = lib._("SummaryRequest", lang) \
            + "\n" + \
            lib._("Type", lang) + f" **{type}**" \
            + "\n" + \
            lib._("Weapon", lang) + f" **{weapon}**" \
            + "\n" + \
            lib._("Element", lang) + f" **{element}**" \

        #note
        note = lib._("Notes_part1", lang) \
            + "\n" + \
            lib._("Notes_part2", lang)

        embed=lib.discord.Embed(title=lib._("BuildTitleRequest", lang), \
        #url=f"{build_link}", \
        description=f"{description}", \
        color=embedcolor)

        embed.add_field(name=lib._("Link", lang), value=lib._("ClickHere", lang) + f"({build_link})", inline=False)
        embed.add_field(name=lib._("Cells", lang), value=Effects, inline=False)
        embed.add_field(name=lib._("Notes", lang), value=note, inline=False)
        
        embed.set_thumbnail(url=f"{thumbnail}")
        embed.set_footer(text=lib._("Request", lang) + f"{count}")
        
        count += 1

        return build_link, embed, count

def create_trial_embed(lang, triallist, names_json, data_json, count, behemoth, type, trialpics):

    #Check que le build existe
    build_link, build_exist = lib.Builds_Tools.get_link(triallist, [behemoth, type])
    if build_link != "":
        
        #On change le lien si FR ou EN
        if lang == "EN":
            build_link = build_link.replace(".fr", ".com")
        elif lang == "FR":
            build_link = build_link.replace(".com", ".fr")

        BuildInfos = lib.Builder_JSON.get_hash(build_link)

        #On récupère les effets
        try:
            Effects = lib.get_Effects.getEffects(build_link, names_json, data_json, BuildInfos)
        except: 
            Effects = lib._("CantCalculateEffects", lang)

        #On calcule la thumbnail
        Weapon = names_json["Weapons"][str(BuildInfos[lib.Builder_Config.weapons[BuildInfos[0]]])]
        thumbnail = "https://dauntless-builder.com/" + data_json["weapons"][Weapon]["icon"]

        #On calcule la color
        if type in lib.BuildsDict.OmniColor:
            embedcolor = lib.BuildsDict.OmniColor[type]
        else:
            embedcolor = lib.BuildsDict.OmniColor['Standard']
        
        if lang == "FR":
            type = reversed_trad(lib.BuildsDict.trad_Weapon, type)

        #description
        description = lib._("SummaryRequest", lang) \
            + "\n" + \
            lib._("Weapon", lang) + f" **{type}**"

        #note
        note = lib._("Trials_Notes_part1", lang) \
            + "\n" + \
            lib._("Trials_Notes_part2", lang)

        embed=lib.discord.Embed(title=lib._("TrialTitleRequest", lang) + behemoth, \
        #url=f"{build_link}", \
        description=f"{description}", \
        color=embedcolor)

        embed.add_field(name=lib._("Link", lang), value=lib._("ClickHere", lang) + f"({build_link})", inline=False)
        embed.add_field(name=lib._("Cells", lang), value=Effects, inline=False)
        embed.add_field(name=lib._("Notes", lang), value=note, inline=False)
        
        embed.set_thumbnail(url=f"{thumbnail}")
        embed.set_footer(text=lib._("Request", lang) + f"{count}")

        #Image
        if behemoth in trialpics:
            embed.set_image(url=trialpics[behemoth][lang])
        
        count += 1

        return build_link, embed, count

def reversed_trad(data, trad):
    for item in data:
        if data[item] == trad:
            trad = item
            break
    return trad