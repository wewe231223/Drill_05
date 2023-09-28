from typing import List, Any

from pico2d import *
from enum import Enum, auto
from random import randint


Running = True
BackGround_Width, BackGround_Height = 1280, 1024

open_canvas(BackGround_Width,BackGround_Height)

# Drill05 2020182009 김승범 

class ImageObject:
    def __init__(self, path: str, frame: int, Width: int, Height: int):
        self.Path = path
        self.Frame = frame
        self.Width = Width
        self.Height = Height


class BehaviorType(Enum):
    Idle = auto()
    Run = auto()

class Arrow:
    def __init__(self,path : str,XRange : tuple , YRaage : tuple):
        self.Object = load_image(path)
        self.x = randint(XRange[0],XRange[1])
        self.y = randint(YRaage[0],YRaage[1])

    def Render(self):
        self.Object.draw(self.x,self.y)



class Character:
    def __init__(self):
        self.Images = {}
        self.Object : pico2d.Image
        self.CurrentBehavior = BehaviorType.Idle.name
        self.FrameCount = 0

        self.IsComposite = False
        self.IsDestined = False

        self.x = 100
        self.y = 100

        self.OldX = 0
        self.OldY = 0

        self.T = 0.0




    def Resister(self, BehaviorName: str, Img: ImageObject):
        self.Images[BehaviorName] = Img

    def Behavior(self,BehaviorName : str):
        self.FrameCount = 0
        self.CurrentBehavior = BehaviorName
        self.Object = load_image(self.Images[BehaviorName].Path)


    def MoveToward(self,arrow : Arrow):
        if not self.IsDestined:
            self.IsDestined = True
            self.OldX = self.x
            self.OldY = self.y
            self.Behavior("Run")


        x2 = arrow.x
        y2 = arrow.y


        if self.x > x2:
            self.IsComposite = True
        else:
            self.IsComposite = False


        if 0.0 <= self.T < 0.2:
            self.T += 0.01
        elif 0.2 <= self.T < 0.8:
            self.T += 0.05
        elif 0.8 <= self.T < 1.0:
            self.T += 0.01




        self.x  = (1-self.T)*self.OldX + self.T * x2
        self.y  = (1-self.T)*self.OldY + self.T * y2

        if self.T >= 1:
            self.T = 0
            self.IsDestined = False
            self.OldX = 0
            self.OldY = 0
            return True

        return False

    def Render(self,Scale = int):
        self.FrameCount = (self.FrameCount + 1) % self.Images[self.CurrentBehavior].Frame
        self.x = clamp(20,self.x,get_canvas_width())
        self.y = clamp(20, self.y, get_canvas_height())



        DrawX = self.x
        DrawY = self.y + self.Images[self.CurrentBehavior].Height * 1.5


        if not self.IsComposite:
            self.Object.clip_draw(
                self.Images[self.CurrentBehavior].Width * self.FrameCount,
                0,
                self.Images[self.CurrentBehavior].Width,
                self.Images[self.CurrentBehavior].Height,
                DrawX,
                DrawY,
                150 * Scale,
                100 * Scale
            )
        elif self.IsComposite:
            self.Object.clip_composite_draw(
                self.Images[self.CurrentBehavior].Width * self.FrameCount,
                0,
                self.Images[self.CurrentBehavior].Width,
                self.Images[self.CurrentBehavior].Height,
                0,
                'h',
                DrawX,
                DrawY,
                150 * Scale,
                100 * Scale
            )





def HandleEvent(Events = List[Any]):
    global Running


    for event in Events:
        if event.type == SDL_QUIT:
            Running = False
            return
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Running = False
                return




Character_IdleImg = ImageObject("_Idle.png", 10, 120, 80)
Character_RunImg = ImageObject("_Run.png", 10, 120, 80)

MainCharacter = Character()

MainCharacter.Resister(BehaviorType.Idle.name,Character_IdleImg)
MainCharacter.Resister(BehaviorType.Run.name,Character_RunImg)

MainCharacter.Behavior("Idle")

BackGround = load_image("TUK_GROUND.png")


ar = Arrow("hand_arrow.png",(0,1280),(0,1024))


Events = []

while Running:
    clear_canvas()
    Events = get_events()
    BackGround.draw(BackGround_Width // 2, BackGround_Height // 2)


    if MainCharacter.MoveToward(ar):
        ar = Arrow("hand_arrow.png",(0,1280),(0,1024))

    MainCharacter.Render(4)
    ar.Render()

    delay(0.05)
    HandleEvent(Events)
    update_canvas()