import pygame, random, time



class Collectible:
    def __init__(self, x: float, y: float, sprite: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
    
    def update(self) -> None:
        pass
      
    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))
    
    def randomize_position(self) -> None:    
        self.x = random.randint(50, 1250)
        self.y = random.randint(50, 670)
        self.rect.x = self.x
        self.rect.y = self.y



class Player:
    def __init__(self, x: float, y: float, sprite: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.sprite = sprite
        self.velocity = 200
        self.angle = 0
        self.direction = "up"
        self.moving =False
        self.rect = self.sprite.get_rect()
        
    def update(self, dt) -> None:
        if self.moving:
           self.move(dt)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)        

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite, (self.x, self.y))
    
    def set_angle(self, new_angle: int) -> None:
        rotation = new_angle - self.angle
        self.sprite = pygame.transform.rotate(self.sprite, rotation)
        self.angle = new_angle
   
    def move(self, dt) -> None:
        if self.direction == "up":
           self.y -= self.velocity * dt
           
        elif self.direction == "down":
           self.y += self.velocity * dt
           
        elif self.direction == "left":
           self.x -= self.velocity * dt

        elif self.direction == "right":
           self.x += self.velocity * dt
           
        self.x = min((1280 - self.rect.width, self.x))
        self.x = max((0, self.x))
        self.y = min((720 - self.rect.height, self.y))
        self.y = max((0, self.y))        


class Text:
    def __init__(self, x, y, text: str) -> None:
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont("Calibri", 36)
        
    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        self.rendered = self.font.render(self.text, True, "black")
        screen.blit(self.rendered, (self.x, self.y))        


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.sprites = self.load_sprites()
        self.score = 0
        
        self.player = Player(200, 200, self.sprites["Aircraft"])
        self.collectible = Collectible(500, 500, self.sprites["Coin"])
        self.collectible.randomize_position()
        self.text = Text(600, 50, str(self.score))
        
        self.keybinds = {pygame.K_w: (0,"up"),
                         pygame.K_d: (270,"right"),                
                         pygame.K_s: (180,"down"),                
                         pygame.K_a: (90,"left")}                
        
        pygame.mixer.music.load("sfx/BG_Music.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        
        self.collect_sound = pygame.mixer.Sound("sfx/Coin-Collect.mp3")
        self.collect_sound.set_volume(0.5)
        
    def poll_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN and event.key in self.keybinds:
               self.player.set_angle(self.keybinds[event.key][0])
               self.player.direction = self.keybinds[event.key][1]
               self.player.moving = True
               
            if event.type == pygame.KEYUP and event.key in self.keybinds:  
               if self.keybinds[event.key][1] == self.player.direction:
                  self.player.moving = False
  
    def update(self) -> None:
        now = time.time()
        dt = now - self.previous_time
        self.previous_time = now
        
        self.player.update(dt)
        self.collectible.update()
        
        if self.player.rect.colliderect(self.collectible.rect):
           self.collectible.randomize_position()
           self.player.velocity += 100
           self.collect_sound.play()
           self.score += 1
           
        self.text.update()
        self.text.text = str(self.score)
        
    def render(self) -> None:
        self.screen.fill((0, 0, 0))
    
        self.screen.blit(self.sprites["Background"], (0, 0))
        self.player.render(self.screen)
        self.collectible.render(self.screen)
        self.text.render(self.screen)
    
        pygame.display.update()

    def run(self) -> None:
        self.previous_time = time.time()
        while self.running:
            self.poll_events()
            self.update()
            self.render()
        pygame.quit()   

    def load_sprites(self) -> dict:
        sprites = {}

        sprites["Aircraft"] = pygame.image.load("gfx/Aircraft.png").convert_alpha()
        sprites["Background"] = pygame.image.load("gfx/Sky_BG.jpg").convert_alpha()
        sprites["Coin"] = pygame.image.load("gfx/Coin.png").convert_alpha()
        
        sprites["Aircraft"] = pygame.transform.scale(sprites["Aircraft"], (48, 48))
        sprites["Background"] = pygame.transform.scale(sprites["Background"], (1280, 720))
        sprites["Coin"] = pygame.transform.scale(sprites["Coin"], (48, 48))
        
        return sprites
        
g = Game()
g.run()