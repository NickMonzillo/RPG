import random
import time

enemies = ['Troll','Goblin','Dire Wolf','Ankou']
bosses = ['Green Dragon','Centaur Lord','Band of Thieves','Kraken']
animals = ['Deer','Squirrel','Boar']
weapon_types = ['Greatsword','Staff','Poleaxe']
class Character:
    '''Class that describes the player character.'''
    def __init__(self,spec):
        self.name = ''
        self.spec = spec
        self.stamina = 5
        self.level = 1
        self.xp = 0
        if spec == 'mage':
            self.strength = 5
            self.magic = 20
            self.vitality = 10
        elif spec == 'fighter':
            self.strength = 15
            self.magic = 5
            self.vitality = 15
        elif spec == 'juggernaut':
            self.strength = 10
            self.magic = 5
            self.vitality = 20
        self.health = self.vitality * 15
        self.max_health = self.vitality * 15
        self.damage = (self.magic*10) + (self.strength*10)

    def __repr__(self):
        info = ''
        info += '\nHealth: ' + str(self.health)
        info += '\nStamina: ' + str(self.stamina)
        info += '\nLevel: ' + str(self.level)
        info += '\nXP: ' + str(self.xp) + '/500'
        return info
    
    def levelup(self,spec):
        '''When experience threshold hits, the character levels up.
        Increases attributes based on class choice.'''
        print '\nCongratulations! You levelled up.'
        if spec == 'Mage':
            self.strength += 1
            self.magic += 4
            self.vitality += 2
        elif spec == 'Fighter':
            self.strength += 3
            self.magic += 1
            self.vitality += 3
        elif spec == 'Juggernaut':
            self.strength += 2
            self.magic += 1
            self.vitality += 4
        self.level += 1
        self.max_health = self.vitality*15
        self.damage = (self.magic*10) + (self.strength*10)
        self.xp -= 500
        self.health*=1.1
            
    def attack(self,enemy):
        '''You attack the enemy.'''
        upperbound = int(self.damage+self.damage*0.2)
        lowerbound = int(self.damage - self.damage*0.2)
        self.attackturn = random.randrange(lowerbound,upperbound)
        enemy.health -= self.attackturn
        
    def defend(self,enemy):
        '''Enemy attacks you.'''
        upperbound = int(enemy.damage + enemy.damage*0.2)
        lowerbound = int(enemy.damage - enemy.damage*0.2)
        self.defendturn = random.randrange(lowerbound,upperbound)
        self.health -= self.defendturn
        
    def dead(self):
        if self.health <= 0:
            return True
        else:
            return False
    def equip(self,weapon):
        self.damage += weapon.damage

    def showAttributes(self):
        print 'Strength: ' + str(self.strength)
        print 'Magic: ' + str(self.magic)
        print 'Vitality: ' + str(self.vitality)

class Weapon:
    def __init__(self,wep_type):
        #self.damage = random.randrange(int(damage - damage*0.1),int(damage + damage*0.1))
        #if wep_type == 'staff':
            
    def __repr__(self):
        info = ''
        info += 'Damage: ' + str(self.damage)
        return info

class Enemy:
    def __init__(self,damage,health,name):
        self.health = health
        self.damage = damage
        self.name = name
    def __repr__(self):
        info = 'Enemy Stats:'
        info += '\nHealth:' + str(self.health)
        info += '\nDamage:' + str(self.damage)
        return info
    
    def dead(self):
        if self.health <= 0:
            return True
        else:
            return False
def encounter(char,enemy,xpGain):
    print "You've encountered a " + enemy.name + '.'
    while 1:
        char.attack(enemy)
        print 'You attack the enemy for ' + str(char.attackturn) + ' damage.'
        print 'Your Health: ' + str(char.health)
        if enemy.health < 0:
            print 'Enemy Health: 0'
        else:
            print 'Enemy Health: ' + str(enemy.health)
        if enemy.dead():
            print 'You have defeated the enemy.'
            char.xp += xpGain
            print 'You gain ' + str(xpGain) + ' xp.'
            break
        char.defend(enemy)
        time.sleep(1)
        print 'The enemy attacks you for ' + str(char.defendturn) + ' damage.'
        if char.health < 0:
            print 'Your Health: 0'
        else:
            print 'Your Health: ' + str(char.health)
        print 'Enemy Health: ' + str(enemy.health)
        if char.dead():
            print '\nYou have died.'
            break
        time.sleep(1)

def ambush(char,enemy,xpGain):
    print "You've been ambushed by a " + enemy.name + '.'
    while 1:
        
        char.defend(enemy)
        print 'The enemy attacks you for ' + str(char.defendturn) + ' damage.'
        if char.health < 0:
            print 'Your Health: 0'
        else:
            print 'Your Health: ' + str(char.health)
        print 'Enemy Health: ' + str(enemy.health)
        if char.dead():
            print '\nYou have died.'
            break
        time.sleep(1)
        char.attack(enemy)
        print 'You attack the enemy for ' + str(char.attackturn) + ' damage.'
        print 'Your Health: ' + str(char.health)
        if enemy.health < 0:
            print 'Enemy Health: 0'
        else:
            print 'Enemy Health: ' + str(enemy.health)
        if enemy.dead():
            print 'You have defeated the enemy.'
            char.xp += xpGain
            print 'You gain ' + str(xpGain) + ' xp.'
            break
        time.sleep(1)    
    

def controls():
    print 'Controls:'
    print "type 'status' to view your status."
    print "type 'attributes' to view your attributes"
    print "type 'rest' to take a rest. (+1 stamina)"
    print "type 'hunt' to look for food. (chance at +3 stamina)"
    print "type 'explore' to search for treasure."
    print "type 'help' to view the controls menu."
    print "type 'quit' to exit the game."

def start():
    print 'Your adventure is about to begin!'
    print 'Choose a class:'
    print 'Mage: High Attack and low HP'
    print 'Fighter: Moderate Attack and HP'
    print 'Juggernaut: Low Attack and High HP'
    classchoice = raw_input('> ').lower()
    while classchoice.lower() not in ['mage','fighter','juggernaut']:
        print 'That is not a valid choice.'
        classchoice = raw_input('> ')
    c = Character(classchoice)
    controls()
    while(c.health > 0):
        if c.xp >= 500:
            c.levelup(c.spec)
        choice = raw_input('> ')
        if choice not in ['rest','hunt','explore','help','quit','status','attributes','d']:
            print 'That is not a valid choice.'
        elif choice == 'help':
            controls()
        elif choice == 'rest':
            #Relatively safe stamina builder.
            c.stamina = min(c.stamina+1,5)
            if random.randint(0,1) == 1:
                print 'You awake to a noise.'
                ambush(c,Enemy(random.randint(10,30),random.randint(175,300),enemies[random.randint(0,len(enemies)-1)]),100)
            else:
                print 'You wake up well rested.'
                c.health += 10
        elif choice == 'hunt':
            #The risky stamina builder.
            huntroll = random.randint(0,1)
            if huntroll == 0:
                print "You didn't manage to find any food."
                c.stamina = max(0,c.stamina - 1)
                if c.stamina == 1:
                    print '\nYou are growing very weary. Perhaps you should take a rest?'
                elif c.stamina == 0:
                    print '\nYou are overcome with exhaustion.'
                    print 'You take 50 damage.'
                    c.health-=50
                    if c.health < 0:
                        print '\nYou have died.'
            else:
                animalselect = random.randint(0,len(animals)-1)
                i = 0
                while i < 3:
                    c.stamina = min(c.stamina+1,5)
                    i += 1
                print 'You found a wild ' + animals[animalselect]
                encounter(c,Enemy(random.randint(5,25),random.randint(100,200),animals[animalselect]),50)
        elif choice == 'explore':
            #The main option that people will use with enough stamina.
            c.stamina = max(0,c.stamina-1)
            roll = random.randint(0,2)
            if roll == 0:
                print "You didn't find anything."
            elif roll == 1:
                print "You were found by the enemy."
                encounter(c,Enemy(random.randint(10,30),random.randint(175,300),enemies[random.randint(0,len(enemies)-1)]),100)
            elif roll == 2:
                print "You stumbled upon some treasure!"
                #TODO: Add loot to treasure rolls. Better treasure for boss rolls.
                bossroll = random.randint(0,3)
                if bossroll == 3:
                    bossSelect = random.randint(0,len(bosses)-1)
                    print "It is guarded by a fearsome " + bosses[bossSelect] + '.'
                    encounter(c,Enemy(random.randint(25,50),random.randint(300,450),bosses[bossSelect]),300)
                else:
                    print 'You took the lone guard unawares' + '.'
                    encounter(c,Enemy(random.randint(10,30),random.randint(175,300),enemies[random.randint(0,len(enemies)-1)]),100)
            if c.stamina == 1:
                print '\nYou are growing very weary. Perhaps you should take a rest?'
            elif c.stamina == 0:
                print '\nYou are overcome with exhaustion.'
                print 'You take 50 damage.'
                c.health-=50
                if c.health < 0:
                    print '\nYou have died.'
        elif choice == 'd': c.stamina -= 1        
        elif choice == 'status':
            print c
        elif choice == 'attributes':
            c.showAttributes()
        elif choice == 'quit': break
    
    
    print '\nYour journey has come to an end.'
    print c
