import lib

def get_link(data, criterias, nbr=1):

    build_link = ""
    name = ""
    hit = 1

    for row in data:
        respected_criterias = 0
        for i in range(len(criterias)):
            if row[i] == criterias[i]:
                respected_criterias += 1
        
        if respected_criterias == len(criterias):
            if hit == nbr:
                #On récupère les infos
                name = row[len(criterias) + 1]
                build_link = row[len(criterias)]

                #On compte le nombre de builds identiques.
                simplified_list = lib.copy.deepcopy(data)
                for simplified_row in simplified_list:
                    simplified_row.pop()
                    simplified_row.pop()
                    simplified_row.pop()
                build_nbr = simplified_list.count(criterias)

                return build_link, True, name, build_nbr
            else:
                hit += 1

    return build_link, False, name, 0

def update_build_link(data, link, omnicellule, arme, élément):
    for row in data:
        if row[0] == omnicellule and row[1] == arme and row[2] == élément:
            row[3]= link
            return data

def get_GoogleData(type, workbook, sheet, range):
    data = lib.GSheet.getData(type, workbook, sheet, range)
    return data

def get_sheetdata(type, workbook, range, sheetList):

    LinkListe = {}
    for Sheet in sheetList:

        LinkListe[Sheet] = []
        
        res = lib.GSheet.getData(type, workbook, Sheet, range)

        for row in res:
            
            for item in row:

                if "=HYPERLINK" in item or "=LIEN_HYPERTEXTE" in item:
                    link = item.split('"')[1]
                    name = item.split('"')[3]

                    LinkListe[Sheet].append([link, name])

    return LinkListe    

def reversed_trad(data, trad):
    for item in data:
        if data[item] == trad:
            trad = item
            break
    return trad

def get_trials_pic(currentTrial, trialPics, lang):
    if currentTrial != "" and currentTrial != "empty":

        #On récupère le lien de l'image du trial
        if currentTrial in trialPics:
            image = trialPics[currentTrial][lang]
            return True, image
        else:
            image = ""
            return True, image
    
    else:
        return False, ""

def create_embed(lang, book, liste, names_json, data_json, count, criterias, image="", nbr=1):

    #Check que le build existe
    build_link, build_exist, name, build_nbr = lib.Builds_Tools.get_link(liste, list(criterias.keys()), nbr)
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

        #embed=lib.discord.Embed(title=lib._(book, "BuildTitleRequest", lang) + f"{list(trad_criterias.keys())[0]}", \
        embed=lib.discord.Embed(title=lib._(book, "BuildTitleRequest", lang) + f"{name}", \
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

        #Components
        component = {}
        buttons = []

        #nbre
        #book
        #criterias

        if nbr > 1:
            #PreviousPage
            buttons.append(lib.create_button(style=lib.ButtonStyle.blue, label="⪡", custom_id=f"{nbr}/{book}/{criterias}/-1"))
        if nbr < build_nbr:
            #NextPage
            buttons.append(lib.create_button(style=lib.ButtonStyle.blue, label="⪢", custom_id=f"{nbr}/{book}/{criterias}/1"))
        if buttons != []:
            component = lib.create_actionrow(*buttons)

        return build_link, embed, count, component