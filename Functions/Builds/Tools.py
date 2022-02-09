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

def get_sheetdata(type, workbook, range, sheetList):

    LinkListe = {}
    for Sheet in sheetList:

        LinkListe[Sheet] = []
        
        res = lib.GSheet.getData(type, workbook, Sheet, range)

        for row in res:
            
            for item in row:

                if "=HYPERLINK" in item or "=LIEN_HYPERTEXTE" in item:
                    link = item.replace('=HYPERLINK("', '')
                    link = link.replace('=LIEN_HYPERTEXTE("', '')
                    link = link.split('"')[0]

                    LinkListe[Sheet].append(link)

    return LinkListe    

def reversed_trad(data, trad):
    for item in data:
        if data[item] == trad:
            trad = item
            break
    return trad

def create_embed(lang, book, liste, names_json, data_json, count, criterias, image=""):

    #Check que le build existe
    build_link, build_exist = lib.Builds_Tools.get_link(liste, list(criterias.keys()))
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
            Effects = lib._(book, "CantCalculateEffects", lang)

        #On calcule la thumbnail
        Weapon = names_json["Weapons"][str(BuildInfos[lib.Builder_Config.weapons[BuildInfos[0]]])]
        thumbnail = "https://dauntless-builder.com/" + data_json["weapons"][Weapon]["icon"]

        #On calcule la color
        if list(criterias.keys())[0] in lib.BuildsDict.OmniColor:
            embedcolor = lib.BuildsDict.OmniColor[list(criterias.keys())[0]]
        else:
            embedcolor = lib.BuildsDict.OmniColor['Standard']
        
        #On trad les critères si FR
        trad_criterias =  {}
        if lang == "FR":
            for item in criterias:
                hit = 0
                for category in lib.BuildsDict.trad_Builds:
                    for trad in lib.BuildsDict.trad_Builds[category]:
                        if item == lib.BuildsDict.trad_Builds[category][trad]:
                            trad_item = reversed_trad(lib.BuildsDict.trad_Builds[category], item)
                            trad_criterias[trad_item] = criterias[item]
                            hit = 1
                if hit == 0:
                    trad_criterias[item] = criterias[item]
        else:
            trad_criterias = criterias


        #description
        description = lib._(book, "SummaryRequest", lang) \
            + "\n"
        for criteria in trad_criterias:
            description += f"- {trad_criterias[criteria]} : **{criteria}**\n"

        #note
        note = lib._(book, "Notes_part1", lang) \
            + "\n" + \
            lib._(book, "Notes_part2", lang)

        embed=lib.discord.Embed(title=lib._(book, "BuildTitleRequest", lang) + f"{list(trad_criterias.keys())[0]}", \
        #url=f"{build_link}", \
        description=f"{description}", \
        color=embedcolor)

        embed.add_field(name=lib._(book, "Link", lang), value=lib._(book, "ClickHere", lang) + f"({build_link})", inline=False)
        embed.add_field(name=lib._(book, "Cells", lang), value=Effects, inline=False)
        embed.add_field(name=lib._(book, "Notes", lang), value=note, inline=False)
        
        embed.set_thumbnail(url=f"{thumbnail}")

        if image != 0:
            embed.set_image(url=image)

        embed.set_footer(text=lib._(book, "Request", lang) + f"{count}")
        
        count += 1

        return build_link, embed, count