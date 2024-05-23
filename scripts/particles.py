class Particle: 

    def __init__(self, game, type, pos, velocity= [ 0,0], frame = 0):
        self.game = game
        self.type = type
        self.pos = list(pos)
        self.velocity = velocity
        self.animation = self.game.assets['particle/' + self.type].copy()
        self.animation.frame = frame
    def update(self): 
        kill = False
        if self.animation.done: 
            kill = True
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        return kill
    def render(self, surf, offset = (0,0)): 
        render_img = self.animation.img()
        surf.blit(render_img, (self.pos[0] - offset[0] - render_img.get_width()//2, self.pos[1] - offset[1] - render_img.get_height()//2))
