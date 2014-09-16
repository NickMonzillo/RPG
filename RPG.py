import random
import time

enemies = ['Troll','Goblin','Dire Wolf','Ankou']
bosses = ['Green Dragon','Centaur Lord','Band of Thieves','Kraken']
animals = ['Deer','Squirrel','Boar']
weapon_types = ['Greatsword','Staff','Poleaxe']

class Character(object):
    '''Class that describes the player character.'''
    def __init__(self,spec):
        self.name = ''
        self.spec = spec
        self.stamina = 5
        self.max_stamina = 5
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
        info += '\nStamina: ' + str(self.stamina) + '/' + str(self.max_stamina)
        info += '\nDamage: ' + str(self.damage)
        info += '\nLevel: ' + str(self.level)
        info += '\nXP: ' + str(self.xp) + '/' + str(500 + self.level**2)
        return info
    
    def levelup(self,spec):
        '''When experience threshold hits, the character levels up.
        Increases attributes based on class choice.'''
        print '\nCongratulations! You levelled up.'
        if spec == 'mage':
            self.strength += 1
            self.magic += 4
            self.vitality += 2
        elif spec == 'fighter':
            self.strength += 3
            self.magic += 1
            self.vitality += 3
        elif spec == 'juggernaut':
            self.strength += 2
            self.magic += 1
            self.vitality += 4
        if self.level%10 == 0:
            self.max_stamina += 1
            print "You feel yourself becoming stronger."
        self.max_health = self.vitality*15
        self.damage = (self.magic*10) + (self.strength*10)
        self.xp -= (500 + (self.level**2))
        self.health*=1.1
        self.health = int(self.health)
        self.level+=1
                 
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
        self.health -= int(self.defendturn)
        
    def dead(self):
        '''Checks if the character's health is at or below 0'''
        if self.health <= 0:
            return True
        else:
            return False
        
    def equip(self,weapon):
        self.damage += weapon.damage

    def showAttributes(self):
        '''Displays the character's attributes.'''
        print 'Strength: ' + str(self.strength)
        print 'Magic: ' + str(self.magic)
        print 'Vitality: ' + str(self.vitality)

    def hunt(self):
        '''Initiates a hunt event.
        Hunt is used to aggressively gain stamina, but has a high chance of failure.'''
        roll = random.randint(0,1)
        if roll == 0:
            print "You didn't manage to find any food."
            self.stamina = max(0,self.stamina - 1)
            self.stamina_check()
        else:
            animalSelect = random.choice(animals)
            i = 0
            while i < 3:
                self.stamina = min(self.stamina+1,self.max_stamina)
                i += 1
            print 'You found a wild ' + animalSelect
            encounter(self,Enemy('weak',self.level,animalSelect),int(50+self.level**1.5))

    def stamina_check(self):
        '''Initiates a check to see if the stamina is low.'''
        if self.stamina == 1:
            print '\nYou are growing very weary. Perhaps you should take a rest?'
        elif self.stamina == 0:
            print '\nYou are overcome with exhaustion.'
            print 'You take 50 damage.'
            self.health-=50
            if self.health < 0:
                print '\nYou have died.'
                
    def rest(self):
        '''Initiates a rest event.
        A relatively safe way for the user to gain stamina.'''
        self.stamina = min(self.stamina+1,self.max_stamina)
        if random.randint(0,2) == 0:
            print 'You awake to a noise.'
            ambush(self,Enemy('standard',self.level,random.choice(enemies)),int(100+self.level**1.5))
        else:
            print 'You wake up well rested.'
            self.health += 10

            
class Weapon(object):
    def __init__(self,damage):
        self.damage = random.randrange(int(damage - damage*0.1),int(damage + damage*0.1))
        #if wep_type == 'staff':
            
    def __repr__(self):
        info = ''
        info += 'Damage: ' + str(self.damage)
        return info

class Enemy(object):
    def __init__(self,variety,level,name):
        if variety == 'standard':
            self.health = 170 + random.randint(15,20)*level
            self.damage = 20 + random.randint(5,10)*level
            self.name = name
        elif variety == 'elite':
            self.health = 300 + random.randint(25,40)*level
            self.damage = 25 + random.randint(5,10)*level
            self.name = name
        elif variety == 'weak':
            self.health = 100 + random.randint(5,15)*level
            self.damage = 10 + random.randint(2,6)*level
            self.name = name
    def __repr__(self):
        info = 'Enemy Stats:'
        info += '\n' + self.name
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
    print "Controls:"
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
        if c.xp >= 500 + (c.level**2):
            c.levelup(c.spec)
        choice = raw_input('> ')
        if choice not in ['rest','hunt','explore','help','quit','status','attributes','d']:
            print 'That is not a valid choice.'
        elif choice == 'help':
            controls()
        elif choice == 'rest':
            c.rest()
        elif choice == 'hunt':
            c.hunt()
        elif choice == 'explore':
            c.stamina = max(0,c.stamina-1)
            roll = random.randint(0,2)
            if roll == 0:
                print "You didn't find anything."
            elif roll == 1:
                print "You were found by the enemy."
                encounter(c,Enemy('standard',c.level,random.choice(enemies)),int(100+c.level**1.5))
            elif roll == 2:
                print "You stumbled upon some treasure!"
                #TODO: Add loot to treasure rolls. Better treasure for boss rolls.
                bossroll = random.randint(0,3)
                if bossroll == 3:
                    bossSelect = random.choice(bosses)
                    print "It is guarded by a fearsome " + bossSelect + '.'
                    encounter(c,Enemy('elite',c.level,bossSelect),int(300+c.level**1.5))
                else:
                    print 'You took the lone guard unawares' + '.'
                    encounter(c,Enemy('standard',c.level,random.choice(enemies)),int(100+c.level**1.5))
            c.stamina_check()
        elif choice == 'd': c.levelup(c.spec)        
        elif choice == 'status':
            print c
        elif choice == 'attributes':
            c.showAttributes()
        elif choice == 'quit': break
    print '\nYour journey has come to an end.'
    print 'You got to level ' + str(c.level) + '!'
