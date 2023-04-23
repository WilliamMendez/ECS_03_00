import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion

def system_explosion_cleaner(world: esper.World):
    components = world.get_components(CTagExplosion, CAnimation)
    for entity, (c_tag, c_anim) in components:
        if c_anim.curr_frame == c_anim.animations_list[c_anim.curr_anim].end:
            world.delete_entity(entity)


