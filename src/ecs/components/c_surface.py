import pygame

class CSurface:
    def __init__(self, size:pygame.Vector2, color:pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()

    @classmethod
    def from_surface(cls, surface:pygame.Surface):
        c_surf = cls(pygame.Vector2(0,0), pygame.Color(0, 0, 0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf

    @classmethod
    def from_circle(cls, radius:int, color:pygame.Color):
        c_surf = cls(pygame.Vector2(0,0), pygame.Color(0, 0, 0))
        c_surf.surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        c_surf.surf.set_alpha(100)
        pygame.draw.circle(c_surf.surf, color, (radius, radius), radius)
        c_surf.area = c_surf.surf.get_rect()
        return c_surf

    def get_area_relative(area:pygame.Rect, pos_top_left:pygame.Vector2):
        area_relative = area.copy()
        area_relative.topleft = pos_top_left.copy()
        return area_relative
