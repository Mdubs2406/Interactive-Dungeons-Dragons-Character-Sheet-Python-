import dice, dnd_class, species, math

SkILL_LIST = ['Acrobatics', 'Animal Handling', 'Arcana', 'Atheltics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 
              'Medicine', 'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 'Sleath', 'Sleight of Hand', 'Survival']

class Character:

    def __init__(self, name:str, level:int, hero: dnd_class.DnD_Class, race: species.Species, STR=10, DEX=10, CON=10, INT=10, WIS=10, CHA=10):
        self.name = name
        self.hero = hero
        self.race = race
        self.prof_bonus = 2
        self.score_str = STR
        self.score_dex = DEX
        self.score_con = CON
        self.score_int = INT
        self.score_wis = WIS
        self.score_cha = CHA
        self.str = (STR - 10) // 2
        self.dex = (DEX - 10) // 2
        self.con = (CON - 10) // 2
        self.int = (INT - 10) // 2
        self.wis = (WIS - 10) // 2
        self.cha = (CHA - 10) // 2
        self.hp_max = hero.hit_dice.max + race.hp_bonus + self.con
        self.hp = self.hp_max
        self.armor_class = 10 + self.dex
        self.initiative = 10 + self.dex
        self.level = level
        self.hit_dice_availble = self.level
        self.lanuages = []
        self.proficiencies = self.prep_profs(hero.proficiencies, race.proficiencies, hero.expertise)
        self.death_saves = (0,0)

    def level_up(self, levels=1):
        self.level += 1*levels
        self.hero.level += 1*levels
        self.hero.level_up()
        self.race.level += 1*levels
        self.race.level_up()
        self.prof_bonus = math.ceil(self.level / 4) + 1
        hp_increase = self.hero.hit_dice.avg + self.con + self.race.hp_bonus
        self.hp += hp_increase
        self.hp_max += hp_increase

    def adjust_hp(self, amount: int):
        self.hp += amount
        if amount >= 0:
            print(f"{self.name} healed {amount} hit points.\nTheir hit points are now {self.hp}.")
        if amount < 0:
            print(f"{self.name} took {amount} points of damage.\nTheir hit points are now {self.hp}.")

    def saving_throw(self, ability):
        bonus = 0
        if ability in self.hero.saving_throws:
            bonus = self.prof_bonus
        roll_result = dice.Dice(20).roll() + getattr(self, ability) + bonus
        print(f"{self.name} rolled a {roll_result} on their {ability} saving throw!")

    def death_saving_throw(self):
        success, fail = self.death_saves
        roll = dice.Dice(20).roll()
        if roll == 1:
            fail += 2
        elif roll < 11:
            fail += 1
        elif roll == 20:
            success += 2
        elif roll >= 11:
            success += 1
        print(f"---Death Saves---\nSuccesses: {success} | Failures: {fail}")
        if success == 3:
            self.hp += 1
            print(f"{self.name} is no longer dying!")
        if fail == 3:
            print(f"{self.name} has died")
        self.death_saves = (success, fail)

    def skill_check(self, skill):
        skill_name, skill_attribute = skill
        modifer = getattr(self, skill_attribute)
        bonus = 0
        if skill in self.proficiencies:
            bonus = self.prof_bonus
        roll = dice.Dice(20).roll() + modifer + bonus
        print(f"{self.name} rolled a {roll} on their {skill_name} check!")

    def __str__(self):
        return (f"{self.name}: Lvl {self.level} {self.race.name} {self.hero.name}.")
    
    def prep_profs(self, lst1, lst2, lst3):
        lst = sorted(lst1 + lst2)
        char_lst = []
        for skill in SkILL_LIST:
            if skill in lst3:
                char_lst.append((skill, self.prof_bonus*2))
            elif skill in lst:
                char_lst.append((skill, self.prof_bonus))
            else:
                char_lst.append((skill, 0))
        return char_lst

    def display_casting(self):
        if self.hero.full_caster:
            slot_list = prep_spell_slots(self.level)
        elif self.hero.half_caster:
            slot_list = prep_spell_slots(math.ceil(self.level / 2))
        else:
            return
        i = 0
        for lvl in slot_list:
            print(f"Level {i+1} ({lvl}/{lvl})")
            for p in range(lvl):
                print("[ ]", end='')
            i += 1
            print()
        

    def display_features(self):
        L = self.proficiencies
        print(self)
        print(f"Armor Class: {self.armor_class} | Hit Points: {self.hp} / {self.hp_max} | Hit Dice: {self.hit_dice_availble} / {self.level}")
        print(f"Intiative: {self.dex} | Speed: {self.race.speed} | Size: {self.race.size} | Passive Perception: {10+self.wis + L[11][1]}")
        print()
        print("\tSTR\tDEX\tCON\tINT\tWIS\tCHA")
        print()
        print(f"\t{self.str}\t{self.dex}\t{self.con}\t{self.int}\t{self.wis}\t{self.cha}")
        print()
        print(f"({self.dex + L[0][1]}): Acrobatics           ({self.wis + L[9][1]}): Medicine\n" +
              f"({self.wis + L[1][1]}): Animal Handling      ({self.int + L[10][1]}): Nature\n" +
              f"({self.int + L[2][1]}): Arcana               ({self.wis + L[11][1]}): Perception\n" +
              f"({self.str + L[3][1]}): Atheltics            ({self.cha + L[12][1]}): Performance\n" +
              f"({self.cha + L[4][1]}): Deception            ({self.cha + L[13][1]}): Persuasion\n" +
              f"({self.int + L[5][1]}): History              ({self.cha + L[14][1]}): Religion\n" +
              f"({self.wis + L[6][1]}): Insight              ({self.dex + L[15][1]}): Sleath\n" +
              f"({self.cha + L[7][1]}): Intimidation         ({self.dex + L[16][1]}): Sleight of Hand\n" +
              f"({self.int + L[8][1]}): Investigation        ({self.wis + L[17][1]}): Survival\n")
        
        self.display_casting()

        self.hero.display_features()
        self.race.display_features()


def prep_spell_slots(lvl):
    spl = [[2],
           [3],
           [4,2],
           [4,3],
           [4,3,2],
           [4,3,3],
           [4,3,3,1],
           [4,3,3,2],
           [4,3,3,3,1],
           [4,3,3,3,2],
           [4,3,3,3,2,1],
           [4,3,3,3,2,1],
           [4,3,3,3,2,1,1],
           [4,3,3,3,2,1,1,1],
           [4,3,3,3,2,1,1,1],
           [4,3,3,3,2,1,1,1,1],
           [4,3,3,3,3,1,1,1,1],
           [4,3,3,3,3,2,1,1,1],
           [4,3,3,3,3,2,2,1,1]]
    return spl[lvl-1]
