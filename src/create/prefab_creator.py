from datetime import datetime
import random
import pygame
import esper

from src.ecs.components.c_animation import AnimationData, CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_hunter import CTagEnemyHunter
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CVelocity(vel))
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_sprite = pygame.image.load(enemy_info["image"]).convert_alpha()
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_sprite(world, pos, velocity, enemy_sprite)
    world.add_component(enemy_entity, CTagEnemy())
    if enemy_info.get("animations") is not None:
        size = enemy_sprite.get_size()
        size = (size[0] / enemy_info["animations"]["number_frames"], size[1])
        world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))
        world.add_component(enemy_entity, CEnemyState())


def create_enemy_hunter(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_sprite = pygame.image.load(enemy_info["image"]).convert_alpha()
    vel_chase = enemy_info["velocity_chase"]
    vel_return = enemy_info["velocity_return"]
    dist_chase = enemy_info["distance_start_chase"]
    dist_return = enemy_info["distance_start_return"]
    origin_pos = pos
    enemy_entity = create_sprite(world, pygame.Vector2(
        pos), pygame.Vector2(0, 0), enemy_sprite)
    world.add_component(enemy_entity, CTagEnemyHunter(
        vel_chase, vel_return, dist_chase, dist_return, origin_pos))

    # show a circle to see the chase and return distance
    # create_debug_circle(world, pos, dist_chase, pygame.Color("red"))
    # create_debug_circle(world, pos, dist_return, pygame.Color("green"))

    if enemy_info.get("animations") is not None:
        size = enemy_sprite.get_size()
        size = (size[0] / enemy_info["animations"]["number_frames"], size[1])
        world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))
        world.add_component(enemy_entity, CEnemyState())


def create_debug_circle(world: esper.World, pos: pygame.Vector2, radius: int, col: pygame.Color):
    debug_circle_entity = world.create_entity()
    center = pygame.Vector2(pos.x - radius, pos.y - radius)
    world.add_component(debug_circle_entity, CTransform(center))
    world.add_component(debug_circle_entity, CSurface.from_circle(radius, col))


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    image = explosion_info["image"]
    animation_info = explosion_info["animations"]
    explosion_sprite = pygame.image.load(image).convert_alpha()
    explosion_entity = create_sprite(
        world, pos, pygame.Vector2(0, 0), explosion_sprite)
    time = datetime.now().time()
    print("sprt created", time, "entity", explosion_entity)

    world.add_component(explosion_entity, CAnimation(animation_info))
    time = datetime.now().time()
    print("anim created", time, "entity", explosion_entity)
    world.add_component(explosion_entity, CTagExplosion())
    time = datetime.now().time()
    print("expl created", time, "entity", explosion_entity)


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    player_sprite = pygame.image.load(player_info["image"]).convert_alpha()
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - size[0] / 2,
                         player_lvl_info["position"]["y"] - size[1] / 2)
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()

    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up,
                        CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down,
                        CInputCommand("PLAYER_DOWN", pygame.K_DOWN))

    input_fire = world.create_entity()
    world.add_component(input_fire,
                        CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))


def create_bullet(world: esper.World,
                  mouse_pos: pygame.Vector2,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):
    bullet_surface = pygame.image.load(bullet_info["image"]).convert_alpha()
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(
        player_pos.x + player_size[0] / 2 - bullet_size[0] / 2,
        player_pos.y + player_size[1] / 2 - bullet_size[1] / 2)
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_info["velocity"]

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
