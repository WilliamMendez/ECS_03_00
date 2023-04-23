
from src.ecs.components.c_animation import AnimationData

class CExplosionspawner:
    def __init__(self, explosion_data: dict):
        self.image = explosion_data['image']
        self.animation_data = explosion_data['animations']
