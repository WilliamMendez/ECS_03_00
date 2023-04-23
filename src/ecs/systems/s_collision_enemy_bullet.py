

import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_explosion_spawner import CExplosionspawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy_hunter import CTagEnemyHunter


def system_collision_enemy_bullet(world: esper.World):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_enemy.extend(world.get_components(CSurface, CTransform, CTagEnemyHunter))
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)

    _, (c_expl_spawner,) = world.get_components(CExplosionspawner)[0]

    for enemy_entity, (c_s, c_t, _) in components_enemy:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                create_explosion(world, c_t.pos, c_expl_spawner.image, c_expl_spawner.animation_data)

                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)

