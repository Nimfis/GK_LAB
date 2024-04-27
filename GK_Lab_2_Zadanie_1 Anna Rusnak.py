import math
import typing
import pygame
import numpy as np
import cv2

pygame.init()
display_surface = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Anna Rusnak zad. 1")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

POLY_CENTER = (300, 300)
POLY_SIDES = 7
POLY_RADIUS = 150

def perspective_warp(surface: pygame.Surface, points, use_smooth=True, output_surface: pygame.Surface = None) -> typing.Tuple[pygame.Surface, pygame.Rect]:
    if len(points) != 4:
        raise ValueError("Punkty powinny zawierać 4 zestawy koordynatów (x, y)")
    surf_width, surf_height = surface.get_size()
    has_alpha = surface.get_flags() & pygame.SRCALPHA

    src_points = np.float32([(0, 0), (0, surf_width), (surf_height, surf_width), (surf_height, 0)])
    dst_points = [tuple(reversed(pt)) for pt in points]

    bbox_x_values, bbox_y_values = zip(*dst_points)
    min_x, max_x = min(bbox_x_values), max(bbox_x_values)
    min_y, max_y = min(bbox_y_values), max(bbox_y_values)
    output_rect = pygame.Rect(int(min_x), int(min_y), int(max_x - min_x), int(max_y - min_y))

    adjusted_dst_points = [(pt[0] - min_x, pt[1] - min_y) for pt in dst_points]
    transformation_matrix = cv2.getPerspectiveTransform(src_points, np.float32(adjusted_dst_points))

    surf_rgb = pygame.surfarray.pixels3d(surface)
    warp_flags = cv2.INTER_LINEAR if use_smooth else cv2.INTER_NEAREST
    warped_rgb = cv2.warpPerspective(surf_rgb, transformation_matrix, output_rect.size, flags=warp_flags)

    if output_surface is None or output_surface.get_size() != warped_rgb.shape[0:2]:
        output_surface = pygame.Surface(warped_rgb.shape[0:2], pygame.SRCALPHA if has_alpha else 0)

    pygame.surfarray.blit_array(output_surface, warped_rgb)

    if has_alpha:
        surf_alpha = pygame.surfarray.pixels_alpha(surface)
        warped_alpha = cv2.warpPerspective(surf_alpha, transformation_matrix, output_rect.size, flags=warp_flags)
        output_alpha_channel = pygame.surfarray.pixels_alpha(output_surface)
        output_alpha_channel[:] = warped_alpha
    else:
        output_surface.set_colorkey(surface.get_colorkey())

    return output_surface, pygame.Rect(output_rect.y, output_rect.x, output_rect.h, output_rect.w)

def generate_polygon_vertices(centre, sides, rad):
    angle_increment = 2 * math.pi / sides
    starting_angle = math.pi / sides / 2
    centre_x, centre_y = centre

    points = []
    for i in range(sides):
        x = centre_x + rad * math.cos(i * angle_increment + starting_angle)
        y = centre_y + rad * math.sin(i * angle_increment + starting_angle)
        points.append((x, y))

    return points

def draw_initial_shapes():
    display_surface.fill(BLACK)
    pygame.draw.rect(display_surface, RED, (100, 100, 400, 400), 400)
    pygame.draw.rect(display_surface, GREEN, (100, 100, 50, 50), 50)

draw_initial_shapes()

game_active = True
while game_active:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            game_active = False
        if evt.type == pygame.KEYDOWN:
            draw_initial_shapes()
            if evt.key in [pygame.K_0, pygame.K_KP0]:
                draw_initial_shapes()

            if evt.key in [pygame.K_1, pygame.K_KP1]:
                transformed = pygame.transform.scale(display_surface, (300, 300))
                display_surface.fill(BLACK)
                display_surface.blit(transformed, (150, 150))

            elif evt.key in [pygame.K_2, pygame.K_KP2]:
                transformed = pygame.transform.rotate(display_surface, 45)
                display_surface.fill(BLACK)
                display_surface.blit(transformed, (-150, -150))

            elif evt.key in [pygame.K_3, pygame.K_KP3]:
                transformed = pygame.transform.rotate(display_surface, 180)
                transformed = pygame.transform.scale(transformed, (500, 600))
                display_surface.fill(BLACK)
                display_surface.blit(transformed, (50, 0))

            elif evt.key in [pygame.K_4, pygame.K_KP4]:
                transformed, rect = perspective_warp(display_surface, [(0, 0), (400, 0), (600, 600), (100, 600)])
                display_surface.fill(BLACK)
                display_surface.blit(transformed, rect.topleft)

            elif evt.key in [pygame.K_5, pygame.K_KP5]:
                transformed = pygame.transform.scale(display_surface, (700, 300))
                display_surface.fill(BLACK)
                display_surface.blit(transformed, (-50, -40))

            elif evt.key in [pygame.K_6, pygame.K_KP6]:
                transformed, rect = perspective_warp(display_surface, [(0, 0), (400, 0), (600, 600), (100, 600)])
                transformed = pygame.transform.rotate(transformed, 270)
                display_surface.fill(BLACK)
                display_surface.blit(transformed, rect.topleft)

            elif evt.key in [pygame.K_7, pygame.K_KP7]:
                transformed = pygame.transform.rotate(display_surface, 180)
                transformed = pygame.transform.scale(transformed, (500, 600))
                display_surface.fill(BLACK)
                display_surface.blit(transformed, (50, 0))

            elif evt.key in [pygame.K_8, pygame.K_KP8]:
                transformed = pygame.transform.scale(display_surface, (700, 300))
                transformed = pygame.transform.rotate(transformed, -30)
                display_surface.fill(BLACK)
                display_surface.blit(transformed, (-50, -40))

            elif evt.key in [pygame.K_9, pygame.K_KP9]:
                transformed, rect = perspective_warp(display_surface, [(0, 0), (400, 0), (600, 600), (100, 600)])
                transformed = pygame.transform.rotate(transformed, 200)
                display_surface.fill(BLACK)
                display_surface.blit(transformed, rect.topleft)

    pygame.display.update()
    
pygame.quit()
