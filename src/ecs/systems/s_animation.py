import esper
from datetime import datetime

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_explosion import CTagExplosion

def system_animation(world: esper.World, deltatime: float):
    components = world.get_components(CSurface, CAnimation)

    c_s: CSurface
    c_a: CAnimation
    for _, (c_s, c_a) in components:
        c_a.curr_anim_time -= deltatime
        if c_a.curr_anim_time <= 0:
            c_a.curr_frame += 1
            c_a.curr_anim_time = c_a.animations_list[c_a.curr_anim].framerate
            if c_a.curr_frame > c_a.animations_list[c_a.curr_anim].end:
                c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame
            # if it has CTagExplosion, print the time
            if world.has_component(_, CTagExplosion):
                time = datetime.now().time()
                print("Anim changed",time, "entity",_)
