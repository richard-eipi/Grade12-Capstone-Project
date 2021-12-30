from functions import *

class PlayerTargetSurface(pygame.sprite.Sprite):
    '''where player selects a target after choosing a move in teamfight'''
    def __init__(self, champ):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image1 = pygame.transform.scale(pygame.image.load(os.path.join('images','other images','target icon.png')), (50,50)).convert_alpha()
        self.image2 = pygame.transform.scale(self.image1, (75,75))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.champ = champ

    def update(self, seconds):
        if (self.champ.opponent and self.champ.opponent.rect.collidepoint(pygame.mouse.get_pos())) or (self.champ.oppoTeammate and self.champ.oppoTeammate.rect.collidepoint(pygame.mouse.get_pos())):
            self.image = self.image2
            battlegroup.move_to_front(self)
        else:
            self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def clicked(self):
        for opponent in sideList[1-self.champ.side]:
            if opponent.rect.collidepoint(pygame.mouse.get_pos()):
                self.champ.target = opponent
                self.champ.playerTargeting = False
                self.kill()


class PlayerSelectionSurface(pygame.sprite.Sprite):
    '''where player selects special stuff after choosing a move'''
    def __init__(self, champ, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((540,360)).convert_alpha()
        self.image.fill((255,255,255))
        self.promptArea = pygame.Surface((540,120)).convert_alpha()
        self.promptArea.fill((255,255,255))
        centerParagraph(False, self.promptArea, text, 'timesnewroman', 25, (0,0,0), True)
        self.image.blit(self.promptArea, (0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (540,360)
        self.ok = pygame.Surface((120,40)).convert_alpha()
        self.champ = champ

    def update(self, seconds):
        if self.ok.get_rect(center=(540,510)).collidepoint(pygame.mouse.get_pos()):
            self.ok.fill((50,50,50))
            centerText(self.ok, 'OK', 'timesnewroman', 22, (255,255,255), True)
            self.image.blit(self.ok, (210,310))
        else:
            self.ok.fill((0,0,0))
            centerText(self.ok, 'OK', 'timesnewroman', 20, (255,255,255), True)
            self.image.blit(self.ok, (210,310))

    def clicked(self):
        self.champ.playerSelect(True)
        if self.ok.get_rect(center=(540,510)).collidepoint(pygame.mouse.get_pos()):
            self.champ.playerSelectionSurface = None
            self.kill()


class Champion(pygame.sprite.DirtySprite):
    '''Champion model'''
    def __init__(self, level=100):
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        # basic information
        self.level = level
        self.experience = 0 # how to deal with leveling up?
        self.stats = [0,0,0,0,0,0]
        self.levelOfExpertise = [0,0,0,0,0,0]
        self.specialTrait = ''
        self.statBooster1 = [0,0,0,0,0,0]
        self.statBooster2 = [0,0,0,0,0,0]
        self.title = ''

        # fighting status
        self.side = 0
        self.position = 0
        self.opponent = None
        self.teammate = None
        self.oppoTeammate = None
        self.directionx = 1 # 1 means to the right
        self.directiony = 1 # 1 means down
        self.battlePosition = [0,0] # for keeping track of rect.center
        self.animationFinished = True
        self.counter = 0
        self.champInfo = None

        self.id = ''
        self.hp = 0
        self.targetMoves = [] # moves that require players to select a target
        self.moveRecord = [] # add the move instantly after player selects a move, can be checked by executeMove()
        self.attackDamageList = []
        self.receiveAttackDamageList = []
        self.magicDamageList = []
        self.receiveMagicDamageList = []
        self.healingAmountList = []
        self.energyLossList = []

        self.attackList = [0,0]
        self.receiveAttackList = [0,0]
        self.magicList = [0,0]
        self.receiveMagicList = [0,0]
        self.healingList = [0,0]
        self.energyList = [0,0]
        self.missingList = [0,0]
        self.dodgingList = [0,0]

        self.specialBuffs = {}
        self.statusEffects = {}
        self.statsER = [0,0,0,0,0,0]
        self.turnEffects = {}
        self.timeEffects = {}
        self.entireBattleEffects = []
        self.shield = 0

        self.healingEffect = 1.00 # [0,infinity]
        self.resetDefenseVariables()
        self.resetAttackVariables()
        self.resetMagicVariables()
        self.resetEnergyVariables()
        self.resetTurnVariables()
        self.phaseFinished = False
        self.dead = False

    def resetDefenseVariables(self):
        self.attacker = None
        self.isCriticalHit = False
        self.receiveAttackIncrement = 0
        self.receiveAttackPercentMultiplier = 0.00 # [-infinity,infinity]
        self.receiveAttackMultiplier = 1.0 # [0,infinity]
        self.attackPercentBlocked = 0.00 # [0,1]
        self.attackPercentRebounded = 0.00
        self.defenseMax = math.inf
        self.defenseMin = 0

        self.receiveMagicIncrement = 0
        self.receiveMagicPercentMultiplier = 0.00 # [-infinity,infinity]
        self.receiveMagicMultiplier = 1.0 # [0,infinity]
        self.magicPercentBlocked = 0.00 # [0,1]

    def resetAttackVariables(self):
        self.defenders = []
        self.moveAttack = False
        self.ignoreOwnStatsR = False
        self.ignoreOppoStatsE = False
        self.attackIncrement = 0
        self.attackPercentMultiplier = 0.00 # [-infinity,infinity]
        self.attackMultiplier = 1.0 # [0,infinity]
        self.rateOfCriticalHitIncrement = 0.0
        self.criticalPercentAdder = 0.00 # [-infinity,infinity]
        self.attackMax = math.inf
        self.attackMin = 0

    def resetMagicVariables(self):
        self.defender = None
        self.magicIncrement = 0
        self.magicPercentMultiplier = 0.00 #[0,infinity]
        self.magicMultiplier = 1.0 # [0,infinity]
        self.magicPercentBlocked = 0.00 # [0,1]

    def resetEnergyVariables(self):
        self.moveEnergy = False
        self.energyLossIncrement = 0
        self.energyLossMultiplier = 1.0 # [0,infinity]

    def resetTurnVariables(self):
        self.preemptiveIncrement = 0 # can be positive or negative
        self.goesFirst = []
        self.abilitiesEffectiveness = True
        self.specialBuffEffectiveness = True
        self.moveEffectiveness = [True,True,[True,True,True,True,True]] # [A,E,[moves]]
        self.healingEffectiveness = True
        self.statsEEffectiveness = True
        self.statusEffectiveness = True
        self.turnEffectiveness = True
        self.timeEffectiveness = True
        self.entireBattleEffectiveness = True
        self.abilitiesEffect = 1.00 # [0,infinity]
        self.specialBuffEffect = 1.00 # [0,infinity]
        self.moveEffect = [1.00,1.00] # [A,E]

        self.immunityFromMoves = {self.opponent:[False,False], self.oppoTeammate:[False,False]}
        self.immunityFromStatsR = False
        self.immunityFromClearingStatsE = False
        self.immunityFromStatusEffects = False
        self.reboundStatusEffects = False
        self.immunityFromClearingTurnEffects = False
        self.immunityFromClearingTimeEffects = False
        self.immunityFromClearingEntireBattleEffects = False
        self.immunityFromSeckill = False

        self.missingIgnored = False
        self.ineffectiveIgnored = False
        self.immuneIgnored = False

        self.rateOfDodgingIncrement = 0.00 # [0,infinity]
        self.accuracyReduction = 0.00 # [0,infinity]
        self.playerSelecting = False
        self.playerTargeting = False
        self.target = None
        self.oppoHit = []

        try:
            self.resetUniqueVariables()
        except:
            pass

    def loadImage(self):
        image = pygame.image.load(os.path.join('images','champion images',self.name+'.png'))
        return image

    def loadText(self):
        with open(os.path.join('text files','champions text files',self.name+'.txt')) as file:
            abilities = file.readline()[:-1]
            specialBuffs = []
            for i in file.readline().split('*'):
                specialBuffs.append(i.split('_'))
            if specialBuffs != []:
                specialBuffs[-1][-1] = specialBuffs[-1][-1][:-1]
            moves = []
            for i in file.readlines():
                moves.append(i.split('_'))
                moves[-1][0] = moves[-1][0].split(',')
                if moves[-1][5] != '':
                    moves[-1][5] = moves[-1][5].split(',')
                moves[-1][-1] = moves[-1][-1][:-1]
                if moves[-1][2] != '0%' and not 'affect both opponents' in moves[-1][6]:
                    self.targetMoves.append(moves[-1])
        return abilities, specialBuffs, moves

    def determineStats(self):
        stats = [0,0,0,0,0,0]
        for i in range(5):
            stats[i] = (self.baseStats[i]*2+self.levelOfExpertise[i]/4+50)*self.level/100+5+self.statBooster1[i]+self.statBooster2[i]
        stats[5] = round((self.baseStats[5]*2+self.levelOfExpertise[5]/4+50)*self.level/100+self.level+10+self.statBooster1[5]+self.statBooster2[5])
        return stats

    def copy(self, name): # create a deepcopy of the champion
        className = getattr(sys.modules[__name__], name)
        copyobj = className()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj

    def update(self, seconds):
        if not self.dead:
            dx, dy = min(1,seconds*20), min(1,seconds*20)
            if not doubles[0]:
                positionY = 370
                moveRange = 5
            else:
                positionY = 490-280*self.position
                moveRange = 3
            if moveStep[self.side][self.position] != 3:
                if self.battlePosition[1] >= positionY+moveRange or self.battlePosition[1] <= positionY-moveRange:
                    self.directiony = -1*self.directiony
                self.battlePosition[1] += dy*self.directiony
            elif self.animationFinished:
                self.animationFinished = False
                self.battlePosition[1] = positionY
                self.directionx = -2*self.side+1
                self.directiony = 1
                battlegroup.move_to_front(self)
            if not self.animationFinished:
                self.moveAnimation(dx, dy)
            self.rect.center = (self.battlePosition[0], self.battlePosition[1])

    def moveAnimation(self, dx, dy):
        if self.moveRecord[-1][0][1] == 'Enchantment':
            if self.counter < 100:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.counter += 1
            else:
                self.animationFinished = True
                self.counter = 0
        elif self.moveRecord[-1][0][1] == 'Physical Attack':
            if self.battlePosition[0] != 216+(1-self.side)*648:
                self.battlePosition[0] += self.directionx*12
                if doubles[0]:
                    if self.target:
                        self.battlePosition[1] += 5*(self.position-self.target.position)*self.directiony
                    elif self.battlePosition[1] != 490-280*self.position:
                        self.battlePosition[1] += 5*self.directiony
            else:
                if not doubles[0] or self.target: # not doubles or not team damage
                    self.directionx = -1*self.directionx
                    self.directiony = -1*self.directiony
                    self.battlePosition[0] += self.directionx*12
                    if doubles[0]: # doubles but not team damage
                        self.battlePosition[1] += 5*(self.position-self.target.position)*self.directiony
                elif not self.target and self.battlePosition[1] != 220+260*self.position: # team damage
                    self.battlePosition[1] -= 10*(-2*self.position+1)
                else:
                    self.directionx = -1*self.directionx
                    self.directiony = (-2*self.position+1)*self.directiony
                    self.battlePosition[0] += self.directionx*12
            if self.battlePosition[0] == 216+self.side*648:
                self.animationFinished = True
        elif self.moveRecord[-1][0][1] == 'Special Attack':
            if not otherBattleSprites[0] in battlegroup:
                otherBattleSprites[0].setup(self, 'special ray', self.color)
            elif otherBattleSprites[0].effectDone:
                battlegroup.remove(otherBattleSprites[0])
                self.animationFinished = True
        elif self.moveRecord[-1][0][1] == 'All-in Attack':
            if self.directionx != 0:
                if self.battlePosition[0] != 216+(1-self.side)*648:
                    self.battlePosition[0] += self.directionx*12
                    if doubles[0]:
                        if self.target:
                            self.battlePosition[1] += 5*(self.position-self.target.position)*self.directiony
                        elif self.battlePosition[1] != 490-280*self.position:
                            self.battlePosition[1] += 5*self.directiony
                else:
                    if not doubles[0] or self.target: # not doubles or not team damage
                        self.directionx = -1*self.directionx
                        self.directiony = -1*self.directiony
                        self.battlePosition[0] += self.directionx*12
                        if doubles[0]: # doubles but not team damage
                            self.battlePosition[1] += 5*(self.position-self.target.position)*self.directiony
                    elif not self.target and self.battlePosition[1] != 220+260*self.position: # team damage
                        self.battlePosition[1] -= 10*(-2*self.position+1)
                    else:
                        self.directionx = -1*self.directionx
                        self.directiony = (-2*self.position+1)*self.directiony
                        self.battlePosition[0] += self.directionx*12
            if self.battlePosition[0] == 216+self.side*648:
                self.directionx = 0
                if not otherBattleSprites[0] in battlegroup:
                    otherBattleSprites[0].setup(self, 'special ray', self.color)
                elif otherBattleSprites[0].effectDone:
                    battlegroup.remove(otherBattleSprites[0])
                    self.animationFinished = True

    def lost(self):
        self.image = pygame.transform.rotate(self.image, (2*self.side-1)*90)
        self.rect.centerx += 60
        self.rect.centery -= 30
        self.dead = True
        self.phaseFinished = True
        self.specialBuffs = {}
        self.statusEffects = {}
        self.statsER = [0,0,0,0,0,0]
        self.turnEffects = {}
        self.timeEffects = {}
        self.entireBattleEffects = []

class Sorensen(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'sorensen'
        self.gender = None
        self.color = (100,0,0)
        self.type = ['dimension', 'elder', 'spirit']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [65,160,110,124,130,160]

        # unique battle variables
        self.opponentMoves = None # a list of opponent's moves still effective
        self.healed = [False, False] # if Sorensen has healed after an opponent dies

    def resetUniqueVariables(self):
        self.healed = [False, False]

    def resetAfterClear(self, element):
        for opponent in sideList[1-self.side]:
            if element == 'Seal':
                self.abilitiesEffect = 1
                self.specialBuffEffect = 1
                self.moveEffect = [1, 1]
            elif element == 'Inferno Galaxy':
                opponent.abilitiesEffect = 1
                opponent.specialBuffEffect = 1
                opponent.moveEffect = [1, 1]
            elif element == 'Cut off all healing effects from '+opponent.name.title()+' '+opponent.id:
                opponent.healingEffectiveness = True

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if not tasklet and phase[0] == 0.5 and turn[0] == 1:
                '''Has {Seal} (effective for fifty turns)'''
                self.specialBuffs.update({'Seal': 50})
            for opponent in sideList[1-self.side]:
                if not tasklet and opponent.hp <= 0 and not self.healed[opponent.position]:
                    self.healed[opponent.position] = True
                    '''Every time an opponent dies, heal by an amount equivalent to 100% of its maximum HP'''
                    if self.healingEffectiveness:
                        heal(self, opponent.stats[5]*self.abilitiesEffect)
            if not tasklet and phase[0] == 0.5:
                '''Immune from status effects'''
                self.immunityFromStatusEffects = True
            if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
                '''Reduce attack damage received by 50%'''
                self.receiveAttackPercentMultiplier -= 0.5*self.abilitiesEffect
            if not tasklet and phase[0] == 2 and self.opponent:
                '''At the start of every turn, clear opponent's stats enhancement and,'''
                if not self.opponent.immunityFromClearingStatsE:
                    clearStatsE(self.opponent)
                '''if having stats reduction, lower the opponent's stats by an equal amount'''
                if not self.opponent.immunityFromStatsR and min(self.statsER) < 0:
                    for i in range(6):
                        self.opponent.statsER[i] = max(-6, self.opponent.statsER[i]+min(0, self.statsER[i]))

        # special buffs
        if self.specialBuffEffectiveness:
            if 'Seal' in self.specialBuffs:
                '''Reduce all attack damage and all effects by (50-x)% when x turns into the battle'''
                if not tasklet and phase[0] == 0.5:
                    self.abilitiesEffect = max(0, self.abilitiesEffect-(50-turn[0])/100)
                    self.specialBuffEffect = max(0, self.specialBuffEffect-(50-turn[0])/100)
                    self.moveEffect = [max(0, self.moveEffect[0]-(50-turn[0])/100), max(0, self.moveEffect[1]-(50-turn[0])/100)]
                if tasklet and self.attackList[0] > self.attackList[1]:
                    self.attackPercentMultiplier -= (50-turn[0])/100
            if 'Inferno Galaxy' in self.specialBuffs:
                '''All attack damage dealt by attacking moves can not be blocked and ignore own stats reduction'''
                if tasklet and self.attackList[0] > self.attackList[1] and self.moveAttack:
                    self.ignoreOwnStatsR = True
                    for defender in self.defenders:
                        defender.attackPercentBlocked = -1*math.inf
                '''Reduce all effects from the opponent by 50% (affect both opponents)'''
                if not tasklet and phase[0] == 0.5:
                    for opponent in sideList[1-self.side]:
                        opponent.abilitiesEffect = max(0, opponent.abilitiesEffect-0.5*self.specialBuffEffect)
                        opponent.specialBuffEffect = max(0, opponent.specialBuffEffect-0.5*self.specialBuffEffect)
                        opponent.moveEffect = [max(0, opponent.moveEffect[0]-0.5*self.specialBuffEffect), max(0, opponent.moveEffect[1]-0.5*self.specialBuffEffect)]
                '''if Sorensen does not use an attacking move this turn'''
                if not tasklet and phase[0] == 4:
                    if self.moveRecord[-1][0][1] == 'Enchantment':
                        if self.timeEffectiveness:
                            checkElement(self.timeEffects, 'Increase next attack damage by', True)
                            self.timeEffects.update({'Increase next attack damage by '+str(round(100*self.specialBuffEffect))+'%': 1})
        if tasklet and self.attackList[0] > self.attackList[1]:
            element = checkElement(self.timeEffects, 'Increase next attack damage by')
            if element:
                minusOneTime(self.timeEffects, element)
                self.attackPercentMultiplier += getNumber(element)
        for opponent in sideList[1-self.side]:
            if 'Elegy' in opponent.specialBuffs and self.specialBuffEffectiveness:
                '''When missing a move, fall into flinching for the entire battle'''
                if tasklet and opponent.missingList[0] > opponent.missingList[1]:
                    addStatusEffect(self, opponent, 'flinching', math.inf, True)
                '''Lose 100% maximum HP if unable to win the entire battle before this buff disappears'''
                if not tasklet and phase[0] == 4 and opponent.specialBuffs['Elegy'] == 1:
                    energyLoss(opponent, None, opponent.stats[5]*self.specialBuffEffect)

        # Chaos
        for opponent in sideList[1-self.side]:
            if not tasklet and moveStep[1-self.side][opponent.position] == '1':
                for i in self.entireBattleEffects:
                    if i.startswith('Make') and i.endswith(opponent.id):
                        move = ''
                        for j in i.split()[1:-2]:
                            move = move+j+' '
                        for k in range(len(opponent.moves)):
                            if opponent.moves[k][0][0] == move[:-1]:
                                opponent.moveEffectiveness[2][k] = False

        # Ascension
        if not tasklet and phase[0] == 0.5:
            for opponent in sideList[1-self.side]:
                if 'Cut off all healing effects from '+opponent.name.title()+' '+opponent.id in self.entireBattleEffects:
                    opponent.healingEffectiveness = False

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Chaos
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]):
                    '''Change the environment to "foreign dimension"'''
                    environment[0] = 'foreign dimension'
                    '''Enter {Inferno Galaxy} (effective for the entire battle and when absent)'''
                    self.specialBuffs.update({'Inferno Galaxy': math.inf})
                    if self.specialBuffEffectiveness:
                        for opponent in sideList[1-self.side]:
                            opponent.abilitiesEffect = max(0, opponent.abilitiesEffect-0.5*self.specialBuffEffect)
                            opponent.specialBuffEffect = max(0, opponent.specialBuffEffect-0.5*self.specialBuffEffect)
                            opponent.moveEffect = [max(0, opponent.moveEffect[0]-0.5*self.specialBuffEffect), max(0, opponent.moveEffect[1]-0.5*self.specialBuffEffect)]
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    if self.entireBattleEffectiveness:
                        self.opponentMoves = []
                        listOfBannedMoves = []
                        for i in self.entireBattleEffects:
                            move = ''
                            if i.startswith('Make') and i.endswith(self.target.id):
                                for j in i.split()[1:-2]:
                                    move = move+j+' '
                            listOfBannedMoves.append(move[:-1])
                        for i in range(len(self.target.moves)):
                            if not self.target.moves[i][0][0] in listOfBannedMoves:
                                self.opponentMoves.append(self.target.moves[i])
                        if self.opponentMoves != []:
                            random.shuffle(self.opponentMoves)
                            move1 = self.opponentMoves.pop()
                            self.entireBattleEffects.append('Make '+move1[0][0]+' ineffective '+self.target.id)
                            if self.opponentMoves != []:
                                move2 = self.opponentMoves.pop()
                                self.entireBattleEffects.append('Make '+move2[0][0]+' ineffective '+self.target.id)

        # Ascension
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.statsEEffectiveness:
                        '''Increase all stats by 10%'''
                        for i in range(4):
                            self.stats[i] = self.stats[i]*(1+0.1*self.moveEffect[1])
                        self.stats[5] = round(self.stats[5]*(1+0.1*self.moveEffect[1]))
                    if self.healingEffectiveness:
                        '''Heal 100% of maximum HP'''
                        heal(self, self.stats[5]*self.moveEffect[1], True)
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    if 'Inferno Galaxy' in self.specialBuffs:
                        if self.entireBattleEffectiveness and not 'Cut off all healing effects from '+self.target.name.title()+' '+self.target.id in self.entireBattleEffects:
                            self.entireBattleEffects.append('Cut off all healing effects from '+self.target.name.title()+' '+self.target.id)

        # Aria
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]):
                    '''Forcefully clear opponent's turn-effects'''
                    clearTurnEffects(self.target)
                    if notImmuned(self, self.moves[2], self.target) and not 'Elegy' in self.target.specialBuffs:
                        '''Impose {Elegy} on the opponent (effective for four turns)'''
                        self.target.specialBuffs.update({'Elegy': 4})
                        self.target.specialBuffsDescription.append(self.specialBuffsDescription[2])

        # Splendor
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[3], [self.target]):
                    attackDamage(self, [self.target], self.moves[3])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[3]):
                    '''Forcefully blind the opponent'''
                    addStatusEffect(self, self.target, 'blind', 0, True)
                    if notImmuned(self, self.moves[3], self.target):
                        '''Apply randomly 200-400 magic damage'''
                        magicDamage(self, self.target, random.randint(200,400)*self.moveEffect[0], True)

        # Myth
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.opponent, self.oppoTeammate]):
                    if isEffective(self, self.moves[4]) and 'Seal' in self.specialBuffs:
                        '''This attack damage will not be greater than 0 when in {Seal}'''
                        self.attackMax = 0
                    attackDamage(self, self.oppoHit, self.moves[4])
            elif moveStep[self.side][self.position] == 5:
                if isEffective(self, self.moves[4]):
                    '''Sacrifice self'''
                    sacrifice(self)

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Zacks(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'zacks'
        self.gender = 'male'
        self.color = (50,0,50)
        self.type = ['ghost', 'elder']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [92,137,113,114,124,152]

        # unique battle variables
        self.seckillChanceIncrement = 0.00 # chance of seckill increased by Celestial Extermination

    def resetUniqueVariables(self):
        self.seckillChanceIncrement = 0.00

    def resetAfterClear(self, element):
        if element == 'Immune from and rebound status effects':
            self.immunityFromStatusEffects = False
            self.reboundStatusEffects = False

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if tasklet and self.hp == self.stats[5]:
                '''When full HP'''
                if self.energyList[0] > self.energyList[1] and moveStep[self.side][self.position] == 1:
                    '''no energy loss by using moves'''
                    self.energyLossMultiplier = 0
                if self.receiveAttackList[0] < self.receiveAttackList[1]:
                    '''and lower opponent's all stats (-1) when receiving attack'''
                    if not self.attacker.immunityFromStatsR:
                        for i in range(6):
                            self.attacker.statsER[i] = max(-6, self.attacker.statsER[i]-round(self.abilitiesEffect))
            '''Reduce all attack damage received by 200'''
            if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
                self.receiveAttackIncrement -= 200*self.abilitiesEffect
            if not tasklet and moveStep[self.side][self.position] == '4':
                '''When the number of dead opponents = x, every move has a (5+5x)% chance of seckilling the opponent'''
                for opponent in self.oppoHit:
                    if opponent and not opponent.immunityFromSeckill:
                        number = 0
                        for identity in list(champIdDict):
                            if identity.startswith(str(1-self.side)) and champIdDict[identity].dead:
                                number += 1
                        if tryLuck((5+5*number)/100*self.abilitiesEffect+self.seckillChanceIncrement):
                            opponent.hp = 0
                            print(' ',opponent.name.title(),'got seckilled by Zacks.')

        # Demon's Rage
        for opponent in sideList[1-self.side]:
            if not tasklet and moveStep[opponent.side][opponent.position] == '1':
                if 'Make all enchantment moves from '+opponent.name.title()+' ineffective '+opponent.id in self.turnEffects:
                    opponent.moveEffectiveness[1] = False

        # Doomsday Declaration
        if not tasklet and moveStep[self.side][self.position] == '4' and isEffective(self, self.moveRecord[-1]):
            for opponent in self.oppoHit:
                if opponent and notImmuned(self, self.moveRecord[-1], opponent):
                    element = checkElement(self.turnEffects, 'All moves absorb')
                    if element:
                        effect = 1
                        if self.hp < 0.5*self.stats[5]:
                            effect = 2
                        magicDamage(self, opponent, getNumber(element)*opponent.stats[5]*effect)
                        if self.healingEffectiveness:
                            heal(self, self.magicDamageList[-1])
        if not tasklet and phase[0] == 0.5:
            if 'Immune from and rebound status effects' in self.turnEffects:
                self.immunityFromStatusEffects = True
                self.reboundStatusEffects = True

        # Absolute Decimation
        if tasklet and self.attackList[0] > self.attackList[1] and self.moveAttack:
            for defender in self.defenders:
                element = checkElement(self.turnEffects, 'Increase attack damage dealt by attacking moves by an amount equivalent to')
                if element:
                    defender.receiveAttackIncrement += getNumber(element)*defender.stats[5]

        # Power from Beyond
        if tasklet and self.attackList[0] > self.attackList[1] and self.moveAttack:
            if 'All attacking moves will make critical hits' in self.turnEffects:
                self.rateOfCriticalHitIncrement = math.inf

        # Celestial Extermination
        if not tasklet and moveStep[self.side][self.position] == '1':
            element = checkElement(self.timeEffects, 'Moves will have a')
            if element:
                minusOneTime(self.timeEffects, element)
                self.seckillChanceIncrement += getNumber(element)

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Demon's Rage
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]):
                    pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    triggered = max(self.target.statsER) > 0
                    if not self.target.immunityFromClearingStatsE:
                        '''Clear opponent's stats enhancement'''
                        clearStatsE(self.target)
                        successful = True
                    else:
                        successful = False
                    if (not triggered or not successful) and self.healingEffectiveness:
                        '''if not successful then heal 100% of maximum HP'''
                        heal(self, self.stats[5]*self.moveEffect[0], True)
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Make all enchantment moves from '+self.target.name.title()+' ineffective '+self.target.id: 2})
                        self.target.moveEffectiveness[1] = False
                elif isEffective(self, self.moves[0]) and self.healingEffectiveness:
                    heal(self, self.stats[5]*self.moveEffect[0], True)

        # Doomsday Declaration
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Immune from and rebound status effects': 5})
                        self.immunityFromStatusEffects = True
                        self.reboundStatusEffects = True
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'All moves absorb', True)
                        self.turnEffects.update({'All moves absorb '+fraction('1/3', self.moveEffect[1])+' of maximum HP from opponent; double the effect when own HP < 50%': 4})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])

        # Absolute Decimation
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    if self.statsEEffectiveness:
                        '''Raise special attack (+2), physical and special defense, and speed stats (+1); double the effect when own HP = 100%'''
                        effect = 1
                        if self.hp == self.stats[5]:
                            effect = 2
                        self.statsER[1] = min(6, self.statsER[1]+round(1*effect*self.moveEffect[1]))
                        self.statsER[2] = min(6, self.statsER[2]+round(1*effect*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(1*effect*self.moveEffect[1]))
                        self.statsER[4] = min(6, self.statsER[4]+round(1*effect*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'Increase attack damage dealt by attacking moves by an amount equivalent to', 'Increase attack damage dealt by attacking moves by an amount equivalent to '+fraction('1/3', self.moveEffect[1])+' of opponent\'s maximum HP', -1)
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])

        # Power from Beyond
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if isEffective(self, self.moves[3]) and max(self.target.statsER) <= 0:
                    '''Multiply this attack damage by 2 if opponent doesn't have stats enhancement'''
                    self.attackMultiplier = self.attackMultiplier*2*self.moveEffect[0]
                if notMissing(self, self.moves[3], [self.target]):
                    attackDamage(self, [self.target], self.moves[3])
                if isEffective(self, self.moves[3]) and self.target.hp > 0:
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'All attacking moves will make critical hits', 'All attacking moves will make critical hits', -2)

        # Celestial Extermination
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[4]):
                    if self.timeEffectiveness:
                        checkElement(self.timeEffects, 'Moves will have a', True)
                        self.timeEffects.update({'Moves will have a '+str(round(10*self.moveEffect[0]))+'% higher chance of seckilling the opponent': 2})
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.opponent, self.oppoTeammate]):
                    attackDamage(self, self.oppoHit, self.moves[4])
            elif moveStep[self.side][self.position] == 4:
                for opponent in self.oppoHit:
                    if opponent and isEffective(self, self.moves[4]) and notImmuned(self, self.moves[4], opponent):
                        triggered = opponent.turnEffects != {}
                        if not opponent.immunityFromClearingTurnEffects:
                            '''Clear opponent's turn-effects; if successful then deal 300 attack damage'''
                            clearTurnEffects(opponent)
                            if triggered:
                                attackDamage(self, [opponent], True, 300*self.moveEffect[0])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Eet(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        self.name = 'eet'
        self.gender = 'female'
        self.color = (255,255,255)
        self.type = ['god']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [90,135,110,110,125,150]

        # unique battle variables
        self.playerSelectionSurface = None
        self.typesOwned = ['god'] # a list of types owned
        self.typesNotOwned = [] # a list of types not owned
        self.typeToAdd = '' # a new type to own this turn
        self.finishedSelecting1 = False # if the player has finished selecting a new type to own
        self.typeToBecome = ['god'] # a type to become this turn
        self.statsBoosted = False # True when stats are boosted by Eet's Realm

    def playerSelect(self, clicked=False):
        if self.moveRecord[-1] == self.moves[0] and not self.finishedSelecting1:
            self.typesNotOwned = []
            for i in typeMatrix:
                if not i[0] in self.typesOwned:
                    self.typesNotOwned.append(i[0])
            if len(self.typesNotOwned) > 0:
                if self.playerSelectionSurface == None:
                    self.playerSelectionSurface = PlayerSelectionSurface(self, 'Eet: Select a new type to own this turn')
                    battlegroup.add(self.playerSelectionSurface)
                    battlegroup.move_to_front(self.playerSelectionSurface)
                    self.playerSelectionSurface.typesNotOwned = []
                    for i in range(len(self.typesNotOwned)):
                        self.playerSelectionSurface.typesNotOwned.append(pygame.Surface((102,30)).convert_alpha())
                    self.playerSelectionSurface.image.blit(self.playerSelectionSurface.ok, (210,310))
                    self.typeToAdd = self.typesNotOwned[0]
                else:
                    counter = 0
                    for i in range(len(self.typesNotOwned)):
                        if i != 0 and i%5 == 0:
                            counter += 5
                        if self.playerSelectionSurface.typesNotOwned[i].get_rect(center=(326+107*(i-counter),270+30*(counter/4+1))).collidepoint(pygame.mouse.get_pos()):
                            self.playerSelectionSurface.typesNotOwned[i].fill((10,185,225))
                            centerText(self.playerSelectionSurface.typesNotOwned[i], self.typesNotOwned[i], 'timesnewroman', 18, (0,0,0))
                            self.playerSelectionSurface.image.blit(self.playerSelectionSurface.typesNotOwned[i], (5+107*(i-counter),75+30*(counter/4+1)))
                            if clicked:
                                self.typeToAdd = self.typesNotOwned[i]
                        else:
                            if self.typesNotOwned[i] == self.typeToAdd:
                                self.playerSelectionSurface.typesNotOwned[i].fill((10,185,225))
                            else:
                                self.playerSelectionSurface.typesNotOwned[i].fill((255,255,255))
                            centerText(self.playerSelectionSurface.typesNotOwned[i], self.typesNotOwned[i], 'timesnewroman', 18, (0,0,0))
                            self.playerSelectionSurface.image.blit(self.playerSelectionSurface.typesNotOwned[i], (5+107*(i-counter),75+30*(counter/4+1)))
                            if clicked and self.playerSelectionSurface.ok.get_rect(center=(540,510)).collidepoint(pygame.mouse.get_pos()):
                                self.finishedSelecting1 = True
            else:
                self.finishedSelecting1 = True
        else:
            if self.playerSelectionSurface == None:
                self.playerSelectionSurface = PlayerSelectionSurface(self, 'Eet: Select a type to become this turn')
                battlegroup.add(self.playerSelectionSurface)
                battlegroup.move_to_front(self.playerSelectionSurface)
                self.playerSelectionSurface.typesOwned = []
                for i in range(len(self.typesOwned)):
                    self.playerSelectionSurface.typesOwned.append(pygame.Surface((102,30)).convert_alpha())
                self.playerSelectionSurface.image.blit(self.playerSelectionSurface.ok, (210,310))
                self.typeToBecome = self.typesOwned[0]
            else:
                counter = 0
                for i in range(len(self.typesOwned)):
                    if i != 0 and i%5 == 0:
                        counter += 5
                    if self.playerSelectionSurface.typesOwned[i].get_rect(center=(326+107*(i-counter),270+30*(counter/4+1))).collidepoint(pygame.mouse.get_pos()):
                        self.playerSelectionSurface.typesOwned[i].fill((10,185,225))
                        centerText(self.playerSelectionSurface.typesOwned[i], self.typesOwned[i], 'timesnewroman', 18, (0,0,0))
                        self.playerSelectionSurface.image.blit(self.playerSelectionSurface.typesOwned[i], (5+107*(i-counter),75+30*(counter/4+1)))
                        if clicked:
                            self.typeToBecome = self.typesOwned[i]
                    else:
                        if self.typesOwned[i] == self.typeToBecome:
                            self.playerSelectionSurface.typesOwned[i].fill((10,185,225))
                        else:
                            self.playerSelectionSurface.typesOwned[i].fill((255,255,255))
                        centerText(self.playerSelectionSurface.typesOwned[i], self.typesOwned[i], 'timesnewroman', 18, (0,0,0))
                        self.playerSelectionSurface.image.blit(self.playerSelectionSurface.typesOwned[i], (5+107*(i-counter),75+30*(counter/4+1)))
                        if clicked and self.playerSelectionSurface.ok.get_rect(center=(540,510)).collidepoint(pygame.mouse.get_pos()):
                            self.phaseFinished = True
                            self.playerSelecting = False
                            self.finishedSelecting1 = False
        return True

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if not tasklet and phase[0] == 0.5:
                '''Immune from clearing stats reduction and status effects'''
                self.immunityFromStatsR = True
                self.immunityFromStatusEffects = True
                '''All moves are non-missable and always effective'''
                self.missingIgnored = True
                self.ineffectiveIgnored = True
            if tasklet and self.receiveMagicList[0] > self.receiveMagicList[1]: 
                '''Block all magic damage received'''
                self.magicPercentBlocked += 1

        # special buffs
        if not tasklet:
            if 'Eet\'s Realm' in self.specialBuffs and self.specialBuffEffectiveness:
                '''Increase all stats by 10% when effective'''
                if not self.statsBoosted:
                    self.statsBoosted = True
                    for i in range(4):
                        self.stats[i] = self.stats[i]*(1+0.1*self.specialBuffEffect)
                    self.stats[5] = round(self.stats[5]*(1+0.1*self.specialBuffEffect))
                if phase[0] == 2:
                    '''At the start of every turn, can become a specific type based on types of power owned'''
                    self.type = [self.typeToBecome]
                if phase[0] == 4:
                    '''Heal 200 HP at the end of every turn'''
                    if self.healingEffectiveness:
                        heal(self, 200*self.specialBuffEffect)
        if tasklet and 'Inexhaustible Resources' in self.specialBuffs:
            '''When having x types of power, increase healing effects and attack damage by 10x%'''
            if self.specialBuffEffectiveness:
                if self.healingList[0] > self.healingList[1]:
                    self.healingEffect += 0.1*len(self.typesOwned)*self.specialBuffEffect
                if self.attackList[0] > self.attackList[1]:
                    self.attackPercentMultiplier += 0.1*len(self.typesOwned)*self.specialBuffEffect

        # Imperial Supremacy
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1] and self.attacker.moveAttack:
            element = checkElement(self.turnEffects, 'Reduce')
            if element:
                self.receiveAttackPercentMultiplier -= getNumber(element)

        # Zenith Absolution
        for opponent in sideList[1-self.side]:
            if not tasklet and self in opponent.oppoHit and moveStep[1-self.side][opponent.position] == '3':
                if 'Immune from the effects of the opponent\'s move' in self.timeEffects:
                    minusOneTime(self.timeEffects, 'Immune from the effects of the opponent\'s move')
                    self.immunityFromMoves[opponent] = [True,True]

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Imperial Supremacy
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]):
                    self.typesOwned.append(self.typeToAdd)
                    typesOwned = ''
                    for i in self.typesOwned:
                        typesOwned = typesOwned+i+', '
                    self.specialBuffs.update({'Eet\'s Realm': str(math.inf)+' ['+typesOwned[:-2]+']'})
                    '''Enter {Eet's Realm} (effective for the entire battle and when absent) and select one type of power to own'''
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'Reduce', True)
                        self.turnEffects.update({'Reduce '+str(round(50*self.moveEffect[1]))+'% of attack damage dealt by attacking moves received for two turns': 2})
                    if self.statsEEffectiveness:
                        '''Raise all stats (+1)'''
                        for i in range(6):
                            self.statsER[i] = min(6, self.statsER[i]+round(self.moveEffect[1]))
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Rainbow Effulgence
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[1], [self.opponent, self.oppoTeammate]):
                    if isEffective(self, self.moves[1]):
                        '''Effective against types owned'''
                        typeEffectiveness = []
                        for opponent in self.oppoHit:
                            effectiveness = 0
                            for i in opponent.type:
                                if i in self.typesOwned:
                                    effectiveness += 2
                                else:
                                    effectiveness += 1
                            effectiveness = effectiveness/len(opponent.type)
                            if len(opponent.type) > 1 and effectiveness == 2.0:
                                effectiveness = len(opponent.type)*2.0
                            typeEffectiveness.append(effectiveness)
                    attackDamage(self, [self.target], self.moves[1], 0, typeEffectiveness)
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                        '''Impose randomly two status effects on the opponent'''
                        statusEffectsList = list(statusEffectsDescription.keys())
                        random.shuffle(statusEffectsList)
                        addStatusEffect(self, self.target, statusEffectsList.pop())
                        addStatusEffect(self, self.target, statusEffectsList.pop())

        # Majestic Vertex Array
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    '''Gain a 500 HP shield'''
                    if not self.shield > 0:
                        self.shield = min(1000, self.shield+round(500*self.moveEffect[1]))
                    if 'Eet\'s Realm' in self.specialBuffs:
                        '''Gain {Inexhaustible Resources} (effective for the entire battle) if in {Eet’s Realm}'''
                        self.specialBuffs.update({'Inexhaustible Resources': math.inf})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    '''Clear opponent’s stats enhancement'''
                    if not self.target.immunityFromClearingStatsE:
                        clearStatsE(self.target)

        # Zenith Absolution
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    '''For the next time, immune from the effects of the opponent's move'''
                    if self.timeEffectiveness:
                        self.timeEffects.update({'Immune from the effects of the opponent\'s move': 1})
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[3], [self.target]):
                    if isEffective(self, self.moves[3]):
                        if max(self.statsER) > 0:
                            '''Critical hit if having stats enhancement'''
                            self.rateOfCriticalHitIncrement = math.inf
                    attackDamage(self, [self.target], self.moves[3])

        # Eet’s Dynasty
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4], self.hp-1)
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    for i in range(len(self.typesOwned)):
                        attackDamage(self, [self.target], self.moves[4])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Seidel(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        self.name = 'seidel'
        self.gender = 'male'
        self.color = (128,0,128)
        self.type = ['dimension', 'spirit']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [140,85,115,110,115,155]

        # unique battle variables
        self.playerSelectionSurface = None
        self.moveChosen = 0 # a move index from the opponent that's to be ineffective this turn, selected by player
        self.ownStatsER = [] # for transferring statsR
        self.magic = False # if having applied magic damage after healing

    def resetAfterClear(self, element):
        for opponent in sideList[1-self.side]:
            if element == 'Make '+opponent.name.title()+'\'s abilities and special buffs ineffective '+opponent.id:
                opponent.abilitiesEffectiveness = True
                opponent.specialBuffEffectiveness = True
        if element == 'Seidel\'s Realm':
            self.immunityFromStatusEffects = False

    def playerSelect(self, clicked=False):
        if self.playerSelectionSurface == None:
            self.playerSelectionSurface = PlayerSelectionSurface(self, 'Seldel: Select a move from the opponent to make ineffective if going first')
            battlegroup.add(self.playerSelectionSurface)
            battlegroup.move_to_front(self.playerSelectionSurface)
            self.playerSelectionSurface.oppoMoves = []
            for i in range(5):
                self.playerSelectionSurface.oppoMoves.append(pygame.Surface((102,120)).convert_alpha())
            self.playerSelectionSurface.image.blit(self.playerSelectionSurface.ok, (210,310))
        else:
            for i in range(5):
                if self.playerSelectionSurface.oppoMoves[i].get_rect(center=(326+i*107,380)).collidepoint(pygame.mouse.get_pos()):
                    self.playerSelectionSurface.oppoMoves[i].fill((50,50,50))
                    centerParagraph(False, self.playerSelectionSurface.oppoMoves[i], self.target.moves[i][0][0], 'timesnewroman', 18, (255,255,255))
                    self.playerSelectionSurface.image.blit(self.playerSelectionSurface.oppoMoves[i], (5+i*107,140))
                    if clicked:
                        self.moveChosen = i
                else:
                    if i == self.moveChosen:
                        self.playerSelectionSurface.oppoMoves[i].fill((50,50,50))
                    else:
                        self.playerSelectionSurface.oppoMoves[i].fill((0,0,0))
                    centerParagraph(False, self.playerSelectionSurface.oppoMoves[i], self.target.moves[i][0][0], 'timesnewroman', 18, (255,255,255))
                    self.playerSelectionSurface.image.blit(self.playerSelectionSurface.oppoMoves[i], (5+i*107,140))
                    if clicked and self.playerSelectionSurface.ok.get_rect(center=(540,510)).collidepoint(pygame.mouse.get_pos()):
                        self.phaseFinished = True
                        self.playerSelecting = False
        return True

    def executeEffects(self, tasklet=False):
        # abilities
        if not tasklet and self.abilitiesEffectiveness:
            if moveStep[self.side][self.position] == '4':
                if self.goesFirst[abs(self.position-self.target.position)] and self.turnEffectiveness:
                    '''When going first, make one move from the opponent ineffective this turn'''
                    self.turnEffects.update({'Make '+self.target.moves[self.moveChosen][0][0]+' (from '+self.target.name.title()+') ineffective '+self.target.id: 1})
            for i in range(len(self.goesFirst)):
                oppoList = [self.opponent, self.oppoTeammate]
                if oppoList[i] and not self.goesFirst[i]:
                    '''When the opponent goes first'''
                    if moveStep[1-self.side][oppoList[i].position] == '1':
                        '''immune from the effects of their attacking moves'''
                        self.immunityFromMoves[oppoList[i]][0] = True
                    if moveStep[self.side][self.position] == '4' and oppoList[i] in self.oppoHit:
                        '''clear their turn-effects when using a move this turn'''
                        if not oppoList[i].immunityFromClearingTurnEffects:
                            clearTurnEffects(oppoList[i])
        for opponent in sideList[1-self.side]:
            if not tasklet and moveStep[1-self.side][opponent.position] == '1' and checkElement(self.turnEffects, 'Make', False, opponent.name.title()+') ineffective '+opponent.id):
                opponent.moveEffectiveness[2][self.moveChosen] = False

        # special buffs
        if 'Seidel\'s Realm' in self.specialBuffs:
            if self.specialBuffEffectiveness:
                if not tasklet and phase[0] == 0.5:
                    '''Immune from status effects'''
                    self.immunityFromStatusEffects = True
                if not tasklet and moveStep[self.side][self.position] == '2':
                    '''All moves heal 1/3 of maximum HP'''
                    if self.healingEffectiveness:
                        heal(self, self.stats[5]/3*self.specialBuffEffect)
                if tasklet and self.opponent and self.healingList[0] < self.healingList[1] and not self.magic:
                    '''Apply an equal amount of magic damage to the opponent when healing'''
                    self.magic = True
                    magicDamage(self, self.opponent, self.healingAmountList[-1])
                if not tasklet:
                    self.magic = False

        # Seidel's Realm
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1] and self.attacker.moveAttack:
            if 'Block attack damage dealt by the opponent\'s next attacking move' in self.timeEffects:
                minusOneTime(self.timeEffects, 'Block attack damage dealt by the opponent\'s next attacking move')
                self.attackPercentBlocked += 1

        # Broken Star Dominion
        for opponent in sideList[1-self.side]:
            if tasklet and opponent.receiveAttackList[0] > opponent.receiveAttackList[1]:
                element = checkElement(self.timeEffects, 'Multiply attack damage received by', False, opponent.id)
                if element:
                    minusOneTime(self.timeEffects, element)
                    opponent.receiveAttackMultiplier = opponent.receiveAttackMultiplier*getNumber(element)
        if not tasklet and phase[0] == 2:
            element = checkElement(self.turnEffects, 'All moves will go first')
            if element:
                self.preemptiveIncrement += getNumber(element)

        # Interstellar Cloud
        if not tasklet and phase[0] == 0:
            for opponent in sideList[1-self.side]:
                if 'Make '+opponent.name.title()+'\'s abilities and special buffs ineffective '+opponent.id in self.turnEffects:
                    opponent.abilitiesEffectiveness = False
                    opponent.specialBuffEffectiveness = False

        # World's End
        if not tasklet and moveStep[self.side][self.position] == '1':
            element = checkElement(self.timeEffects, 'Multiply effects of the next move by')
            if element:
                minusOneTime(self.timeEffects, element)
                number = getNumber(element)
                self.moveEffect[0], self.moveEffect[1] = self.moveEffect[0]*number, self.moveEffect[1]*number

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Seidel's Realm
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]):
                    '''Enter {Seidel’s Realm} (effective for the entire battle)'''
                    self.specialBuffs.update({'Seidel\'s Realm': math.inf})
                    if self.specialBuffEffectiveness:
                        self.immunityFromStatusEffects = True
                    if self.timeEffectiveness:
                        self.timeEffects.update({'Block attack damage dealt by the opponent\'s next attacking move': 1})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[0], [self.target])

        # Debris Oblivion
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    self.ownStatsER = copy.deepcopy(self.statsER)
                    clearStatsR(self)
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[1], [self.target]):
                    attackDamage(self, [self.target], self.moves[1])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    if not self.target.immunityFromClearingStatsE:
                        '''Inverse opponent's stats enhancement'''
                        if not self.target.immunityFromStatsR:
                            inverseStatsE(self.target)
                        else:
                            clearStatsE(self.target)
                    if not self.target.immunityFromStatsR:
                        '''transfer own stats reduction to opponent'''
                        transferStatsR(self.ownStatsER, self.target)
                    '''Apply 200 magic damage'''
                    magicDamage(self, self.target, 200*self.moveEffect[0], True)

        # Broken Star Dominion
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    if self.statsEEffectiveness:
                        '''Raise physical attack, physical and special defense, and speed stats (+1)'''
                        self.statsER[0] = min(6, self.statsER[0]+round(1*self.moveEffect[1]))
                        self.statsER[2] = min(6, self.statsER[2]+round(1*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(1*self.moveEffect[1]))
                        self.statsER[4] = min(6, self.statsER[4]+round(1*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'All moves will go first', 'All moves will go first (+'+str(round(1*self.moveEffect[1]))+')', -2)
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    if self.timeEffectiveness:
                        checkElement(self.timeEffects, 'Multiply attack damage received by', True, self.target.id)
                        self.timeEffects.update({'Multiply attack damage received by '+self.target.name.title()+' by '+str(round(2*self.moveEffect[1]))+' '+self.target.id: 1})

        # Interstellar Cloud
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[3], [self.target]):
                    attackDamage(self, [self.target], self.moves[3])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[3]) and notImmuned(self, self.moves[3], self.target):
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'Make '+self.target.name.title()+'\'s abilities and special buffs ineffective '+self.target.id, 'Make '+self.target.name.title()+'\'s abilities and special buffs ineffective '+self.target.id, -1)
                    '''Absorb 80 maximum HP from the opponent'''
                    self.target.stats[5] = max(1, self.target.stats[5]-round(80*self.moveEffect[0]))
                    self.target.hp = min(self.target.stats[5], self.target.hp)
                    self.stats[5] += round(80*self.moveEffect[0])

        # World's End
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[4]):
                    if self.timeEffectiveness:
                        checkElement(self.timeEffects, 'Multiply effects of the next move by', True)
                        self.timeEffects.update({'Multiply effects of the next move by '+str(round(2*self.moveEffect[0])): 1})
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    if isEffective(self, self.moves[4]) and 'Seidel\'s Realm' in self.specialBuffs:
                        '''Increase this attack damage by an amount equivalent to 1/3 of HP if in {Seidel’s Realm}'''
                        self.attackIncrement += self.hp/3*self.moveEffect[0]
                    attackDamage(self, [self.target], self.moves[4])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Cassius(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'cassius'
        self.gender = 'male'
        self.color = (200,200,255)
        self.type = ['ghost', 'fighting']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [130,105,100,105,135,145]

        # unique battle variables
        self.energyLevels = 0 # special buff
        self.healed = False # if having healed after receiving attack at energy level 5

    def resetAfterClear(self, element):
        for opponent in sideList[1-self.side]:
            if element == 'Cut off all healing effects from '+opponent.name.title()+' '+opponent.id:
                opponent.healingEffectiveness = True
        if element == 'Energy Levels':
            if self.energyLevels >= 1:
                self.preemptiveIncrement -= self.specialBuffEffect
            if self.energyLevels >= 2:
                self.ineffectiveIgnored = False
            if self.energyLevels >= 4:
                self.immunityFromClearingTurnEffects = True
            self.energyLevels = 0

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if not tasklet and phase[0] == 0.5 and turn[0] == 1:
                self.turnEffects.update({'Immune from the effects of the opponent\'s moves': 2})
                '''Has {Energy Levels} (effective for the entire battle but reset once subbed out)'''
                self.specialBuffs.update({'Energy Levels': str(math.inf)+' ['+str(self.energyLevels)+']'})
            if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
                '''When having x energy levels, reduce attack damage received by 10x%'''
                self.receiveAttackPercentMultiplier -= 10*self.energyLevels*self.abilitiesEffect/100
        for opponent in sideList[1-self.side]:
            if not tasklet and self in opponent.oppoHit and moveStep[1-self.side][opponent.position] == '3':
                if 'Immune from the effects of the opponent\'s moves' in self.turnEffects:
                    self.immunityFromMoves[opponent] = [True,True]

        # special buffs
        if 'Energy Levels' in self.specialBuffs:
            if self.specialBuffEffectiveness:
                if not tasklet and self.energyLevels >= 1:
                    '''All moves go first (+1)'''
                    if phase[0] == 2:
                        self.preemptiveIncrement += self.specialBuffEffect
                if not tasklet and self.energyLevels >= 2:
                    '''All moves are always effective'''
                    self.ineffectiveIgnored = True
                if not tasklet and self.energyLevels >= 3:
                    '''All moves clear opponent's stats enhancement.'''
                    if moveStep[self.side][self.position] == '4':
                        for opponent in self.oppoHit:
                            if opponent and not opponent.immunityFromClearingStatsE:
                                clearStatsE(opponent)
                if not tasklet and self.energyLevels >= 4:
                    '''Immune from clearing turn-effects'''
                    self.immunityFromClearingTurnEffects = True
                if tasklet and self.energyLevels >= 5:
                    '''Heal 1/3 of maximum HP when receiving attack damage'''
                    if self.receiveAttackList[0] < self.receiveAttackList[1] and self.healingEffectiveness and not self.healed:
                        self.healed = True
                        heal(self, 1/3*self.stats[5]*self.specialBuffEffect)
                    if not tasklet:
                        self.healed = False
                if tasklet and self.energyLevels >= 6:
                    '''Block all magic damage received'''
                    if self.receiveMagicList[0] > self.receiveMagicList[1]: 
                        self.magicPercentBlocked += 1
                if tasklet and self.energyLevels >= 7:
                    '''Multiply all attack damage by 2'''
                    if self.attackList[0] > self.attackList[1]:
                        self.attackMultiplier = self.attackMultiplier*2

        # Quantum Extinction Wave
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
            element = checkElement(self.timeEffects, 'Rebound')
            if element:
                minusOneTime(self.timeEffects, element)
                self.attackPercentRebounded += getNumber(element)

        # Cosmological Mastery
        if not tasklet and moveStep[self.side][self.position] == '2':
            element = checkElement(self.turnEffects, 'All moves gain')
            if element and 'Energy Levels' in self.specialBuffs:
                self.energyLevels = min(7, self.energyLevels+round(getNumber(element)*self.abilitiesEffect))
                self.specialBuffs['Energy Levels'] = str(math.inf)+' ['+str(self.energyLevels)+']'

        # Seal of Soul
        if not tasklet and phase[0] == 2:
            for opponent in sideList[1-self.side]:
                element = checkElement(self.turnEffects, 'At the start of each turn, absorb', False, opponent.id)
                if element:
                    magicDamage(self, opponent, getNumber(element))
                    if self.healingEffectiveness:
                        heal(self, self.magicDamageList[-1])
        if not tasklet and phase[0] == 0.5:
            for opponent in sideList[1-self.side]:
                if 'Cut off all healing effects from '+opponent.name.title()+' '+opponent.id in self.turnEffects:
                    opponent.healingEffectiveness = False

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Quantum Extinction Wave
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]):
                    if self.timeEffectiveness:
                        checkElement(self.timeEffects, 'Rebound', True)
                        self.timeEffects.update({'Rebound '+str(round(150*self.moveEffect[0]))+'% of attack damage received': 1})
                    if 'Energy Levels' in self.specialBuffs:
                        self.energyLevels = min(7, self.energyLevels+round(1*self.moveEffect[0]))
                        self.specialBuffs['Energy Levels'] = str(math.inf)+' ['+str(self.energyLevels)+']'
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    critical = attackDamage(self, [self.target], self.moves[0])
                    if isEffective(self, self.moves[0]) and critical[0] and 'Energy Levels' in self.specialBuffs:
                        '''Gain 2 energy levels if critical hit; otherwise gain 1 energy level.'''
                        self.energyLevels = min(7, self.energyLevels+round(1*self.moveEffect[0]))
                        self.specialBuffs['Energy Levels'] = str(math.inf)+' ['+str(self.energyLevels)+']'

        # Cosmological Mastery
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.statsEEffectiveness:
                        '''Raise physical and special attack and speed stats (+2)'''
                        self.statsER[0] = min(6, self.statsER[0]+round(2*self.moveEffect[1]))
                        self.statsER[1] = min(6, self.statsER[1]+round(2*self.moveEffect[1]))
                        self.statsER[4] = min(6, self.statsER[4]+round(2*self.moveEffect[1]))
                    if self.healingEffectiveness:
                        '''Heal 100% of maximum HP'''
                        heal(self, self.stats[5]*self.moveEffect[1], True)
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'All moves gain', True)
                        self.turnEffects.update({'All moves gain '+str(round(1*self.moveEffect[1]))+' energy level': 3})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])

        # Seal of Soul
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'At the start of each turn, absorb', 'At the start of each turn, absorb '+str(round(200*self.moveEffect[1]))+' HP from '+self.target.name.title()+' '+self.target.id, -2, self.target.id)
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Cut off all healing effects from '+self.target.name.title()+' '+self.target.id: 2})
                        self.target.healingEffectiveness = False

        # Trial of Gods
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[3], [self.target]):
                    attackDamage(self, [self.target], self.moves[3])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[3]) and notImmuned(self, self.moves[3], self.target):
                    if not self.target.immunityFromClearingTurnEffects:
                        '''Clear opponent's turn-effects'''
                        clearTurnEffects(self.target)
                    '''Make the opponent lose an amount of energy equivalent to 35% of their maximum HP'''
                    energyLoss(self.target, True, 0.35*self.target.stats[5]*self.moveEffect[0])

        # Apocalyptic Ultimatum
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.opponent, self.oppoTeammate]):
                    if isEffective(self, self.moves[4]) and 'Energy Levels' in self.specialBuffs:
                        '''Increase this attack damage by 30y % and lose y energy levels when having y energy levels.'''
                        self.attackPercentMultiplier += 0.3*self.energyLevels*self.moveEffect[0]
                        self.energyLevels = 0
                        self.specialBuffs['Energy Levels'] = str(math.inf)+' ['+str(self.energyLevels)+']'
                    attackDamage(self, self.oppoHit, self.moves[4])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Erring(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'erring'
        self.gender = 'male'
        self.color = (0,200,200)
        self.type = ['rock', 'fire']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [126,83,123,121,109,156]

        # unique battle variables
        self.critical = [] # to detect if Magma Burst is critical hit.
        self.opponentMoves = None # a list of opponent's moves still effective
        self.receiveAttackDamageListCopy = [] # keeps track of attack damage received

    def resetUniqueVariables(self):
        self.receiveAttackDamageListCopy = copy.deepcopy(self.receiveAttackDamageList)

    def resetAfterClear(self, element):
        for opponent in sideList[1-self.side]:
            if element == 'Make '+opponent.name.title()+'\'s status effects ineffective '+opponent.id:
                opponent.statusEffectiveness = True

    def executeEffects(self, tasklet=False):
        # abilities
        if not tasklet and self.abilitiesEffectiveness:
            if phase[0] == 2:
                '''At the start of every turn, gain a 200 HP shield or recover an equal amount of shield health if already having a shield'''
                self.shield = min(1000, self.shield+round(200*self.abilitiesEffect))
            if phase[0] == 4:
                if self.receiveAttackDamageListCopy == self.receiveAttackDamageList:
                    if self.healingEffectiveness:
                        '''At the end of every turn, heal 200 HP if no attack damage is received this turn'''
                        heal(self, 200*self.abilitiesEffect)
                elif self.turnEffectiveness:
                    '''otherwise block all attack damage received next turn'''
                    trickyTurnUpdate(self.turnEffects, 'Block all attack damage received', 'Block all attack damage received', -1)
            if phase[0] == 0.5:
                '''Immune from clearing turn-effects'''
                self.immunityFromClearingTurnEffects = True
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
            if 'Block all attack damage received' in self.turnEffects:
                self.attackPercentBlocked += 1

        # Magma Burst
        if not tasklet and phase[0] == 0.5:
            for opponent in sideList[1-self.side]:
                if 'Make '+opponent.name.title()+'\'s status effects ineffective '+opponent.id in self.turnEffects:
                    opponent.statusEffectiveness = False

        # Fire from the Core
        if not tasklet and moveStep[self.side][self.position] == '4' and isEffective(self, self.moveRecord[-1]) and self.healingEffectiveness:
            element = checkElement(self.turnEffects, 'All moves heal')
            if element:
                magic = False
                if self.hp > self.stats[5]*0.5:
                    magic = True
                heal(self, getNumber(element)*self.stats[5])
                if magic:
                    for opponent in self.oppoHit:
                        if opponent and notImmuned(self, self.moveRecord[-1], opponent):
                            magicDamage(self, opponent, self.healingAmountList[-1])
        if tasklet and self.attackList[0] > self.attackList[1]:
            element = checkElement(self.turnEffects, 'Increase all damage dealt or applied by')
            if element:
                self.attackPercentMultiplier += getNumber(element)
        if tasklet and self.magicList[0] > self.magicList[1]:
            element = checkElement(self.turnEffects, 'Increase all damage dealt or applied by')
            if element:
                self.magicPercentMultiplier += getNumber(element)

        # Earth is the Limit
        if not tasklet and phase[0] == 2:
            element = checkElement(self.turnEffects, 'Move will go first')
            if element:
                self.preemptiveIncrement += getNumber(element)

        # Mountain Crushing Force
        for opponent in sideList[1-self.side]:
            if not tasklet and moveStep[1-self.side][opponent.position] == '1':
                for i in self.entireBattleEffects:
                    if i.startswith('Make') and i.endswith(opponent.id):
                        move = ''
                        for j in i.split()[1:-2]:
                            move = move+j+' '
                        for k in range(len(opponent.moves)):
                            if opponent.moves[k][0][0] == move[:-1]:
                                opponent.moveEffectiveness[2][k] = False

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Magma Burst
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.opponent, self.oppoTeammate]):
                    self.critical = attackDamage(self, self.oppoHit, self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]):
                    for opponent in self.oppoHit:
                        if opponent and notImmuned(self, self.moves[0], opponent):
                            if self.critical[self.oppoHit.index(opponent)] and self.turnEffectiveness:
                                self.turnEffects.update({'Make '+opponent.name.title()+'\'s status effects ineffective '+opponent.id: 3})
                                opponent.statusEffectiveness = False
                            '''Burn the opponent'''
                            addStatusEffect(self, opponent, 'burnt')

        # Fire from the Core
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'All moves heal', True)
                        self.turnEffects.update({'All moves heal '+fraction('1/3', self.moveEffect[1])+' of maximum HP; apply an equal amount of magic damage when own HP > 50%': 4})
                        checkElement(self.turnEffects, 'Increase all damage dealt or applied by', True)
                        self.turnEffects.update({'Increase all damage dealt or applied by '+str(round(50*self.moveEffect[1]))+'%': 3})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])

        # Seismic Meltdown
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[2], [self.target]):
                    attackDamage(self, [self.target], self.moves[2])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    '''Apply 222 magic damage; double the effect when own HP > opponent's HP'''
                    effect = 1
                    if self.hp > self.target.hp:
                        effect = 2
                    magicDamage(self, self.target, 222*effect*self.moveEffect[0], True)

        # Earth is the Limit
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.statsEEffectiveness:
                        '''Raise physical attack and physical and special defense stats (+2)'''
                        self.statsER[0] = min(6, self.statsER[0]+round(2*self.moveEffect[1]))
                        self.statsER[2] = min(6, self.statsER[2]+round(2*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(2*self.moveEffect[1]))
                    if self.shield > 0:
                        '''When having a shield, recover 500 shield health'''
                        self.shield = min(1000, self.shield+round(500*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'Move will go first', 'Move will go first (+'+str(round(2*self.moveEffect[1]))+')', -1)
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[3], [self.target])

        # Mountain Crushing Force
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    if isEffective(self, self.moves[4]):
                        '''This attack damage can not be blocked'''
                        self.target.attackPercentBlocked = -1*math.inf
                    attackDamage(self, [self.target], self.moves[4])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[4]):
                    '''Forcefully clear opponent's turn-effects'''
                    clearTurnEffects(self.target)
                    if notImmuned(self, self.moves[4], self.target) and self.entireBattleEffectiveness:
                        self.opponentMoves = []
                        listOfBannedMoves = []
                        for i in self.entireBattleEffects:
                            move = ''
                            if i.startswith('Make') and i.endswith(self.target.id):
                                for j in i.split()[1:-2]:
                                    move = move+j+' '
                            listOfBannedMoves.append(move[:-1])
                        for i in range(len(self.target.moves)):
                            if not self.target.moves[i][0][0] in listOfBannedMoves:
                                self.opponentMoves.append(self.target.moves[i])
                        if self.opponentMoves != []:
                            random.shuffle(self.opponentMoves)
                            move1 = self.opponentMoves.pop()
                            self.entireBattleEffects.append('Make '+move1[0][0]+' ineffective '+self.target.id)
                            if self.opponentMoves != []:
                                move2 = self.opponentMoves.pop()
                                self.entireBattleEffects.append('Make '+move2[0][0]+' ineffective '+self.target.id)

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Kuubaesah(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'kuubaesah'
        self.gender = 'male'
        self.color = (150,0,0)
        self.type = ['fighting', 'elder']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [150,45,120,120,130,150]

        # unique battle variables
        self.damageStored = 0 # damage stored in Enchanted Armor

    def resetAfterClear(self, element):
        if element == 'Throne Power':
            self.immunityFromSeckill = False
            self.reboundStatusEffects = False

    def executeEffects(self, tasklet=False):
        # abilities
        if not tasklet and self.abilitiesEffectiveness:
            if phase[0] == 0.5 and turn[0] == 1:
                '''For the first turn of the battle'''
                self.turnEffects.update({'Block all damage received': 1})
                '''Increase special attack stats by an amount equivalent to 60% of physical attack stats'''
                self.stats[1] += self.stats[0]*0.6*self.abilitiesEffect
            if phase[0] == 2 and self.statsEEffectiveness:
                '''Raise physical and special attack stats (+1) at the start of every turn'''
                self.statsER[0] = min(6, self.statsER[0]+round(self.abilitiesEffect))
                self.statsER[1] = min(6, self.statsER[1]+round(self.abilitiesEffect))
        if tasklet and 'Block all damage received' in self.turnEffects:
            if self.receiveAttackList[0] > self.receiveAttackList[1]:
                self.attackPercentBlocked += 1
            if self.receiveMagicList[0] > self.receiveMagicList[1]: 
                self.magicPercentBlocked += 1

        # special buffs
        if 'Enchanted Armor' in self.specialBuffs:
            if not self.shield > 0:
                del self.specialBuffs['Enchanted Armor']
                self.damageStored = 0
            elif tasklet and self.specialBuffEffectiveness:
                if self.receiveAttackList[0] < self.receiveAttackList[1]:
                    '''Record and store attack damage received (maximum 500)'''
                    self.damageStored = min(500, self.damageStored+self.receiveAttackDamageList[-1])
                    self.specialBuffs['Enchanted Armor'] = 'until shield broken ['+str(self.damageStored)+']'
                if self.attackList[0] < self.attackList[1]:
                    '''Recover an equal amount of shield health when dealing attack damage'''
                    self.shield = min(1000, self.shield+self.attackDamageList[-1])
        if not tasklet and 'Throne Power' in self.specialBuffs:
            if self.specialBuffEffectiveness:
                if phase[0] == 0.5:
                    '''Immune from seckill. Rebound status effects'''
                    self.immunityFromSeckill = True
                    self.reboundStatusEffects = True
                if phase[0] == 2 and self.healingEffectiveness:
                    '''At the start of every turn, heal an amount equivalent to 10% of the sum of all stats except for maximum HP'''
                    amount = (self.stats[0]+self.stats[1]+self.stats[2]+self.stats[3]+self.stats[4])/10*self.specialBuffEffect
                    heal(self, amount)
                    '''apply an equal amount of magic damage'''
                    if self.opponent:
                        magicDamage(self, self.opponent, amount)

        # Enchanted Armor
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
            for opponent in sideList[1-self.side]:
                element = checkElement(self.turnEffects, 'Rebound', False, opponent.id)
                if element and opponent == self.attacker:
                    self.attackPercentRebounded += getNumber(element)

        # Emperor's Pride
        if not tasklet and moveStep[self.side][self.position] == '2' and isEffective(self, self.moveRecord[-1]) and self.healingEffectiveness:
            element = checkElement(self.turnEffects, 'All moves heal')
            if element:
                heal(self, getNumber(element)*self.stats[5])
        if not tasklet and phase[0] == 4 and max(self.statsER) <= 0:
            element = checkElement(self.timeEffects, 'Absorb')
            if element:
                minusOneTime(self.timeEffects, element)
                if self.opponent:
                    magicDamage(self, self.opponent, getNumber(element)*self.opponent.stats[5])
                    if self.healingEffectiveness:
                        heal(self, self.magicDamageList[-1])

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Enchanted Armor
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]):
                    for i in range(len(self.goesFirst)):
                        oppoList = [self.opponent, self.oppoTeammate]
                        if oppoList[i] and self.goesFirst[i] and self.turnEffectiveness:
                            '''if going first this turn'''
                            checkElement(self.turnEffects, 'Rebound', True, oppoList[i].id)
                            self.turnEffects.update({'Rebound '+str(round(200*self.moveEffect[1]))+'% of attack damage received from '+oppoList[i].name.title()+' '+oppoList[i].id: 1})
                    if not self.shield > 0:
                        '''Gain a 600 HP shield called {Enchanted Armor} (effective until shield is broken)'''
                        self.shield += round(600*self.moveEffect[1])
                        self.specialBuffs.update({'Enchanted Armor': 'until shield broken [0]'})
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Fury of the Sky
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    '''multiply this attack damage by (1+0.2x) when having physical and special attack stats enhancement (+x)'''
                    statsE = max(0, self.statsER[0])+max(0, self.statsER[1])
                    self.attackMultiplier = self.attackMultiplier*(1+0.2*statsE)*self.moveEffect[1]
                    '''Deal 200 fighting, elder attack damage'''
                    typeEffectiveness = determineTypeEffectiveness(['fighting','elder'], self.target.type)
                    attackDamage(self, [self.target], True, 200*self.moveEffect[1], [typeEffectiveness])

        # Dismantle
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[2], [self.target]):
                    attackDamage(self, [self.target], self.moves[2])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    if max(self.target.statsER) > 0:
                        triggered = True
                    else:
                        triggered = False
                    if not self.target.immunityFromClearingStatsE:
                        '''Absorb opponent's stats enhancement'''
                        if self.statsEEffectiveness:
                            absorbStatsE(self, self.target)
                        else:
                            clearStatsE(self.target)
                    if triggered:
                        '''if triggered, then apply an amount of magic damage equivalent to 60% of own special attack stats'''
                        magicDamage(self, self.target, 0.6*self.stats[1]*self.moveEffect[0], True)

        # Emperor's Pride
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.statsEEffectiveness:
                        '''Raise physical and special attack and speed stats (+1)'''
                        self.statsER[0] = min(6, self.statsER[0]+round(self.moveEffect[1]))
                        self.statsER[1] = min(6, self.statsER[1]+round(self.moveEffect[1]))
                        self.statsER[4] = min(6, self.statsER[4]+round(self.moveEffect[1]))
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'All moves heal', True)
                        self.turnEffects.update({'All moves heal '+str(round(50*self.moveEffect[1]))+'% of maximum HP': 2})
                    if self.timeEffectiveness:
                        self.timeEffects.update({'Absorb '+fraction('2/3', self.moveEffect[1])+' of maximum HP from the opponent if not having stats enhancement at the end of a turn': 1})
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Long Live the King
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[4]):
                    '''Obtain {Throne Power} (effective for the entire battle)'''
                    self.specialBuffs.update({'Throne Power': math.inf})
                    self.immunityFromSeckill = True
                    self.reboundStatusEffects = True
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    attackDamage(self, [self.target], self.moves[4])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[4]) and notImmuned(self, self.moves[4], self.target):
                    if 'Enchanted Armor' in self.specialBuffs:
                        '''Apply an amount of magic damage equivalent to the damage stored in {Enchanted Armor}'''
                        magicDamage(self, self.target, self.damageStored, True)
                        '''clear the damage stored'''
                        self.damageStored = 0
                        self.specialBuffs.update({'Enchanted Armor': 'until shield broken [0]'})

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Blake(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'blake'
        self.gender = 'male'
        self.color = (1,1,1)
        self.type = ['machine', 'dark']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [115,129,102,96,118,152]

        # unique battle variables
        self.deathTimes = 0 # how many times self has died
        self.oldReceiveAttackDamageList = [] # keeps track of attack damage received before this turn
        self.critical = False # if Steely Puncture has made critical hit
        self.magic = False # if Revitalize needs to apply magic damage

    def resetUniqueVariables(self):
        self.critical = False
        self.magic = False
        self.oldReceiveAttackDamageList = copy.deepcopy(self.receiveAttackDamageList)

    def resetAfterClear(self, element, champ=None):
        for opponent in sideList[1-self.side]:
            if element == 'Cut off all turn-effects from '+opponent.name.title()+' '+opponent.id:
                opponent.turnEffectiveness = True
        if element == 'Immune from status effects, stats reduction, and clearing turn-effects *'+self.id:
            if champ:
                champ.immunityFromStatusEffects = False
                champ.immunityFromStatsR = False
                champ.immunityFromClearingTurnEffects = False

    def ghostEffects(self, tasklet=False):
        if not tasklet and phase[0] == 0.5:
            for teammember in sideList[self.side]:
                if 'Immune from status effects, stats reduction, and clearing turn-effects *'+self.id in teammember.turnEffects:
                    teammember.immunityFromStatusEffects = True
                    teammember.immunityFromStatsR = True
                    teammember.immunityFromClearingTurnEffects = True

    def revive(self):
        self.deathTimes += 1
        if self.abilitiesEffectiveness and self.healingEffectiveness:
            '''Heal an amount of HP equivalent to the total attack damage received this turn when dying (maximum 600)'''
            heal(self, min(600, sum(self.receiveAttackDamageList)-sum(self.oldReceiveAttackDamageList)), None, True)
        return self.hp > 0

    def executeEffects(self, tasklet=False):
        # abilities
        if tasklet and self.abilitiesEffectiveness:
            '''Block all magic damage received when own HP < 50%'''
            if self.receiveMagicList[0] > self.receiveMagicList[1] and self.hp < 0.5*self.stats[5]:
                self.magicPercentBlocked += 1
            '''All attack damage dealt by attacking moves will be no less than 200'''
            if self.attackList[0] > self.attackList[1] and self.moveAttack:
                self.attackMin = 200*self.abilitiesEffect

        # Revitalize
        if tasklet and self.receiveAttackList[0] < self.receiveAttackList[1] and self.hp <= 0:
            if 'Make the opponent flinch when receiving fatal attack damage' in self.timeEffects:
                minusOneTime(self.timeEffects, 'Make the opponent flinch when receiving fatal attack damage')
                addStatusEffect(self, self.attacker, 'flinching')

        # Twin Shadow Attack
        if not tasklet and phase[0] == 0.5:
            for opponent in sideList[1-self.side]:
                if 'Cut off all turn-effects from '+opponent.name.title()+' '+opponent.id in self.turnEffects:
                    opponent.turnEffectiveness = False

        # Night Guardian
        if not tasklet and phase[0] == 0.5:
            for teammember in sideList[self.side]:
                if 'Immune from status effects, stats reduction, and clearing turn-effects *'+self.id in teammember.turnEffects:
                    teammember.immunityFromStatusEffects = True
                    teammember.immunityFromStatsR = True
                    teammember.immunityFromClearingTurnEffects = True

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Steely Puncture
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    self.critical = attackDamage(self, [self.target], self.moves[0])[0]
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]):
                    '''Forcefully make the opponent bleed'''
                    addStatusEffect(self, self.target, 'bleeding', 0, True)
                    if notImmuned(self, self.moves[0], self.target) and not self.target.immunityFromStatsR:
                        '''Absorb opponent's physical and special attack stats (+-1)'''
                        '''double the effect if critical hit'''
                        effect = 1
                        if self.critical:
                            effect = 2
                        self.target.statsER[0] = max(-6, self.target.statsER[0]-round(1*effect*self.moveEffect[0]))
                        self.target.statsER[1] = max(-6, self.target.statsER[1]-round(1*effect*self.moveEffect[0]))
                        if self.statsEEffectiveness:
                            self.statsER[0] = min(6, self.statsER[0]+round(1*effect*self.moveEffect[0]))
                            self.statsER[1] = min(6, self.statsER[1]+round(1*effect*self.moveEffect[0]))

        # Revitalize
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.statsEEffectiveness:
                        '''Inverse own stats reduction'''
                        inverseStatsR(self)
                    else:
                        clearStatsR(self)
                    '''Heal 50% of maximum HP'''
                    if self.healingEffectiveness:
                        self.magic = self.hp < 0.5*self.stats[5]
                        heal(self, 0.5*self.stats[5]*self.moveEffect[1], True)
                    if self.timeEffectiveness:
                        self.timeEffects.update({'Make the opponent flinch when receiving fatal attack damage': 1})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    if self.magic:
                        '''apply an equal amount of magic damage when own HP < 50%'''
                        magicDamage(self, self.target, 0.5*self.stats[5]*self.moveEffect[1], True)

        # Twin Shadow Attack
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[2], [self.target]):
                    for i in range(2):
                        attackDamage(self, [self.target], self.moves[2])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Cut off all turn-effects from '+self.target.name.title()+' '+self.target.id: 3})
                        self.target.turnEffectiveness = False

        # Night Guardian
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    for teammember in [self, self.teammate]:
                        if teammember:
                            '''Prolong all turn-effects by one turn'''
                            for i in teammember.turnEffects:
                                if teammember.turnEffects[i] > 0:
                                    teammember.turnEffects[i] += 1
                                else:
                                    teammember.turnEffects[i] -= 1
                            if teammember.turnEffectiveness:
                                teammember.turnEffects.update({'Immune from status effects, stats reduction, and clearing turn-effects *'+self.id: 3})
                                teammember.immunityFromStatusEffects = True
                                teammember.immunityFromStatsR = True
                                teammember.immunityFromClearingTurnEffects = True
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Into The Abyss
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    if isEffective(self, self.moves[4]):
                        '''Multiply this attack damage by (1+x) when having died x times'''
                        self.attackMultiplier = self.attackMultiplier*(1+self.deathTimes)*self.moveEffect[0]
                    attackDamage(self, [self.target], self.moves[4])
                    if self.target.hp <= 0 and self.healingEffectiveness:
                        '''Heal 100% of maximum HP when defeating current opponent'''
                        heal(self, self.stats[5]*self.moveEffect[0], True)

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Hamlet(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'hamlet'
        self.gender = 'male'
        self.color = (255,120,0)
        self.type = ['dragon']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [138,81,113,108,117,153]

        # unique battle variables
        self.triggered = False # if hard engage has triggered extra attack damage
        self.defeating = False # if dragon smash has defeated the opponent

    def executeEffects(self, tasklet=False):
        # abilities
        if not tasklet and (self.hp <= 0.5*self.stats[5] or not self.abilitiesEffectiveness):
            self.immunityFromStatusEffects = False
        if self.abilitiesEffectiveness:
            if self.hp > 0.5*self.stats[5]:
                '''Immune from status effects'''
                if not tasklet:
                    self.immunityFromStatusEffects = True
                '''reduce attack damage received and dealt by the opponent's attacking moves by 50%'''
                if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1] and self.attacker.moveAttack:
                    self.receiveAttackPercentMultiplier -= 0.5*self.abilitiesEffect
            if tasklet and self.receiveAttackList[0] < self.receiveAttackList[1]:
                if not self.attacker.immunityFromStatsR:
                    '''Lower three of the opponent's stats (-1) by random when receiving attack'''
                    array = [0,1,2,3,4,5]
                    random.shuffle(array)
                    for i in range(3):
                        number = array.pop()
                        self.attacker.statsER[number] = max(-6, self.attacker.statsER[number]-round(1*self.abilitiesEffect))
            if not tasklet and moveStep[self.side][self.position] == '2':
                '''All moves heal 1/3 of maximum HP; double the effect when own HP < 50%'''
                if self.healingEffectiveness:
                    effect = 1
                    if self.hp < 0.5*self.stats[5]:
                        effect = 2
                    heal(self, self.stats[5]/3*effect*self.abilitiesEffect)

        # Dragon Smash
        for opponent in sideList[1-self.side]:
            if tasklet and opponent.receiveAttackList[0] > opponent.receiveAttackList[1]:
                element = checkElement(self.turnEffects, 'Multiply all damage received by', False, opponent.id)
                if element:
                    opponent.receiveAttackMultiplier = opponent.receiveAttackMultiplier*getNumber(element)
            if tasklet and opponent.receiveMagicList[0] > opponent.receiveMagicList[1]:
                element = checkElement(self.turnEffects, 'Multiply all damage received by', False, opponent.id)
                if element:
                    opponent.receiveMagicMultiplier = opponent.receiveMagicMultiplier*getNumber(element)

        # Dragon's Dignity
        if not tasklet and moveStep[self.side][self.position] == '4' and isEffective(self, self.moveRecord[-1]):
            for opponent in self.oppoHit:
                if opponent and notImmuned(self, self.moveRecord[-1], opponent):
                    element = checkElement(self.turnEffects, 'All moves absorb')
                    if element:
                        magicDamage(self, opponent, getNumber(element))
                        if self.healingEffectiveness:
                            heal(self, self.magicDamageList[-1])
        for opponent in sideList[1-self.side]:
            if not tasklet and moveStep[1-self.side][opponent.position] == '1':
                if 'Make '+opponent.name.title()+'\'s move ineffective '+opponent.id in self.timeEffects:
                    minusOneTime(self.timeEffects, 'Make '+opponent.name.title()+'\'s move ineffective '+opponent.id)
                    opponent.moveEffectiveness[0] = False
                    opponent.moveEffectiveness[1] = False

        # Dragon's Will
        if tasklet and self.attackList[0] > self.attackList[1] and self.moveAttack:
            if 'Attacking move will make a critical hit' in self.timeEffects:
                minusOneTime(self.timeEffects, 'Attacking move will make a critical hit')
                self.rateOfCriticalHitIncrement = math.inf

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Hard Engage
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]):
                    self.triggered = min(self.statsER) < 0
                    '''Clear own stats reduction'''
                    clearStatsR(self)
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    if isEffective(self, self.moves[0]):
                        '''This attack damage will be no less than 200'''
                        self.attackMin = 200*self.moveEffect[0]
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    if self.triggered:
                        '''if triggered, then deal 300 attack damage to the opponent'''
                        attackDamage(self, [self.target], True, 300*self.moveEffect[0])

        # Dragon Smash
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[1], [self.target]):
                    attackDamage(self, [self.target], self.moves[1])
                    self.defeating = self.target.hp <= 0
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]):
                    if self.defeating:
                        '''Raise all stats (+1) if defeating current opponent'''
                        if self.statsEEffectiveness:
                            for i in range(6):
                                self.statsER[i] = min(6, self.statsER[i]+round(1*self.moveEffect[0]))
                    elif notImmuned(self, self.moves[1], self.target) and self.turnEffectiveness:
                        '''if not defeating current opponent'''
                        checkElement(self.turnEffects, 'Multiply all damage received by', True, self.target.id)
                        self.turnEffects.update({'Multiply all damage received by '+self.target.name.title()+' by '+str(round(2*self.moveEffect[0]))+' '+self.target.id: 2})
                    if notImmuned(self, self.moves[1], self.target):
                        if not self.target.immunityFromClearingStatsE:
                            '''Clear opponent's stats enhancement'''
                            clearStatsE(self.target)

        # Dragon's Dignity
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'All moves absorb', True)
                        self.turnEffects.update({'All moves absorb '+str(round(200*self.moveEffect[1]))+' HP from opponent': 3})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    if self.timeEffectiveness:
                        self.timeEffects.update({'Make '+self.target.name.title()+'\'s move ineffective '+self.target.id: 1})

        # Dragon's Will
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.statsEEffectiveness:
                        '''Raise all stats (+1); double the effect when own HP < 50%'''
                        effect = 1
                        if self.hp < 0.5*self.stats[5]:
                            effect = 2
                        for i in range(6):
                            self.statsER[i] = min(6, self.statsER[i]+round(1*effect*self.moveEffect[1]))
                    if self.timeEffectiveness:
                        self.timeEffects.update({'Attacking move will make a critical hit': 1})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[3], [self.target])

        # Dragon Onslaught
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    if isEffective(self, self.moves[4]):
                        '''Multiply this attack damage by (1+x%) when having x% of maximum HP'''
                        self.attackMultiplier = self.attackMultiplier*(1+self.hp/self.stats[5])*self.moveEffect[0]
                    attackDamage(self, [self.target], self.moves[4])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Satan(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'satan'
        self.gender = 'male'
        self.color = (150,50,200)
        self.type = ['ghost', 'psychic']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [133,92,101,105,128,149]

        # unique battle variables
        self.amountHealed = 0 # keeps track of the amount of HP healed by Reborn From Darkness
        self.nextTeammemberBoost = False # if Satan sacrifices himself and no teammate's present, then boost up next teammember

    def resetUniqueVariables(self):
        self.amountHealed = 0

    def resetAfterClear(self, element):
        if element == 'Immune from status effects and stats reduction':
            self.immunityFromStatusEffects = False
            self.immunityFromStatsR = False

    def ghostEffects(self, tasklet=False):
        if not tasklet and self.nextTeammemberBoost and phase[0] == '2':
            self.nextTeammemberBoost = False
            if sideList[self.side][self.position].statsEEffectiveness:
                for i in range(6):
                    sideList[self.side][self.position].statsER[i] = min(6, sideList[self.side][self.position].statsER[i]+1)
            if sideList[self.side][self.position].timeEffectiveness:
                sideList[self.side][self.position].timeEffects.update({'Attacking moves will make critical hits *'+self.id: 2})
        for teammember in sideList[self.side]:
            if tasklet and teammember.attackList[0] > teammember.attackList[1] and teammember.moveAttack:
                if 'Attacking moves will make critical hits *'+self.id in teammember.timeEffects:
                    minusOneTime(teammember.timeEffects, 'Attacking moves will make critical hits *'+self.id)
                    teammember.rateOfCriticalHitIncrement = math.inf

    def executeEffects(self, tasklet=False):
        # abilities
        if not tasklet and self.abilitiesEffectiveness:
            if phase[0] == 0.5:
                '''All moves are always effective.'''
                self.ineffectiveIgnored = True
            if moveStep[self.side][self.position] == '4':
                for opponent in self.oppoHit:
                    if self.goesFirst[abs(self.position-opponent.position)]:
                        '''Moves that go first will clear opponent's turn-effects'''
                        if not opponent.immunityFromClearingTurnEffects:
                            clearTurnEffects(opponent)
                    else:
                        '''Moves that go last will apply an amount of magic damage equivalent to 1/3 of own HP'''
                        magicDamage(self, opponent, 1/3*self.hp*self.abilitiesEffect)

        # Awakening
        if not tasklet and moveStep[self.side][self.position] == '2' and isEffective(self, self.moveRecord[-1]):
            element = checkElement(self.turnEffects, 'All moves heal')
            if element and self.healingEffectiveness:
                heal(self, getNumber(element))
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
            element = checkElement(self.turnEffects, 'Attack damage received will be no greater than')
            if element:
                self.defenseMax = getNumber(element)

        # Final Verdict
        if not tasklet and phase[0] == 0.5:
            if 'Immune from status effects and stats reduction' in self.turnEffects:
                self.immunityFromStatusEffects = True
                self.immunityFromStatsR = True

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Tranquill Extinction
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.opponent, self.oppoTeammate]):
                    attackDamage(self, self.oppoHit, self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]):
                    for opponent in self.oppoHit:
                        if notImmuned(self, self.moves[0], opponent):
                            '''Apply an amount of magic damage equivalent to 50% of the HP lost by the opponent.'''
                            magicDamage(self, opponent, 0.5*(opponent.stats[5]-opponent.hp)*self.moveEffect[0], True)
                            '''Lower opponent's speed stats and accuracy (-2).'''
                            if not opponent.immunityFromStatsR:
                                opponent.statsER[4] = max(-6, opponent.statsER[4]-round(2*self.moveEffect[0]))
                                opponent.statsER[5] = max(-6, opponent.statsER[5]-round(2*self.moveEffect[0]))

        # Spiritual Appendage
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.teammate:
                        if self.teammate.statsEEffectiveness:
                            '''Raise teammate's all stats (+1)'''
                            for i in range(6):
                                self.teammate.statsER[i] = min(6, self.teammate.statsER[i]+round(1*self.moveEffect[1]))
                        if self.teammate.timeEffectiveness:
                            self.teammate.timeEffects.update({'Attacking moves will make critical hits *'+self.id: 2})
                    else:
                        self.nextTeammemberBoost = True
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    '''Inverse opponent's stats enhancements with 2 times bonus'''
                    if not self.target.immunityFromStatsR:
                        inverseStatsE(self.target, round(2*self.moveEffect[1]))
                    else:
                        clearStatsE(self.target)
            elif moveStep[self.side][self.position] == 5:
                if isEffective(self, self.moves[1]):
                    '''Sacrifice self'''
                    sacrifice(self)

        # Reborn From Darkness
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    if self.healingEffectiveness:
                        '''Heal an amount equivalent to the amount of HP lost'''
                        heal(self, (self.stats[5]-self.hp), True)
                        self.amountHealed = self.healingAmountList[-1]
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target) and self.amountHealed:
                    '''apply an amount of magic damage equivalent to the amount healed'''
                    magicDamage(self, self.target, self.amountHealed, True)

        # Awakening
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    '''Increase physical attack stats by 50 and maximum HP by 100'''
                    self.stats[0] += 50*self.moveEffect[1]
                    self.stats[5] += round(100*self.moveEffect[1])
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'All moves heal', True)
                        self.turnEffects.update({'All moves heal '+str(round(300*self.moveEffect[1]))+' HP': 3})
                        checkElement(self.turnEffects, 'Attack damage received will be no greater than', True)
                        self.turnEffects.update({'Attack damage received will be no greater than '+str(round(250*self.moveEffect[1])): 3})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[3], [self.target])

        # Final Verdict
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[4]):
                    if self.statsEEffectiveness:
                        '''Raise physical and special attack stats (+2) and accuracy (+1)'''
                        self.statsER[0] = min(6, self.statsER[0]+round(2*self.moveEffect[0]))
                        self.statsER[1] = min(6, self.statsER[1]+round(2*self.moveEffect[0]))
                        self.statsER[5] = min(6, self.statsER[5]+round(1*self.moveEffect[0]))
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Immune from status effects and stats reduction': 3})
                        self.immunityFromStatusEffects = True
                        self.immunityFromStatsR = True
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    attackDamage(self, [self.target], self.moves[4])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Gaia(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'gaia'
        self.gender = 'male'
        self.color = (100,100,100)
        self.type = ['fighting']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [128,92,104,108,126,147]

        # unique battle variables
        self.playerSelectionSurface = None
        self.choice = 'No' # whether or not to exchange positions with teammate
        self.ownStatsER = [] # for transferring statsR
        self.totalAttackDamageReceived = 0 # for Soul Snap

    def resetUniqueVariables(self):
        self.choice = 'No'
        self.totalAttackDamageReceived = sum(self.receiveAttackDamageList)
        if self.teammate:
            self.totalAttackDamageReceived += sum(self.teammate.receiveAttackDamageList)

    def resetAfterClear(self, element, champ=None):
        if element == 'Immune from status effects':
            self.immunityFromStatusEffects = False

    def playerSelect(self, clicked=False):
        if self.teammate:
            if self.playerSelectionSurface == None:
                self.playerSelectionSurface = PlayerSelectionSurface(self, 'Gaia: Do you want to switch positions with teammate?')
                battlegroup.add(self.playerSelectionSurface)
                battlegroup.move_to_front(self.playerSelectionSurface)
                self.playerSelectionSurface.choices = []
                for i in range(2):
                    self.playerSelectionSurface.choices.append(pygame.Surface((120,120)).convert_alpha())
                self.playerSelectionSurface.image.blit(self.playerSelectionSurface.ok, (210,310))
            else:
                for i in range(2):
                    if self.playerSelectionSurface.choices[i].get_rect(center=(430+i*220,380)).collidepoint(pygame.mouse.get_pos()):
                        self.playerSelectionSurface.choices[i].fill((50,50,50))
                        centerText(self.playerSelectionSurface.choices[i], ['Yes','No'][i], 'timesnewroman', 25, (255,255,255))
                        self.playerSelectionSurface.image.blit(self.playerSelectionSurface.choices[i], (100+i*220,140))
                        if clicked:
                            self.choice = ['Yes','No'][i]
                    else:
                        if ['Yes','No'][i] == self.choice:
                            self.playerSelectionSurface.choices[i].fill((50,50,50))
                        else:
                            self.playerSelectionSurface.choices[i].fill((0,0,0))
                        centerText(self.playerSelectionSurface.choices[i], ['Yes','No'][i], 'timesnewroman', 25, (255,255,255))
                        self.playerSelectionSurface.image.blit(self.playerSelectionSurface.choices[i], (100+i*220,140))
                        if clicked and self.playerSelectionSurface.ok.get_rect(center=(540,510)).collidepoint(pygame.mouse.get_pos()):
                            self.phaseFinished = True
                            self.playerSelecting = False
        else:
            self.phaseFinished = True
            self.playerSelecting = False
        return True

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if not tasklet and phase[0] == 2 and turn[0] <= 2 and self.statsEEffectiveness:
                '''At the start of the first two turns of the battle, randomly raise four stats (+1)'''
                array = [0,1,2,3,4,5]
                random.shuffle(array)
                for i in range(4):
                    number = array.pop()
                    self.statsER[number] = min(6, self.statsER[number]+round(1*self.abilitiesEffect))
            if tasklet and self.receiveAttackList[0] < self.receiveAttackList[1] and self.isCriticalHit and self.entireBattleEffectiveness:
                '''When receiving a critical hit'''
                self.entireBattleEffects.append('All attacking moves will make critical hits')
            if not tasklet and phase[0] == 2 and self.choice == 'Yes':
                '''At the start of every turn, can switch positions with teammate'''
                sideList[self.side][0], sideList[self.side][1] = sideList[self.side][1], sideList[self.side][0]
                self.position, self.teammate.position = self.teammate.position, self.position
                self.battlePosition[1], self.teammate.battlePosition[1] = 490-280*self.position, 490-280*self.teammate.position
                for opponent in sideList[1-self.side]:
                    if opponent.target:
                        opponent.target = opponent.target.teammate
                for moveBox in moveBoxes:
                    moveBox.champList[-2*self.side], moveBox.champList[-2*self.side+1] = moveBox.champList[-2*self.side+1], moveBox.champList[-2*self.side]
                    moveBox.moves[-2*self.side], moveBox.moves[-2*self.side+1] = moveBox.moves[-2*self.side+1], moveBox.moves[-2*self.side]
                    moveBox.moveBoxImages[-2*self.side], moveBox.moveBoxImages[-2*self.side+1] = moveBox.moveBoxImages[-2*self.side+1], moveBox.moveBoxImages[-2*self.side]
                    moveBox.scrollInters[-2*self.side], moveBox.scrollInters[-2*self.side+1] = moveBox.scrollInters[-2*self.side+1], moveBox.scrollInters[-2*self.side]
                for teammember in sideList[self.side]:
                    teammember.champInfo.position = teammember.position
                    teammember.champInfo.rect.center = (65+teammember.side*950,80+(1-teammember.position)*280)
                    teammember.champInfo.killingSpree()
                    teammember.champInfo.setInfoSprites()
        if tasklet and self.attackList[0] > self.attackList[1] and self.moveAttack:
            if 'All attacking moves will make critical hits' in self.entireBattleEffects:
                self.rateOfCriticalHitIncrement = math.inf

        # Fighting Spirit
        if not tasklet and phase[0] == 0.5:
            if 'Immune from status effects' in self.turnEffects:
                self.immunityFromStatusEffects = True
        if not tasklet and phase[0] == 4 and self.healingEffectiveness:
            element = checkElement(self.turnEffects, 'At the end of every turn, heal')
            if element:
                heal(self, getNumber(element))

        # Simplicity at Its Finest
        if not tasklet and phase[0] == 2:
            element = checkElement(self.turnEffects, 'All moves will go first')
            if element:
                self.preemptiveIncrement += getNumber(element)
        if not tasklet and moveStep[self.side][self.position] == '2' and isEffective(self, self.moveRecord[-1]):
            element = checkElement(self.turnEffects, 'All moves raise physical and special attack and speed stats')
            if element and self.statsEEffectiveness:
                self.statsER[0] = min(6, self.statsER[0]+round(getNumber(element)))
                self.statsER[1] = min(6, self.statsER[1]+round(getNumber(element)))
                self.statsER[4] = min(6, self.statsER[4]+round(getNumber(element)))
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
            element = checkElement(self.timeEffects, 'Reduce attack damage received by')
            if element:
                minusOneTime(self.timeEffects, element)
                self.receiveAttackIncrement -= getNumber(element)

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Flash Kick
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]):
                    self.ownStatsER = copy.deepcopy(self.statsER)
                    clearStatsR(self)
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    if not self.target.immunityFromStatsR:
                        '''transfer own stats reduction to opponent'''
                        transferStatsR(self.ownStatsER, self.target)
                        for i in range(len(self.statsER)):
                            if self.statsER[i] > 0:
                                '''When having stats enhancement, lower corresponding stats from the opponent by the same amount'''
                                self.target.statsER[i] -= self.statsER[i]

        # Fighting Spirit
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.statsEEffectiveness:
                        '''Raise physical and special defense stats (+2)'''
                        self.statsER[2] = min(6, self.statsER[2]+round(2*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(2*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Immune from status effects': 4})
                        self.immunityFromStatusEffects = True
                        checkElement(self.turnEffects, 'At the end of every turn, heal', True)
                        self.turnEffects.update({'At the end of every turn, heal '+str(round(200*self.moveEffect[1]))+' HP': 4})
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Soul Snap
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[2], [self.opponent, self.oppoTeammate]):
                    if isEffective(self, self.moves[2]):
                        '''Increase this attack damage by an amount equivalent to the total attack damage received by self and teammate this turn'''
                        totalAttackDamageReceived = 0
                        for teammember in sideList[self.side]:
                            totalAttackDamageReceived += sum(teammember.receiveAttackDamageList)
                        increment = totalAttackDamageReceived-self.totalAttackDamageReceived
                        self.attackIncrement += increment
                    attackDamage(self, self.oppoHit, self.moves[2])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]):
                    for opponent in self.oppoHit:
                        if opponent and notImmuned(self, self.moves[4], opponent):
                            if not opponent.immunityFromClearingTurnEffects:
                                '''Clear opponent's turn-effects'''
                                clearTurnEffects(opponent)

        # Simplicity at Its Finest
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'All moves will go first', 'All moves will go first (+'+str(round(1*self.moveEffect[1]))+')', -2)
                        checkElement(self.turnEffects, 'All moves raise physical and special attack and speed stats', True)
                        self.turnEffects.update({'All moves raise physical and special attack and speed stats (+'+str(round(1*self.moveEffect[1]))+')': 3})
                    if self.timeEffectiveness:
                        checkElement(self.timeEffects, 'Reduce attack damage received by', True)
                        self.timeEffects.update({'Reduce attack damage received by '+str(round(200*self.moveEffect[1])): 2})
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Rampage
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    if isEffective(self, self.moves[4]):
                        '''Multiply this attack damage by 2 when opponent has stats reduction'''
                        if min(self.target.statsER) < 0:
                            self.attackMultiplier = self.attackMultiplier*2*self.moveEffect[0]
                    attackDamage(self, [self.target], self.moves[4])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Wesker(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'wesker'
        self.gender = 'male'
        self.color = (25,10,25)
        self.type = ['ice', 'dark']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [88,134,97,101,134,148]

    def resetAfterClear(self, element):
        if element == 'Immune from status effects':
            self.immunityFromStatusEffects = False
        if self.abilitiesEffectiveness and self.turnEffectiveness:
            self.turnEffects.update({'Immune from status effects': 2})
            self.immunityFromStatusEffects = True

    def executeEffects(self, tasklet=False):
        # abilities
        if not tasklet and self.abilitiesEffectiveness:
            if phase[0] == 2:
                for opponent in sideList[1-self.side]:
                    if self.hp > opponent.hp:
                        '''At the start of every turn, frostbite the opponent if own HP > opponent's HP'''
                        addStatusEffect(self, opponent, 'frostbitten')
                    else:
                        '''absorb 1/3 of maximum HP from the opponent if otherwise'''
                        magicDamage(self, opponent, 1/3*opponent.stats[5]*self.abilitiesEffect)
                        if self.healingEffectiveness:
                            heal(self, self.magicDamageList[-1])

        # Dusky Raid
        for opponent in sideList[1-self.side]:
            if tasklet and opponent.attackList[0] > opponent.attackList[1]:
                element = checkElement(self.timeEffects, 'Reduce attack damage dealt by', False, opponent.id)
                if element:
                    minusOneTime(self.timeEffects, element)
                    opponent.attackPercentMultiplier -= getNumber(element)

        # Spectre Dance
        if not tasklet and moveStep[self.side][self.position] == '2' and isEffective(self, self.moveRecord[-1]):
            element = checkElement(self.turnEffects, 'All moves raise special attack and speed stats')
            if element and self.statsEEffectiveness:
                self.statsER[1] = min(6, self.statsER[1]+round(getNumber(element)))
                self.statsER[4] = min(6, self.statsER[4]+round(getNumber(element)))
        if not tasklet and moveStep[self.side][self.position] == '4' and isEffective(self, self.moveRecord[-1]):
            if 'All moves make the opponent flinch' in self.turnEffects:
                for opponent in self.oppoHit:
                    if opponent and notImmuned(self, self.moveRecord[-1], opponent):
                        addStatusEffect(self, opponent, 'flinching')
        if tasklet and self.receiveAttackList[0] < self.receiveAttackList[1] and self.hp <= 0:
            if 'When receiving lethal attack damage, heal an amount of HP equivalent to opponent\'s HP' in self.timeEffects:
                minusOneTime(self.timeEffects, 'When receiving lethal attack damage, heal an amount of HP equivalent to opponent\'s HP')
                if self.healingEffectiveness:
                    heal(self, self.attacker.hp, None, True)

        # Ruler of Darkness
        if not tasklet and phase[0] == 2:
            for opponent in sideList[1-self.side]:
                element = checkElement(self.turnEffects, 'Make '+opponent.name.title()+'\'s moves go last', False, opponent.id)
                if element:
                    opponent.preemptiveIncrement += getNumber(element)

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Dusky Raid
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    if not self.target.immunityFromClearingStatsE:
                        '''Clear opponent's stats enhancement'''
                        clearStatsE(self.target)
                    if self.attackDamageList[-1] < 150 and self.timeEffectiveness:
                        checkElement(self.timeEffects, 'Reduce attack damage dealt by', True, self.target.id)
                        self.timeEffects.update({'Reduce attack damage dealt by '+self.target.name.title()+' by '+str(round(100*self.moveEffect[0]))+'% '+self.target.id: 1})

        # Cold Assassination
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[1], [self.target]):
                    attackDamage(self, [self.target], self.moves[1])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    if not self.target.immunityFromStatsR:
                        '''Lower opponent's physical and special attack and physical and special defense stats (-1)'''
                        '''double the effect when opponent does not have stats reduction.'''
                        if min(self.target.statsER) >= 0:
                            effect = 2
                        else:
                            effect = 1
                        self.target.statsER[0] = max(-6, self.target.statsER[0]-round(1*self.moveEffect[0]*effect))
                        self.target.statsER[1] = max(-6, self.target.statsER[1]-round(1*self.moveEffect[0]*effect))
                        self.target.statsER[2] = max(-6, self.target.statsER[2]-round(1*self.moveEffect[0]*effect))
                        self.target.statsER[3] = max(-6, self.target.statsER[3]-round(1*self.moveEffect[0]*effect))

        # Spectre Dance
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'All moves raise special attack and speed stats', True)
                        self.turnEffects.update({'All moves raise special attack and speed stats (+'+str(round(1*self.moveEffect[1]))+')': 3})
                        self.turnEffects.update({'All moves make the opponent flinch': 3})
                    if self.timeEffectiveness:
                        self.timeEffects.update({'When receiving lethal attack damage, heal an amount of HP equivalent to opponent\'s HP': 1})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])

        # Ruler of Darkness
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    '''Change the environment to "dark"'''
                    environment[0] = 'dark'
                    if self.statsEEffectiveness:
                        '''Raise special attack stats (+2)'''
                        self.statsER[1] = min(6, self.statsER[1]+round(2*self.moveEffect[1]))
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[3], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[3]) and notImmuned(self, self.moves[3], self.target):
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'Make '+self.target.name.title()+'\'s moves go last', 'Make '+self.target.name.title()+'\'s moves go last (-'+str(round(1*self.moveEffect[1]))+') '+self.target.id, -2, self.target.id)

        # Evil Discharge
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.opponent, self.oppoTeammate]):
                    attackDamage(self, self.oppoHit, self.moves[4])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[4]):
                    timesUsed = self.moveRecord.count(self.moves[4])
                    effect = (0.5+0.5*timesUsed)*self.moveEffect[0]
                    for opponent in self.oppoHit:
                        if opponent and notImmuned(self, self.moves[4], opponent):
                            '''Apply an amount of magic damage equivalent to 40% of own speed stats'''
                            '''multiply this effect by (0.5+0.5x) when using this move for the x time in this battle'''
                            magicDamage(self, opponent, 0.4*self.stats[4]*effect*self.moveEffect[0],True)

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Muse(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'muse'
        self.gender = 'female'
        self.color = (200,0,0)
        self.type = ['psychic']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [87,133,107,105,125,143]

        # unique battle variables
        self.healed = False # if having healed after receiving attack in Wonderland

    def ghostEffects(self, tasklet=False):
        for teammember in sideList[self.side]:
            if 'Wonderland' in teammember.specialBuffs and self.id in teammember.specialBuffs['Wonderland'] and teammember.specialBuffEffectiveness:
                if not tasklet and moveStep[self.side][teammember.position] == '4' and teammember.moveRecord[-1][0][1] != 'Enchantment':
                    for opponent in teammember.oppoHit:
                        if opponent:
                            magicDamage(teammember, opponent, 0.25*(teammember.stats[0]+teammember.stats[1])*teammember.specialBuffEffect)
                if tasklet and teammember.receiveAttackList[0] < teammember.receiveAttackList[1] and teammember.healingEffectiveness and not self.healed:
                    self.healed = True
                    heal(teammember, 0.25*(teammember.stats[2]+teammember.stats[3])*teammember.specialBuffEffect)
                    self.healed = False

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if not tasklet and phase[0] == 4:
                '''Clear own status effects at the end of every turn'''
                for i in list(self.statusEffects):
                    del self.statusEffects[i]
            for i in range(len(self.goesFirst)):
                oppoList = [self.opponent, self.oppoTeammate]
                if oppoList[i] and not self.goesFirst[i]:
                    '''When the opponent goes first'''
                    if tasklet and oppoList[i].attackList[0] > oppoList[i].attackList[1] and oppoList[i].moveAttack and self in oppoList[i].defenders:
                        '''block 75% of their attack damage dealt by their attacking move this turn'''
                        self.attackPercentBlocked += 0.75*self.abilitiesEffect
            if self.teammate and self.teammate.name == 'jeremies' and self.hp > 0.5*self.stats[5]:
                '''When fighting alongside Jeremies and own HP > 50%'''
                if tasklet and self.energyList[0] > self.energyList[1] and self.moveEnergy:
                    '''multiply all energy lost by using moves by 2'''
                    self.energyLossMultiplier = self.energyLossMultiplier*2*self.abilitiesEffect

        # special buffs
        for teammember in sideList[self.side]:
            if 'Wonderland' in teammember.specialBuffs and self.id in teammember.specialBuffs['Wonderland'] and teammember.specialBuffEffectiveness:
                if not tasklet and moveStep[self.side][teammember.position] == '4' and teammember.moveRecord[-1][0][1] != 'Enchantment':
                    '''All attacking moves apply an amount of magic damage equivalent to 25% of the sum of physical and special attack stats'''
                    for opponent in teammember.oppoHit:
                        if opponent:
                            magicDamage(teammember, opponent, 0.25*(teammember.stats[0]+teammember.stats[1])*teammember.specialBuffEffect)
                if tasklet and teammember.receiveAttackList[0] < teammember.receiveAttackList[1] and teammember.healingEffectiveness and not self.healed:
                    '''Heal an amount equivalent to 25% of the sum of physical and special defense stats when receiving attack'''
                    self.healed = True
                    heal(teammember, 0.25*(teammember.stats[2]+teammember.stats[3])*teammember.specialBuffEffect)
                if not tasklet:
                    self.healed = False

        # Secret Interspace
        if not tasklet and phase[0] == 4 and self.healingEffectiveness:
            element = checkElement(self.turnEffects, 'At the end of every turn, heal')
            if element:
                heal(self, getNumber(element)*self.stats[5])
        if not tasklet and moveStep[self.side][self.position] == '1' and 'Moves are non-missable' in self.timeEffects:
            minusOneTime(self.timeEffects, 'Moves are non-missable')
            self.missingIgnored = True

        # Psychic Chain
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
            if 'Block attack damage received' in self.timeEffects:
                minusOneTime(self.timeEffects, 'Block attack damage received')
                self.attackPercentBlocked += 1

        # Wonderland
        if not tasklet and phase[0] == 2 and self.teammate and self.teammate.name == 'jeremies' and self.moveRecord[-1][0][0] == 'Wonderland':
            self.ineffectiveIgnored = True

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Requiem
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[0], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    if not self.target.immunityFromClearingTurnEffects:
                        '''Clear opponent's turn-effects and time-effects'''
                        clearTurnEffects(self.target)
                    if not self.target.immunityFromClearingTimeEffects:
                        self.target.timeEffects.clear()
                    '''Make the opponent asleep'''
                    addStatusEffect(self, self.target, 'asleep')

        # Secret Interspace
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'At the end of every turn, heal', True)
                        self.turnEffects.update({'At the end of every turn, heal '+fraction('1/3', self.moveEffect[1])+' of maximum HP': 4})
                    if self.timeEffectiveness:
                        self.timeEffects.update({'Moves are non-missable': 2})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    if not self.target.immunityFromStatsR:
                        '''Lower opponent’s physical and special attack and speed stats (-1) and accuracy (-2)'''
                        self.target.statsER[0] = max(-6, self.target.statsER[0]-round(1*self.moveEffect[1]))
                        self.target.statsER[1] = max(-6, self.target.statsER[1]-round(1*self.moveEffect[1]))
                        self.target.statsER[4] = max(-6, self.target.statsER[4]-round(1*self.moveEffect[1]))
                        self.target.statsER[5] = max(-6, self.target.statsER[5]-round(2*self.moveEffect[1]))

        # Psychic Chain
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    '''If in {Wonderland}, for the next time, block attack damage received'''
                    if self.timeEffectiveness and 'Wonderland' in self.specialBuffs:
                        self.timeEffects.update({'Block attack damage received': 1})
                    '''Absorb opponent's stats enhancement and transfer own stats reduction to opponent when effective'''
                    ownStatsER = copy.deepcopy(self.statsER)
                    clearStatsR(self)
                    if notImmuned(self, self.moves[2], self.target):
                        if not self.target.immunityFromClearingStatsE:
                            if self.statsEEffectiveness:
                                absorbStatsE(self, self.target)
                            else:
                                clearStatsE(self.target)
                        if not self.target.immunityFromStatsR:
                            transferStatsR(ownStatsER, self.target)
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[2], [self.target]):
                    attackDamage(self, [self.target], self.moves[2])

        # Wonderland
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    '''Enter {Wonderland} (effective for the entire battle and when absent) (affect teammate)'''
                    if not 'Wonderland' in self.specialBuffs:
                        self.specialBuffs.update({'Wonderland': str(math.inf)+' *'+self.id})
                    if self.teammate and not 'Wonderland' in self.teammate.specialBuffs:
                        self.teammate.specialBuffs.update({'Wonderland': str(math.inf)+' *'+self.id})
                        self.teammate.specialBuffsDescription.append(self.specialBuffsDescription[0])
                    if self.statsEEffectiveness:
                        '''Raise special attack, physical and special defense, and speed stats (+1)'''
                        self.statsER[1] = min(6, self.statsER[1]+round(1*self.moveEffect[1]))
                        self.statsER[2] = min(6, self.statsER[2]+round(1*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(1*self.moveEffect[1]))
                        self.statsER[4] = min(6, self.statsER[4]+round(1*self.moveEffect[1]))
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Unparalleled Excellence
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    if isEffective(self, self.moves[4]):
                        '''Increase this attack damage by an amount equivalent to the amount of HP lost'''
                        hpLost = self.stats[5]-self.hp
                        self.attackIncrement += hpLost
                    attackDamage(self, [self.target], self.moves[4])
                    if isEffective(self, self.moves[4]) and self.healingEffectiveness:
                        '''Heal an amount of HP equivalent to this attack damage'''
                        heal(self, self.attackDamageList[-1], True)

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Smash(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'smash'
        self.gender = 'female'
        self.color = (255,60,0)
        self.type = ['fighting']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [135,88,103,103,116,155]

        # unique battle variables
        self.healed = False # if having healed after dealing attack damage while having statsE
        self.doubleDamage = False # if move4 multiplies damage by 2

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if not tasklet and phase[0] == 0 and not 'God\'s Wrath' in self.specialBuffs:
                if self.hp < self.stats[5]/3 or (doubles[0] and not self.teammate):
                    self.specialBuffs.update({'God\'s Wrath': math.inf})
            if tasklet and self.attackList[0] < self.attackList[1] and self.moveAttack and max(self.statsER) > 0 and self.healingEffectiveness and not self.healed:
                self.healed = True
                heal(self, 0.5*self.attackDamageList[-1]*self.abilitiesEffect)
            if not tasklet:
                self.healed = False

        # special buffs
        if 'God\'s Wrath' in self.specialBuffs:
            if self.specialBuffEffectiveness:
                if not tasklet and phase[0] == 2 and self.statsEEffectiveness:
                    for i in range(6):
                        self.statsER[i] = min(6, self.statsER[i]+round(6*self.specialBuffEffect))
                if tasklet and self.attackList[0] < self.attackList[1] and self.moveAttack:
                    self.rateOfCriticalHitIncrement += 0.25*self.specialBuffEffect
                if not tasklet:
                    for i in list(self.statusEffects):
                        if i in ['paralyzed', 'worn-out', 'suffocating', 'frozen', 'petrified', 'asleep', 'flinching', 'confused']:
                            del self.statusEffects[i]

        # Move2
        if not tasklet and phase[0] == 2 and self.opponent and self.hp < self.opponent.hp and self.moveRecord[-1][0][0] == 'Move2':
            self.preemptiveIncrement += 2
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
            element = checkElement(self.turnEffects, 'Reduce all damage received by')
            if element:
                self.receiveAttackIncrement -= getNumber(element)
        if tasklet and self.receiveMagicList[0] > self.receiveMagicList[1]:
            element = checkElement(self.turnEffects, 'Reduce all damage received by')
            if element:
                self.receiveMagicIncrement -= getNumber(element)

        # Move5
        if not tasklet and phase[0] == 2:
            element = checkElement(self.turnEffects, 'Move will go first')
            if element:
                self.preemptiveIncrement += getNumber(element)
                self.ineffectiveIgnored = True

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Move1
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    if isEffective(self, self.moves[1]):
                        self.target.attackPercentBlocked = -1*math.inf
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and 'God\'s Wrath' in self.specialBuffs:
                    addStatusEffect(self, self.target, 'worn-out', 0, True)

        # Move2
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if not self.shield > 0:
                        self.shield += self.hp
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'Reduce all damage received by', True)
                        self.turnEffects.update({'Reduce all damage received by '+str(round(200*self.moveEffect[1])): 3})
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Move3
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    environment[0] = 'fighting pit'
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.opponent, self.oppoTeammate])
            elif moveStep[self.side][self.position] == 4:
                for opponent in self.oppoHit:
                    if opponent and isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], opponent):
                        triggered = False
                        if max(opponent.statsER) > 0:
                            triggered = True
                        if not opponent.immunityFromClearingStatsE:
                            if not opponent.immunityFromStatsR:
                                inverseStatsE(opponent)
                            else:
                                clearStatsE(opponent)
                        if triggered:
                            magicDamage(self, opponent, 250*self.moveEffect[1], True)

        # Move4
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]) and self.hp < self.stats[5]/3:
                    self.doubleDamage = True
                    self.stats[0], self.stats[5] = self.stats[5], round(self.stats[0])
                    self.hp = min(self.hp, self.stats[5])
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[3], [self.target]):
                    if self.doubleDamage:
                        self.attackMultiplier = self.attackMultiplier*2*self.moveEffect[0]
                        self.doubleDamage = False
                    attackDamage(self, [self.target], self.moves[3])

        # Move5
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[4]):
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'Move will go first', 'Move will go first (+'+str(round(2*self.moveEffect[0]))+') and be effective', -1)
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    attackDamage(self, [self.target], self.moves[4])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[4]) and notImmuned(self, self.moves[4], self.target):
                    if not self.goesFirst[abs(self.position-self.target.position)]:
                        amount = round(self.target.stats[5]*0.2*self.moveEffect[0])
                        self.target.stats[5] -= amount
                        self.target.hp = min(self.target.stats[5], self.target.hp)
                        self.stats[5] += amount

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Glare(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'glare'
        self.gender = 'female'
        self.color = (255,255,128)
        self.type = ['light']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [85,136,100,97,140,142]

        # unique battle variables
        self.startingTurn = 0 # records the turn when Kingdom of Light comes into effect
        self.defeating = [] # if move5 has defeated current opponents

    def executeEffects(self, tasklet=False):
        # abilities
        if not tasklet and (self.hp <= 0.5*self.stats[5] or not self.abilitiesEffectiveness):
            self.immunityFromClearingStatsE = False
        if not tasklet and self.abilitiesEffectiveness:
            if self.hp > 0.5*self.stats[5]:
                self.immunityFromClearingStatsE = True
            if phase[0] == 2:
                if self.statsER[1] > 0:
                    self.preemptiveIncrement += self.statsER[1]*self.abilitiesEffect
                self.rateOfDodgingIncrement += (1-self.hp/self.stats[5])*self.abilitiesEffect

        # special buffs
        if 'Kingdom of Light' in self.specialBuffs and self.specialBuffEffectiveness:
            if not tasklet:
                for opponent in sideList[1-self.side]:
                    if moveStep[1-self.side][opponent.position] == '1':
                        '''immune from the effects of all enchantment moves'''
                        self.immunityFromMoves[opponent][1] = True
                if phase[0] == 4 and self.specialBuffs['Kingdom of Light'] == 1:
                    energyLoss(self, None, self.stats[5]*self.specialBuffEffect)
            if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
                numberOfTurns = turn[0]-self.startingTurn+1
                self.receiveAttackPercentMultiplier -= (80*(math.acos(1/math.sqrt(numberOfTurns))**2)+20)/(math.e**(0.2*numberOfTurns))/100

        # Move5
        if not tasklet and phase[0] == 0.5 and self.defeating:
            for i in self.defeating:
                if sideList[1-self.side][i]:
                    addStatusEffect(self, sideList[1-self.side][i], 'blind')
            self.defeating = []

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Move1
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[0]) and not 'Kingdom of Light' in self.specialBuffs:
                    self.specialBuffs.update({'Kingdom of Light': 10})
                    self.startingTurn = turn[0]
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Move2
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[1], [self.target]):
                    attackDamage(self, [self.target], self.moves[1])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    if not self.target.immunityFromClearingStatsE:
                        '''Absorb opponent's stats enhancement'''
                        if self.statsEEffectiveness:
                            absorbStatsE(self, self.target)
                        else:
                            clearStatsE(self.target)
                    addStatusEffect(self, self.target, 'blind')
                    if not self.target.immunityFromStatsR:
                        self.target.statsER[5] = max(-6, self.target.statsER[5]-round(2*self.moveEffect[0]))

        # Move3
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.opponent, self.oppoTeammate])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]):
                    for opponent in self.oppoHit:
                        if opponent and notImmuned(self, self.moves[2], opponent):
                            for i in list(opponent.specialBuffs):
                                try:
                                    opponent.resetAfterClear(i)
                                except:
                                    pass
                                del opponent.specialBuffs[i]
                            if not opponent.immunityFromClearingTurnEffects:
                                clearTurnEffects(opponent)
                            if not opponent.immunityFromClearingTimeEffects:
                                opponent.timeEffects.clear()
                            if not opponent.immunityFromClearingEntireBattleEffects:
                                opponent.entireBattleEffects.clear()

        # Move4
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.statsEEffectiveness:
                        timesUsedInARow = 0
                        for i in range(len(self.moveRecord)-1, -1, -1):
                            if self.moveRecord[i] == self.moves[3]:
                                timesUsedInARow += 1
                            else:
                                break
                        self.statsER[1] = min(6, self.statsER[1]+round(timesUsedInARow*self.moveEffect[1]))
                    if self.healingEffectiveness:
                        '''Heal 100% of maximum HP'''
                        heal(self, self.stats[5]*self.moveEffect[1], True)
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Move5
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[4]):
                    environment[0] = 'bright'
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.opponent, self.oppoTeammate]):
                    attackDamage(self, self.oppoHit, self.moves[4])
                    for opponent in self.oppoHit:
                        if opponent.hp <= 0:
                            self.defeating.append(opponent.position)

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Phoenix(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'phoenix'
        self.gender = 'male'
        self.color = (255,0,0)
        self.type = ['flying', 'fire']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [83,129,108,105,128,144]

        # unique battle variables
        self.reborn = False
        self.energyLost = 0 # to keep track of the energy lost by using Embers of the Sun

    def resetAfterClear(self, element, champ=None):
        if element == 'Immune from status effects':
            self.immunityFromStatusEffects = False

    def revive(self):
        if not self.reborn and self.abilitiesEffectiveness and self.healingEffectiveness:
            '''When dying for the first time, heal an amount of HP equivalent to the HP lost'''
            heal(self, self.stats[5]-self.hp, None, True)
            if self.timeEffectiveness:
                checkElement(self.timeEffects, 'Multiply attack damage by')
                self.timeEffects.update({'Multiply attack damage by '+str(round(2*self.abilitiesEffect)): 1})
            self.reborn = True
        return self.hp > 0

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if not tasklet and moveStep[self.side][self.position] == '2' and isEffective(self, self.moveRecord[-1]) and self.statsEEffectiveness:
                '''All moves raise speed stats (+2)'''
                self.statsER[4] = min(6, self.statsER[4]+round(2*self.abilitiesEffect))
            if tasklet and self.attackList[0] > self.attackList[1] and self.statsER[4] > 0:
                '''When having speed stats enhancement (+x), increase all attack damage dealt by 10x%'''
                self.attackPercentMultiplier += self.statsER[4]*0.1*self.abilitiesEffect
        if tasklet and self.attackList[0] > self.attackList[1]:
            element = checkElement(self.timeEffects, 'Multiply attack damage by')
            if element:
                minusOneTime(self.timeEffects, element)
                self.attackMultiplier = self.attackMultiplier*getNumber(element)

        # Immortal Blaze
        if not tasklet and phase[0] == 4 and self.healingEffectiveness:
            element = checkElement(self.turnEffects, 'At the end of every turn, heal', False, 'when own HP < 50%')
            if element:
                heal(self, getNumber(element)*self.stats[5])

        # Cloud Nine
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1] and self.attacker.moveAttack and max(self.statsER) > 0:
            if 'Block all attack damage dealt by opponent\'s attacking moves when having stats enhancement' in self.turnEffects:
                self.attackPercentBlocked += 1
        if not tasklet and phase[0] == 0.5:
            if 'Immune from status effects' in self.turnEffects:
                self.immunityFromStatusEffects = True

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Crimson Feathers
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    if tryLuck(0.4*self.moveEffect[0]):
                        '''Have a 40% chance of making the opponent burn for the entire battle'''
                        addStatusEffect(self, self.target, 'burnt', math.inf)
                    else:
                        '''if not triggered, then deal an amount of attack damage equivalent to 1/3 of opponent's maximum HP'''
                        attackDamage(self, [self.target], True, 1/3*self.target.stats[5]*self.moveEffect[0])

        # Immortal Blaze
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if not self.shield > 0:
                        '''Gain a 400 HP shield'''
                        self.shield += round(400*self.moveEffect[1])
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'At the end of every turn, heal', True, 'when own HP < 50%')
                        self.turnEffects.update({'At the end of every turn, heal '+str(round(100*self.moveEffect[1]))+'% of maximum HP when own HP < 50%': 3})
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Hyperthermia
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    '''Change the environment to "intense heat"'''
                    environment[0] = 'intense heat'
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[2], [self.target]):
                    attackDamage(self, [self.target], self.moves[2])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    if not self.target.immunityFromClearingStatsE:
                        '''Clear opponent's stats enhancement'''
                        clearStatsE(self.target)
                    if self.target.statusEffects != {} and not self.target.immunityFromStatsR:
                        '''Lower opponent's physical and special attack stats and accuracy (-2) when they have status effects'''
                        self.target.statsER[0] = max(-6, self.target.statsER[0]-round(2*self.moveEffect[0]))
                        self.target.statsER[1] = max(-6, self.target.statsER[1]-round(2*self.moveEffect[0]))
                        self.target.statsER[5] = max(-6, self.target.statsER[5]-round(2*self.moveEffect[0]))

        # Cloud Nine
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.statsEEffectiveness:
                        '''Raise special attack and physical and special defense stats (+1)'''
                        self.statsER[1] = min(6, self.statsER[1]+round(1*self.moveEffect[1]))
                        self.statsER[2] = min(6, self.statsER[2]+round(1*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(1*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Block all attack damage dealt by opponent\'s attacking moves when having stats enhancement': 3})
                        self.turnEffects.update({'Immune from status effects': 5})
                        self.immunityFromStatusEffects = True
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Embers of the Sun
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4], self.hp-1)
                self.energyLost = self.energyLossList[-1]
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    if isEffective(self, self.moves[4]) and environment[0] == 'intense heat':
                        '''When in "intense heat" environment, increase this attack damage by an amount equivalent to the energy lost caused by using this move'''
                        self.attackIncrement += self.energyLost
                    attackDamage(self, [self.target], self.moves[4])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Ray(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'ray'
        self.gender = 'male'
        self.color = (255,255,0)
        self.type = ['electricity']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [134,105,93,85,138,141]

        # unique battle variables
        self.chance = 0.00 # chance of paralyzing the opponent with every move

    def resetUniqueVariables(self):
        self.chance = 0.00

    def executeEffects(self, tasklet=False):
        # abilities
        if not tasklet and self.abilitiesEffectiveness:
            if moveStep[self.side][self.position] == '3':
                '''All moves have a 20% higher chance of paralysing the opponent'''
                self.chance += 0.2*self.abilitiesEffect
            if phase[0] == 0.5 and turn[0] == 1:
                '''Increase maximum HP by an amount equivalent to 30% of speed stats'''
                self.stats[5] += round(self.stats[4]*0.3*self.abilitiesEffect)
                self.hp = self.stats[5]
        if not tasklet and moveStep[self.side][self.position] == '4':
            for opponent in self.oppoHit:
                if opponent:
                    if tryLuck(self.chance):
                        addStatusEffect(self, opponent, 'paralyzed')
                    elif self.abilitiesEffectiveness:
                        '''if not triggered, then apply an amount of magic damage equivalent to 25% of own maximum HP'''
                        magicDamage(self, opponent, 0.25*self.stats[5]*self.abilitiesEffect)
                        if self.turnEffectiveness:
                            trickyTurnUpdate(self.turnEffects, 'Move will go first', 'Move will go first (+'+str(round(1*self.abilitiesEffect))+')', -1)

        # Disconnection
        if not tasklet and phase[0] == 0.5:
            for opponent in sideList[1-self.side]:
                if 'Cut off all healing effects from '+opponent.name.title()+' '+opponent.id in self.turnEffects:
                    opponent.healingEffectiveness = False

        # Aurora
        if tasklet and self.receiveAttackList[0] < self.receiveAttackList[1]:
            element = checkElement(self.turnEffects, 'Has an')
            if element and tryLuck(getNumber(element)):
                addStatusEffect(self, self.attacker, 'paralyzed')

        # Ray Shine
        if not tasklet and moveStep[self.side][self.position] == '2' and isEffective(self, self.moveRecord[-1]) and self.healingEffectiveness:
            element = checkElement(self.turnEffects, 'All moves heal')
            if element:
                heal(self, getNumber(element)*self.stats[5])
        if tasklet and self.attackList[0] > self.attackList[1]:
            element = checkElement(self.turnEffects, 'Multiply all attack damage by')
            if element:
                self.attackMultiplier = self.attackMultiplier*getNumber(element)

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Disconnection
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    if not self.target.immunityFromClearingTurnEffects:
                        '''Clear opponent's turn-effects'''
                        clearTurnEffects(self.target)
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Cut off all healing effects from '+self.target.name.title()+' '+self.target.id: 2})
                        self.target.healingEffectiveness = False
                    '''Has a 40% chance of paralyzing the opponent'''
                    self.chance += 0.4*self.moveEffect[0]

        # Thunder Touch
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[1], [self.target]):
                    if isEffective(self, self.moves[1]):
                        if self.goesFirst[abs(self.position-self.target.position)]:
                            '''Critical hit if going first'''
                            self.rateOfCriticalHitIncrement = math.inf
                    attackDamage(self, [self.target], self.moves[1])
                    if isEffective(self, self.moves[1]) and self.healingEffectiveness:
                        '''Heal an amount of HP equivalent to this attack damage'''
                        heal(self, self.attackDamageList[-1], True)
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    triggered = max(self.target.statsER) > 0
                    if not self.target.immunityFromClearingStatsE:
                        '''Clear opponent's stats enhancement'''
                        clearStatsE(self.target)
                    if not triggered:
                        '''if not triggered, then has a 70% chance of paralyzing the opponent'''
                        self.chance += 0.7*self.moveEffect[0]

        # Aurora
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    '''Clear everyone's special buffs when effective'''
                    for champion in [self, self.teammate, self.opponent, self.oppoTeammate]:
                        if champion:
                            for i in list(champion.specialBuffs):
                                try:
                                    champion.resetAfterClear(i)
                                except:
                                    pass
                                del champion.specialBuffs[i]
                    if self.statsEEffectiveness:
                        '''Raise physical and special defense stats (+2)'''
                        self.statsER[2] = min(6, self.statsER[2]+round(2*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(2*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'Has an', True)
                        self.turnEffects.update({'Has an '+str(round(80*self.moveEffect[1]))+'% chance of paralysing the opponent when receiving attack': 3})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[2], [self.target])

        # Ray Shine
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.statsEEffectiveness:
                        '''Raise physical attack and speed stats (+2)'''
                        self.statsER[0] = min(6, self.statsER[0]+round(2*self.moveEffect[1]))
                        self.statsER[4] = min(6, self.statsER[4]+round(2*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'All moves heal', True)
                        self.turnEffects.update({'All moves heal '+fraction('1/3', self.moveEffect[1])+' of maximum HP': 3})
                        checkElement(self.turnEffects, 'Multiply all attack damage by', True)
                        self.turnEffects.update({'Multiply all attack damage by '+str(round(2*self.moveEffect[1])): 2})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[3], [self.target])

        # Daybreak Lightning
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.opponent, self.oppoTeammate]):
                    if isEffective(self, self.moves[4]):
                        '''Has a 10% chance of multiplying this attack damage by 4'''
                        if tryLuck(0.1*self.moveEffect[0]):
                            self.attackMultiplier = self.attackMultiplier*4*self.moveEffect[0]
                    attackDamage(self, self.oppoHit, self.moves[4])

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Mystic(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'mystic'
        self.gender = 'male'
        self.color = (100,20,100)
        self.type = ['ghost']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [70,126,110,119,116,151]

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if not tasklet and turn[0] == 1 and phase[0] == 0.5 and self.turnEffectiveness:
                self.turnEffects.update({'Make all enchantment moves from the opponent ineffective': 2})
            if tasklet and self.receiveAttackList[0] < self.receiveAttackList[1] and self.receiveAttackDamageList[-1] < 200:
                '''Make the opponent confused when receiving attack damage < 200'''
                addStatusEffect(self, self.attacker, 'confused')
        for opponent in sideList[1-self.side]:
            if not tasklet and moveStep[opponent.side][opponent.position] == '1' and 'Make all enchantment moves from the opponent ineffective' in self.turnEffects:
                opponent.moveEffectiveness[1] = False
                if opponent.moveRecord[-1][0][1] == 'Enchantment' and self.abilitiesEffectiveness:
                    '''if triggered, then apply 350 magic damage'''
                    magicDamage(self, opponent, 350*self.abilitiesEffect)
                    if self.timeEffectiveness:
                        checkElement(self.timeEffects, 'Multiply attack damage received by', True, opponent.id)
                        self.timeEffects.update({'Multiply attack damage received by '+opponent.name.title()+' by '+str(round(2*self.abilitiesEffect))+' '+opponent.id: 1})
        for opponent in sideList[1-self.side]:
            if tasklet and opponent.receiveAttackList[0] > opponent.receiveAttackList[1]:
                element = checkElement(self.timeEffects, 'Multiply attack damage received by', False, opponent.id)
                if element:
                    minusOneTime(self.timeEffects, element)
                    opponent.receiveAttackMultiplier = opponent.receiveAttackMultiplier*getNumber(element)

        # Nail in the Coffin
        for opponent in sideList[1-self.side]:
            if tasklet and opponent.attackList[0] > opponent.attackList[1]:
                element = checkElement(self.entireBattleEffects, 'Reduce all attack damage dealt by', False, opponent.id)
                if element:
                    opponent.attackPercentMultiplier -= getNumber(element)

        # Surreal Manipulation
        if moveStep[self.side][self.position] == '1' and 'Moves are always effective' in self.timeEffects:
            minusOneTime(self.timeEffects, 'Moves are always effective')
            self.ineffectiveIgnored = True

        # Mystic Power
        if not tasklet and moveStep[self.side][self.position] == '4' and isEffective(self, self.moveRecord[-1]):
            for opponent in self.oppoHit:
                if opponent and notImmuned(self, self.moveRecord[-1], opponent) and self.hp < opponent.hp:
                    if 'All moves exchange HP with the opponent if own HP < opponent\'s HP' in self.turnEffects:
                        magicDamage(self, opponent, opponent.hp-self.hp)
                        if self.healingEffectiveness:
                            heal(self, self.magicDamageList[-1])

        # Evil Cleansing Shot
        for opponent in sideList[1-self.side]:
            if not tasklet and moveStep[opponent.side][opponent.position] == '2' and 'Make '+opponent.name.title()+' miss '+opponent.id in self.turnEffects:
                opponent.accuracyReduction = math.inf

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Wake Up Call
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.target]):
                    attackDamage(self, [self.target], self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]) and notImmuned(self, self.moves[0], self.target):
                    triggered = max(self.target.statsER) > 0
                    if not self.target.immunityFromClearingStatsE:
                        '''Clear opponent's stats enhancement'''
                        clearStatsE(self.target)
                    if not triggered:
                        '''if not triggered, then absorb 250 HP from the opponent'''
                        magicDamage(self, self.target, 250*self.moveEffect[0], True)
                        if self.healingEffectiveness:
                            heal(self, self.magicDamageList[-1], True)

        # Nail in the Coffin
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    if not self.target.immunityFromStatsR:
                        '''Lower opponent's physical and special attack and speed stats (-1)'''
                        self.target.statsER[0] = max(-6, self.target.statsER[0]-round(1*self.moveEffect[1]))
                        self.target.statsER[1] = max(-6, self.target.statsER[1]-round(1*self.moveEffect[1]))
                        self.target.statsER[4] = max(-6, self.target.statsER[4]-round(1*self.moveEffect[1]))
                    if self.entireBattleEffectiveness:
                        checkElement(self.entireBattleEffects, 'Reduce all attack damage dealt by', True, self.target.id)
                        self.entireBattleEffects.append('Reduce all attack damage dealt by '+self.target.name.title()+' by '+str(round(35*self.moveEffect[0]))+'% '+self.target.id)

        # Surreal Manipulation
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    if self.timeEffectiveness:
                        self.timeEffects.update({'Moves are always effective': 2})
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[2], [self.target]):
                    attackDamage(self, [self.target], self.moves[2])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[2]) and notImmuned(self, self.moves[2], self.target):
                    if not self.target.immunityFromClearingTurnEffects:
                        '''Clear opponent's turn-effects'''
                        clearTurnEffects(self.target)

        # Mystic Power
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.statsEEffectiveness:
                        '''Raise special attack (+2) and physical and special defense stats (+1)'''
                        self.statsER[1] = min(6, self.statsER[1]+round(2*self.moveEffect[1]))
                        self.statsER[2] = min(6, self.statsER[2]+round(1*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(1*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        self.turnEffects.update({'All moves exchange HP with the opponent if own HP < opponent\'s HP': 4})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[3], [self.target])

        # Evil Cleansing Shot
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    attackDamage(self, [self.target], self.moves[4])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[4]) and notImmuned(self, self.moves[4], self.target):
                    if self.goesFirst[abs(self.position-self.target.position)] and self.turnEffectiveness:
                        '''When going first'''
                        self.turnEffects.update({'Make '+self.target.name.title()+' miss '+self.target.id: 1})

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


class Jeremies(Champion):
    def __init__(self, level=100):
        Champion.__init__(self)
        # basic information
        self.name = 'jeremies'
        self.gender = 'male'
        self.color = (200,0,0)
        self.type = ['fighting']
        self.image = self.loadImage().convert_alpha()
        self.imageCopy = self.image.copy()
        self.rect = self.image.get_rect()
        self.abilities, self.specialBuffsDescription, self.moves = self.loadText()
        self.baseStats = [132,86,102,106,114,148]

    def resetAfterClear(self, element, champ=None):
        if element == 'Immune from clearing stats enhancement and from clearing turn-effects *'+self.id:
            if champ:
                champ.immunityFromClearingStatsE = False
                champ.immunityFromClearingTurnEffects = False

    def ghostEffects(self, tasklet=False):
        for teammember in sideList[self.side]:
            if tasklet and teammember.receiveAttackList[0] < teammember.receiveAttackList[1] and teammember.hp <= 0:
                if 'Keep 1 HP when receiving lethal attack damage *'+self.id in teammember.timeEffects:
                    minusOneTime(teammember.timeEffects, 'Keep 1 HP when receiving lethal attack damage *'+self.id)
                    teammember.hp = 1
        if not tasklet and phase[0] == 0.5:
            for teammember in sideList[self.side]:
                if 'Immune from clearing stats enhancement and from clearing turn-effects *'+self.id in teammember.turnEffects:
                    teammember.immunityFromClearingStatsE = True
                    teammember.immunityFromClearingTurnEffects = True

    def executeEffects(self, tasklet=False):
        # abilities
        if self.abilitiesEffectiveness:
            if tasklet and self.statusEffects != {}:
                '''Block all damage received when having status effects'''
                if self.receiveAttackList[0] > self.receiveAttackList[1]:
                    self.attackPercentBlocked += 1
                if self.receiveMagicList[0] > self.receiveMagicList[1]: 
                    self.magicPercentBlocked += 1
            if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
                '''Reduce critical hit damage received by 50%'''
                self.attacker.criticalPercentAdder -= 0.5*self.abilitiesEffect
            if not tasklet and phase[0] == 4 and 'Wonderland' in self.specialBuffs and self.opponent:
                '''Absorb 200 HP from the opponent at the end of every turn when in {Wonderland}'''
                magicDamage(self, self.opponent, 200*self.abilitiesEffect)
                if self.healingEffectiveness:
                    heal(self, self.magicDamageList[-1])

        # Instant Engage
        for opponent in sideList[1-self.side]:
            if tasklet and opponent.receiveAttackList[0] > opponent.receiveAttackList[1]:
                element = checkElement(self.turnEffects, 'Increase all damage received by', False, opponent.id)
                if element:
                    opponent.receiveAttackPercentMultiplier += getNumber(element)
            if tasklet and opponent.receiveMagicList[0] > opponent.receiveMagicList[1]:
                element = checkElement(self.turnEffects, 'Increase all damage received by', False, opponent.id)
                if element:
                    opponent.receiveMagicPercentMultiplier += getNumber(element)

        # Phantasmagoric
        if tasklet and self.receiveAttackList[0] > self.receiveAttackList[1]:
            element = checkElement(self.turnEffects, 'Reduce attack damage received by')
            if element:
                self.receiveAttackPercentMultiplier -= getNumber(element)
        for opponent in sideList[1-self.side]:
            if tasklet and opponent.magicList[0] > opponent.magicList[1] and 'Make '+opponent.name.title()+'\'s magic damage be blocked '+opponent.id in self.turnEffects:
                opponent.defender.magicPercentBlocked += 1

        # Flaming Heart
        if not tasklet and phase[0] == 2 and self.teammate and self.teammate.name == 'muse' and self.moveRecord[-1][0][0] == 'Flaming Heart':
            self.preemptiveIncrement += 2
        for teammember in sideList[self.side]:
            if tasklet and teammember.receiveAttackList[0] < teammember.receiveAttackList[1] and teammember.hp <= 0:
                if 'Keep 1 HP when receiving lethal attack damage *'+self.id in teammember.timeEffects:
                    minusOneTime(teammember.timeEffects, 'Keep 1 HP when receiving lethal attack damage *'+self.id)
                    teammember.hp = 1

        # Wild Passion
        if tasklet and self.attackList[0] > self.attackList[1] and self.moveAttack:
            if 'All attacking moves will make critical hits' in self.turnEffects:
                self.rateOfCriticalHitIncrement = math.inf
        if not tasklet and phase[0] == 0.5:
            for teammember in sideList[self.side]:
                if 'Immune from clearing stats enhancement and from clearing turn-effects *'+self.id in teammember.turnEffects:
                    teammember.immunityFromClearingStatsE = True
                    teammember.immunityFromClearingTurnEffects = True

        # titles, specialTraits, status effects
        statusEffectEffects(self, tasklet)
        specialTraitEffects(self, tasklet)
        titleEffects(self, tasklet)

    def executeMoves(self):
        if moveStep[self.side][self.position] == 0:
            print(self.name.title(),'used',self.moveRecord[-1][0][0])
            moveStep[self.side][self.position] = 1

        # Instant Engage
        if self.moveRecord[-1] == self.moves[0]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[0])
            elif moveStep[self.side][self.position] == 2:
                pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[0], [self.opponent, self.oppoTeammate]):
                    attackDamage(self, self.oppoHit, self.moves[0])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[0]):
                    for opponent in self.oppoHit:
                        if opponent and notImmuned(self, self.moves[0], opponent):
                            if not opponent.immunityFromClearingStatsE:
                                '''Clear opponent's stats enhancement'''
                                clearStatsE(opponent)
                            if not opponent.immunityFromStatsR:
                                '''Lower opponent's physical and special defense stats (-1)'''
                                opponent.statsER[2] = max(-6, opponent.statsER[2]-round(1*self.moveEffect[0]))
                                opponent.statsER[3] = max(-6, opponent.statsER[3]-round(1*self.moveEffect[0]))
                            if self.turnEffectiveness:
                                checkElement(self.turnEffects, 'Increase all damage received by', True, opponent.id)
                                self.turnEffects.update({'Increase all damage received by '+opponent.name.title()+' by '+str(round(50*self.moveEffect[0]))+'% '+opponent.id: 2})

        # Phantasmagoric
        if self.moveRecord[-1] == self.moves[1]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[1])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[1]):
                    if self.statsEEffectiveness:
                        '''Raise speed stats (+2)'''
                        self.statsER[4] = min(6, self.statsER[4]+round(2*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        checkElement(self.turnEffects, 'Reduce attack damage received by', True)
                        self.turnEffects.update({'Reduce attack damage received by '+str(round(50*self.moveEffect[1]))+'%': 3})
            elif moveStep[self.side][self.position] == 3:
                notMissing(self, self.moves[1], [self.target])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[1]) and notImmuned(self, self.moves[1], self.target):
                    if self.turnEffectiveness:
                        self.turnEffects.update({'Make '+self.target.name.title()+'\'s magic damage be blocked '+self.target.id: 3})

        # Flaming Heart
        if self.moveRecord[-1] == self.moves[2]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[2])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[2]):
                    for teammember in [self, self.teammate]:
                        if teammember:
                            if teammember.healingEffectiveness:
                                '''Heal 100% of maximum HP'''
                                heal(teammember, teammember.stats[5]*self.moveEffect[1], True)
                            if teammember.timeEffectiveness:
                                teammember.timeEffects.update({'Keep 1 HP when receiving lethal attack damage *'+self.id: 1})
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Wild Passion
        if self.moveRecord[-1] == self.moves[3]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[3])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[3]):
                    if self.statsEEffectiveness:
                        '''Raise physical attack and physical and special defense stats and accuracy (+1)'''
                        self.statsER[0] = min(6, self.statsER[0]+round(1*self.moveEffect[1]))
                        self.statsER[2] = min(6, self.statsER[2]+round(1*self.moveEffect[1]))
                        self.statsER[3] = min(6, self.statsER[3]+round(1*self.moveEffect[1]))
                        self.statsER[5] = min(6, self.statsER[5]+round(1*self.moveEffect[1]))
                    if self.turnEffectiveness:
                        trickyTurnUpdate(self.turnEffects, 'All attacking moves will make critical hits', 'All attacking moves will make critical hits', -2)
                    for teammember in [self, self.teammate]:
                        if teammember and teammember.turnEffectiveness:
                            teammember.turnEffects.update({'Immune from clearing stats enhancement and from clearing turn-effects *'+self.id: 3})
                            teammember.immunityFromClearingStatsE = True
                            teammember.immunityFromClearingTurnEffects = True
            elif moveStep[self.side][self.position] == 3:
                moveStep[self.side][self.position] += 2

        # Thunderous Execution
        if self.moveRecord[-1] == self.moves[4]:
            if moveStep[self.side][self.position] == 1:
                energyLoss(self, self.moves[4])
            elif moveStep[self.side][self.position] == 2:
                if isEffective(self, self.moves[4]):
                    pass
            elif moveStep[self.side][self.position] == 3:
                if notMissing(self, self.moves[4], [self.target]):
                    attackDamage(self, [self.target], self.moves[4])
            elif moveStep[self.side][self.position] == 4:
                if isEffective(self, self.moves[4]) and notImmuned(self, self.moves[4], self.target):
                    if self.target.turnEffects != {}:
                        triggered = True
                    else:
                        triggered = False
                    if not self.target.immunityFromClearingTurnEffects:
                        '''Clear opponent's turn-effects; if triggered, then apply 200 magic damage'''
                        clearTurnEffects(self.target)
                    if triggered:
                        magicDamage(self, self.target, 200*self.moveEffect[0], True)
                    if self.attackDamageList[-1] > 300:
                        '''Make the opponent worn out if this attack damage > 300'''
                        addStatusEffect(self, self.target, 'worn-out')

        if moveStep[self.side][self.position] == 5:
            self.phaseFinished = True
            return
        moveStep[self.side][self.position] = str(moveStep[self.side][self.position])
        for i in range(2):
            for j in range(len(sideList[i])):
                stackless.tasklet(sideList[i][j].executeEffects)()
        executeGhostEffects(sideList)
        stackless.schedule()
        moveStep[self.side][self.position] = int(moveStep[self.side][self.position])+1


Champion.groups = battlegroup
PlayerTargetSurface.groups = battlegroup

# for display only
def allChampions():
    allChampions = [
    Sorensen(),
    Zacks(),
    Eet(),
    Seidel(),
    Cassius(),
    Erring(),
    Kuubaesah(),
    Blake(),
    Hamlet(),
    Satan(),
    Gaia(),
    Wesker(),
    Muse(),
    Smash(),
    Glare(),
    Phoenix(),
    Ray(),
    Mystic(),
    Jeremies()
    ]
    return allChampions

