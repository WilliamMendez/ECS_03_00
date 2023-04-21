import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity

def system_player_state(world:esper.World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)

    for _, (c_v, c_a, c_p) in components:
        if c_p.state == PlayerState.IDLE:
            _do_idle_state(c_v, c_a, c_p)
        elif c_p.state == PlayerState.MOVE:
            _do_move_state(c_v, c_a, c_p)

def _do_idle_state(c_v:CVelocity, c_a:CAnimation, c_p:CPlayerState):
    _set_animation(c_a, 1)
    if c_v.vel.magnitude() > 0:
        c_p.state = PlayerState.MOVE

def _do_move_state(c_v:CVelocity, c_a:CAnimation, c_p:CPlayerState):
    _set_animation(c_a, 0)
    if c_v.vel.magnitude() <= 0:
        c_p.state = PlayerState.IDLE

def _set_animation(c_a:CAnimation, anim:int):
    if c_a.curr_anim == anim:
        return
    c_a.curr_anim = anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.curr_frame = c_a.animations_list[anim].start
