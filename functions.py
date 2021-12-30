import pygame
import math
import random
import os
import time
import importlib
import sys
import copy
import traceback
import stackless

# general ##########################################################################################################
def basicMainloop(x, events):
    global clickedSprite, background
    if clickedSprite == None: # don't set it to None when something got clicked but the mouse is not up
        clickedSprite = None
    milliseconds = clock.tick(FPS)
    seconds = milliseconds/1000.0
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN: # check what sprite is getting clicked
            if len(errorgroup) > 0:
                for i in errorgroup:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        clickedSprite = i
            else:
                for i in allgroups[x]:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        clickedSprite = i
            if event.dict['button'] == 4 or event.dict['button'] == 5:
                try:
                    if clickedSprite != None:
                        clickedSprite.scrolled(event.dict['button'])
                except Exception:
                    traceback.print_exc()

        elif event.type == pygame.MOUSEBUTTONUP and event.dict['button'] == 1: # do something with clicked() function
            if clickedSprite != None:
                if clickedSprite.rect.collidepoint(pygame.mouse.get_pos()):
                    try:
                        output = clickedSprite.clicked() # can include argument (x?) for back button and continue button
                        if output != None:
                            background = output
                    except Exception:
                        traceback.print_exc()
                    clickedSprite = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

    allgroups[x].clear(screen, background)
    if not len(errorgroup) > 0:
        allgroups[x].update(seconds)
    allgroups[x].draw(screen)
    errorgroup.update(seconds)
    errorgroup.draw(screen)
    pygame.display.update()

    if not mainArray[x]: # change to new background
        for i in mainArray:
            if i:
                newNumber = mainArray.index(i)
        screen.blit(background, (0,0))
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join('soundtracks',random.choice(musicList[newNumber])+'.mp3'))
        pygame.mixer.music.play(-1)

    #print(pygame.mouse.get_pos())
    return True

def everyoneElseFinished(orderList, i):
    for champ in orderList[:i]:
        if not champ.phaseFinished:
            return False
    return True

def text(message, fontName, size, color, bold=False, italic=False):
    mytext = pygame.font.SysFont(fontName, size, bold, italic).render(message, True, color).convert_alpha()
    return mytext

def centerText(surface, message, fontName, size, color, bold=False, italic=False):
    mytext = pygame.font.SysFont(fontName, size, bold, italic).render(message, True, color).convert_alpha()
    centerx, centery = surface.get_width()/2, surface.get_height()/2
    textrect = mytext.get_rect(center=(centerx,centery))
    surface.blit(mytext, textrect)

def centerParagraph(spacing, surface, message, fontName, size, color, bold=False, italic=False): # textrect(size/2, size)
    message = message.splitlines()
    for i in range(len(message)):
        message[i] = message[i].split()
    paragraphList = []
    surfaceWidth, surfaceHeight = surface.get_width(), surface.get_height()
    centerx, centery = surfaceWidth/2, surfaceHeight/2
    for i in message:
        line = ''
        for j in range(len(i)):
            lineCopy = copy.copy(line)
            line = line+i[j]+' '
            if len(line)*size/2 >= surfaceWidth-size:
                if lineCopy != '':
                    paragraphList.append(pygame.font.SysFont(fontName, size, bold, italic).render(lineCopy[:-1], True, color).convert_alpha())
                    line = i[j]+' '
            if j == len(i)-1:
                paragraphList.append(pygame.font.SysFont(fontName, size, bold, italic).render(line[:-1], True, color).convert_alpha())
        if spacing and i != message[-1]:
            paragraphList.append(pygame.font.SysFont(fontName, size, bold, italic).render(' ', True, color).convert_alpha())
    for i in range(len(paragraphList)):
        yi = round((surfaceHeight-(size+5)*len(paragraphList))/2+((size+5)*(i+0.5)))
        textrect = paragraphList[i].get_rect(center=(centerx,yi))
        surface.blit(paragraphList[i], textrect)

def championInfoSurface(spacing, paragraph, surface, color, extraSpace=False):
    height = (len(paragraph)//18+1)*18
    if spacing:
        height += len(paragraph.splitlines())*20
    if extraSpace:
        height += len(paragraph.splitlines())*15
    surface.image = pygame.Surface((324,height)).convert_alpha()
    surface.image.fill(color)
    surface.rect = surface.image.get_rect()
    surface.rect.center = (surface.left+surface.rect.width//2,surface.top+surface.rect.height//2)
    centerParagraph(spacing, surface.image, paragraph, 'timesnewroman', 18, (255,255,255))

def numberKey(surface, rect, color1, size, color2=(0,0,0)):
    numberStr = ''
    running = True
    changed = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif pygame.K_0 <= event.key <= pygame.K_9:
                    number = chr(event.key)
                    numberStr += str(number)
                    changed = True
                elif event.key == pygame.K_BACKSPACE:
                    numberStr = numberStr[:-1]
                    changed = True
                surface.fill(color1)
                if numberStr == '':
                    numberStr = '0'
                centerText(surface, numberStr, 'timesnewroman', size, color2)
        screen.blit(surface, (rect.centerx-rect.width//2,rect.centery-rect.height//2))
        pygame.display.update()
    if numberStr == '':
        numberStr = 0
    return int(numberStr), changed

def scrollSurface(scroll, surface, intermediate, button):
    if button == 4:
        scroll = min(scroll+50, 0)
    elif button == 5:
        if intermediate.get_height() < surface.get_height():
            scroll = 0
        else:
            scroll = max(scroll-50, -1*(intermediate.get_height()-surface.get_height()))
    return scroll

def backgrounds(file, screenWidth, screenHeight):
    output = pygame.transform.scale(pygame.image.load(os.path.join('images','background images',file)), (screenWidth,screenHeight)).convert()
    return output

def moveDescription(move):
    output = move[0][1]+'. '+'Energy loss: '+move[1]+'. '+'Accuracy: '+move[2]+'.\n'
    if move[3] != '':
        output = output+'RCH: '+move[3]+'. '+'Power: '+move[4]+'. '+'Type: '
        for i in move[5]:
            output = output+i+','
        output = output[:-1]+'.\n'
    if move[6] != '':
        output = output+'Property: '
        for i in move[6].split(';'):
            output = output+i+'; '
        output = output[:-2]+'.\n'
    if move[7] != '':
        output = output+'Effects: '+move[7]
    return output

def autoSelect(champ):
    if champ:
        attack = champ.baseStats.index(max(champ.baseStats[0], champ.baseStats[1]))
        if sum(champ.levelOfExpertise) == 0:
            champ.levelOfExpertise[attack] = 255
            champ.levelOfExpertise[5] = 255
        if champ.statBooster1 == [0,0,0,0,0,0]:
            if attack == 0:
                champ.statBooster1 = [60,0,28,28,18,66]
                champ.statBooster2 = [60,0,28,28,18,66]
            else:
                champ.statBooster1 = [0,41,23,23,28,85]
                champ.statBooster2 = [0,41,23,23,28,85]
        if champ.title == '':
            champ.title = 'the overwatcher'

# battle ##########################################################################################################
def tryLuck(chance):
    result = random.random()
    if result < chance:
        return True
    else:
        return False

def typeFile():
    typeMatrix = []
    #a = 0
    #b = 0
    with open (os.path.join('text files','other text files','types1.txt')) as file:
        for line in file.readlines():
            typeMatrix.append(line.split(';'))
            for i in range(1,3):
                typeMatrix[-1][i] = typeMatrix[-1][i].split(',')
                if i == 2:
                    typeMatrix[-1][i][-1] = typeMatrix[-1][i][-1][:-1]
    with open (os.path.join('text files','other text files','types2.txt'), 'w') as file:
        for i in range(len(typeMatrix)):
            msg1 = ''
            msg2 = ''
            for j in typeMatrix:
                if typeMatrix[i][0] in j[2]:
                    msg1 = msg1+j[0]+','
                if typeMatrix[i][0] in j[1]:
                    msg2 = msg2+j[0]+','
            file.write(typeMatrix[i][0]+';'+msg1[:-1]+';'+msg2[:-1]+'\n')
            typeMatrix[i].append(msg1[:-1].split(','))
            typeMatrix[i].append(msg2[:-1].split(','))
            #print(typeMatrix[i][0], len(typeMatrix[i][1])+len(typeMatrix[i][3]), len(typeMatrix[i][2])+len(typeMatrix[i][4]))
            #a += len(typeMatrix[i][1])
            #b += len(typeMatrix[i][2])
    #print(a,b)
    return typeMatrix

def typeCompare(type1, type2):
    for i in typeMatrix:
        if i[0] == type1:
            if type2 in i[1]:
                effectiveness = 2.0
            elif type2 in i[2]:
                effectiveness = 0.5
            else:
                effectiveness = 1.0
            return effectiveness

def determineTypeEffectiveness(attackingType, defendingType):
    effectiveness = 0
    for i in defendingType:
        for j in attackingType:
            effectiveness += typeCompare(j,i)
    effectiveness = effectiveness/len(attackingType)/len(defendingType)
    if effectiveness == 2.0:
        effectiveness = max(len(attackingType),len(defendingType))*2.0
    return effectiveness

def determineTypeFamiliarity(attackerType, attackingType):
    if attackingType == ['god']:
        return 1.5
    for i in attackingType:
        if i in attackerType:
            return 1.5
    return 1

def attackDamage(attacker, defenderList, move, baseDamage=0, typeEffectivenessList=[]):
    defenders = []
    if move != None and move != True:
        attacker.moveAttack = True
    if 'confused' in attacker.statusEffects and attacker.moveAttack:
        defenderList = [attacker]
    for defender in defenderList:
        if defender:
            defenders.append(defender)
            attacker.defenders.append(defender)
            defender.attacker = attacker
    attacker.attackList[0] += 0.5
    for defender in defenders:
        defender.receiveAttackList[0] += 0.5
    for i in range(2):
        for j in range(len(sideList[i])):
            #if move != None or i < attacker.side or (i == attacker.side and j <= attacker.position):
            sideList[i][j].executeEffects(True)
    executeGhostEffects(sideList, True)
    critical = []
    for defender in defenders:
        criticalHit = 1.0
        critical.append(False)
        if attacker.moveAttack:
            rateOfCriticalHit = int(move[3][0:len(move[3])-1])/100+attacker.rateOfCriticalHitIncrement
            power = int(move[4])
            attackingType = move[5]
            if defenders.index(defender) == 0:
                environmentEffects(attacker, attackingType)
            if move[0][1] == 'Physical Attack':
                attackStats = attacker.stats[0]
                defenseStats = defender.stats[2]
                attackerStatsER = attacker.statsER[0]
                defenderStatsER = defender.statsER[2]
            elif move[0][1] == 'Special Attack':
                attackStats = attacker.stats[1]
                defenseStats = defender.stats[3]
                attackerStatsER = attacker.statsER[1]
                defenderStatsER = defender.statsER[3]
            else:
                attackStats = attacker.stats[0]+attacker.stats[1]
                defenseStats = defender.stats[2]+defender.stats[3]
                attackerStatsER = attacker.statsER[0]+attacker.statsER[1]
                defenderStatsER = defender.statsER[2]+defender.statsER[3]
            typeFamiliarity = determineTypeFamiliarity(attacker.type, attackingType)
            if not typeEffectivenessList:
                typeEffectiveness = determineTypeEffectiveness(attackingType, defender.type)
            else:
                typeEffectiveness = typeEffectivenessList[defenders.index(defender)]
            if typeEffectiveness < 1 and 'ignore type disadvantages' in move[6].split(';'):
                typeEffectiveness = 1
            if tryLuck(rateOfCriticalHit):
                criticalHit = 2.0
                critical[-1] = True
                attacker.attackPercentMultiplier = max(0, attacker.attackPercentMultiplier+attacker.criticalPercentAdder)
                defender.isCriticalHit = True
            if attacker.ignoreOwnStatsR and attackerStatsER <= 0:
                numerator = power*attackStats
            else:
                numerator = power*attackStats*(1+0.5*abs(attackerStatsER))**((attackerStatsER+0.5)/abs(attackerStatsER+0.5))
            if attacker.ignoreOppoStatsE and defenderStatsER >= 0:
                denominator = defenseStats
            else:
                denominator = defenseStats*(1+0.5*abs(defenderStatsER))**((defenderStatsER+0.5)/abs(defenderStatsER+0.5))
            baseDamage = numerator/denominator*typeFamiliarity*typeEffectiveness*random.randint(600,800)/1000
        else:
            if typeEffectivenessList:
                typeEffectiveness = typeEffectivenessList[0]
            else:
                typeEffectiveness = 1
            baseDamage = baseDamage*typeEffectiveness
        finalDamage = max(0, (baseDamage+attacker.attackIncrement+defender.receiveAttackIncrement))*max(0, 1+attacker.attackPercentMultiplier+defender.receiveAttackPercentMultiplier)*attacker.attackMultiplier*defender.receiveAttackMultiplier*criticalHit
        damageMax = min(attacker.attackMax, defender.defenseMax)
        damageMin = max(attacker.attackMin, defender.defenseMin)
        if damageMax > damageMin:
            finalDamage = min(damageMax, max(damageMin, finalDamage))
        else:
            finalDamage = (damageMax+damageMin)//2
        finalDamage = round(finalDamage*(1-min(1, max(0, defender.attackPercentBlocked))))
        shield = defender.shield
        defender.shield = max(0, defender.shield-finalDamage)
        defender.hp -= max(0, finalDamage-shield)
        attacker.attackDamageList.append(finalDamage)
        defender.receiveAttackDamageList.append(finalDamage)
        print(' ',attacker.name.title(),'dealt',finalDamage,'attack damage to',defender.name.title()+'. critical =',
              critical[-1],'type:',typeEffectiveness,'increments:',attacker.attackIncrement,defender.receiveAttackIncrement,
              'percent multipliers:',attacker.attackPercentMultiplier,defender.receiveAttackPercentMultiplier,
              'multipliers:',attacker.attackMultiplier,defender.receiveAttackMultiplier,defender.attackPercentBlocked)
        attackPercentRebounded = defender.attackPercentRebounded
        if attackPercentRebounded > 0:
            attacker.hp -= round(finalDamage*attackPercentRebounded)
            print(' ',defender.name.title(),'rebounded',round(finalDamage*attackPercentRebounded),'damage to',attacker.name.title())
    attacker.attackList[1] += 1
    for defender in defenders:
        defender.receiveAttackList[1] += 1
    executeGhostEffects(sideList, True)
    for i in range(2):
        for j in range(len(sideList[i])):
            sideList[i][j].executeEffects(True)
    attacker.resetAttackVariables()
    attacker.attackList[0] += 0.5
    for defender in defenders:
        defender.resetDefenseVariables()
        defender.receiveAttackList[0] += 0.5
    return critical

def magicDamage(attacker, defender, baseDamage, move=None):
    attacker.defender = defender
    defender.attacker = attacker
    attacker.magicList[0] += 0.5
    defender.receiveMagicList[0] += 0.5
    for i in range(2):
        for j in range(len(sideList[i])):
            sideList[i][j].executeEffects(True)
    executeGhostEffects(sideList, True)
    finalDamage = round(max(0, (baseDamage+attacker.magicIncrement+defender.receiveMagicIncrement))*max(0, 1+attacker.magicPercentMultiplier+defender.receiveMagicPercentMultiplier)*attacker.magicMultiplier*defender.receiveMagicMultiplier*(1-min(1, max(0, defender.magicPercentBlocked))))
    defender.hp -= finalDamage
    attacker.magicDamageList.append(finalDamage)
    defender.receiveMagicDamageList.append(finalDamage)
    print(' ',attacker.name.title(),'applied',finalDamage,'magic damage to',defender.name.title()+'.',
          'increments:',attacker.magicIncrement,defender.receiveMagicIncrement,'percent multipliers:',
          attacker.magicPercentMultiplier,defender.receiveMagicPercentMultiplier,'multipliers:',
          attacker.magicMultiplier,defender.receiveMagicMultiplier,defender.magicPercentBlocked)
    attacker.magicList[1] += 1
    defender.receiveMagicList[1] += 1
    executeGhostEffects(sideList, True)
    for i in range(2):
        for j in range(len(sideList[i])):
            sideList[i][j].executeEffects(True)
    attacker.resetMagicVariables()
    defender.resetDefenseVariables()
    attacker.magicList[0] += 0.5
    defender.receiveMagicList[0] += 0.5

def energyLoss(champ, move, number=None):
    if move != None and move != True:
        champ.moveEnergy = True
    champ.energyList[0] += 0.5
    for i in range(2):
        for j in range(len(sideList[i])):
            sideList[i][j].executeEffects(True)
    executeGhostEffects(sideList, True)
    if number == None:
        number = int(move[1])
    finalLoss = round((number+champ.energyLossIncrement)*champ.energyLossMultiplier)
    champ.hp -= finalLoss
    champ.energyLossList.append(finalLoss)
    print(' ',champ.name.title(),'lost',finalLoss,'hp.')
    champ.energyList[1] += 1
    executeGhostEffects(sideList, True)
    for i in range(2):
        for j in range(len(sideList[i])):
            sideList[i][j].executeEffects(True)
    champ.resetEnergyVariables()
    champ.energyList[0] += 0.5

def heal(champ, baseNumber, move=None, revive=False):
    if phase[0] == 2 or phase[0] == 4:
        revive = True
    if not revive and champ.hp <= 0:
        return
    else:
        champ.healingList[0] += 0.5
        for i in range(2):
            for j in range(len(sideList[i])):
                sideList[i][j].executeEffects(True)
        executeGhostEffects(sideList, True)
        finalNumber = min(champ.stats[5]-champ.hp, round(baseNumber*champ.healingEffect))
        champ.hp += finalNumber
        champ.healingAmountList.append(finalNumber)
        print(' ',champ.name.title(),'healed',str(finalNumber),'hp.',champ.healingEffect)
        champ.healingList[1] += 1
        executeGhostEffects(sideList, True)
        for i in range(2):
            for j in range(len(sideList[i])):
                sideList[i][j].executeEffects(True)
        champ.healingEffect = 1.00
        champ.healingList[0] += 0.5

def notMissing(champ, move, targetList):
    targets, outcomes, output = [], [], []
    for target in targetList:
        if target:
            targets.append(target)
    if champ.missingIgnored or 'non-missable' in move[6].split(';'):
        champ.oppoHit = targets
        return targets
    accuracy = max(0, int(move[2][:-1])/100-champ.accuracyReduction)
    accuracyER = champ.statsER[5]
    if accuracyER > 0:
        rateOfMissing = 1-accuracy-(1-accuracy)*(2-1/accuracyER)/2
    else:
        rateOfMissing = 1-accuracy/1.2**(accuracyER*(-1))
    for target in targets:
        if not 'trapped' in target.statusEffects and not 'paralyzed' in target.statusEffects and not 'worn-out' in target.statusEffects and not 'suffocating' in target.statusEffects and not 'frozen' in target.statusEffects and not 'asleep' in target.statusEffects:
            rateOfDodgingIncrement = (target.stats[4]*(1+0.5*abs(target.statsER[4]))**((target.statsER[4]+0.5)/abs(target.statsER[4]+0.5)))/10000
        else:
            rateOfDodgingIncrement = -1*target.rateOfDodgingIncrement
        outcomes.append(not tryLuck(rateOfMissing+target.rateOfDodgingIncrement+rateOfDodgingIncrement))
    if not (True in outcomes):
        moveStep[champ.side][champ.position] += 2
    for outcome in range(len(outcomes)):
        if not outcomes[outcome]:
            print(' ',champ.name.title(),'missed against',targets[outcome].name.title()+'.',rateOfMissing,targets[outcome].rateOfDodgingIncrement,champ.accuracyReduction)
            champ.missingList[0] += 1
            targets[outcome].dodgingList[0] += 1
            executeGhostEffects(sideList, True)
            for i in range(2):
                for j in range(len(sideList[i])):
                    sideList[i][j].executeEffects(True)
            champ.missingList[1] += 1
            targets[outcome].dodgingList[1] += 1
        else:
            output.append(targets[outcome])
    champ.oppoHit = output
    return output

def faster(list1, list2):
    champ1, pree1 = list1[0], list1[1]
    champ2, pree2 = list2[0], list2[1]
    if pree1 > pree2: # compare preemptive number
        return True
    elif pree2 > pree1:
        return False
    else:
        speed1 = champ1.stats[4]*(1+0.5*abs(champ1.statsER[4]))**((champ1.statsER[4]+0.5)/abs(champ1.statsER[4]+0.5))
        speed2 = champ2.stats[4]*(1+0.5*abs(champ2.statsER[4]))**((champ2.statsER[4]+0.5)/abs(champ2.statsER[4]+0.5))
        if speed1 > speed2: # compare speed
            return True
        elif speed2 > speed1:
            return False
        else:
            if champ1.hp > champ2.hp: # compare hp
                return True
            elif champ2.hp > champ1.hp:
                return False
            else:
                choice = random.choice([True, False]) # select random
                return choice

def whoGoesFirst(sideList):
    output = []
    champList = []
    orderDict = {}
    for i in sideList:
        for champ in i:
            output.append(None)
            champList.append([champ,champ.preemptiveIncrement])
            orderDict.update({champ.id: None})
    for i in range(len(champList)):
        try:
            champList[i][1] += int(champList[i][0].moveRecord[-1][6].split(';')[0][-3:-1])
        except:
            pass
    for i in range(len(champList)): # selection sort
        currentFastest = 0
        for j in range(1, len(champList)-i):
            if faster(champList[j], champList[currentFastest]):
                currentFastest = j
        orderDict[champList[currentFastest][0].id] = i
        champList[-1*i-1], champList[currentFastest] = champList[currentFastest], champList[-1*i-1]
    for i in range(len(champList)):
        champList[i][0].goesFirst = []
        for opponent in [champList[i][0].opponent, champList[i][0].oppoTeammate]:
            if opponent:
                champList[i][0].goesFirst.append(orderDict[champList[i][0].id] < orderDict[opponent.id])
            else:
                champList[i][0].goesFirst.append(True)
        output[orderDict[champList[i][0].id]] = champList[i][0]
    return output

def sacrifice(champ):
    champ.hp = 0
    if champ.gender == 'male':
        gender = 'him'
    elif champ.gender == 'female':
        gender = 'her'
    else:
        gender = 'it'
    print(' ',champ.name.title(),'sacrificed',gender+'self!')

def clearStatsE(champ):
    champ.statsER = list(map(lambda x: min(0, x), champ.statsER))

def clearStatsR(champ):
    champ.statsER = list(map(lambda x: max(0, x), champ.statsER))

def inverseStatsE(champ, bonus=1):
    champ.statsER = list(map(lambda x: min(x, max(-6, -1*bonus*x)), champ.statsER))

def inverseStatsR(champ, bonus=1):
    champ.statsER = list(map(lambda x: max(x, min(6, -1*bonus*x)), champ.statsER))

def absorbStatsE(you, opponent):
    for i in range(6):
        you.statsER[i] = min(6, you.statsER[i]+max(0, opponent.statsER[i]))
        opponent.statsER[i] = min(0, opponent.statsER[i])

def transferStatsR(yourStatsER, opponent):
    for i in range(6):
        opponent.statsER[i] = max(-6, opponent.statsER[i]+min(0, yourStatsER[i]))

def clearTurnEffects(champ):
    for i in list(champ.turnEffects):
        try:
            if i[-3] == '*' and i[-2:] in champIdDict:
                champIdDict[i[-2:]].resetAfterClear(i, champ)
            if champ.turnEffects[i] > 0:
                champ.resetAfterClear(i)
        except:
            pass
        del champ.turnEffects[i]

def executeGhostEffects(sideList, tasklet=False):
    for identity in list(champIdDict):
        if not champIdDict[identity] in sideList[champIdDict[identity].side]:
            try:
                if tasklet:
                    champIdDict[identity].ghostEffects(True)
                else:
                    stackless.tasklet(champIdDict[identity].ghostEffects)()
            except:
                pass

def isEffective(champ, move):
    if champ.ineffectiveIgnored or 'always effective' in move[6].split(';'):
        return True
    moveType = move[0][1]
    moveNumber = champ.moves.index(move)
    if moveType == 'Enchantment':
        effectiveness = champ.moveEffectiveness[1]
    else:
        effectiveness = champ.moveEffectiveness[0]
    if effectiveness and champ.moveEffectiveness[2][moveNumber]:
        return True
    elif not ineffectiveCalled[champ.side][champ.position]:
        print(' ',champ.name.title()+'\'s',move[0][0],'is ineffective.')
        ineffectiveCalled[champ.side][champ.position] = True
        return False

def notImmuned(champ, move, defender):
    if champ.immuneIgnored or 'ignore immunity' in move[6].split(';'):
        return True
    moveType = move[0][1]
    immunedList = defender.immunityFromMoves[champ]
    if moveType == 'Enchantment':
        immunity = immunedList[1]
    else:
        immunity = immunedList[0]
    if not immunity:
        return True
    elif not immunedCalled[champ.side][champ.position]:
        print(' ',champ.name.title()+'\'s',move[0][0],'is immuned by',defender.name.title()+'.')
        immunedCalled[champ.side][champ.position] = True
        return False

def fraction(baseNumber, multiplier):
    if multiplier == 1:
        return baseNumber
    else:
        baseNumber = int(baseNumber[:baseNumber.index('/')])/int(baseNumber[baseNumber.index('/')+1:])
        return str(float("{0:.2f}".format(float(baseNumber)*multiplier)))

def checkElement(iterable, string, delete=False, endString=''):
    for i in iterable:
        if i.startswith(string) and i.endswith(endString):
            if delete:
                try:
                    iterable.remove(i)
                except:
                    del iterable[i]
            return i
    return False

def getNumber(string):
    for i in string.split():
        if i.isdigit():
            return float(i)
        if i.endswith('%'):
            return int(i[:-1])/100
        if i.startswith('(+') or i.startswith('(-'):
            return int(i[1:-1])
        if '/' in i:
            return int(i[:i.index('/')])/int(i[i.index('/')+1:])
        if '.' in i:
            return int(i[:i.index('.')])+int(i[i.index('.')+1:])/10**len(i[i.index('.')+1:])

def minusOneTime(dictionary, key):
    dictionary[key] -= 1
    if not dictionary[key] > 0:
        del dictionary[key]

def resetIterableVariables():
    for side in range(2):
        for champ in sideList[side]:
            for i in list(champ.specialBuffs):
                try:
                    champ.specialBuffs[i] -= 1
                    if not champ.specialBuffs[i] > 0:
                        del champ.specialBuffs[i]
                except:
                    pass
            for i in list(champ.statusEffects):
                champ.statusEffects[i] -= 1
                if not champ.statusEffects[i] > 0:
                    if i == 'frozen':
                        champ.statusEffects.update({'frostbitten': random.randint(1,3)})
                        champ.hp -= round(1/8*champ.stats[5])
                    del champ.statusEffects[i]
            for i in list(champ.turnEffects):
                if champ.turnEffects[i] < 0:
                    champ.turnEffects[i] = -1*champ.turnEffects[i]
                else:
                    champ.turnEffects[i] -= 1
                    if not champ.turnEffects[i] > 0:
                        del champ.turnEffects[i]

def trickyTurnUpdate(dictionary, key1, key2, value, endString=''):
    element = checkElement(dictionary, key1, False, endString)
    if element:
        if element == key2:
            dictionary.update({key2: value*-1+1})
        else:
            dictionary[element] = 1
            dictionary.update({key2: value})
    else:
        dictionary.update({key2: value})

def phaseFunction():
    if phase[0] == 2:
        phase[0] += 1
    else:
        phase[0] = 0

def checkPlayerSelect(champ):
    try:
        champ.playerSelect()
    except:
        champ.phaseFinished = True
        champ.playerSelecting = False

def titleStats(champ):
    if champ.title == 'the warden':
        for i in range(5):
            champ.stats[i] = champ.stats[i]*1.1
        champ.stats[5] = round(champ.stats[5]*1.1)
    elif champ.title == 'the phoenix':
        champ.stats[5] = round(champ.stats[5]*1.15)

def titleEffects(champ, tasklet=False):
    if tasklet and champ.title == 'the silver knight':
        if champ.attackList[0] > champ.attackList[1] and champ.moveAttack:
            champ.attackPercentMultiplier += 0.4
    elif tasklet and champ.title == 'the overwatcher':
        if champ.receiveAttackList[0] > champ.receiveAttackList[1]:
            champ.receiveAttackPercentMultiplier -= 0.25
        if champ.receiveMagicList[0] > champ.receiveMagicList[1]:
            champ.receiveMagicPercentMultiplier -= 0.25
    elif not tasklet and champ.title == 'the demon king':
        if moveStep[champ.side][champ.position] == '3':
            for opponent in champ.oppoHit:
                if opponent:
                    magicDamage(champ, opponent, 0.2*opponent.stats[5])
    elif tasklet and champ.title == 'the phoenix':
        if champ.healingList[0] > champ.healingList[1]:
            champ.healingEffect += 0.15

def specialTraitEffects(champ, tasklet=False):
    if tasklet and champ.specialTrait == 'born murderer':
        if champ.attackList[0] < champ.attackList[1] and champ.moveAttack:
            for opponent in champ.defenders:
                if not opponent.immunityFromSeckill and tryLuck(0.05):
                    opponent.hp = 0
                    print(' ',opponent.name.title(),'got seckilled by',champ.name.title()+'.')
    elif tasklet and champ.specialTrait == 'sturdy body':
        if champ.receiveAttackList[0] > champ.receiveAttackList[1] and champ.attacker.moveAttack:
            champ.receiveAttackPercentMultiplier -= 0.08
    elif tasklet and champ.specialTrait == 'quick tempered':
        if champ.attackList[0] > champ.attackList[1] and champ.moveAttack and champ.moveRecord[-1][0][1] == 'Physical Attack':
            champ.attackPercentMultiplier += 0.08
    elif tasklet and champ.specialTrait == 'thoroughly cunning':
        if champ.attackList[0] > champ.attackList[1] and champ.moveAttack and champ.moveRecord[-1][0][1] == 'Special Attack':
            champ.attackPercentMultiplier += 0.08
    elif tasklet and champ.specialTrait == 'ghostly':
        if champ.receiveAttackList[0] < champ.receiveAttackList[1] and champ.attacker.moveAttack and champ.attacker.moveRecord[-1][0][1] == 'Special Attack':
            if tryLuck(0.08):
                addStatusEffect(champ, champ.attacker, 'flinching')
    elif tasklet and champ.specialTrait == 'prickly':
        if champ.receiveAttackList[0] < champ.receiveAttackList[1] and champ.attacker.moveAttack and champ.attacker.moveRecord[-1][0][1] == 'Physical Attack':
            if tryLuck(0.08):
                addStatusEffect(champ, champ.attacker, 'paralyzed')
    elif tasklet and champ.specialTrait == 'malevolent':
        if champ.attackList[0] > champ.attackList[1] and champ.moveAttack:
            champ.rateOfCriticalHitIncrement += 0.08
    elif tasklet and champ.specialTrait == 'strongly defiant':
        if champ.receiveAttackList[0] < champ.receiveAttackList[1] and champ.hp <= 0:
            if tryLuck(0.08):
                champ.hp = 1
    elif not tasklet and champ.specialTrait == 'somewhat paranoid':
        if phase[0] == 2:
            champ.rateOfDodgingIncrement += 0.08
    elif tasklet and champ.specialTrait == 'highly persistent':
        if champ.receiveAttackList[0] > champ.receiveAttackList[1] and champ.hp < 1/3*champ.stats[5]:
            champ.receiveAttackPercentMultiplier -= 0.3
        if champ.receiveMagicList[0] > champ.receiveMagicList[1] and champ.hp < 1/3*champ.stats[5]:
            champ.receiveMagicPercentMultiplier -= 0.3
    elif tasklet and champ.specialTrait == 'bloodthirsty':
        if champ.attackList[0] > champ.attackList[1]:
            triggered = False
            for opponent in champ.defenders:
                if opponent.hp < 1/3*opponent.stats[5]:
                    triggered = True
            if triggered:
                champ.attackPercentMultiplier += 0.3
        if champ.magicList[0] > champ.magicList[1] and champ.defender.hp < 1/3*champ.defender.stats[5]:
            champ.magicPercentMultiplier += 0.3
    elif not tasklet and champ.specialTrait == 'total glutton':
        if phase[0] == 4:
            if tryLuck(0.08):
                champ.hp = champ.stats[5]
    elif tasklet and champ.specialTrait == 'counterattack master':
        if champ.receiveAttackList[0] > champ.receiveAttackList[1]:
            if tryLuck(0.08):
                champ.attackPercentRebounded = max(1, champ.attackPercentRebounded)

def addStatusEffect(adder, champ, statusEffect, numberOfTurns=0, forcefully=False):
    if not numberOfTurns:
        numberOfTurns = random.randint(1,4)
    if forcefully or (adder.statusEffectiveness and not champ.immunityFromStatusEffects):
        if statusEffect in champ.statusEffects:
            numberOfTurns = max(champ.statusEffects[statusEffect], numberOfTurns)
            champ.statusEffects.update({statusEffect: numberOfTurns})
        else:
            champ.statusEffects.update({statusEffect: numberOfTurns})
        print(' ',champ.name.title(),'is',statusEffect,'for',str(numberOfTurns),'turns.')
    if champ.reboundStatusEffects and not adder.immunityFromStatusEffects:
        if statusEffect in adder.statusEffects:
            numberOfTurns = max(adder.statusEffects[statusEffect], numberOfTurns)
            adder.statusEffects.update({statusEffect: numberOfTurns})
        else:
            adder.statusEffects.update({statusEffect: numberOfTurns})
        print(' ',adder.name.title(),'is',statusEffect,'for',str(numberOfTurns),'turns.')

def resetGoesFirst(champ):
    oppoList = [champ.opponent, champ.oppoTeammate]
    for i in range(len(champ.goesFirst)):
        champ.goesFirst[i] = False
        if oppoList[i]:
            oppoList[i].goesFirst[i] = True

def statusEffectEffects(champ, tasklet=False):
    if not tasklet and 'paralyzed' in champ.statusEffects:
        if moveStep[champ.side][champ.position] == 0:
            moveStep[champ.side][champ.position] = 5
            resetGoesFirst(champ)
    if not tasklet and 'worn-out' in champ.statusEffects:
        if moveStep[champ.side][champ.position] == 0 and champ.moveRecord[-1][0][1] != 'Enchantment':
            moveStep[champ.side][champ.position] = 5
            resetGoesFirst(champ)
    if not tasklet and 'suffocating' in champ.statusEffects:
        if moveStep[champ.side][champ.position] == 0 and champ.moveRecord[-1][0][1] == 'Enchantment':
            moveStep[champ.side][champ.position] = 5
            resetGoesFirst(champ)
        if phase[0] == 4:
            champ.hp -= round(1/8*champ.stats[5])
    if not tasklet and 'frozen' in champ.statusEffects:
        if moveStep[champ.side][champ.position] == 0:
            moveStep[champ.side][champ.position] = 5
            resetGoesFirst(champ)
    if not tasklet and 'petrified' in champ.statusEffects:
        if moveStep[champ.side][champ.position] == 0:
            moveStep[champ.side][champ.position] = 5
            resetGoesFirst(champ)
    if 'asleep' in champ.statusEffects:
        if not tasklet and moveStep[champ.side][champ.position] == 0:
            moveStep[champ.side][champ.position] = 5
            resetGoesFirst(champ)
        if tasklet and champ.receiveAttackList[0] < champ.receiveAttackList[1] and champ.attacker.moveAttack:
            del champ.statusEffects['asleep']
            moveStep[champ.side][champ.position] = 0
            champ.phaseFinished = False
    if not tasklet and 'flinching' in champ.statusEffects:
        if moveStep[champ.side][champ.position] == 0:
            if tryLuck(0.5):
                moveStep[champ.side][champ.position] = 5
                resetGoesFirst(champ)
            else:
                champ.moveRecord[-1] = random.choice(champ.moves)
                whoGoesFirst(sideList)
    if not tasklet and 'blind' in champ.statusEffects:
        if moveStep[champ.side][champ.position] == '2':
            champ.accuracyReduction += 0.6
    if 'burnt' in champ.statusEffects:
        if not tasklet and phase[0] == 4:
            champ.hp -= round(1/8*champ.stats[5])
        if tasklet and champ.receiveAttackList[0] > champ.receiveAttackList[1] and champ.attacker.moveAttack and champ.attacker.moveRecord[-1][0][1] == 'Physical Attack':
            champ.receiveAttackPercentMultiplier += 0.25
    if 'poisoned' in champ.statusEffects:
        if not tasklet and phase[0] == 4:
            champ.hp -= round(1/8*champ.stats[5])
        if tasklet and champ.receiveAttackList[0] > champ.receiveAttackList[1] and champ.attacker.moveAttack and champ.attacker.moveRecord[-1][0][1] == 'Special Attack':
            champ.receiveAttackPercentMultiplier += 0.25
    if 'frostbitten' in champ.statusEffects:
        if not tasklet and phase[0] == 4:
            champ.hp -= round(1/8*champ.stats[5])
        if tasklet and champ.attackList[0] > champ.attackList[1] and champ.moveAttack and champ.moveRecord[-1][0][1] == 'Physical Attack':
            champ.attackPercentMultiplier -= 0.25
    if 'drowning' in champ.statusEffects:
        if not tasklet and phase[0] == 4:
            champ.hp -= round(1/8*champ.stats[5])
        if tasklet and champ.attackList[0] > champ.attackList[1] and champ.moveAttack and champ.moveRecord[-1][0][1] == 'Special Attack':
            champ.attackPercentMultiplier -= 0.25
    if not tasklet and 'bleeding' in champ.statusEffects:
        if phase[0] == 4:
            champ.hp -= round(1/5*champ.stats[5])
    if 'fractured' in champ.statusEffects:
        if tasklet and champ.receiveAttackList[0] > champ.receiveAttackList[1]:
            champ.receiveAttackPercentMultiplier += 0.15
        if not tasklet and phase[0] == 4:
            champ.hp -= round(1/8*champ.stats[5])
    if 'dizzy' in champ.statusEffects:
        if tasklet and champ.attackList[0] > champ.attackList[1]:
            champ.attackPercentMultiplier -= 0.15
        if not tasklet and moveStep[champ.side][champ.position] == '2':
            champ.accuracyReduction += 0.3
    if not tasklet and 'confused' in champ.statusEffects:
        if moveStep[champ.side][champ.position] == '1':
            champ.moveEffectiveness[0], champ.moveEffectiveness[1] = False, False

def environmentEffects(champ, attackingType):
    currentEnvironment = environment[0]
    if currentEnvironment != None:
        if attackingType == ['god']:
            champ.attackPercentMultiplier += 0.15
        else:
            benefitedTypes = environments[currentEnvironment].split(',')
            for i in attackingType:
                if i in benefitedTypes:
                    champ.attackPercentMultiplier += 0.35
                    return

def checkEndBattle():
    champList = []
    for i in range(2):
        for champ in sideList[i]:
            champList.append(champ)
    for champ in champList:
        if champ.hp <= 0:
            try:
                revived = champ.revive()
            except:
                try:
                    revived = champ.teammate.reviveTeammate()
                except:
                    revived = False
            if not revived:
                champ.lost()
                sideList[champ.side].remove(champ)
                if champ.opponent:
                    champ.opponent.opponent = None
                if doubles[0]:
                    if champ.teammate:
                        champ.teammate.teammate = None
                    if champ.oppoTeammate:
                        champ.oppoTeammate.oppoTeammate = None
                print('\n'+champ.name.title(),'is defeated.'+'\n')
                # clear champ's effects? (tho they're not gonna get executed bc no longer in sideList)
    winner = None
    # in 6v6 doubles, check if there's any champs remaining
    if len(sideList[0]) > 0 and len(sideList[1]) == 0:
        if doubles[0]:
            winner = 'Red side'
        else:
            winner = sideList[0][0].name.title()
    elif len(sideList[0]) == 0 and len(sideList[1]) > 0:
        if doubles[0]:
            winner = 'Blue side'
        else:
            winner = sideList[1][0].name.title()
    elif len(sideList[0]) == 0 and len(sideList[1]) == 0:
        redHpTotal = 0
        blueHpTotal = 0
        for identity in list(champIdDict):
            if identity.startswith('0'):
                redHpTotal += champIdDict[identity].hp
            else:
                blueHpTotal += champIdDict[identity].hp
        if redHpTotal > blueHpTotal:
            if doubles[0]:
                winner = 'Red side'
            else:
                winner = champIdDict['0A'].name.title()
        elif redHpTotal < blueHpTotal:
            if doubles[0]:
                winner = 'Blue side'
            else:
                winner = champIdDict['1A'].name.title()
        else:
            winner = 'It\'s a tie: No one'
    return winner

def battleResultReport(winner):
    print('\n')
    for i in range(2):
        for j in range(len(list(champIdDict))//2):
            champ = champIdDict[str(i)+chr(65+j)]
            print('\n'+champ.name.title(),champ.id,'stats:')
            print(' total attacking times:',len(champ.attackDamageList))
            print(' total attack damage dealt:',sum(champ.attackDamageList))
            print(' total magic damage applied:',sum(champ.magicDamageList))
            print(' total hp healed:',sum(champ.healingAmountList))
            print(' total attack damage received:',sum(champ.receiveAttackDamageList))
            print(' total magic damage received:',sum(champ.receiveMagicDamageList))
            if champ.attackDamageList:
                print(' maximum attack damage dealt:',max(champ.attackDamageList))
    print('\n'+winner+' won!')

# setting up ##########################################################################################################
# initializing
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
screen = pygame.display.set_mode((1080,720))
screenWidth, screenHeight = screen.get_width(), screen.get_height()

# variables for mainloop and time
mainloop = True
mainArray = [True,False,False,False,False]
'''[menu,select,1v1,2v2,6v6]'''
FPS = 150
clock = pygame.time.Clock()
clickedSprite = None

# variables for champions and battle
sideList = [[],[]]
champIdDict = {}
typeMatrix = typeFile()
otherBattleSprites = []
statTypes = ['Physical Attack', 'Special Attack', 'Physcial Defense', 'Special Defense', 'Speed', 'Hit Points']
statERTypes = ['Physical Attack', 'Special Attack', 'Physcial Defense', 'Special Defense', 'Speed', 'Accuracy']
statTypesShort = ['PA', 'SA', 'PD', 'SD', 'SP', 'HP']
moveStep = [[0,0],[0,0]]
doubles = [False]
phase = [0]
turn = [0]
environment = [None]
ineffectiveCalled = [[False,False],[False,False]]
immunedCalled = [[False,False],[False,False]]

# textmaker mouse cursor
xormasks, andmasks = pygame.cursors.compile(pygame.cursors.textmarker_strings)
textmaker = ((8,16), (4,8), xormasks, andmasks)

# music files
musicList = [['Main'],['Selecting'],['PVP1','PVP2','PVP3'],['PVP1','PVP2','PVP3','PVE']]
pygame.mixer.music.load(os.path.join('soundtracks','Main.mp3'))

# special traits for champions
specialTraits = {}
with open(os.path.join('text files','other text files', 'special traits short.txt')) as file:
    for line in file.readlines():
        content = line.split(':')
        specialTraits.update({content[0]: content[1][:-1]})
specialTraitsList = sorted(specialTraits.keys())
specialTraits.update({'Special Traits': 'Description'})
specialTraitsList.insert(0, 'Special Traits')

# stat boosters for champions
statBoosters = {}
with open(os.path.join('text files','other text files', 'stat boosters.txt')) as file:
    for line in file.readlines():
        content = line.split(':')
        if content[1] != '\n':
            content[1] = list(map(lambda x: int(x), content[1].split(',')))
        else:
            break
        statBoosters.update({content[0]: content[1]})
statBoostersList = sorted(statBoosters.keys())
statBoosters.update({'Stat Boosters': 'Description'})
statBoostersList.insert(0, 'Stat Boosters')

# titles for champions
titles = {}
with open(os.path.join('text files','other text files', 'titles short.txt')) as file:
    for line in file.readlines():
        content = line.split(':')
        titles.update({content[0]: content[1][:-1]})
titlesList = sorted(titles.keys())
titles.update({'Titles': 'Description'})
titlesList.insert(0, 'Titles')

# status effects for battle
statusEffectsDescription = {}
with open(os.path.join('text files','other text files', 'status effects.txt')) as file:
    for line in file.readlines():
        content = line.split(':')
        statusEffectsDescription.update({content[0]: content[1][:-1]})

# environments for battle
environments = {}
with open(os.path.join('text files','other text files', 'environments.txt')) as file:
    for line in file.readlines():
        content = line.split(':')
        environments.update({content[0]: content[1][:-1]})

# set up background
backgroundImages = []
for i in range(11):
    backgroundImages.append(backgrounds(str(i+1)+'.jpg', screenWidth, screenHeight))
'''background images list'''
background = backgroundImages[0].copy()
background.blit(text('Simulation', 'timesnewroman', 100, (255,255,255), True), (75,100))
screen.blit(background, (0,0))

# set up sprite groups
menugroup = pygame.sprite.Group()
selectgroup = pygame.sprite.LayeredUpdates()
championgroup = pygame.sprite.LayeredUpdates()
battlegroup = pygame.sprite.LayeredUpdates()
infogroup = pygame.sprite.Group()
errorgroup = pygame.sprite.Group()
allgroups = [menugroup,selectgroup,battlegroup,battlegroup]
moveBoxes = pygame.sprite.Group() # used when champs switch positions/sides during battle


