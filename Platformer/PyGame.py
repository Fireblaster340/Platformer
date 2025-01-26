import os
import random
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import OptionMenu, StringVar
from tkinter import Listbox, END,RIGHT
#All imports
showinfo("Welcome","Welcome to my platformer! You are the small and slightly gray block. Use arrow keys to move around the screen. Press Space/Up arrow to jump. IMPORTANT: Colliding with the bottom of a block allows you to stick to it if you hold space/up arrow. Press P to pause the game and P again to resume. Press E to open the editor where you can navigate via the arrow keys. Place blocks by clicking. Press P to playtest your level. Your goal is to reach the green blocks. Enjoy.")
os.system('clear')
try:
    import pyperclip
    print("Importing pyperclip now...")
except ModuleNotFoundError:
    print("Installing pyperclip now...")
    os.system('pip3 install pyperclip')
    import pyperclip
#Automatic pip command to install pyperclip (Copy paste library)
try:
    import pygame
    print("Importing pygame now...")
except ModuleNotFoundError:
    print("Installing pygame now...")
    os.system('pip3 install pygame')
#Automatic pip command to install pygame (Game engine)
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    K_SPACE,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_p,
    K_e,
    K_c,
    K_r,
    MOUSEBUTTONDOWN,
    BUTTON_LEFT
)
from pygame.mouse import *
#Pygame controls

CodeStored = None
#Function to get savecode entered
def GetNameEntered(Entry:object):
    global root2, NameSaved, Quit
    Quit = False
    NameSaved = Entry.get()
    if NameSaved == "":
        NameSaved = "Unnamed Stage"
    root2.destroy()
def GetCodeEntered(Entry:object):
    global CodeStored, Quit, root2, NameSaved
    try:
        CodeStored = int(Entry.get())
        NameSaved = "Unnamed Stage Remix"
    except ValueError:
        if Entry.get() == "":
            CodeStored = 0
            Quit = True
            root.destroy()
            root2 = tk.Tk()
            root2.title("Enter Your Stage Name")
            root2.geometry("300x120")
            LName = tk.Entry(root2)
            LName.pack(padx=0,pady=10)
            root2.bind("<Return>",lambda e:GetNameEntered(LName))
            tk.Button(root2,command=lambda:GetNameEntered(LName),text="Select Name",height=2).pack(padx=0,pady=10)
            root2.mainloop()
            if Quit:
                quit()
            return None
        showinfo("Error!","You didn't enter an integer value")
        CodeStored = None
        return None
    if float(len(str(CodeStored))/10) != float(len(str(CodeStored))//10):
        showinfo("Error!","You didn't enter a valid savecode")
        CodeStored = None
        return None
    root.destroy()
#Function to get data from dropdown box
def DropCodeEntered():
    global LvlIndexed, CodeStored, root, NameSaved
    if "Save" in LvlIndexed.get():
        file = open("StageNames.txt","r")
        List = AllLevelsSaved
    else:
        file = open("MyStageNames.txt","r")
        List = MyLevels
    Names = []
    for k in file.readlines():
        Names.append(k[:-1])

    if LvlIndexed.get() != "":
        CodeStored = List[0][List[1].index(LvlIndexed.get())]
        NameSaved = Names[List[1].index(LvlIndexed.get())]+" remix"
        file.close()
        root.destroy()
root = tk.Tk()
AllLevelsSaved = [[],[]]
MyLevels = [[],[]]
#Checking if file is there
try:
    file = open("SavedStages.txt","r")
except FileNotFoundError:
    showinfo("File Error","SavedStages.txt was not found")
    quit()

try:
    file2 = open("CoolStages.txt","r")
except FileNotFoundError:
    showinfo("File Error","CoolStages.txt was not found, enjoy playing without my levels :(")
k=0
#Parsing your saved levels
for item in file.readlines():
    k+=1
    item = item[:-1]
    AllLevelsSaved[0].append(item)
    AllLevelsSaved[1].append("Save "+str(k))

#Parsing my levels
k=0
for item in file2.readlines():
    k+=1
    item = item[:-1]
    MyLevels[0].append(item)
    MyLevels[1].append("Level "+str(k))
#Entering level info and initialisation
LvlIndexed = StringVar()
root.title("Welcome!")
root.geometry("720x350")
root.resizable(False,False)
file = open("StageNames.txt","r")
SText = Listbox(root,height=100,width=30)
SText.insert(0,"Saved Stage Names:")
SText.insert(1,"")
k = 0
for item in file.readlines():
    k+=1
    SText.insert(END,"Save "+str(k)+": "+item[:-1])
SText.insert(END,"")
SText.insert(END,"My Level Names:")
SText.insert(END,"")

file = open("MyStageNames.txt","r")
k = 0
for item in file.readlines():
    k+=1
    SText.insert(END,"Level "+str(k)+": "+item[:-1])
SText.pack(padx=0,pady=0,side=RIGHT)

tk.Label(root, text="Enter save code and hit return. Leave empty for fresh stage").pack(padx=0,pady=20)
CodeEntry = tk.Entry(root)
CodeEntry.pack(padx=0,pady=0)
SBar = tk.Scrollbar(root)
if len(AllLevelsSaved) !=0:
    tk.Label(root, text="Alternatively, select a level from the drop down and press the button").pack(padx=0,pady=10)
    OptionMenu(root, LvlIndexed, *AllLevelsSaved[1]).pack(padx=0,pady=10)
    LvlIndexed.set("")
if len(MyLevels) != 0:
    tk.Label(root, text="You can also play my levels!").pack(padx=0,pady=10)
    OptionMenu(root,LvlIndexed, *MyLevels[1]).pack(padx=0,pady=10)
if len(MyLevels) != 0 and len(AllLevelsSaved) != 0:
    tk.Button(root,text="Select Level",height=2,command=lambda:DropCodeEntered(),background="dark gray").pack(padx=0,pady=15)
root.bind("<Return>",lambda e:GetCodeEntered(CodeEntry))
SBar.config(command=SText.yview)
tk.Button(root,text="?",height=1,width=1,command=lambda:showinfo("Help menu","Space/Up arrow to jump and Arrow keys to move. You can edit levels with E. Press the X button or press Escape to close the game. Before closing, the game prompts you to save the level to your file. You don't have to but you can save if you'd like. I will be saying the word 'Traverse' a lot. It means sticking to the bottom of a block and holding to get a jump boost. All block types: Black (Simple platform with traverse), Red (Kills you), Delete (Deletes block), Finish (Colliding with this completes the stage), Invisible (Black but invisible), False Red (Behaves like black), Non Traversable (Black but you cannot traverse), Breakable (Breaks on contact, you can still jump off it and traverse it), Ice (Black block with less deceleration), False Finish (Finish but kills you), Black & Red Passables (Both are purely for decoration and do not do anything upon collision).")).place(x=10,y=315)
root.mainloop()
#Nothing entered
if CodeStored is None:
    quit()
#Initialize pygame modules
pygame.init()
Iterations = 0
AllLocs = ""
Win = False
screen = pygame.display.set_mode((1500,1000))
#Player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #Surface
        self.surface = pygame.Surface((70,70))
        #Rect
        self.rect = self.surface.get_rect(center=(50,700))
        #Filling surface, grayish
        self.surface.fill((50,50,50))
        #XVelo & YVelo start at 0
        self.YVelo = 0
        self.XVelo = 0
        #Not able to jump
        self.colliding = False
        #Boost YVelo, traversing adds to this
        self.YVeloB = 0
        #Can traverse under a block
        self.traverse = True
        #Deceleration
        self.decell = 0.7
    def update(self,keys):
        global running
        #Falling down, terminal speed = 60
        if self.YVelo < 60:
            self.YVelo+=1
        #Right press
        if keys[K_RIGHT]:
            #Not colliding with wall
            if self.rect.left < 1375:
                #XVelo below terminal
                if self.XVelo < 30:
                    #Accelerate
                    self.XVelo+=6
            else:
                #If colliding, reset position
                self.rect.x = 1375
        #Left press
        if keys[K_LEFT]:
            #Not colliding with other wall
            if self.rect.right > 70:
                #XVelo above minimum
                if self.XVelo > -30:
                    #Accelerate
                    self.XVelo-= 6
            else:
                #If colliding, reset position
                self.rect.right = 70
        #Decelerate player
        if abs(self.XVelo)>0:
            self.XVelo*=self.decell
        #Post all checks, move the player only on the X axis
        self.rect.move_ip(self.XVelo,0)
        #Reset values
        self.colliding = False
        self.YVeloB = 0
        #Important to prevent infinite while loop
        Iterations = 0
        self.decell = 0.7
        if pygame.sprite.spritecollideany(self,AllSprites):
            #Vertical below 
            self.collided()
            self.colliding = True
            for _ in range(8):
                if pygame.sprite.spritecollideany(self,AllSprites):
                    self.rect.y-=1
        if pygame.sprite.spritecollideany(self,AllSprites):
            #Horizontal movement
            self.collided()
            self.rect.y+=8
            self.colliding = False
            while pygame.sprite.spritecollideany(self,AllSprites):
                Iterations+=1
                if Iterations >= 500:
                    break
                self.rect.x-=self.XVelo
            self.XVelo = 0
        self.rect.move_ip(0,self.YVelo)
        Iterations = 0
        if pygame.sprite.spritecollideany(self,AllSprites):
            #Vertical above
            self.collided()
            self.colliding = True
            if self.YVelo < 0:
                self.YVeloB = 5
                if not self.traverse:
                    self.colliding = False
                #Change self.colliding to False here to disable traversing (Holding down at bottom of block)
            while pygame.sprite.spritecollideany(self,AllSprites):
                Iterations+=1
                if Iterations >= 500:
                    break
                self.rect.y-=self.YVelo
            self.YVelo = 0
        self.rect.y+=4
        if (keys[K_SPACE] or keys[K_UP]) and self.colliding:
            self.YVelo = -20-self.YVeloB
        self.rect.y-=4
    def collided(self):
        global running,Win,AllLocs,playing
        for sprite in pygame.sprite.spritecollide(self,AllSprites,False):
            #Sprite kills you
            if sprite.type in [2,10]:
                for sp in AllBlocksEver:
                    sp.reset()
                self.rect.x = 50
                self.rect.y = 600
                while pygame.sprite.spritecollideany(self, AllSprites):
                    self.rect.y-=1
                self.YVelo = 0
            #Sprite completes level
            elif sprite.type == 4:
                playing = False
                screen.blit(pygame.font.SysFont("Arial",50).render("Level complete! Press P to restart",True,"Black","White"),(300,400))
                pygame.display.flip()
                while not playing:
                    self.YVelo = 0
                    self.XVelo = 0
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                playing = True
                                running = False
                            if event.key == K_p:
                                for sp in AllBlocksEver:
                                    sp.reset()
                                playing = True
                        if event.type == QUIT:
                            playing = True
                            running = False
                self.rect.x=50
                self.rect.y=600
                while pygame.sprite.spritecollideany(self, AllSprites):
                    self.rect.y-=1
                self.YVelo = 0
            #Sprite is breakable
            elif sprite.type == 8:
                AllSprites.remove(sprite)
            #Sprite is icy
            elif sprite.type == 9:
                self.decell = 0.9
            #Sprite blocks traversal
            if sprite.type == 7:
                self.traverse = False
            else:
                #Sprite allows traversal
                self.traverse = True
#Create a block
class Block(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, h:int, w:int, type:int):
        global AllLocs, AllBlocksEver
        super(Block, self).__init__()
        #Add to all blocks ever placed
        AllBlocksEver.add(self)
        #Block type
        self.type = type
        #Surface
        self.surface = pygame.Surface((w,h))
        #Rect
        self.rect = self.surface.get_rect(center=(x,y))
        #Self string to add to save code
        self.loc = ""
        if h == 100 and w == 100:
            #Temporarily limits size to prevent ground from being added to savecode
            #Self string for savecode is set
            self.loc=str(self.rect.x+3550)+str(self.rect.y+3050)+(("0" if len(str(self.type))<2 else "")+str(self.type))
        #Set block colour
        if self.type == 0:
            self.surface.fill((0,0,0))
        else:
            try:
                self.surface.fill([(0,0,0),(255,0,0),(255,255,255),(0,255,0),(255,255,255),(255,0,0),(0,0,0),(255,230,0),(0,230,255),(0,255,0),(0,0,0),(255,0,0)][type-1])
            except IndexError:
                self.surface.fill((200,0,255))
    def reset(self):
        #Reset breakable blocks mainly. Happens after crashing or winning or resetting your character
        if not self.passable:
            AllSprites.add(self)
        else:
            BonusBlits.add(self)
    def update(self):
        #Is Passable
        if self.type in [11,12]:
            self.passable = True
            self.kill()
            BonusBlits.add(self)
        else:
            self.passable = False
running = True
build = False
#Its you! The player
P1 = Player()

#Initialising stuff ig
AllBlocksEver = pygame.sprite.Group()
AllSprites = pygame.sprite.Group()
BonusBlits = pygame.sprite.Group()
Clock = pygame.time.Clock()
#Ground
NewObj = Block(0, 800, 100, 10000,0)
AllSprites.add(NewObj)
playing = True
CodeStored = str(CodeStored)
TView = 1
#Parsing the code entered
for x in range(len(CodeStored)//10):
    AllSprites.add(Block(int(CodeStored[10*x:10*x+4])-3500,int(CodeStored[10*x+4:10*x+8])-3000,100,100,int(CodeStored[10*x+8:10*x+10])))

#Event handler
while running:
    for sprite in AllSprites:
        sprite.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_p:
                if playing:
                    playing = False
                else:
                    build = False
                    playing = True
            if event.key == K_e:
                playing = False
                build = True
            if event.key == K_RIGHT and build:
                TView+=1 if TView < 12 else 0
            if event.key == K_LEFT and build:
                TView-=1 if TView > 1 else 0
            if event.key == K_r:
                for sp in AllBlocksEver:
                    sp.reset()
                P1.rect.x = 50
                P1.rect.y = 600

        if event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT and build:
                if TView != 3:
                    NewObj = Block(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],100,100,TView)
                    AllSprites.add(NewObj)
                else:
                    for sprite in AllSprites:
                        if sprite.rect.collidepoint(pygame.mouse.get_pos()) and sprite.type != 0:
                            sprite.kill()
                    for sprite in BonusBlits:
                        if sprite.rect.collidepoint(pygame.mouse.get_pos()) and sprite.type != 0:
                            sprite.kill()
    allkeys = pygame.key.get_pressed()
    screen.fill((255,255,255))
    screen.blit(P1.surface, P1.rect)
    for sprite in AllSprites:
        screen.blit(sprite.surface,sprite.rect)
    for sprite in BonusBlits:
        screen.blit(sprite.surface,sprite.rect)
    #else:
    if playing:
        P1.update(allkeys)
    if build:
        screen.blit(pygame.font.SysFont("Arial",30).render("Block type: "+["Black","Red","Delete","Finish","Invisible","False Red","Non traversable","Breakable","Ice","False Finish","Black Passable", "Red Passable"][TView-1],True,"Black","White"),(10,10))
    pygame.display.flip()
    Clock.tick(40)
running = True
os.system('clear')
EndTxt = pygame.font.SysFont("Arial",30).render("Press C to copy save code to clipboard and save the level!",True,"White","Black")
while running:
    screen.blit(EndTxt,(600,800))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_c:
                screen.fill((255,255,255))
                EndTxt = pygame.font.SysFont("Arial",30).render("Copied to clipboard and saved!",True,"White","Black")
                for sprite in AllBlocksEver:
                    AllLocs += sprite.loc
                for sprite in BonusBlits:
                    AllLocs+= sprite.loc
                file = open("SavedStages.txt","a")
                file.writelines(AllLocs+"\n")
                file.close()
                file = open("StageNames.txt","a")
                file.writelines(NameSaved+"\n")
                file.close()
                pyperclip.copy(AllLocs)
    pygame.display.flip()

#352135563617355036353569371835793850357537763574 For some reason
#Rish lvl old save system: 40923472405835663959366247373266449533154146357240813271409032044088312440993045416332254167328241653279413832794138327941293279412732824057328340413233403532874030315640363092403030384147312941703127417030744170306241703062417030524171304541793160417531714175317341753183417532034086329241243292415632924191329240513300403733004095329641103296415332964176329642483269429932674368328044013280429131954238320642373201423732014238319842383196482832714828327148283267490032354899305647383204473732044749316247423164473931644738316447373164
#Rish lvl 2 old save system: 38573722385636583857347638563281407631624070305540813072407730694062306840993050404830394324328443223467451635643768372437163735371437273714372336383735355637413506372549193453473032444917310349143373432235644518366845083656451136574516365745213658448436994566372844653753449737573921374539613745398437813945379040043752398037393969373441073746417937464173376041573772415437024310373742763739429637634336369443903739439437054054374943173650462137564652374246793734469137044700368147323689474537224816376448803730491437554830372543883651423636214233366741483660409237144187362541463662412236694138365042133611407037104042375840193725433336374358363543643629435936284348361843373605444236734563367345533677483136384880364249003667491736904772367749103597488336013846375437993744380638213841382038823838398530063918300538813005382030133757301337193016361230163679301635483008415830274222300542933021
#New Save System: 3574367101352636810135003756013562373501360437320139583743023686373402367037200237023718023773375202384637220238953731023616375301351537780135893752023540375202362037290236673758023667379602372737990236073812023516382002402337970240443785024134374302420037590243043759024377373302455637390245453752024442375202449137540243283788024256378802429137410242113756024079382102422338360241473812024328380702441937870245263753024631373902463337570246973766024720374402480537440248053749024805383702489437880249363703024861370302475337080246933723024595372302443436190244073684024482368602454136900244703650024265368102411437730240293773024288384602477338080238783657013914369201389437560138513796014506380501448937820144643743014507365001445136500143913586014436359101444737520144413790014408382101437838210143753770014310379601427438390143223839014582380001452237220145863751014652381701472338280148223680014903361001487636310149013672014881369901490737450148963775014936379001490138170148363829014793383501485137530147843794014812374801472337660146223810014708374801466237660147543734014450372201
#Very cool lvl: 376736990139383698013764375401382837540139133754013969375401402237540141173740014207371701364137280237153728023775372802391937280237613736023537373602354937360236103736023873371202385937310240223731024150369602423137150241623747024112374502395137360240823719024291371902427237410243433741024452374102456037010247053701024801372702490337340249143662024838368102477437410246843741024850374102471137480246473699024575373902445237390243943773024241380802414838080240493808023957375502386137810237203781023579381602350038160235553816023665381402376238150238633815023962381502377938290243633845024302382102444838280245163828024620383102457338260247183826024820382602492638260248763823024805382302465637800245463774024004369302405036910243993765024453372502451737320236593670013715368201364537080135863729013528372901353036710135773671013574380401365838040137223748013574383501350038280138033693013787376201371238230139193687013885371701384637720138893831013819383101386336980137823801014118364801415336940141463746014103381301416338010144423696014424373701439337780143933801014453383501449237640145413819014296382601422438330140333841013950384401458938180146603818014741383401479838220148153827014871383901491938430149233785014923372701493936510149263599014871366101487037220148283789014758378501482837220147983683024836373701485536740145363670024348366702429537090243953660014471364301451537190143463727014382372801428737700145763780014939335401473030130146843060014635309701465230160146973146014755310601456330660145113032014578303201443330320143523016014289301401422530010141583005014227301001351432060135943214013665321401372632110138103207013857320901393832090140173237014065322501408432250141093229014785313401478031590148303172014864317201491331760149223136014878311901482731080148273062014833300501493930300149373065014900305201490530120147813014013683315802373031970136963212013651321201
pygame.quit()