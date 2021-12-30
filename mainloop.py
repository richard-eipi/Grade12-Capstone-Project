from otherSprites import *

def battleMainloop(x):
    global orderList
    for i in infogroup:
        i.ownUpdate()
    if len(errorgroup.sprites()) == 0:
        winner = checkEndBattle()
        if winner:
            EndBattleWindow(winner)
    if len(errorgroup.sprites()) == 0:
        allFinished = True
        for i in range(2):
            for j in range(len(sideList[i])):
                if not sideList[i][j].phaseFinished:
                    allFinished = False
        if allFinished:
            if phase[0] == 0.5:
                phase[0] = 1
            else:
                phase[0] += 1
            for i in range(2):
                for j in range(len(sideList[i])):
                    sideList[i][j].phaseFinished = False
        if phase[0] == 0:
            turn[0] += 1
            print('\nTurn:',turn[0])
            resetIterableVariables()
            for i in range(2):
                for j in range(len(sideList[i])):
                    sideList[i][j].resetTurnVariables()
                    stackless.tasklet(sideList[i][j].executeEffects)()
            executeGhostEffects(sideList)
            stackless.run()
            phase[0] = 0.5
            for i in range(2):
                for j in range(len(sideList[i])):
                    stackless.tasklet(sideList[i][j].executeEffects)()
            executeGhostEffects(sideList)
            stackless.run()
            for i in range(2):
                for j in range(len(sideList[i])):
                    sideList[i][j].phaseFinished = True
        elif phase[0] == 1:
            for i in range(2):
                for j in range(len(sideList[i])):
                    if sideList[i][j].playerSelecting and not sideList[i][j].playerTargeting:
                        checkPlayerSelect(sideList[i][j])
        elif phase[0] == 2:
            for i in range(2):
                for j in range(len(sideList[i])):
                    stackless.tasklet(sideList[i][j].executeEffects)()
            executeGhostEffects(sideList)
            stackless.tasklet(phaseFunction)()
            stackless.run()
            moveStep[0], moveStep[1] = [0,0], [0,0]
            ineffectiveCalled[0], ineffectiveCalled[1] = [False,False], [False,False]
            immunedCalled[0], immunedCalled[1]= [False,False], [False,False]
            orderList = whoGoesFirst(sideList)
        elif phase[0] == 3:
            for i in range(len(orderList)):
                if (i == 0 or (everyoneElseFinished(orderList, i) and not orderList[i].phaseFinished)):
                    if not (moveStep[orderList[i].side][orderList[i].position] == 3 and not orderList[i].animationFinished):
                        if moveStep[orderList[i].side][orderList[i].position] == 0:
                            statusEffectEffects(orderList[i])
                        stackless.tasklet(orderList[i].executeMoves)()
            stackless.run()
        elif phase[0] == 4:
            for i in range(2):
                for j in range(len(sideList[i])):
                    stackless.tasklet(sideList[i][j].executeEffects)()
            executeGhostEffects(sideList)
            stackless.tasklet(phaseFunction)()
            stackless.run()

    if not mainArray[x]:
        errorgroup.empty()

pygame.mixer.music.play(-1)
while mainloop:
    '''menu'''
    while mainloop and mainArray[0]:
        mainloop = basicMainloop(0, pygame.event.get())

    '''select'''
    while mainloop and mainArray[1]:
        mainloop = basicMainloop(1, pygame.event.get())

    '''battle practice 1v1'''
    while mainloop and mainArray[2]:
        mainloop = basicMainloop(2, pygame.event.get())
        battleMainloop(2)

        if not mainArray[2]:
            errorgroup.empty()

    '''battle practice 2V2'''       
    while mainloop and mainArray[3]:
        mainloop = basicMainloop(3, pygame.event.get())
        battleMainloop(3)

        if not mainArray[3]:
            errorgroup.empty()

pygame.quit()
sys.exit()
