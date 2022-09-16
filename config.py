drink_list = [
        {
                "name": "Johannsen-Cola",
                "ingredients": {
                    "rum": 40,
                    "cola": 160
                }
        }, {
                "name": "Tequila-Sunrise",
                "ingredients": {
                    "tequila": 30,
                    "lime": 10,
                    "orange": 150,
                    "syrup": 10
                }
        }, {
                "name": "Lynchburg",
                "ingredients": {
                    "whisky": 40,
                    "lime": 20,
                    "sprite": 150,
                }
        }, {
                "name": "Caipi",
                "ingredients": {
                    "rum": 40,
                    "syrup": 10,
                    "lime": 20
                }
        }, {
                "name": "Hurricane",
                "ingredients": {
                    "rum": 40,
                    "cola": 160
                }
        },
        {
                "name": "Caipi",
                "ingredients": {
                    "whisky": 40,
                    "lime": 20,
                    "sprite": 150,
                }
        }, {
                "name": "Mojito",
                "ingredients": {
                    "rum": 40,
                    "syrup": 10,
                    "lime": 20
                }
        }, {
                "name": "Long-Island",
                "ingredients": {
                    "vodka": 40,
                    "orange": 160
                }
        }
]

pump_config = [
    {
        "name": "rum",
        "GPIO": 29,
        "pump": 1
    },
    {
        "name": "tequila",
        "GPIO": 31,
        "pump": 2
    },
    {
        "name": "vodka",
        "GPIO": 33,
        "pump": 3
    },
    {
        "name": "cola",
        "GPIO": 36,
        "pump": 4
    },
    {
        "name": "sprite",
        "GPIO": 35,
        "pump": 5
    },
    {
        "name": "orange",
        "GPIO": 38,
        "pump": 6
    },
    {
        "name": "lime",
        "GPIO": 40,
        "pump": 7
    },
    {
        "name": "syrup",
        "GPIO": 37,
        "pump": 8
    },
]

main_options  = [
    {
        "name": "COCKTAILS",
        "GPIO": 20,
        "value": "rum"
    },
    {
        "name": "FLASCHEN",
        "GPIO": 20,
        "value": "rum"
    },
    {
        "name": "REINIGUNG",
        "GPIO": 20,
        "value": "rum"
    }  
]


def testing():
    test = ['rum', 'cola', 'fanta', 'sprite', 'korn']
    list = ['rum', 'fanta', 'cola','korn', 'sprite']
    list_status = 0
    for i in list:
        if i in test:
            list_status += 1
    if list_status == len(test):
        return True
    else: return False
    


print(testing())
