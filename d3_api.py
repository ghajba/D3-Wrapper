import urllib
import json

US_SERVER = 'http://us.battle.net'
EU_SERVER = 'http://eu.battle.net'
KOREA_SERVER = 'http://kr.battle.net'
TAIWAN_SERVER = 'http://tw.battle.net'
SOUTHEAST_ASIA_SERVER = 'http://sea.battle.net'

MEDIA_SERVER = "http://media.blizzard.com/d3/icons"

KNOWN_ATTRIBUTES = ['Durability_Cur',
'Damage_Percent_Reduction_From_Ranged',
'Item_LegendaryItem_Level_Override',
'Armor_Item',
'Season',
'Durability_Max',
'Resistance_All',
'Hitpoints_On_Hit',
'Item_Legendary_Item_Base_Item',
'Item_Binding_Level_Override',
'Durability_Max_Before_Reforge',
'Sockets',
'Gold_PickUp_Radius',
'Armor_Bonus_Item',
'Damage_Weapon_Percent_Bonus#Physical',
'Weapon_On_Hit_Chill_Proc_Chance',
'Hitpoints_On_Kill',
'Damage_Weapon_Delta#Physical',
'Damage_Weapon_Min#Fire',
'Attacks_Per_Second_Item_Percent',
'Intelligence_Item',
'Damage_Weapon_Delta#Fire',
'Damage_Weapon_Min#Physical',
'Attacks_Per_Second_Item',
'Crit_Percent_Bonus_Capped',
'Resistance#Arcane',
'Attacks_Per_Second_Percent',
'Experience_Bonus',
'Vitality_Item',
'Hitpoints_Regen_Per_Second',
'Item_Power_Passive#ItemPassive_Unique_Ring_651_x1',
'Item_Power_Passive#ItemPassive_Unique_Ring_593_x1',
'Power_Cooldown_Reduction_Percent_All',
'Damage_Delta#Physical',
'Damage_Min#Physical',
'Resource_Max_Bonus#Arcanum',
'On_Hit_Blind_Proc_Chance',
'Resistance#Poison',
'Item_Power_Passive#ItemPassive_Unique_Shoulder_002_x1',
'Hitpoints_Max_Percent_Bonus_Item',
'Health_Globe_Bonus_Health',
'Power_Damage_Percent_Bonus#Wizard_EnergyTwister',
'Crit_Damage_Percent',
'Resistance#Cold',
'Resource_Cost_Reduction_Percent_All',
'Gold_Find',
'IsCrafted',
'Item_Power_Passive#ItemPassive_Unique_Ring_589_x1',
'Resource_Max_Bonus#Mana',
'Item_Power_Passive#ItemPassive_Unique_Ring_526_x1',
'Resource_Regen_Per_Second#Mana',
'Resistance#Fire',
'Power_Damage_Percent_Bonus#Witchdoctor_Gargantuan',
'Power_Damage_Percent_Bonus#Witchdoctor_ZombieCharger',
'Thorns_Fixed#Physical',
'Item_Power_Passive#ItemPassive_Unique_Ring_520_x1',
'Damage_Weapon_Min#Lightning',
'Dexterity_Item',
'Damage_Weapon_Delta#Lightning',
'Resource_Max_Bonus#Spirit',
'Damage_Dealt_Percent_Bonus#Physical',
'CrowdControl_Reduction',
'Power_Damage_Percent_Bonus#Monk_SevenSidedStrike',
'Movement_Scalar',
'Resistance#Lightning',
'Power_Damage_Percent_Bonus#Monk_LashingTailKick',
'Splash_Damage_Effect_Percent',
'On_Hit_Knockback_Proc_Chance',
'Item_Power_Passive#ItemPassive_Unique_Ring_636_x1',
'Damage_Dealt_Percent_Bonus#Fire']

class Rune():
    def __init__(self, rune_data):
        self.name = rune_data['name']
        self.description = rune_data['description']
        self.skill_calc_id = rune_data['skillCalcId']
        self.type = rune_data['type']
        self.order = rune_data['order']

class Skill:
    def __init__(self, name, description, skill_calc_id, icon):
        self.name = name
        self.description = description
        self.skill_calc_id = skill_calc_id
        self.icon = icon
        self.icon_url_21 = "%s/skills/21/%s.png"%(MEDIA_SERVER,self.icon)
        self.icon_url_64 = "%s/skills/64/%s.png"%(MEDIA_SERVER,self.icon)

class ActiveSkill(Skill):
    def __init__(self, skill_data, rune_data):
        Skill.__init__(self, skill_data['name'], skill_data['description'], skill_data['skillCalcId'], skill_data['icon'])
        self.simple_description = skill_data['simpleDescription']
        self.rune = Rune(rune_data)


class PassiveSkill(Skill):
    def __init__(self, skill_data):
        Skill.__init__(self, skill_data['name'], skill_data['description'], skill_data['skillCalcId'], skill_data['icon'])
        self.flavor = skill_data['flavor']

class Attribute:
    def __init__(self, attribute_data):
        self.text = attribute_data['text']
        self.affix_type = attribute_data['affixType']

class RawAttribute:
    def __init__(self, min_value, max_value):
        self.min = min_value
        self.max = max_value

class AttributeSet:
    def __init__(self, attribute_data):
        for key in attribute_data.keys():
            if key not in KNOWN_ATTRIBUTES:
                print "'"+key+"',"

class Gem():
    def __init__(self, host, gem_data):
        self.host = host
        self.icon = gem_data['item']['icon']
        self.tooltip_params = gem_data['item']['tooltipParams']
        self.id = gem_data['item']['id']
        self.name = gem_data['item']['name']
        if len(gem_data['attributes']['primary']) > 0:
            self.text = gem_data['attributes']['primary'][0]['text']
        if len(gem_data['attributes']['secondary']) > 0:
            self.text = gem_data['attributes']['secondary'][0]['text']
        if len(gem_data['attributes']['passive']) > 0:
            self.text = gem_data['attributes']['passive'][0]['text']
        self.loaded = False


    def load_gem(self):
        gem_data = get_complete_item(self.host, self.tooltipParams)
        self.loaded = True

    def get_details(self):
        if not self.loaded:
            self.load_gem()
        return self
        

class ItemType:
    def __init__(self, type_id, two_handed, name):
        self.id = type_id
        self.two_handed = two_handed
        self.name = name

class Item:
    def __init__(self, host, item_data):
        self.host = host
        self.name = item_data['name']
        self.crafted_by = item_data['craftedBy']
        self.id = item_data['id']
        self.icon = item_data['icon']
        self.icon_url_large = "%s/items/large/%s.png"%(MEDIA_SERVER,self.icon)
        self.icon_url_small = "%s/items/large/%s.png"%(MEDIA_SERVER,self.icon)
        self.display_color = item_data['displayColor']
        self.tooltip_params = item_data['tooltipParams']
        self.random_affixes = item_data['randomAffixes']
        self.loaded = False

    def load_item(self):
        item_data = get_complete_item(self.host, self.tooltip_params)
        self.armor = item_data['armor'] if 'armor' in item_data else None
        self.account_bound = item_data['accountBound'] == 'True'
        self.required_level = item_data['requiredLevel']
        self.type = ItemType(item_data['type']['id'], item_data['type']['twoHanded']=='True', item_data['typeName'])
        self.flavor_text = item_data['flavorText'] if 'flavorText' in item_data else None
        self.item_level = item_data['itemLevel']
        self.bonus_affixes = item_data['bonusAffixes']
        self.bonus_affixes_max = item_data['bonusAffixesMax']
        self.gems = [Gem(self.host, gem) for gem in item_data['gems']]
        self.primary_attributes = [Attribute(data) for data in item_data['attributes']['primary']]
        self.secondary_attributes = [Attribute(data) for data in item_data['attributes']['secondary']]
        self.passive_attributes = [Attribute(data) for data in item_data['attributes']['passive']]
        # item_data['socketEffects'] #TODO find an item with socketEffects
        # item_data['randomAffixes'] #TODO find item with random affixes
        self.attributeSet = AttributeSet(item_data['attributesRaw'])

        self.loaded = True

    def get_details(self):
        if not self.loaded:
            self.load_item()
        return self


class ItemSet:
    def __init__(self, host, items):
        self.main_hand = Item(host, items['mainHand']) if 'mainHand' in items else None
        self.head = Item(host, items['head']) if 'head' in items else None
        self.waist = Item(host, items['waist']) if 'waist' in items else None
        self.off_hand = Item(host, items['offHand']) if 'offHand' in items else None
        self.neck = Item(host, items['neck']) if 'neck' in items else None
        self.shoulders = Item(host, items['shoulders']) if 'shoulders' in items else None
        self.feet = Item(host, items['feet']) if 'feet' in items else None
        self.right_finger = Item(host, items['rightFinger']) if 'rightFinger' in items else None
        self.left_finger = Item(host, items['leftFinger']) if 'leftFinger' in items else None
        self.hands = Item(host, items['hands']) if 'hands' in items else None
        self.legs = Item(host, items['legs']) if 'legs' in items else None
        self.bracers = Item(host, items['bracers']) if 'bracers' in items else None
        self.torso = Item(host, items['torso']) if 'torso' in items else None
        self.items = list()
        if self.main_hand is not None:
            self.items.append(self.main_hand)
        if self.head is not None:
            self.items.append(self.head)
        if self.waist is not None:
            self.items.append(self.waist)
        if self.off_hand is not None:
            self.items.append(self.off_hand)
        if self.neck is not None:
            self.items.append(self.neck)
        if self.shoulders is not None:
            self.items.append(self.shoulders)
        if self.feet is not None:
            self.items.append(self.feet)
        if self.right_finger is not None:
            self.items.append(self.right_finger)
        if self.left_finger is not None:
            self.items.append(self.left_finger)
        if self.hands is not None:
            self.items.append(self.hands)
        if self.legs is not None:
            self.items.append(self.legs)
        if self.bracers is not None:
            self.items.append(self.bracers)
        if self.torso is not None:
            self.items.append(self.torso)


class Follower:
    def __init__(self, host, follower_type, follower_data):
        self.type = follower_type
        self.skills = [Skill(skill['skill']['name'], skill['skill']['description'], skill['skill']['skillCalcId'], skill['skill']['icon']) for skill in follower_data['skills'] if len(skill.keys()) > 0]
        items = follower_data['items']
        self.main_hand = Item(host, items['mainHand']) if 'mainHand' in items else None
        self.off_hand = Item(host, items['offHand']) if 'offHand' in items else None
        self.neck = Item(host, items['neck']) if 'neck' in items else None
        self.right_finger = Item(host, items['rightFinger']) if 'rightFinger' in items else None
        self.left_finger = Item(host, items['leftFinger']) if 'leftFinger' in items else None
        self.special = Item(host, items['special']) if 'special' in items else None
        self.magic_find = follower_data['stats']['magicFind']
        self.gold_find = follower_data['stats']['goldFind']
        self.experience_bonus = follower_data['stats']['experienceBonus']

class Hero:
    def __init__(self, hero_data, battle_tag, host):
        self.battle_tag = battle_tag
        self.host = host
        self.name = hero_data['name']
        self.id = hero_data['id']
        self.level = hero_data['level']
        self.charecter_class = hero_data['class']
        self.hardcore = hero_data['hardcore'] == 'True'
        self.dead = hero_data['dead'] == 'True'
        self.loaded = False

    def __str__(self):
        hero = "%s (level %s %s)"%(self.name, self.level, self.charecter_class)
        if self.hardcore:
            hero += ' a'
            if self.dead:
                hero += ' dead'
            hero += ' hardcore hero'
        return hero

    def load_hero_data(self):
        hero_details = get_hero(self.host, self.battle_tag, self.id)
        gender = hero_details['gender']
        if gender == 0:
            self.gender = 'Male'
        else:
            self.gender = 'Female'

        stats = hero_details['stats']
        self.strength = stats['strength']
        self.dexterity = stats['dexterity']
        self.intelligence = stats['intelligence']
        self.vitality = stats['vitality']
        
        self.life = stats['life']
        self.primaryResource = stats['primaryResource']
        self.secondaryResource = stats['secondaryResource']

        self.attack_speed = stats['attackSpeed']
        self.damage = stats['damage']
        self.damage_increase = stats['damageIncrease']
        self.critical_chance = stats['critChance']
        self.critical_damage = stats['critDamage']

        self.life_steal = stats['lifeSteal']
        self.life_on_hit = stats['lifeOnHit']
        self.life_per_kill = stats['lifePerKill']
        
        self.arcane_resist = stats['arcaneResist']
        self.fire_resist = stats['fireResist']
        self.lightning_resist = stats['lightningResist']
        self.poison_resist = stats['poisonResist']
        self.cold_resist = stats['coldResist']
        self.physical_resist = stats['physicalResist']

        self.armor = stats['armor']
        self.block_chance = stats['blockChance']
        self.block_amount_min = stats['blockAmountMin']
        self.block_amount_max = stats['blockAmountMax']
        self.damage_reduction = stats['damageReduction']

        self.gold_find = stats['goldFind']
        self.magic_find = stats['magicFind']
        self.thorns = stats['thorns']

        self.elites = hero_details['kills']['elites']
        
        skills = hero_details['skills']
        self.active_skills = [ActiveSkill(skill['skill'], skill['rune']) for skill in skills['active'] if len(skill.keys()) > 0]
        self.passive_skills = [PassiveSkill(skill['skill']) for skill in skills['passive'] if len(skill.keys()) > 0]
        
        self.items = ItemSet(self.host, hero_details['items'])

        followers = hero_details['followers']
        self.templar = Follower(self.host, 'Templar', followers['templar']) if 'templar' in followers else None
        self.scoundrel = Follower(self.host, 'Scoundrel', followers['scoundrel']) if 'scoundrel' in followers else None
        self.enchantress = Follower(self.host, 'Enchantress', followers['enchantress']) if 'enchantress' in followers else None

        self.loaded = True


    def hero_details(self):
        if not self.loaded:
            self.load_hero_data()
        return self


class Profile:
    def __init__(self, host, profile_data):
        self.battle_tag = profile_data['battleTag']
        self.host = host
        self.paragon = profile_data['paragonLevel']
        self.heroes = [Hero(data, self.battle_tag, self.host) for data in profile_data['heroes']]
        self.last_played_hero = profile_data['lastHeroPlayed']
        self.monsers = profile_data['kills']['monsters']
        self.elites = profile_data['kills']['elites']
        self.hardcore_monsters = profile_data['kills']['hardcoreMonsters']

    def __str__(self):
        profile = "%s (paragon level: %s) has %d heroes: "%(self.battle_tag, self.paragon, len(self.heroes))
        for hero in self.heroes:
            profile = profile + "\n\t%s"%str(hero)
            if hero.id == self.last_played_hero:
                profile += " (last played hero)"
        return profile


def get_profile(server_id, battle_tag):
    url = "%s/api/d3/profile/%s/"%(server_id, battle_tag.replace("#","-"))
    response = urllib.urlopen(url).read()
    data = json.loads(response)
    if 'heroes' in data:
        return Profile(server_id, data) 
    else:
         print "Profile %s not found."%(battle_tag)


def get_hero(server_id, battle_tag, hero_id):
    url = "%s/api/d3/profile/%s/hero/%s"%(server_id, battle_tag.replace("#","-"), hero_id)
    return json.loads(urllib.urlopen(url).read())

def get_complete_item(server_id, tooltip_params):
    url = "%s/api/d3/data/%s"%(server_id, tooltip_params)
    return json.loads(urllib.urlopen(url).read())

