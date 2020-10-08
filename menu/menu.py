
class Menu:
    def __init__(self,x,y,img):
        self.img = img
        self.x = x
        self.y = y
        self.height = img.get_height()
        self.width = img.get_width()

    def draw(self,win):
        win.blit(self.img,(self.x-self.img.get_width()//2,self.y - self.img.get_height()//2))

    def click(self,x,y):
        if self.x - self.width//2 < x < self.x + self.width//2:
            if self.y - self.height//2 < y < self.y + self.height//2:
                return True
        return False


