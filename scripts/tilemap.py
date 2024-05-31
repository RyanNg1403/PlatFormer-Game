import pygame
import json
NEIGHBOR_OFFSET = [(0,0), (0,1), (0,-1), (1,0), (1,-1), (1,1), (-1,0), (-1,1), (-1,-1)]
AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

PHYSICS_TILES =  AUTOTILE_TYPES =  {'grass', 'stone'}
class TileMap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        
        # for i in range(15):
        #     # Tiles that the player will interact with: the key is the coordinates.
        #     self.tilemap[str(i +3) + ';10'] = {'type': 'grass', 'variant': 2, 'pos': (i+3,10)}
        #     self.tilemap[ '10;' + str(i)] = {'type': 'stone', 'variant': 1, 'pos': (10, i)}
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0]//self.tile_size), int(pos[1]//self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return  tiles
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    def render(self, surf, offset = (0,0)):
        # Render both the tilemaps and the offgrid tiles

        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], 
                      (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
            
        # Optimization
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width())//self.tile_size+1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height())//self.tile_size+1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], 
                            (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 
                   'tile_size': self.tile_size,
                   'offgrid': self.offgrid_tiles, 
                   }, f)
    def extract(self, pairs, keep = True):
        matches = []
        # Off-grid tiles
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in pairs:
                matches.append(tile.copy())
                if not keep: 
                    self.offgrid_tiles.remove(tile)
        # On-grid tiles 
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in pairs:
                matches.append(tile.copy())
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if  not keep: 
                    del self.tilemap[loc]
        return matches
    def load(self, path):
        f = open(path, 'r')
        data_map = json.load(f)
        self.tilemap = data_map['tilemap']
        self.tile_size = data_map['tile_size']
        self.offgrid_tiles = data_map['offgrid']
    def autotile(self):
        for loc in self.tilemap:
            tile  = self.tilemap[loc]
            neighbors = set()
            for shift in [(0,1), (1,0), (-1,0), (0,-1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if (check_loc in self.tilemap) and (self.tilemap[check_loc]['type'] == tile['type']):
                    neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (neighbors in AUTOTILE_MAP) and (tile['type'] in AUTOTILE_TYPES):
                tile['variant']  = AUTOTILE_MAP[neighbors]


    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]