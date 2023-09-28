from typing import List, Any

from pico2d import *
from enum import Enum, auto


Running = True
BackGround_Width, BackGround_Height = 1280, 1024

open_canvas(BackGround_Width,BackGround_Height)


class ImageObject:
    def __init__(self, path: str, frame: int, Width: int, Height: int):
        self.Path = path
        self.Frame = frame
        self.Width = Width
        self.Height = Height


class BehaviorType(Enum):
    Idle = auto()
    Run = auto()


class Character:
    def __init__(self):
        self.Images = {}
        self.Object : pico2d.Image
        self.CurrentBehavior = BehaviorType.Idle.name
        self.FrameCount = 0
        self.IsComposite = False

        self.x = 100
        self.y = 100


    def Resister(self, BehaviorName: str, Img: ImageObject):
        self.Images[BehaviorName] = Img

    def Behavior(self,BehaviorName : str):
        self.Object = load_image(self.Images[BehaviorName].Path)

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




Events = []

while Running:
    clear_canvas()
    Events = get_events()
    BackGround.draw(BackGround_Width // 2, BackGround_Height // 2)

    MainCharacter.Render(4)

    delay(0.05)
    HandleEvent(Events)
    update_canvas()