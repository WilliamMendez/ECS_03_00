

from datetime import datetime
import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_hunter import CTagEnemyHunter


def system_collision_player_enemy(world: esper.World, player_entity: int, level_cfg: dict, explosion_info: dict):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    components.extend(world.get_components(
        CSurface, CTransform, CTagEnemyHunter))

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    pl_rect.topleft = pl_t.pos

    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        ene_rect.topleft = c_t.pos
        if ene_rect.colliderect(pl_rect):
            time = datetime.now().time()
            print("Collision   ", time)
            create_explosion(world, c_t.pos, explosion_info)

            world.delete_entity(enemy_entity)
            player_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
            size = player_rect.size
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - size[0] / 2
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - size[1] / 2
