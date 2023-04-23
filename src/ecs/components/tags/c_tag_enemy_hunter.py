import pygame

class CTagEnemyHunter:
    def __init__(self, vel_chase: int, vel_return: int, dist_chase: int, dist_return: int, origin_pos: pygame.Vector2):
        self.vel_chase = vel_chase
        self.vel_return = vel_return
        self.dist_chase = dist_chase
        self.dist_return = dist_return
        self.positionData = PositionData(origin_pos)
        self.hunting = True

class PositionData:
    def __init__(self, origin_pos: pygame.Vector2):
        # print("PositionData")
        # print(origin_pos)
        self.origin_pos = pygame.Vector2(origin_pos[0], origin_pos[1])

