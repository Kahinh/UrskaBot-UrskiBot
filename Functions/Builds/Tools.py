import lib

def get_build_link(data, omnicellule, arme, élément):
    build_link = ""
    for row in data:
        if row[0] == omnicellule and row[1] == arme and row[2] == élément:
            build_link = row[3]
            return build_link, True

    return build_link, False

def update_build_link(data, link, omnicellule, arme, élément):
    for row in data:
        if row[0] == omnicellule and row[1] == arme and row[2] == élément:
            row[3]= link
            return data

def get_buildsdata():
    data = lib.GSheet.getData("Builds", lib.BuildsDict.Builds_Workbook, lib.BuildsDict.Builds_Sheet, lib.BuildsDict.Builds_Range)
    lib.Pickles.DumpPickle(lib.GlobalFiles.file_BuildList, data)
    buildlist = lib.Pickles.LoadPickle(lib.GlobalFiles.file_BuildList)
    return buildlist

def get_trialdata():
    pass

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
    build_link, build_exist = lib.Builds_Tools.get_build_link(buildlist, type, weapon, element)
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
            Effects = "Cannot calculate the effects."

        #On calcule la thumbnail
        Weapon = names_json["Weapons"][str(BuildInfos[lib.Builder_Config.weapons[BuildInfos[0]]])]
        thumbnail = "https://dauntless-builder.com/" + data_json["weapons"][Weapon]["icon"]

        #On calcule la color
        if type in lib.BuildsDict.OmniColor:
            embedcolor = lib.BuildsDict.OmniColor[type]
        else:
            embedcolor = lib.BuildsDict.OmniColor['Standard']
        
        #description
        description = "__Summary of your request :__\n" \
        f"- Type : **{type}**\n" \
        f"- Weapon : **{weapon}**\n" \
        f"- Element : **{element}**" \

        #note
        note = "All **UrskaBot** builds come from the [Official Metasheet](https://docs.google.com/spreadsheets/d/1-I4LQ_8uNqV9LuybXhz2wjmcPeTNNGWRZ-kFjsckwtk/edit#gid=0).\n" \
        "Those builds are standard and optimized ones. If they didn't fit your needs, you can follow the link to the metasheet or make a request in a dedicated channel."

        embed=lib.discord.Embed(title=f"Build Request", \
        #url=f"{build_link}", \
        description=f"{description}", \
        color=embedcolor)

        embed.add_field(name="__Link__", value=f"Click here -> [Dauntless-Builder.com]({build_link})", inline=False)
        embed.add_field(name="__Cells__", value=Effects, inline=False)
        embed.add_field(name="__Notes__", value=note, inline=False)
        
        embed.set_thumbnail(url=f"{thumbnail}")
        embed.set_footer(text=f"Request n° : {count}")
        
        count += 1

    return build_link, embed, count