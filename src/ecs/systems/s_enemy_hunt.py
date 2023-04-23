import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy_hunter import CTagEnemyHunter


def system_enemy_hunt(world: esper.World, player_entity: int):
    c_pl_tr = world.component_for_entity(player_entity, CTransform)

    for _, (c_ene_tr, c_ene_vel, c_hun_tag) in world.get_components(CTransform, CVelocity, CTagEnemyHunter):
        dist_to_player = (c_pl_tr.pos - c_ene_tr.pos).magnitude()
        # print(c_hun_tag.positionData.origin_pos)
        dist_to_origin = (c_hun_tag.positionData.origin_pos -
                          c_ene_tr.pos).magnitude()
        if dist_to_origin >= c_hun_tag.dist_return:
            # print(dist_to_origin)
            c_hun_tag.hunting = False
            c_ene_vel.vel = (c_hun_tag.positionData.origin_pos -
                            c_ene_tr.pos).normalize() * c_hun_tag.vel_return
        elif dist_to_player < c_hun_tag.dist_chase and c_hun_tag.hunting:
                c_ene_vel.vel = (
                    c_pl_tr.pos - c_ene_tr.pos).normalize() * c_hun_tag.vel_chase
        elif dist_to_origin < 1:
            c_hun_tag.hunting = True
            c_ene_vel.vel = pygame.Vector2(0, 0)
