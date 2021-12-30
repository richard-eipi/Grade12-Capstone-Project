import pygame
import math
import random
import os
from champions import *

class V1Button(pygame.sprite.Sprite):
    '''click this button to enter 1v1 picking stage'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((150,50)).convert_alpha()
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (200,300)
        centerText(self.image, '1v1', 'timesnewroman', 30, (0,0,0))

    def clicked(self):
        mainArray[0] = False
        mainArray[1] = True
        BackButton()
        ContinueButton()
        SelectionMenu()
        return backgroundImages[0].copy()
        

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((10,185,225))
            centerText(self.image, '1v1', 'timesnewroman', 32, (0,0,0))
        else:
            self.image.fill((255,255,255))
            centerText(self.image, '1v1', 'timesnewroman', 30, (0,0,0))


class V2Button(pygame.sprite.Sprite):
    '''click this button to enter 2v2 picking stage'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((150,50)).convert_alpha()
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (200,400)
        centerText(self.image, '2v2', 'timesnewroman', 30, (0,0,0))

    def clicked(self):
        mainArray[0] = False
        mainArray[1] = True
        BackButton()
        ContinueButton()
        SelectionMenu2()
        return backgroundImages[0].copy()

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((10,185,225))
            centerText(self.image, '2v2', 'timesnewroman', 32, (0,0,0))
        else:
            self.image.fill((255,255,255))
            centerText(self.image, '2v2', 'timesnewroman', 30, (0,0,0))


class V6Button(pygame.sprite.Sprite):
    '''click this button to enter 6v6 picking stage'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((150,50)).convert_alpha()
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (200,500)
        centerText(self.image, '6v6', 'timesnewroman', 30, (0,0,0))

    def clicked(self):
        mainArray[0] = False
        mainArray[4] = True
        BackButton()
        ContinueButton()
        SelectionMenu()
        return backgroundImages[0].copy()

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((10,185,225))
            centerText(self.image, '6v6', 'timesnewroman', 32, (0,0,0))
        else:
            self.image.fill((255,255,255))
            centerText(self.image, '6v6', 'timesnewroman', 30, (0,0,0))


class ShopButton(pygame.sprite.Sprite):
    '''click this button to enter shop'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((80,80)).convert_alpha()
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (255,255,255), (40,40), 40)
        self.rect = self.image.get_rect()
        self.rect.center = (150,625)
        centerText(self.image, 'Shop', 'timesnewroman', 30, (0,0,0))

    #def clicked(self):
        

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.circle(self.image, (10,185,225), (40,40), 40)
            centerText(self.image, 'Shop', 'timesnewroman', 32, (0,0,0))
        else:
            pygame.draw.circle(self.image, (255,255,255), (40,40), 40)
            centerText(self.image, 'Shop', 'timesnewroman', 30, (0,0,0))


class MyChampionsButton(pygame.sprite.Sprite):
    '''click this button to view your champions'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((100,100)).convert_alpha()
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (255,255,255), (50,50), 50)
        self.rect = self.image.get_rect()
        self.rect.center = (275,625)
        self.image.blit(text('My'+'\n'+'Champions', 'timesnewroman', 20, (0,0,0)), (34,18))
        self.image.blit(text('Champions', 'timesnewroman', 20, (0,0,0)), (8,46))

    #def clicked(self):
        

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.circle(self.image, (10,185,225), (50,50), 50)
            self.image.blit(text('My', 'timesnewroman', 21, (0,0,0)), (33,17))
            self.image.blit(text('Champions', 'timesnewroman', 21, (0,0,0)), (4,45))
        else:
            pygame.draw.circle(self.image, (255,255,255), (50,50), 50)
            self.image.blit(text('My', 'timesnewroman', 20, (0,0,0)), (34,18))
            self.image.blit(text('Champions', 'timesnewroman', 20, (0,0,0)), (8,46))


class RulebookButton(pygame.sprite.Sprite):
    '''click this button to read rulebook'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((150,50)).convert_alpha()
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (960,60)
        centerText(self.image, 'Rulebook', 'timesnewroman', 30, (0,0,0))

    #def clicked(self):
        

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((10,185,225))
            centerText(self.image, 'Rulebook', 'timesnewroman', 32, (0,0,0))
        else:
            self.image.fill((255,255,255))
            centerText(self.image, 'Rulebook', 'timesnewroman', 30, (0,0,0))


class BackButton(pygame.sprite.Sprite):
    '''click this button to take a step back'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((150,50)).convert_alpha()
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (125,670)
        centerText(self.image, 'Back', 'timesnewroman', 30, (0,0,0))

    def clicked(self):
        mainArray[1] = False
        mainArray[0] = True
        for i in selectgroup:
            i.kill()
        background = backgroundImages[0].copy()
        background.blit(text('Simulation', 'timesnewroman', 100, (255,255,255), True), (75,100))
        return background

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((10,185,225))
            centerText(self.image, 'Back', 'timesnewroman', 32, (0,0,0))
        else:
            self.image.fill((255,255,255))
            centerText(self.image, 'Back', 'timesnewroman', 30, (0,0,0))


class ContinueButton(pygame.sprite.Sprite):
    '''click this button to proceed'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((150,50)).convert_alpha()
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (955,670)
        centerText(self.image, 'Continue', 'timesnewroman', 30, (0,0,0))
        self.condition = None
        self.ignored = []

    def clicked(self, condition=None):
        if condition != None:
            self.ignored.append(condition)
        conditions = []
        for i in selectgroup:
            try:
                conditions.append(i.checkContinue())
            except:
                pass
        for i in conditions:
            for j in i:
                if j != True and not j in self.ignored: # if condition is not True and it's not included in the ignored list
                    self.condition = j
                    ErrorWindow(j[0],j[1],self) # call ErrorWindow with condition
                    return
        for i in selectgroup:
            try:
                page = i.doContinue()
            except:# Exception:
                #traceback.print_exc()
                pass
        mainArray[1] = False
        mainArray[page] = True
        return backgroundImages[random.randint(1,10)].copy()

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((10,185,225))
            centerText(self.image, 'Continue', 'timesnewroman', 32, (0,0,0))
        else:
            self.image.fill((255,255,255))
            centerText(self.image, 'Continue', 'timesnewroman', 30, (0,0,0))


class ErrorWindow(pygame.sprite.Sprite):
    '''an error window that requires immediate and undivided attention and operation'''
    def __init__(self, text, cancel=False, button=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((360,200)).convert_alpha()
        pygame.draw.rect(self.image, (255,255,255), (2,2,356,196))
        self.two = cancel
        self.cancel = pygame.Surface((120,40)).convert_alpha()
        self.ok = pygame.Surface((120,40)).convert_alpha()
        self.rect = self.image.get_rect(center=(540,360))
        centerText(self.image, text, 'timesnewroman', 20, (0,0,0), True)
        self.button = button

    def clicked(self):
        if self.two == True:
            if self.cancel.get_rect(center=(430,430)).collidepoint(pygame.mouse.get_pos()):
                self.kill()
            if self.ok.get_rect(center=(650,430)).collidepoint(pygame.mouse.get_pos()):
                self.kill()
                return self.button.clicked(self.button.condition)
        else:
            if self.ok.get_rect(center=(540,430)).collidepoint(pygame.mouse.get_pos()):
                self.kill()

    def update(self, seconds):
        if self.two == True:
            if self.cancel.get_rect(center=(430,430)).collidepoint(pygame.mouse.get_pos()):
                self.cancel.fill((50,50,50))
                centerText(self.cancel, 'Cancel', 'timesnewroman', 22, (255,255,255), True)
                self.image.blit(self.cancel, (70-self.cancel.get_rect().width//2,170-self.cancel.get_rect().height//2))
            else:
                self.cancel.fill((0,0,0))
                centerText(self.cancel, 'Cancel', 'timesnewroman', 20, (255,255,255), True)
                self.image.blit(self.cancel, (70-self.cancel.get_rect().width//2,170-self.cancel.get_rect().height//2))

            if self.ok.get_rect(center=(650,430)).collidepoint(pygame.mouse.get_pos()):
                self.ok.fill((50,50,50))
                centerText(self.ok, 'OK', 'timesnewroman', 22, (255,255,255), True)
                self.image.blit(self.ok, (290-self.ok.get_rect().width//2,170-self.ok.get_rect().height//2))
            else:
                self.ok.fill((0,0,0))
                centerText(self.ok, 'OK', 'timesnewroman', 20, (255,255,255), True)
                self.image.blit(self.ok, (290-self.ok.get_rect().width//2,170-self.ok.get_rect().height//2))
        else:
            if self.ok.get_rect(center=(540,430)).collidepoint(pygame.mouse.get_pos()):
                self.ok.fill((50,50,50))
                centerText(self.ok, 'OK', 'timesnewroman', 22, (255,255,255), True)
                self.image.blit(self.ok, (180-self.ok.get_rect().width//2,170-self.ok.get_rect().height//2))
            else:
                self.ok.fill((0,0,0))
                centerText(self.ok, 'OK', 'timesnewroman', 20, (255,255,255), True)
                self.image.blit(self.ok, (180-self.ok.get_rect().width//2,170-self.ok.get_rect().height//2))

class SelectionMenu(pygame.sprite.Sprite):
    '''where player selects champions for 1v1'''
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.side = ''
        self.sideList = [None,None]
        self.sideListCopy = [None,None]
        for i in range(6):
            SelectionMenu.images.append(pygame.Surface((980,570)).convert_alpha())
            SelectionMenu.images[i].fill((255,255,255))
        self.cancel = pygame.Surface((120,40)).convert_alpha()
        self.ok = pygame.Surface((120,40)).convert_alpha()
        # general selection menu
        SelectionMenu.images[0].fill((0,0,0))
        for i in range(6):
            pygame.draw.line(SelectionMenu.images[0], (255,255,255), (0,50+103*i), (980,50+103*i), 5)
        pygame.draw.line(SelectionMenu.images[0], (255,255,255), (490,0), (490,570), 5)
        SelectionMenu.images[0].blit(text('Player 1', 'timesnewroman', 30, (255,0,0), True), (200,8))
        SelectionMenu.images[0].blit(text('Player 2', 'timesnewroman', 30, (0,0,255), True), (690,8))
        self.champions = allChampions()
        # scroll windows
        self.scrollWindow1, self.scrollWindow3, self.scrollWindow4, self.scrollWindow5 = pygame.Surface((980,405)).convert_alpha(), pygame.Surface((550,380)).convert_alpha(), pygame.Surface((550,380)).convert_alpha(), pygame.Surface((550,380)).convert_alpha()
        self.scrollWindow1.fill((255,255,255))
        self.scrollWindow3.fill((255,255,255))
        self.scrollWindow4.fill((255,255,255))
        self.scrollWindow5.fill((255,255,255))
        self.scrollInter1, self.scrollInter3, self.scrollInter4, self.scrollInter5 = pygame.Surface((980,800)).convert_alpha(), pygame.Surface((550,40*(len(specialTraitsList))+1)).convert_alpha(), pygame.Surface((550,40*(len(statBoostersList))+1)).convert_alpha(), pygame.Surface((550,40*(len(titlesList))+1)).convert_alpha()
        self.checkBoxes3, self.checkBoxes4, self.checkBoxes5 = [], [[],[]], []
        # special traits table
        for i in range(len(specialTraitsList)):
            surface1, surface2 = pygame.Surface((168,39)), pygame.Surface((340,39))
            surface1.fill((255,255,255))
            surface2.fill((255,255,255))
            centerText(surface1, specialTraitsList[i], 'timesnewroman', 20, (0,0,0))
            centerText(surface2, specialTraits.get(specialTraitsList[i]), 'timesnewroman', 20, (0,0,0))
            self.checkBoxes3.append(pygame.Surface((20,20)))
            self.scrollInter3.blit(surface1, (1,1+40*i))
            self.scrollInter3.blit(surface2, (170,1+40*i))
        # stat boosters table
        for i in range(len(statBoostersList)):
            surface1, surface2 = pygame.Surface((168,39)), pygame.Surface((301,39))
            surface1.fill((255,255,255))
            surface2.fill((255,255,255))
            centerText(surface1, statBoostersList[i], 'timesnewroman', 20, (0,0,0))
            string = ''
            if i != 0:
                for j in statBoosters.get(statBoostersList[i]):
                    string += str(j)+', '
                centerText(surface2, string[:-2], 'timesnewroman', 20, (0,0,0))
            else:
                string = statBoosters.get(statBoostersList[i])
                centerText(surface2, string, 'timesnewroman', 20, (0,0,0))
                for j in range(2):
                    surface = pygame.Surface((38,39))
                    surface.fill((255,255,255))
                    centerText(surface, str(j+1), 'timesnewroman', 20, (0,0,0))
                    self.scrollInter4.blit(surface, (472+39*(j),1))
            self.checkBoxes4[0].append(pygame.Surface((20,20)))
            self.checkBoxes4[1].append(pygame.Surface((20,20)))
            self.scrollInter4.blit(surface1, (1,1+40*i))
            self.scrollInter4.blit(surface2, (170,1+40*i))
        # titles table
        for i in range(len(titlesList)):
            surface1, surface2 = pygame.Surface((168,39)), pygame.Surface((340,39))
            surface1.fill((255,255,255))
            surface2.fill((255,255,255))
            centerText(surface1, titlesList[i], 'timesnewroman', 20, (0,0,0))
            centerText(surface2, titles.get(titlesList[i]), 'timesnewroman', 20, (0,0,0))
            self.checkBoxes5.append(pygame.Surface((20,20)))
            self.scrollInter5.blit(surface1, (1,1+40*i))
            self.scrollInter5.blit(surface2, (170,1+40*i))
        self.image = SelectionMenu.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (540,335)
        # small sprites for main selection page
        self.surfaces = [[],[]]
        self.texts = ['Select Champion', 'Level of Expertise', 'Special Trait', 'Stat Boosters', 'Title']
        self.colors = [(255,0,0),(0,0,255)]
        for i in range(5):
            self.surfaces[0].append(pygame.Surface((487.5,98)).convert_alpha())
            self.surfaces[0][i].fill((250-i*50,0,0))
            centerText(self.surfaces[0][i], self.texts[i], 'timesnewroman', 40, (255,255,255), True)
            self.image.blit(self.surfaces[0][i], (1,53+103*i))
            self.surfaces[1].append(pygame.Surface((487.5,98)).convert_alpha())
            self.surfaces[1][i].fill((0,0,250-i*50))
            centerText(self.surfaces[1][i], self.texts[i], 'timesnewroman', 40, (255,255,255), True)
            self.image.blit(self.surfaces[1][i], (493.5,53+103*i))
            
    def clicked(self):
        if self.image == SelectionMenu.images[0]: # main selection page: direct to smaller divisions
            for i in range(len(self.surfaces)):
                for j in range(len(self.surfaces[i])):
                    if self.surfaces[i][j].get_rect(center=(293.75+492.5*i,154+103*j)).collidepoint(pygame.mouse.get_pos()):
                        if self.checkError1(i,j):
                            self.image = SelectionMenu.images[j+1]
                            self.side = i
                            self.scroll = 0
                            for champion in range(len(self.sideListCopy)):
                                if self.sideList[champion] != None:
                                    self.sideListCopy[champion] = self.sideList[champion].copy(self.sideList[champion].name.title())
                                else:
                                    self.sideListCopy[champion] = None
                            if not j == 0:
                                self.smallUpdate(j+1)
                                self.sideList[self.side].imageCopy = pygame.transform.scale(self.sideList[self.side].image, (300,225))
                                self.image.blit(self.sideList[self.side].imageCopy, (25,175))
                            if j == 1:
                                self.image.blit(text('Stats:', 'timesnewroman', 35, (0,0,0), True), (660,110))
                                self.image.blit(text('LoE:', 'timesnewroman', 35, (0,0,0), True), (810,110))
                                self.statTextFields = []
                                self.loeTextFields = []
                                self.loeTextRects = []
                                self.promptField = pygame.Surface((400,80)).convert_alpha()
                                self.promptField.fill((255,255,255))
                                centerText(self.promptField, 'Total LoE remaining: '+str(510-sum(self.sideList[self.side].levelOfExpertise)), 'timesnewroman', 25, (0,0,0))
                                self.image.blit(self.promptField, (290,490))
                                self.sideList[self.side].stats = self.sideList[self.side].determineStats()
                                for k in range(len(self.sideList[self.side].stats)):
                                    self.image.blit(text(statTypes[k]+':', 'timesnewroman', 25, (0,0,0)), (420,180+k*50))
                                    self.statTextFields.append(pygame.Surface((60,30)).convert_alpha())
                                    self.statTextFields[-1].fill((255,255,255))
                                    centerText(self.statTextFields[-1], str(int(self.sideList[self.side].stats[k])), 'timesnewroman', 25, (0,0,0))
                                    self.image.blit(self.statTextFields[-1], (670,180+k*50))
                                    self.loeTextFields.append(pygame.Surface((60,30)).convert_alpha())
                                    self.loeTextFields[-1].fill(self.colors[self.side])
                                    self.loeTextRects.append(self.loeTextFields[-1].get_rect())
                                    self.loeTextRects[-1].center = (895,245+k*50)
                                    centerText(self.loeTextFields[-1], str(self.sideList[self.side].levelOfExpertise[k]), 'timesnewroman', 25, (0,0,0))
                                    self.image.blit(self.loeTextFields[-1], (815,180+k*50))
                        else:
                            ErrorWindow('Please select a champion first.')
        elif self.image == SelectionMenu.images[1]:
            self.cancelOkClicked()
            for i in range(len(self.champions)):
                if self.champions[i].rect.collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side] = self.champions[i]
        elif self.image == SelectionMenu.images[2]:
            self.cancelOkClicked()
            for i in range(len(self.loeTextRects)):
                if self.loeTextRects[i].collidepoint(pygame.mouse.get_pos()):
                    number, changed = numberKey(self.loeTextFields[i], self.loeTextRects[i], self.colors[self.side], 25)
                    self.image.blit(self.loeTextFields[i], (815,180+i*50))
                    if not(changed == False and self.sideListCopy[self.side].levelOfExpertise[i] != 0 and number == 0):
                        self.sideListCopy[self.side].levelOfExpertise[i] = number
                    self.sideListCopy[self.side].stats = self.sideListCopy[self.side].determineStats()
                    self.statTextFields[i].fill((255,255,255))
                    centerText(self.statTextFields[i], str(int(self.sideListCopy[self.side].stats[i])), 'timesnewroman', 25, (0,0,0))
                    self.image.blit(self.statTextFields[i], (670,180+i*50))
                    self.promptField.fill((255,255,255))
                    centerText(self.promptField, 'Total LoE remaining: '+str(510-sum(self.sideListCopy[self.side].levelOfExpertise)), 'timesnewroman', 25, (0,0,0))
                    self.image.blit(self.promptField, (290,490))
        elif self.image == SelectionMenu.images[3]:
            self.cancelOkClicked()
            for i in range(len(self.checkBoxes3)):
                if self.checkBoxes3[i].get_rect(center=(940,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side].specialTrait = specialTraitsList[i+1]
        elif self.image == SelectionMenu.images[4]:
            self.cancelOkClicked()
            for i in range(len(self.checkBoxes4[0])):
                if self.checkBoxes4[0][i].get_rect(center=(901,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side].statBooster1 = statBoosters.get(statBoostersList[i+1])
                if self.checkBoxes4[1][i].get_rect(center=(940,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side].statBooster2 = statBoosters.get(statBoostersList[i+1])
        elif self.image == SelectionMenu.images[5]:
            self.cancelOkClicked()
            for i in range(len(self.checkBoxes5)):
                if self.checkBoxes5[i].get_rect(center=(940,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side].title = titlesList[i+1]

    def update(self, seconds):
        if self.image == SelectionMenu.images[0]:
            for i in range(len(self.surfaces)):
                for j in range(len(self.surfaces[i])):
                    if self.surfaces[i][j].get_rect(center=(293.75+492.5*i,154+103*j)).collidepoint(pygame.mouse.get_pos()):
                        self.surfaces[i][j].fill((0,0,0))
                        centerText(self.surfaces[i][j], self.texts[j], 'timesnewroman', 42, (255,255,255), True)
                    else:
                        self.surfaces[i][j].fill(((1-i)*(250-j*50),0,i*(250-j*50)))
                        centerText(self.surfaces[i][j], self.texts[j], 'timesnewroman', 40, (255,255,255), True)
                    self.image.blit(self.surfaces[i][j], (1+492.5*i,53+103*j))
        elif self.image == SelectionMenu.images[1]:
            counter = 0
            self.smallUpdate(1)
            surface = pygame.Surface((980,80)).convert_alpha()
            surface.fill((255,255,255))
            self.scrollInter1.fill((255,255,255))
            if self.sideListCopy[self.side] != None:
                centerText(surface, self.sideListCopy[self.side].name.title(), 'timesnewroman', 50, (0,0,0), True, True)
            self.image.blit(surface, (0,490))
            for i in range(len(self.champions)):
                if i != 0 and i%5 == 0:
                    counter += 5
                if self.champions[i].rect.collidepoint(pygame.mouse.get_pos()):
                    self.champions[i].imageCopy = pygame.transform.scale(self.champions[i].image, (180,135))
                    self.champions[i].rect = self.champions[i].imageCopy.get_rect(center=(180+180*(i-counter),90+150*(counter/4+1)+self.scroll))
                    self.scrollInter1.blit(self.champions[i].imageCopy, (180+180*(i-counter)-50-self.champions[i].rect.width//2,90+150*(counter/4+1)-130-self.champions[i].rect.height//2))
                else:
                    self.champions[i].imageCopy = pygame.transform.scale(self.champions[i].image, (170,128))
                    self.champions[i].rect = self.champions[i].imageCopy.get_rect(center=(180+180*(i-counter),90+150*(counter/4+1)+self.scroll))
                    self.scrollInter1.blit(self.champions[i].imageCopy, (180+180*(i-counter)-50-self.champions[i].rect.width//2,90+150*(counter/4+1)-130-self.champions[i].rect.height//2))
            self.scrollWindow1.blit(self.scrollInter1, (0,self.scroll))
            self.image.blit(self.scrollWindow1, (0,82.5))
            self.cancelOkUpdate()
        elif self.image == SelectionMenu.images[2]:
            if self.loeTextRects[0].collidepoint(pygame.mouse.get_pos()) or self.loeTextRects[1].collidepoint(pygame.mouse.get_pos()) or self.loeTextRects[2].collidepoint(pygame.mouse.get_pos()) or self.loeTextRects[3].collidepoint(pygame.mouse.get_pos()) or self.loeTextRects[4].collidepoint(pygame.mouse.get_pos()) or self.loeTextRects[5].collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(*textmaker)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.cancelOkUpdate()
        elif self.image == SelectionMenu.images[3]:
            surface = pygame.Surface((38,39))
            surface.fill((255,255,255))
            for i in range(len(self.checkBoxes3)):
                if i != 0:
                    if self.checkBoxes3[i].get_rect(center=(940,180+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()) or specialTraitsList[i] == self.sideListCopy[self.side].specialTrait:
                        self.checkBoxes3[i].fill(self.colors[self.side])
                    else:
                        self.checkBoxes3[i].fill((200,200,200))
                    surface.blit(self.checkBoxes3[i], (surface.get_width()//2-self.checkBoxes3[i].get_width()//2, surface.get_height()//2-self.checkBoxes3[i].get_height()//2))
                self.scrollInter3.blit(surface, (511,1+40*i))
            self.scrollWindow3.blit(self.scrollInter3, (0,self.scroll))
            self.image.blit(self.scrollWindow3, (360,110))
            self.cancelOkUpdate()
        elif self.image == SelectionMenu.images[4]:
            surface1, surface2 = pygame.Surface((38,39)), pygame.Surface((38,39))
            surface1.fill((255,255,255))
            surface2.fill((255,255,255))
            for i in range(len(self.checkBoxes4[0])):
                if i != 0:
                    if self.checkBoxes4[0][i].get_rect(center=(901,180+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()) or statBoosters.get(statBoostersList[i]) == self.sideListCopy[self.side].statBooster1:
                        self.checkBoxes4[0][i].fill(self.colors[self.side])
                    else:
                        self.checkBoxes4[0][i].fill((200,200,200))
                    if self.checkBoxes4[1][i].get_rect(center=(940,180+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()) or statBoosters.get(statBoostersList[i]) == self.sideListCopy[self.side].statBooster2:
                        self.checkBoxes4[1][i].fill(self.colors[self.side])
                    else:
                        self.checkBoxes4[1][i].fill((200,200,200))
                    surface1.blit(self.checkBoxes4[0][i], (surface1.get_width()//2-self.checkBoxes4[0][i].get_width()//2, surface1.get_height()//2-self.checkBoxes4[0][i].get_height()//2))
                    surface2.blit(self.checkBoxes4[1][i], (surface2.get_width()//2-self.checkBoxes4[1][i].get_width()//2, surface2.get_height()//2-self.checkBoxes4[1][i].get_height()//2))
                    self.scrollInter4.blit(surface1, (472,1+40*i))
                    self.scrollInter4.blit(surface2, (511,1+40*i))
            self.scrollWindow4.blit(self.scrollInter4, (0,self.scroll))
            self.image.blit(self.scrollWindow4, (360,110))
            self.cancelOkUpdate()
        elif self.image == SelectionMenu.images[5]:
            surface = pygame.Surface((38,39))
            surface.fill((255,255,255))
            for i in range(len(self.checkBoxes5)):
                if i != 0:
                    if self.checkBoxes5[i].get_rect(center=(940,180+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()) or titlesList[i] == self.sideListCopy[self.side].title:
                        self.checkBoxes5[i].fill(self.colors[self.side])
                    else:
                        self.checkBoxes5[i].fill((200,200,200))
                    surface.blit(self.checkBoxes5[i], (surface.get_width()//2-self.checkBoxes5[i].get_width()//2, surface.get_height()//2-self.checkBoxes5[i].get_height()//2))
                self.scrollInter5.blit(surface, (511,1+40*i))
            self.scrollWindow5.blit(self.scrollInter5, (0,self.scroll))
            self.image.blit(self.scrollWindow5, (360,110))
            self.cancelOkUpdate()

    def scrolled(self, button):
        if self.image == SelectionMenu.images[1]:
            if self.scrollWindow1.get_rect(center=(540,360)).collidepoint(pygame.mouse.get_pos()):
                self.scroll = scrollSurface(self.scroll, self.scrollWindow1, self.scrollInter1, button)
        elif self.image == SelectionMenu.images[3]:
            if self.scrollWindow3.get_rect(center=(685,350)).collidepoint(pygame.mouse.get_pos()):
                self.scroll = scrollSurface(self.scroll, self.scrollWindow3, self.scrollInter3, button)
        elif self.image == SelectionMenu.images[4]:
            if self.scrollWindow4.get_rect(center=(685,350)).collidepoint(pygame.mouse.get_pos()):
                self.scroll = scrollSurface(self.scroll, self.scrollWindow4, self.scrollInter4, button)
        elif self.image == SelectionMenu.images[5]:
            if self.scrollWindow5.get_rect(center=(685,350)).collidepoint(pygame.mouse.get_pos()):
                self.scroll = scrollSurface(self.scroll, self.scrollWindow5, self.scrollInter5, button)

    def cancelOkClicked(self):
        if self.cancel.get_rect(center=(120,580)).collidepoint(pygame.mouse.get_pos()):
            self.image = self.images[0]
        if self.ok.get_rect(center=(960,580)).collidepoint(pygame.mouse.get_pos()):
            if self.image == SelectionMenu.images[2] and not self.checkError2(self.sideListCopy[self.side]):
                return
            for i in range(len(self.sideList)):
                if self.sideListCopy[i] != None:
                    self.sideList[i] = self.sideListCopy[i].copy(self.sideListCopy[i].name.title())
                    if self.image == SelectionMenu.images[1]:
                        autoSelect(self.sideList[i])
            self.image = self.images[0]

    def cancelOkUpdate(self):
        if self.cancel.get_rect(center=(120,580)).collidepoint(pygame.mouse.get_pos()):
            self.cancel.fill((50,50,50))
            centerText(self.cancel, 'Cancel', 'timesnewroman', 22, (255,255,255), True)
            self.image.blit(self.cancel, (70-self.cancel.get_rect().width//2,530-self.cancel.get_rect().height//2))
        else:
            self.cancel.fill((0,0,0))
            centerText(self.cancel, 'Cancel', 'timesnewroman', 20, (255,255,255), True)
            self.image.blit(self.cancel, (70-self.cancel.get_rect().width//2,530-self.cancel.get_rect().height//2))
        if self.ok.get_rect(center=(960,580)).collidepoint(pygame.mouse.get_pos()):
            self.ok.fill((50,50,50))
            centerText(self.ok, 'OK', 'timesnewroman', 22, (255,255,255), True)
            self.image.blit(self.ok, (910-self.ok.get_rect().width//2,530-self.ok.get_rect().height//2))
        else:
            self.ok.fill((0,0,0))
            centerText(self.ok, 'OK', 'timesnewroman', 20, (255,255,255), True)
            self.image.blit(self.ok, (910-self.ok.get_rect().width//2,530-self.ok.get_rect().height//2))

    def smallUpdate(self, number):
        self.image.fill((255,255,255))
        surface = pygame.Surface((980,80)).convert_alpha()
        surface.fill((255,255,255))
        centerText(surface, 'Player '+str(self.side+1)+': '+self.texts[number-1], 'timesnewroman', 50, self.colors[self.side], True)
        self.image.blit(surface, (0,0))
        pygame.draw.line(self.image, self.colors[self.side], (0,80), (980,80), 5)
    
    def checkError1(self, side, item): # checks if player has selected a champion before moving on
        if item != 0:
            if self.sideList[side] == None:
                return False
        return True

    def checkError2(self, champion): # checks if player has entered valid LoEs for the champion
        if sum(champion.levelOfExpertise) > 510:
            ErrorWindow('Total LoE should not exceed 510.')
            return False
        for i in champion.levelOfExpertise:
            if i > 255:
                ErrorWindow('Single LoE should not exceed 255.')
                return False
        return True

    def checkContinue(self):
        output = []
        for i in range(2):
            if self.sideList[i] == None:
                return [('P'+str(i+1)+': No champion selected.', False)]
        for i in range(2):
            if sum(self.sideList[i].levelOfExpertise) < 510:
                output.append(('P'+str(i+1)+': Total LoE < 510. Continue?', True))
            if self.sideList[i].specialTrait == '':
                output.append(('P'+str(i+1)+': No special Trait selected. Continue?', True))
            if self.sideList[i].statBooster1 == [0,0,0,0,0,0] or self.sideList[i].statBooster2 == [0,0,0,0,0,0]:
                output.append(('P'+str(i+1)+': # of stat boosters < 2. Continue?', True))
            if self.sideList[i].title == '':
                output.append(('P'+str(i+1)+': No title selected. Continue?', True))
        if len(output) == 0:
            return [True]
        else:
            return output

    def doContinue(self):
        battlegroup.empty()
        for i in range(2):
            self.sideList[i].id = str(i)+'A'
            champIdDict.update({self.sideList[i].id: self.sideList[i]})
            self.sideList[i].side = i
            self.sideList[i].opponent = self.sideList[1-i]
            self.sideList[i].image = pygame.transform.scale(self.sideList[i].image, (432,308))
            self.sideList[i].rect = self.sideList[i].image.get_rect()
            self.sideList[i].battlePosition = [216+i*648,370]
            self.sideList[i].stats = self.sideList[i].determineStats()
            titleStats(self.sideList[i])
            self.sideList[i].hp = self.sideList[i].stats[5]
            sideList[i] = []
            sideList[i].append(self.sideList[i])
            battlegroup.add(sideList[i][0])
            sideList[i][0].champInfo = ChampionInfo(i)
            sideList[i][0]._layer = 4
            print('P'+str(i+1)+': '+sideList[i][0].name.title(),'\n',' Stats: ',sideList[i][0].stats,'\n',' Special trait: ',sideList[i][0].specialTrait,
                  '\n',' Stat boosters: ',sideList[i][0].statBooster1,sideList[i][0].statBooster2,'\n',' Title: ',sideList[i][0].title,'\n',sep='')
        print()
        sideList[1][0].image = pygame.transform.flip(sideList[1][0].image, 1, 0)
        for i in range(5):
            MoveBoxes(sideList[0][0].moves[i], None, sideList[1][0].moves[i], None, i)
        moveStep[0], moveStep[1] = [0,0], [0,0]
        doubles[0] = False
        phase[0] = 0
        turn[0] = 0
        environment[0] = None
        ShowTurn()
        ShowEnvironment()
        otherBattleSprites.append(SpecialEffects())
        for i in selectgroup:
            i.kill()
        return 2


class SelectionMenu2(pygame.sprite.Sprite):
    '''where player selects champions for 2v2'''
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.side = ''
        self.sideList = [[None,None],[None,None]]
        self.sideListCopy = [[None,None],[None,None]]
        for i in range(6):
            SelectionMenu2.images.append(pygame.Surface((980,570)).convert_alpha())
            SelectionMenu2.images[i].fill((255,255,255))
        self.cancel = pygame.Surface((120,40)).convert_alpha()
        self.ok = pygame.Surface((120,40)).convert_alpha()
        # general selection menu
        SelectionMenu2.images[0].fill((0,0,0))
        for i in range(6):
            pygame.draw.line(SelectionMenu2.images[0], (255,255,255), (0,50+103*i), (980,50+103*i), 5)
        pygame.draw.line(SelectionMenu2.images[0], (255,255,255), (490,0), (490,570), 5)
        SelectionMenu2.images[0].blit(text('Player 1', 'timesnewroman', 30, (255,0,0), True), (200,8))
        SelectionMenu2.images[0].blit(text('Player 2', 'timesnewroman', 30, (0,0,255), True), (690,8))
        self.champions = allChampions()
        # scroll windows
        self.scrollWindow1, self.scrollWindow5 = pygame.Surface((980,405)).convert_alpha(), pygame.Surface((261,380)).convert_alpha()
        self.scrollWindow3, self.scrollWindow4 = pygame.Surface((300,380)).convert_alpha(), pygame.Surface((378,380)).convert_alpha()
        self.scrollWindow1.fill((255,255,255))
        self.scrollWindow3.fill((255,255,255))
        self.scrollWindow4.fill((255,255,255))
        self.scrollWindow5.fill((255,255,255))
        self.scrollInter1, self.scrollInter5 = pygame.Surface((980,800)).convert_alpha(), pygame.Surface((261,40*(len(titlesList))+1)).convert_alpha()
        self.scrollInter3, self.scrollInter4 = pygame.Surface((300,40*(len(specialTraitsList))+1)).convert_alpha(), pygame.Surface((378,40*(len(statBoostersList))+1)).convert_alpha()
        self.checkBoxes3, self.checkBoxes4, self.checkBoxes5 = [[],[]], [[[],[]],[[],[]]], []
        # special traits table
        for i in range(len(specialTraitsList)):
            surface = pygame.Surface((220,39))
            surface.fill((255,255,255))
            centerText(surface, specialTraitsList[i], 'timesnewroman', 20, (0,0,0))
            self.checkBoxes3[0].append(pygame.Surface((20,20)))
            self.checkBoxes3[1].append(pygame.Surface((20,20)))
            self.scrollInter3.blit(surface, (40,1+40*i))
        # stat boosters table
        for i in range(len(statBoostersList)):
            surface = pygame.Surface((220,39))
            surface.fill((255,255,255))
            centerText(surface, statBoostersList[i], 'timesnewroman', 20, (0,0,0))
            self.checkBoxes4[0][0].append(pygame.Surface((20,20)))
            self.checkBoxes4[1][0].append(pygame.Surface((20,20)))
            self.checkBoxes4[0][1].append(pygame.Surface((20,20)))
            self.checkBoxes4[1][1].append(pygame.Surface((20,20)))
            self.scrollInter4.blit(surface, (79,1+40*i))
        # titles table
        for i in range(len(titlesList)):
            surface = pygame.Surface((220,39))
            surface.fill((255,255,255))
            centerText(surface, titlesList[i], 'timesnewroman', 20, (0,0,0))
            self.checkBoxes5.append(pygame.Surface((20,20)))
            self.scrollInter5.blit(surface, (1,1+40*i))
        self.image = SelectionMenu2.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (540,335)
        # small sprites for main selection page
        self.surfaces = [[],[]]
        self.texts = ['Select Champions', 'Level of Expertise', 'Special Traits', 'Stat Boosters', 'Title']
        self.colors = [(255,0,0),(0,0,255)]
        for i in range(5):
            self.surfaces[0].append(pygame.Surface((487.5,98)).convert_alpha())
            self.surfaces[0][i].fill((250-i*50,0,0))
            centerText(self.surfaces[0][i], self.texts[i], 'timesnewroman', 40, (255,255,255), True)
            self.image.blit(self.surfaces[0][i], (1,53+103*i))
            self.surfaces[1].append(pygame.Surface((487.5,98)).convert_alpha())
            self.surfaces[1][i].fill((0,0,250-i*50))
            centerText(self.surfaces[1][i], self.texts[i], 'timesnewroman', 40, (255,255,255), True)
            self.image.blit(self.surfaces[1][i], (493.5,53+103*i))
            
    def clicked(self):
        if self.image == SelectionMenu2.images[0]: # main selection page: direct to smaller divisions
            for i in range(len(self.surfaces)):
                for j in range(len(self.surfaces[i])):
                    if self.surfaces[i][j].get_rect(center=(293.75+492.5*i,154+103*j)).collidepoint(pygame.mouse.get_pos()):
                        if self.checkError1(i,j):
                            self.image = SelectionMenu2.images[j+1]
                            self.side = i
                            self.scroll = 0
                            for champion in range(len(self.sideListCopy[self.side])):
                                if self.sideList[self.side][champion] != None:
                                    self.sideListCopy[self.side][champion] = self.sideList[self.side][champion].copy(self.sideList[self.side][champion].name.title())
                                else:
                                    self.sideListCopy[self.side][champion] = None
                            if not j == 0:
                                self.smallUpdate(j+1)
                                self.sideList[self.side][0].imageCopy = pygame.transform.scale(self.sideList[self.side][0].image, (240,180))
                                self.image.blit(self.sideList[self.side][0].imageCopy, (20,200))
                                self.sideList[self.side][1].imageCopy = pygame.transform.flip(pygame.transform.scale(self.sideList[self.side][1].image, (240,180)), 1, 0)
                                self.image.blit(self.sideList[self.side][1].imageCopy, (720,200))
                            if j == 1:
                                mytext = text('LoE:', 'timesnewroman', 35, (0,0,0), True)
                                self.image.blit(mytext, mytext.get_rect(center=(490,125)))
                                self.loeTextFields = [[],[]]
                                self.loeTextRects = [[],[]]
                                self.statTextFields = [[],[]]
                                self.promptField = [pygame.Surface((360,80)).convert_alpha(), pygame.Surface((360,80)).convert_alpha()]
                                for x in range(2):
                                    self.promptField[x].fill((255,255,255))
                                    centerText(self.promptField[x], str(510-sum(self.sideListCopy[self.side][x].levelOfExpertise))+'  remaining', 'timesnewroman', 25, (0,0,0))
                                    self.image.blit(self.promptField[x], (130+x*360,490))
                                    self.sideListCopy[self.side][x].stats = self.sideListCopy[self.side][x].determineStats()
                                    for y in range(6):
                                        self.statTextFields[x].append(pygame.Surface((60,30)).convert_alpha())
                                        self.statTextFields[x][-1].fill((255,255,255))
                                        self.loeTextFields[x].append(pygame.Surface((60,30)).convert_alpha())
                                        self.loeTextFields[x][-1].fill(self.colors[self.side])
                                        self.loeTextRects[x].append(self.loeTextFields[0][-1].get_rect())
                                        self.loeTextRects[x][-1].center = (450+x*180,245+y*50)
                                        centerText(self.loeTextFields[x][-1], str(self.sideList[self.side][x].levelOfExpertise[y]), 'timesnewroman', 25, (0,0,0))
                                        self.image.blit(self.loeTextFields[x][-1], (370+x*180,180+y*50))
                                        centerText(self.statTextFields[x][-1], str(int(self.sideListCopy[self.side][x].stats[y])), 'timesnewroman', 25, (0,0,0))
                                        self.image.blit(self.statTextFields[x][-1], (280+x*360,180+y*50))
                                        if x == 1:
                                            mytext = text(statTypesShort[y], 'timesnewroman', 25, (0,0,0))
                                            self.image.blit(mytext, mytext.get_rect(center=(490,195+y*50)))
                        else:
                            ErrorWindow('Please select two champions.')
        elif self.image == SelectionMenu2.images[1]:
            self.cancelOkClicked()
            for i in range(len(self.champions)):
                if self.champions[i].rect.collidepoint(pygame.mouse.get_pos()):
                    if self.sideListCopy[self.side][0] == None and self.sideListCopy[self.side][1] == None:
                        self.sideListCopy[self.side][0] = self.champions[i]
                    elif self.sideListCopy[self.side][0] != None and self.sideListCopy[self.side][1] == None:
                        self.sideListCopy[self.side][1] = self.champions[i]
                    else:
                        self.sideListCopy[self.side][0] = self.sideListCopy[self.side][1]
                        self.sideListCopy[self.side][1] = self.champions[i]
        elif self.image == SelectionMenu2.images[2]:
            self.cancelOkClicked()
            for i in range(2):
                for j in range(6):
                    if self.loeTextRects[i][j].collidepoint(pygame.mouse.get_pos()):
                        number, changed = numberKey(self.loeTextFields[i][j], self.loeTextRects[i][j], self.colors[self.side], 25)
                        self.image.blit(self.loeTextFields[i][j], (370+i*180,180+j*50))
                        if not(changed == False and self.sideListCopy[self.side][i].levelOfExpertise[j] != 0 and number == 0):
                            self.sideListCopy[self.side][i].levelOfExpertise[j] = number
                            self.promptField[i].fill((255,255,255))
                            centerText(self.promptField[i], str(510-sum(self.sideListCopy[self.side][i].levelOfExpertise))+'  remaining', 'timesnewroman', 25, (0,0,0))
                            self.image.blit(self.promptField[i], (130+i*360,490))
                            self.sideListCopy[self.side][i].stats = self.sideListCopy[self.side][i].determineStats()
                            self.statTextFields[i][j].fill((255,255,255))
                            centerText(self.statTextFields[i][j], str(int(self.sideListCopy[self.side][i].stats[j])), 'timesnewroman', 25, (0,0,0))
                            self.image.blit(self.statTextFields[i][j], (280+i*360,180+j*50))
        elif self.image == SelectionMenu2.images[3]:
            self.cancelOkClicked()
            for i in range(2):
                for j in range(len(self.checkBoxes3[0])):
                    if self.checkBoxes3[i][j].get_rect(center=(410+258*i,220+40*j+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                        self.sideListCopy[self.side][i].specialTrait = specialTraitsList[j+1]
        elif self.image == SelectionMenu2.images[4]:
            self.cancelOkClicked()
            for i in range(len(self.checkBoxes4[0][0])):
                if self.checkBoxes4[0][0][i].get_rect(center=(371,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side][0].statBooster1 = statBoosters.get(statBoostersList[i+1])
                if self.checkBoxes4[0][1][i].get_rect(center=(410,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side][0].statBooster2 = statBoosters.get(statBoostersList[i+1])
                if self.checkBoxes4[1][0][i].get_rect(center=(709,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side][1].statBooster1 = statBoosters.get(statBoostersList[i+1])
                if self.checkBoxes4[1][1][i].get_rect(center=(670,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side][1].statBooster2 = statBoosters.get(statBoostersList[i+1])
        elif self.image == SelectionMenu2.images[5]:
            self.cancelOkClicked()
            for i in range(len(self.checkBoxes5)):
                if self.checkBoxes5[i].get_rect(center=(650,220+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()):
                    self.sideListCopy[self.side][0].title = titlesList[i+1]
                    self.sideListCopy[self.side][1].title = titlesList[i+1]

    def update(self, seconds):
        if self.image == SelectionMenu2.images[0]:
            for i in range(len(self.surfaces)):
                for j in range(len(self.surfaces[i])):
                    if self.surfaces[i][j].get_rect(center=(293.75+492.5*i,154+103*j)).collidepoint(pygame.mouse.get_pos()):
                        self.surfaces[i][j].fill((0,0,0))
                        centerText(self.surfaces[i][j], self.texts[j], 'timesnewroman', 42, (255,255,255), True)
                    else:
                        self.surfaces[i][j].fill(((1-i)*(250-j*50),0,i*(250-j*50)))
                        centerText(self.surfaces[i][j], self.texts[j], 'timesnewroman', 40, (255,255,255), True)
                    self.image.blit(self.surfaces[i][j], (1+492.5*i,53+103*j))
        elif self.image == SelectionMenu2.images[1]:
            counter = 0
            self.smallUpdate(1)
            surface1, surface2 = pygame.Surface((360,80)).convert_alpha(), pygame.Surface((360,80)).convert_alpha()
            surface1.fill((255,255,255))
            surface2.fill((255,255,255))
            self.scrollInter1.fill((255,255,255))
            if self.sideListCopy[self.side][0] != None:
                centerText(surface1, self.sideListCopy[self.side][0].name.title(), 'timesnewroman', 50, (0,0,0), True, True)
            if self.sideListCopy[self.side][1] != None:
                centerText(surface2, self.sideListCopy[self.side][1].name.title(), 'timesnewroman', 50, (0,0,0), True, True)
            self.image.blit(surface1, (130,490))
            self.image.blit(surface2, (490,490))
            for i in range(len(self.champions)):
                if i != 0 and i%5 == 0:
                    counter += 5
                if self.champions[i].rect.collidepoint(pygame.mouse.get_pos()):
                    self.champions[i].imageCopy = pygame.transform.scale(self.champions[i].image, (180,135))
                    self.champions[i].rect = self.champions[i].imageCopy.get_rect(center=(180+180*(i-counter),90+150*(counter/4+1)+self.scroll))
                    self.scrollInter1.blit(self.champions[i].imageCopy, (180+180*(i-counter)-50-self.champions[i].rect.width//2,90+150*(counter/4+1)-130-self.champions[i].rect.height//2))
                else:
                    self.champions[i].imageCopy = pygame.transform.scale(self.champions[i].image, (170,128))
                    self.champions[i].rect = self.champions[i].imageCopy.get_rect(center=(180+180*(i-counter),90+150*(counter/4+1)+self.scroll))
                    self.scrollInter1.blit(self.champions[i].imageCopy, (180+180*(i-counter)-50-self.champions[i].rect.width//2,90+150*(counter/4+1)-130-self.champions[i].rect.height//2))
            self.scrollWindow1.blit(self.scrollInter1, (0,self.scroll))
            self.image.blit(self.scrollWindow1, (0,82.5))
            self.cancelOkUpdate()
        elif self.image == SelectionMenu2.images[2]:
            ready = False
            for i in range(6):
                if self.loeTextRects[0][i].collidepoint(pygame.mouse.get_pos()) or self.loeTextRects[1][i].collidepoint(pygame.mouse.get_pos()):
                    ready = True
            if ready:
                pygame.mouse.set_cursor(*textmaker)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.cancelOkUpdate()
        elif self.image == SelectionMenu2.images[3]:
            for i in range(2):
                surface = pygame.Surface((38,39))
                surface.fill((255,255,255))
                for j in range(len(self.checkBoxes3[0])):
                    if j != 0:
                        if self.checkBoxes3[i][j].get_rect(center=(410+258*i,180+40*j+self.scroll)).collidepoint(pygame.mouse.get_pos()) or specialTraitsList[j] == self.sideListCopy[self.side][i].specialTrait:
                            self.checkBoxes3[i][j].fill(self.colors[self.side])
                        else:
                            self.checkBoxes3[i][j].fill((200,200,200))
                        surface.blit(self.checkBoxes3[i][j], (surface.get_width()//2-self.checkBoxes3[i][j].get_width()//2, surface.get_height()//2-self.checkBoxes3[i][j].get_height()//2))
                    self.scrollInter3.blit(surface, (1+260*i,1+40*j))
            self.scrollWindow3.blit(self.scrollInter3, (0,self.scroll))
            self.image.blit(self.scrollWindow3, (340,110))
            self.cancelOkUpdate()
        elif self.image == SelectionMenu2.images[4]:
            for i in range(2):
                surface1, surface2 = pygame.Surface((38,39)), pygame.Surface((38,39))
                surface1.fill((255,255,255))
                surface2.fill((255,255,255))
                for j in range(len(self.checkBoxes4[0][0])):
                    if j != 0:
                        if self.checkBoxes4[i][0][j].get_rect(center=(371+338*i,180+40*j+self.scroll)).collidepoint(pygame.mouse.get_pos()) or statBoosters.get(statBoostersList[j]) == self.sideListCopy[self.side][i].statBooster1:
                            self.checkBoxes4[i][0][j].fill(self.colors[self.side])
                        else:
                            self.checkBoxes4[i][0][j].fill((200,200,200))
                        if self.checkBoxes4[i][1][j].get_rect(center=(410+260*i,180+40*j+self.scroll)).collidepoint(pygame.mouse.get_pos()) or statBoosters.get(statBoostersList[j]) == self.sideListCopy[self.side][i].statBooster2:
                            self.checkBoxes4[i][1][j].fill(self.colors[self.side])
                        else:
                            self.checkBoxes4[i][1][j].fill((200,200,200))
                        surface1.blit(self.checkBoxes4[i][0][j], (surface1.get_width()//2-self.checkBoxes4[i][0][j].get_width()//2, surface1.get_height()//2-self.checkBoxes4[i][0][j].get_height()//2))
                        surface2.blit(self.checkBoxes4[i][1][j], (surface2.get_width()//2-self.checkBoxes4[i][1][j].get_width()//2, surface2.get_height()//2-self.checkBoxes4[i][1][j].get_height()//2))
                    self.scrollInter4.blit(surface1, (1+338*i,1+40*j))
                    self.scrollInter4.blit(surface2, (40+260*i,1+40*j))
            self.scrollWindow4.blit(self.scrollInter4, (0,self.scroll))
            self.image.blit(self.scrollWindow4, (301,110))
            self.cancelOkUpdate()
        elif self.image == SelectionMenu2.images[5]:
            surface = pygame.Surface((38,39))
            surface.fill((255,255,255))
            for i in range(len(self.checkBoxes5)):
                if i != 0:
                    if self.checkBoxes5[i].get_rect(center=(650,180+40*i+self.scroll)).collidepoint(pygame.mouse.get_pos()) or titlesList[i] == self.sideListCopy[self.side][0].title:
                        self.checkBoxes5[i].fill(self.colors[self.side])
                    else:
                        self.checkBoxes5[i].fill((200,200,200))
                    surface.blit(self.checkBoxes5[i], (surface.get_width()//2-self.checkBoxes5[i].get_width()//2, surface.get_height()//2-self.checkBoxes5[i].get_height()//2))
                self.scrollInter5.blit(surface, (222,1+40*i))
            self.scrollWindow5.blit(self.scrollInter5, (0,self.scroll))
            self.image.blit(self.scrollWindow5, (359.5,110))
            self.cancelOkUpdate()

    def scrolled(self, button):
        if self.image == SelectionMenu2.images[1]:
            if self.scrollWindow1.get_rect(center=(540,360)).collidepoint(pygame.mouse.get_pos()):
                self.scroll = scrollSurface(self.scroll, self.scrollWindow1, self.scrollInter1, button)
        elif self.image == SelectionMenu2.images[3]:
            if self.scrollWindow3.get_rect(center=(540,350)).collidepoint(pygame.mouse.get_pos()):
                self.scroll = scrollSurface(self.scroll, self.scrollWindow3, self.scrollInter3, button)
        elif self.image == SelectionMenu2.images[4]:
            if self.scrollWindow4.get_rect(center=(540,350)).collidepoint(pygame.mouse.get_pos()):
                self.scroll = scrollSurface(self.scroll, self.scrollWindow4, self.scrollInter4, button)
        elif self.image == SelectionMenu2.images[5]:
            if self.scrollWindow5.get_rect(center=(540,350)).collidepoint(pygame.mouse.get_pos()):
                self.scroll = scrollSurface(self.scroll, self.scrollWindow5, self.scrollInter5, button)

    def cancelOkClicked(self):
        if self.cancel.get_rect(center=(120,580)).collidepoint(pygame.mouse.get_pos()):
            self.image = self.images[0]
        if self.ok.get_rect(center=(960,580)).collidepoint(pygame.mouse.get_pos()):
            if self.image == SelectionMenu2.images[2] and (not self.checkError2(self.sideListCopy[self.side][0]) or not self.checkError2(self.sideListCopy[self.side][1])):
                return
            for i in range(2):
                if self.sideListCopy[self.side][i] != None:
                    self.sideList[self.side][i] = self.sideListCopy[self.side][i].copy(self.sideListCopy[self.side][i].name.title())
                if self.image == SelectionMenu2.images[1]:
                    autoSelect(self.sideList[self.side][i])
            self.image = self.images[0]

    def cancelOkUpdate(self):
        if self.cancel.get_rect(center=(120,580)).collidepoint(pygame.mouse.get_pos()):
            self.cancel.fill((50,50,50))
            centerText(self.cancel, 'Cancel', 'timesnewroman', 22, (255,255,255), True)
            self.image.blit(self.cancel, (70-self.cancel.get_rect().width//2,530-self.cancel.get_rect().height//2))
        else:
            self.cancel.fill((0,0,0))
            centerText(self.cancel, 'Cancel', 'timesnewroman', 20, (255,255,255), True)
            self.image.blit(self.cancel, (70-self.cancel.get_rect().width//2,530-self.cancel.get_rect().height//2))
        if self.ok.get_rect(center=(960,580)).collidepoint(pygame.mouse.get_pos()):
            self.ok.fill((50,50,50))
            centerText(self.ok, 'OK', 'timesnewroman', 22, (255,255,255), True)
            self.image.blit(self.ok, (910-self.ok.get_rect().width//2,530-self.ok.get_rect().height//2))
        else:
            self.ok.fill((0,0,0))
            centerText(self.ok, 'OK', 'timesnewroman', 20, (255,255,255), True)
            self.image.blit(self.ok, (910-self.ok.get_rect().width//2,530-self.ok.get_rect().height//2))

    def smallUpdate(self, number):
        self.image.fill((255,255,255))
        surface = pygame.Surface((980,80)).convert_alpha()
        surface.fill((255,255,255))
        centerText(surface, 'Player '+str(self.side+1)+': '+self.texts[number-1], 'timesnewroman', 50, self.colors[self.side], True)
        self.image.blit(surface, (0,0))
        pygame.draw.line(self.image, self.colors[self.side], (0,80), (980,80), 5)
    
    def checkError1(self, side, item): # checks if player has selected two champions before moving on
        if item != 0:
            if self.sideList[side][0] == None or self.sideList[side][1] == None:
                return False
        return True

    def checkError2(self, champion): # checks if player has entered valid LoEs for the champion
        if sum(champion.levelOfExpertise) > 510:
            ErrorWindow('Total LoE should not exceed 510.')
            return False
        for i in champion.levelOfExpertise:
            if i > 255:
                ErrorWindow('Single LoE should not exceed 255.')
                return False
        return True

    def checkContinue(self):
        for i in range(2):
            if self.sideList[i][0] == None or self.sideList[i][1] == None:
                return [('P'+str(i+1)+': Please select 2 champions.', False)]
        return []

    def doContinue(self):
        battlegroup.empty()
        print(self.sideList[0][0].name, self.sideList[0][1].name, self.sideList[1][0].name, self.sideList[1][1].name)
        for i in range(2):
            sideList[i] = [self.sideList[i][0], self.sideList[i][1]]
            for j in range(2):
                self.sideList[i][j].id = str(i)+chr(65+j)
                champIdDict.update({self.sideList[i][j].id: self.sideList[i][j]})
                self.sideList[i][j].side = i
                self.sideList[i][j].position = j
                self.sideList[i][j].opponent = self.sideList[1-i][j]
                self.sideList[i][j].teammate = self.sideList[i][1-j]
                self.sideList[i][j].oppoTeammate = self.sideList[1-i][1-j]
                self.sideList[i][j].image = pygame.transform.scale(self.sideList[i][j].image, (216,154))
                self.sideList[i][j].rect = self.sideList[i][j].image.get_rect()
                self.sideList[i][j].battlePosition = [216+i*648,490-280*j]
                self.sideList[i][j].stats = self.sideList[i][j].determineStats()
                titleStats(self.sideList[i][j])
                self.sideList[i][j].hp = self.sideList[i][j].stats[5]
                battlegroup.add(self.sideList[i][j])
                self.sideList[i][j]._layer = 4
                print('P'+str(i+1)+': '+self.sideList[i][j].name.title(),'\n',' Stats: ',self.sideList[i][j].stats,'\n',' Special trait: ',self.sideList[i][j].specialTrait,
                      '\n',' Stat boosters: ',self.sideList[i][j].statBooster1,self.sideList[i][j].statBooster2,'\n',' Title: ',self.sideList[i][j].title,'\n',sep='')
                self.sideList[i][j].champInfo = ChampionInfo(i, j)
                moveStep[i][j] = 0
        print()
        sideList[1][0].image = pygame.transform.flip(sideList[1][0].image, 1, 0)
        sideList[1][1].image = pygame.transform.flip(sideList[1][1].image, 1, 0)
        for i in range(5):
            MoveBoxes(sideList[0][0].moves[i], sideList[0][1].moves[i], sideList[1][0].moves[i], sideList[1][1].moves[i], i)
        doubles[0] = True
        phase[0] = 0
        turn[0] = 0
        environment[0] = None
        ShowTurn()
        ShowEnvironment()
        otherBattleSprites.append(SpecialEffects())
        for i in selectgroup:
            i.kill()
        return 3


class MoveBoxes(pygame.sprite.DirtySprite):
    '''click this button to select a move'''
    def __init__(self, move1, move2, move3, move4, moveNumber):
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.doubles = move2 and move4
        self.champList = [sideList[0][0], sideList[1][0]]
        self.moves = [move1, move3]
        self.moveBoxImages = [[],[]]
        if self.doubles:
            self.champList.insert(1, sideList[0][1])
            self.champList.append(sideList[1][1])
            self.moves.insert(1, move2)
            self.moves.append(move4)
            self.moveBoxImages.append([])
            self.moveBoxImages.append([])
        self.scrollWindows = []
        self.scrollInters = []
        for i in range(3):
            for j in range(len(self.champList)):
                if j+1 <= len(self.moves)//2:
                    side = 0
                else:
                    side = 1
                self.images(i, self.moves[j], self.moveBoxImages[j], side)
        self.image = self.moveBoxImages[0][0]
        self.rect = self.image.get_rect()
        self.rect.center = (108+moveNumber*216,648)
        self.scroll = 0

    def images(self, number, move, moveList, side):
        moveList.append(pygame.Surface((216,144)).convert_alpha())
        moveList[-1].fill((255,255,255))
        if number != 2:
            surface = pygame.Surface((212,136)).convert_alpha()
            surface.fill(((255-number*155)*(1-side),0,(255-number*155)*side))
            centerParagraph(False, surface, move[0][0], 'timesnewroman', 30, (255,255,255), True)
            moveList[-1].blit(surface, (2,4))
        else:
            paragraph = moveDescription(move)
            self.scrollWindows.append(pygame.Surface((212,136)).convert_alpha())
            self.scrollInters.append(pygame.Surface((212,(len(paragraph)//10+1)*18+20)).convert_alpha())
            self.scrollInters[-1].fill((255*(1-side),0,255*side))
            centerParagraph(True, self.scrollInters[-1], paragraph, 'timesnewroman', 18, (255,255,255), True)

    def clicked(self):
        if phase[0] == 1:
            for i in range(len(self.champList)):
                if self.image in self.moveBoxImages[i] and not self.champList[i].phaseFinished:
                    self.champList[i].moveRecord.append(self.moves[i])
                    if not self.doubles:
                        self.champList[i].target = self.champList[i].opponent
                    elif self.moves[i] in self.champList[i].targetMoves:
                        self.champList[i].playerTargeting = True
                        PlayerTargetSurface(self.champList[i])
                    self.champList[i].playerSelecting = True

    def update(self, seconds):
        if phase[0] == 1:
            for i in range(len(self.champList)):
                if not self.champList[i].phaseFinished:
                    number = i
                    break
                if i == len(self.champList)-1:
                    return
            if self.champList[number].playerSelecting:
                self.image = self.moveBoxImages[number][1]
            else:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image = self.moveBoxImages[number][2]
                    self.scrollWindows[number].blit(self.scrollInters[i], (0,self.scroll))
                    self.image.blit(self.scrollWindows[number], (2,4))
                else:
                    self.image = self.moveBoxImages[number][0]
        else:
            self.image = self.moveBoxImages[-1][1]

    def scrolled(self, button):
        for i in range(len(self.champList)):
            if self.image == self.moveBoxImages[i][2]:
                self.scroll = scrollSurface(self.scroll, self.scrollWindows[i], self.scrollInters[i], button)


class ChampionInfo(pygame.sprite.DirtySprite):
    '''displays champion info while in battle'''
    def __init__(self, side, position=None): # stat enhancement/status effects/turn effects/special buffs and ALL be like abilitiesSurface2!
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.side = side
        if position != None:
            self.champ = sideList[side][position]
            self.position = position
        else:
            self.champ = sideList[side][0]
            self.position = 1
        self.color = (255*(1-side),0,255*side)
        self.image = pygame.Surface((130,92)).convert_alpha()
        self.image.fill((255,255,255))
        self.typeSurface, self.nameSurface, self.abilitiesSurface1 = pygame.Surface((126,28)).convert_alpha(), pygame.Surface((126,28)).convert_alpha(), pygame.Surface((126,28)).convert_alpha()
        self.height = (len(self.champ.abilities)//18+1)*18+20
        self.typeSurface.fill(self.color)
        self.nameSurface.fill(self.color)
        self.abilitiesSurface1.fill(self.color)
        self.champType = copy.deepcopy(self.champ.type)
        typestr = ''
        for i in self.champType:
            typestr = typestr+i+','
        centerText(self.typeSurface, typestr[:-1], 'timesnewroman', 15, (0,0,0))
        centerText(self.nameSurface, self.champ.name.title(), 'timesnewroman', 20, (255,255,255), True)
        centerText(self.abilitiesSurface1, 'Abilities', 'timesnewroman', 15, (0,0,0))
        self.image.blit(self.typeSurface, (2,2))
        self.image.blit(self.nameSurface, (2,32))
        self.image.blit(self.abilitiesSurface1, (2,62))
        self.rect = self.image.get_rect()
        self.rect.center = (65+side*950,80+(1-self.position)*280)
        self.setInfoSprites()

    def setInfoSprites(self):
        self.abilitiesSurface2 = AbilitiesSurface2(self.champ, self.height, self.color, 1-self.position)
        self.healthBar = HealthBar(self.champ, 1-self.position)
        self.specialBuffsBox = OtherInfoBox(self.side, self.champ.specialBuffs, 'special buffs box.png', (280+self.side*520, 40+(1-self.position)*280))
        self.statusEffectsBox = OtherInfoBox(self.side, self.champ.statusEffects, 'status effects box.png', (160+self.side*760, 120+(1-self.position)*280))
        self.statsEBox = OtherInfoBox(self.side, self.champ.statsER, 'statsE box.png', (200+self.side*680, 120+(1-self.position)*280))
        self.statsRBox = OtherInfoBox(self.side, self.champ.statsER, 'statsR box.png', (240+self.side*600, 120+(1-self.position)*280))
        self.turnEffectsBox = OtherInfoBox(self.side, self.champ.turnEffects, 'turn effects box.png', (280+self.side*520, 120+(1-self.position)*280))
        self.timeEffectsBox = OtherInfoBox(self.side, self.champ.timeEffects, 'time effects box.png', (320+self.side*440, 120+(1-self.position)*280))
        self.entireBattleEffectsBox = OtherInfoBox(self.side, self.champ.entireBattleEffects, 'entire battle effects box.png', (360+self.side*360, 120+(1-self.position)*280))
        self.shieldBox = OtherInfoBox(self.side, self.champ.shield, 'shield box.png', (400+self.side*280, 120+(1-self.position)*280))

    def killingSpree(self):
        self.healthBar.healthNumber.kill()
        self.specialBuffsBox.kill()
        self.statusEffectsBox.kill()
        self.statsEBox.kill()
        self.statsRBox.kill()
        self.turnEffectsBox.kill()
        self.timeEffectsBox.kill()
        self.entireBattleEffectsBox.kill()
        self.shieldBox.kill()

    def update(self, seconds):
        self.statsEBox.attribute = self.champ.statsER
        self.statsRBox.attribute = self.champ.statsER
        self.entireBattleEffectsBox.attribute = self.champ.entireBattleEffects
        self.shieldBox.attribute = self.champ.shield
        # type
        if self.champType != self.champ.type:
            self.champType = copy.deepcopy(self.champ.type)
            self.typeSurface.fill(self.color)
            typestr = ''
            for i in self.champType:
                typestr = typestr+i+','
            centerText(self.typeSurface, typestr[:-1], 'timesnewroman', 15, (0,0,0))
            self.image.blit(self.typeSurface, (2,2))
        # abilities
        if self.abilitiesSurface1.get_rect(center=(65+self.side*950,110+(1-self.position)*280)).collidepoint(pygame.mouse.get_pos()):
            if not self.abilitiesSurface2 in battlegroup:
                battlegroup.add(self.abilitiesSurface2)
                battlegroup.move_to_front(self.abilitiesSurface2)
        else:
            if self.abilitiesSurface2 in battlegroup:
                battlegroup.remove(self.abilitiesSurface2)
        # special buffs
        if self.specialBuffsBox.changed:
            paragraph = ''
            for i in self.champ.specialBuffs:
                for j in self.champ.specialBuffsDescription:
                    if j[0] == i:
                        description = j[1]
                duration = '['+str(self.champ.specialBuffs[i])+']'
                paragraph = paragraph+i+' '+duration+': '+description+'\n'
            championInfoSurface(True, paragraph, self.specialBuffsBox.surface, self.color)
            if len(self.champ.specialBuffs) > 0:
                if not self.specialBuffsBox in battlegroup:
                    battlegroup.add(self.specialBuffsBox)
            else:
                if self.specialBuffsBox in battlegroup:
                    battlegroup.remove(self.specialBuffsBox)
                if self.specialBuffsBox.surface in battlegroup:
                    battlegroup.remove(self.specialBuffsBox.surface)
        # status effects
        if self.statusEffectsBox.changed:
            paragraph = ''
            for i in self.champ.statusEffects:
                description = statusEffectsDescription[i]
                duration = '['+str(self.champ.statusEffects[i])+']'
                paragraph = paragraph+i.title()+' '+duration+': '+description+'\n'
            championInfoSurface(False, paragraph, self.statusEffectsBox.surface, self.color, True)
            if len(self.champ.statusEffects) > 0:
                if not self.statusEffectsBox in battlegroup:
                    battlegroup.add(self.statusEffectsBox)
            else:
                if self.statusEffectsBox in battlegroup:
                    battlegroup.remove(self.statusEffectsBox)
                if self.statusEffectsBox.surface in battlegroup:
                    battlegroup.remove(self.statusEffectsBox.surface)
        # stats ER
        if self.statsEBox.changed:
            paragraphE, paragraphR = '', ''
            for i in range(len(self.champ.statsER)):
                if self.champ.statsER[i] > 0:
                    paragraphE = paragraphE+statERTypes[i]+': +'+str(self.champ.statsER[i])+'\n'
                elif self.champ.statsER[i] < 0:
                    paragraphR = paragraphR+statERTypes[i]+': '+str(self.champ.statsER[i])+'\n'
            if paragraphE != '':
                if not self.statsEBox in battlegroup:
                    battlegroup.add(self.statsEBox)
            else:
                if self.statsEBox in battlegroup:
                    battlegroup.remove(self.statsEBox)
                if self.statsEBox.surface in battlegroup:
                    battlegroup.remove(self.statsEBox.surface)
            if paragraphR != '':
                if not self.statsRBox in battlegroup:
                    battlegroup.add(self.statsRBox)
            else:
                if self.statsRBox in battlegroup:
                    battlegroup.remove(self.statsRBox)
                if self.statsRBox.surface in battlegroup:
                    battlegroup.remove(self.statsRBox.surface)
            championInfoSurface(False, paragraphE, self.statsEBox.surface, self.color, True)
            championInfoSurface(False, paragraphR, self.statsRBox.surface, self.color, True)
        # turn effects
        if self.turnEffectsBox.changed:
            paragraph = ''
            for i in self.champ.turnEffects:
                description = i
                if self.champ.turnEffects[i] < 0:
                    duration = '[next '+str(-1*self.champ.turnEffects[i])+']'
                else:
                    duration = '['+str(self.champ.turnEffects[i])+']'
                paragraph = paragraph+description+' '+duration+'\n'
            championInfoSurface(True, paragraph, self.turnEffectsBox.surface, self.color, True)
            if len(self.champ.turnEffects) > 0:
                if not self.turnEffectsBox in battlegroup:
                    battlegroup.add(self.turnEffectsBox)
            else:
                if self.turnEffectsBox in battlegroup:
                    battlegroup.remove(self.turnEffectsBox)
                if self.turnEffectsBox.surface in battlegroup:
                    battlegroup.remove(self.turnEffectsBox.surface)
        # time effects
        if self.timeEffectsBox.changed:
            paragraph = ''
            for i in self.champ.timeEffects:
                description = i
                duration = '['+str(self.champ.timeEffects[i])+' time]'
                if self.champ.timeEffects[i] > 1:
                    duration = duration[:-1]+'s]'
                paragraph = paragraph+description+' '+duration+'\n'
            championInfoSurface(True, paragraph, self.timeEffectsBox.surface, self.color, True)
            if len(self.champ.timeEffects) > 0:
                if not self.timeEffectsBox in battlegroup:
                    battlegroup.add(self.timeEffectsBox)
            else:
                if self.timeEffectsBox in battlegroup:
                    battlegroup.remove(self.timeEffectsBox)
                if self.timeEffectsBox.surface in battlegroup:
                    battlegroup.remove(self.timeEffectsBox.surface)
        # entire battle effects
        if self.entireBattleEffectsBox.changed:
            paragraph = ''
            for i in self.champ.entireBattleEffects:
                description = i
                paragraph = paragraph+description+'\n'
            championInfoSurface(True, paragraph, self.entireBattleEffectsBox.surface, self.color, True)
            if len(self.champ.entireBattleEffects) > 0:
                if not self.entireBattleEffectsBox in battlegroup:
                    battlegroup.add(self.entireBattleEffectsBox)
            else:
                if self.entireBattleEffectsBox in battlegroup:
                    battlegroup.remove(self.entireBattleEffectsBox)
                if self.entireBattleEffectsBox.surface in battlegroup:
                    battlegroup.remove(self.entireBattleEffectsBox.surface)
        # shield
        if self.shieldBox.changed:
            championInfoSurface(False, 'Shield: '+str(self.champ.shield), self.shieldBox.surface, self.color, True)
            if self.champ.shield > 0:
                if not self.shieldBox in battlegroup:
                    battlegroup.add(self.shieldBox)
            else:
                if self.shieldBox in battlegroup:
                    battlegroup.remove(self.shieldBox)
                if self.shieldBox.surface in battlegroup:
                    battlegroup.remove(self.shieldBox.surface)


class AbilitiesSurface2(pygame.sprite.DirtySprite):
    '''displays abilities of a champion'''
    def __init__(self, champ, height, color, position):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((324,height)).convert_alpha()
        self.image.fill((255,255,255))
        self.abilitiesSurface = pygame.Surface((316,height-8)).convert_alpha()
        self.abilitiesSurface.fill(color)
        centerParagraph(False, self.abilitiesSurface, champ.abilities, 'timesnewroman', 18, (255,255,255))
        self.image.blit(self.abilitiesSurface, (4,4))
        self.rect = self.image.get_rect()
        self.rect.center = (162+champ.side*756,126+height//2+position*280)
        

class HealthBar(pygame.sprite.DirtySprite):
    '''displays hp of a champion'''
    def __init__(self, champ, position):
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.champ = champ
        self.side = champ.side
        self.image = pygame.Surface((380,40)).convert_alpha()
        self.image.fill((0,0,0))
        self.maxhp = self.champ.stats[5]
        self.hp = self.champ.hp
        self.percentage = self.hp/self.maxhp
        pygame.draw.rect(self.image, (0,255,0), (0,0,self.percentage*380,40))
        self.rect = self.image.get_rect()
        self.rect.center = (320+self.side*440,80+position*280)
        self.healthNumber = HealthNumber(self.side, self.maxhp, self.hp, position)
        self.position = position

    def update(self, seconds):
        if self.hp != self.champ.hp or self.maxhp != self.champ.stats[5]:
            self.hp = self.champ.hp
            self.maxhp = self.champ.stats[5]
            self.image.fill((0,0,0))
            self.percentage = max(self.hp, 0)/self.maxhp
            pygame.draw.rect(self.image, (min(round((-1020*self.percentage+1020)), 255),min(round(340*self.percentage), 255),0), (self.side*(380-self.percentage*380),0,self.percentage*380,40))
            self.healthNumber.hp = self.hp
            self.healthNumber.text = str(self.healthNumber.hp)+'/'+str(self.maxhp)
            self.healthNumber.image = pygame.Surface((12.5*len(self.healthNumber.text)+2,30))
            self.healthNumber.image.set_colorkey((0,0,0))
            centerText(self.healthNumber.image, self.healthNumber.text, 'timesnewroman', 25, self.healthNumber.color, True)
            self.healthNumber.rect = self.healthNumber.image.get_rect()
            self.healthNumber.rect.center = (140+self.healthNumber.image.get_width()//2+self.side*(800-2*self.healthNumber.image.get_width()//2),40+self.position*280)


class HealthNumber(pygame.sprite.DirtySprite):
    '''displays hp of a champion'''
    def __init__(self, side, maxhp, hp, position):
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.side = side
        self.maxhp = maxhp
        self.hp = hp
        self.text = str(self.hp)+'/'+str(self.maxhp)
        self.color = ((1-side)*255,0,side*255)
        self.image = pygame.Surface((12.5*len(self.text)+2,30))
        self.image.set_colorkey((0,0,0))
        centerText(self.image, self.text, 'timesnewroman', 25, self.color, True)
        self.rect = self.image.get_rect()
        self.rect.center = (140+self.image.get_width()//2+side*(800-2*self.image.get_width()//2),40+position*280)


class OtherInfoBox(pygame.sprite.DirtySprite):
    '''displays info like stats enhancement'''
    def __init__(self, side, attribute, file, position):
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.side = side
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('images','other images',file)), (30,30)).convert_alpha()
        self.attribute = attribute
        self.attributeCopy = copy.deepcopy(attribute)
        self.changed = True
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.surface = OtherInfoSurface(side, self.rect.center)

    def ownUpdate(self):
        if self.attributeCopy == self.attribute:
            if self.changed:
                self.changed = False
        else:
            self.attributeCopy = copy.deepcopy(self.attribute)
            if not self.changed:
                self.changed = True

    def update(self, seconds):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.surface in battlegroup:
                battlegroup.add(self.surface)
                battlegroup.move_to_front(self.surface)
        else:
            if self.surface in battlegroup:
                battlegroup.remove(self.surface)


class OtherInfoSurface(pygame.sprite.DirtySprite):
    '''just a surface'''
    def __init__(self, side, position):
        pygame.sprite.DirtySprite.__init__(self)
        self.left = position[0]-side*324-(-2*side+1)*15
        self.top = position[1]+15


class ShowTurn(pygame.sprite.DirtySprite):
    '''displays turn in battle'''
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.turn = turn[0]
        self.text = 'Turn: '+str(self.turn)
        self.image = pygame.Surface((100,20)).convert_alpha()
        self.image.fill((255,255,255))
        centerText(self.image, self.text, 'timesnewroman', 18, (0,0,0), True)
        self.rect = self.image.get_rect()
        self.rect.center = (540,30)

    def update(self, seconds):
        if self.turn != turn[0]:
            self.turn = turn[0]
            self.text = 'Turn: '+str(self.turn)
            self.image.fill((255,255,255))
            centerText(self.image, self.text, 'timesnewroman', 18, (0,0,0), True)


class ShowEnvironment(pygame.sprite.DirtySprite):
    '''displays environment in battle'''
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.currentEnvironment = environment[0]
        self.text = 'Enviro: '+str(self.currentEnvironment)
        self.image = pygame.Surface((200,20)).convert_alpha()
        self.image.fill((0,0,0))
        centerText(self.image, self.text, 'timesnewroman', 18, (255,255,255), True)
        self.rect = self.image.get_rect()
        self.rect.center = (540,10)

    def update(self, seconds):
        if self.currentEnvironment != environment[0]:
            self.currentEnvironment = environment[0]
            self.text = 'Enviro: '+str(self.currentEnvironment)
            self.image.fill((0,0,0))
            centerText(self.image, self.text, 'timesnewroman', 18, (255,255,255), True)


class SpecialEffects(pygame.sprite.DirtySprite):
    '''displays special attack graphics effect'''
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((1080,720))
        self.image.set_colorkey((0,0,0))
        self.color = (255,255,255)
        self.position = [540,360]
        self.specialType = None
        self.side = 0
        self.effectDone = False
        self.rect = self.image.get_rect()
        self.rect.center = (540,360)
        self.teamDamage = False

    def setup(self, champ, specialType, color):
        self.effectDone = False
        self.teamDamage = False
        self.champ = champ
        battlegroup.add(self)
        battlegroup.move_to_front(self)
        self.specialType = specialType
        self.color = color
        self.side = champ.side
        self.position[0] = 216+self.side*648
        self.doubles = doubles[0]
        if self.doubles:
            self.position[1] = 490-champ.position*280
            if not champ.target:
                self.teamDamage = True
        else:
            self.position[1] = 360

    def update(self, seconds):
        if self.specialType == 'special ray':
            if self.position[0] != 216+(1-self.side)*648:
                self.position[0] += 12*(-2*self.side+1)
                self.ray = pygame.Surface((100,80)).convert_alpha()
                self.ray.fill((self.color))
                if self.doubles:
                    if self.teamDamage:
                        self.position[1] += 5*(2*self.champ.position-1)
                        self.ray2 = pygame.Surface((100,80)).convert_alpha()
                        self.ray2.fill((self.color))
                        self.image.blit(self.ray2, (self.position[0]-50,490-self.champ.position*280-40))
                    else:
                        self.position[1] += 5*(self.champ.position-self.champ.target.position)
                self.image.blit(self.ray, (self.position[0]-50,self.position[1]-40))
            else:
                self.image.fill((0,0,0))
                self.effectDone = True
                self.specialType = None
                self.side = 0


class EndBattleWindow(pygame.sprite.Sprite):
    '''displays result of the battle'''
    def __init__(self, winner):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((360,200)).convert_alpha()
        pygame.draw.rect(self.image, (255,255,255), (2,2,356,196))
        self.ok = pygame.Surface((120,40)).convert_alpha()
        self.rect = self.image.get_rect(center=(540,360))
        centerText(self.image, winner+' won!', 'timesnewroman', 20, (0,0,0), True)
        battleResultReport(winner)

    def clicked(self):
        if self.ok.get_rect(center=(540,430)).collidepoint(pygame.mouse.get_pos()):
            mainArray[2] = False
            mainArray[3] = False
            mainArray[0] = True
            for i in battlegroup:
                i.kill()
            background = backgroundImages[0].copy()
            background.blit(text('Simulation', 'timesnewroman', 100, (255,255,255), True), (75,100))
            return background

    def update(self, seconds):
        if self.ok.get_rect(center=(540,430)).collidepoint(pygame.mouse.get_pos()):
            self.ok.fill((50,50,50))
            centerText(self.ok, 'OK', 'timesnewroman', 22, (255,255,255), True)
            self.image.blit(self.ok, (180-self.ok.get_rect().width//2,170-self.ok.get_rect().height//2))
        else:
            self.ok.fill((0,0,0))
            centerText(self.ok, 'OK', 'timesnewroman', 20, (255,255,255), True)
            self.image.blit(self.ok, (180-self.ok.get_rect().width//2,170-self.ok.get_rect().height//2))
        

# assign groups
ErrorWindow.groups = errorgroup
EndBattleWindow.groups = errorgroup

V1Button.groups = menugroup
V2Button.groups = menugroup
V6Button.groups = menugroup
ShopButton.groups = menugroup
MyChampionsButton.groups = menugroup
RulebookButton.groups = menugroup
    
BackButton.groups = selectgroup
ContinueButton.groups = selectgroup
SelectionMenu.groups = selectgroup
SelectionMenu2.groups = selectgroup

MoveBoxes.groups = battlegroup, moveBoxes
ChampionInfo.groups = battlegroup
HealthBar.groups = battlegroup
HealthNumber.groups = battlegroup
ShowTurn.groups = battlegroup
ShowEnvironment.groups = battlegroup

OtherInfoBox.groups = infogroup

# assign layers
ChampionInfo._layer = 6
MoveBoxes._layer = 1

# sprites for menu
V1Button()
V2Button()
V6Button()
ShopButton()
MyChampionsButton()
RulebookButton()

