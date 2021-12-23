import lib

def get_CellSlots(CellList, BuildInfos, names_json):
    for slot in lib.Builder_Config.JSONCellSlots[BuildInfos[0]]:
        if BuildInfos[slot] != 0:
            Cell = names_json["Cells"][str(BuildInfos[slot])]
            while Cell[-1:] == " ":
                Cell = Cell[:-1]
            CellList.append(Cell)

    return CellList

def get_CellArmors(CellList, BuildInfos, names_json, data_json):
    for armor in lib.Builder_Config.JSONArmours[BuildInfos[0]]:
        if BuildInfos[armor["Armour"]] != 0:
            armourID = BuildInfos[armor["Armour"]]
            armourLevel = BuildInfos[armor["Level"]]
            armourName = names_json["Armours"][str(armourID)]
            armourCell = data_json["armours"][armourName]

            Cell = armourCell["perks"][armourLevel]["name"] + " +" + str(armourCell["perks"][armourLevel]["value"])

            CellList.append(Cell)
    
    return CellList

def get_CellWeapons(CellList, BuildInfos, names_json, data_json):
    #Si c'est bondé
    if BuildInfos[lib.Builder_Config.JSONWeapons[BuildInfos[0]][1]["Weapon"]] != 0:
        weaponID = BuildInfos[lib.Builder_Config.JSONWeapons[BuildInfos[0]][1]["Weapon"]]
        weaponLevel = 1
        weaponName = names_json["Weapons"][str(weaponID)]
        weaponCell = data_json["weapons"][weaponName]

        Cell = weaponCell["perks"][weaponLevel]["name"] + " +3"
        
        CellList.append(Cell)
    else:
        weaponID = BuildInfos[lib.Builder_Config.JSONWeapons[BuildInfos[0]][0]["Weapon"]]
        weaponLevel = BuildInfos[lib.Builder_Config.JSONWeapons[BuildInfos[0]][0]["Level"]]
        weaponName = names_json["Weapons"][str(weaponID)]
        weaponCell = data_json["weapons"][weaponName]

        Cell = weaponCell["perks"][weaponLevel]["name"] + " +3"
        
        CellList.append(Cell)

    return CellList

def rank_order_effects(CellList):

    DictCell = {}
    for cell in CellList:
        if cell[:-3] in DictCell:
            DictCell[cell[:-3]] += int(cell[-1:])
        else:
            DictCell[cell[:-3]] = int(cell[-1:])

    DictCellRanked = ""
    for k, v in sorted(DictCell.items(), key=lambda x : x[1], reverse = True):
        DictCellRanked += k + " +" + str(v) + "\n"

    return DictCellRanked

def getEffects(lien, names_json, data_json, BuildInfos):
    CellList = []

    CellList = get_CellSlots(CellList, BuildInfos, names_json)
    CellList = get_CellArmors(CellList, BuildInfos, names_json, data_json)
    CellList = get_CellWeapons(CellList, BuildInfos, names_json, data_json)

    CellList = correct_CellList(CellList)

    Effects = rank_order_effects(CellList)

    return Effects

def correct_CellList(CellList):
    CellListCorrected = []
    for Cell in CellList:
        CellCorrected = ""
        if Cell[:1] == "+":
            level = Cell[:3]
            lenght = len(Cell)-3
            cellname = Cell[-lenght:]

            CellCorrected = cellname + " " + level

        if CellCorrected == "":
            CellCorrected = Cell

        CellCorrected = CellCorrected.replace(" Cell", "")

        while CellCorrected[-1:] ==" ":
            CellCorrected = CellCorrected[:len(CellCorrected)-1]

        CellListCorrected.append(CellCorrected)

    return CellListCorrected 