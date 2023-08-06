#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:38:00 2023

@author: anthony
"""
from collections.abc import Callable
import pygame
from pygame.sprite import Sprite
from kiri_walkgame.shortcuts import SOURCES, equal_pos, in_rect


class BaseSprite(Sprite):
    "base module of sprites"

    def get_size(self):
        "get the image size"
        return self.image.get_size()


class Kiri(BaseSprite):
    """
    module of the character: Kiri

    params
    ------
    size : int,
        the size of the image

    """

    def __init__(self, size=40, fps=10):
        super().__init__()
        self.__load_frames(size, fps)
        self.rect = None
        self._frame_ind = 0
        self.__update_image()
        self._queue = []
        self._current_pos = None
        self._to_flip = False

    @property
    def moving(self):
        "the character is moving or not"
        return len(self._queue) > 0

    def stop(self):
        "stop the move and clean the queue"
        self._queue.clear()

    def reset(self):
        "reset all property"
        self.stop()
        self._current_pos = None

    def move(self, position, speed):
        """
        move the character to the position in the given speed

        params
        ------
        position : (int, int)
            The target position
        speed : int,
            The quantity of moving steps.
            The larger the given number, the slower the character moves.

        """
        # cases do not need to move
        if self._current_pos is None or equal_pos(self._current_pos, position):
            self._current_pos = position
            return

        # divide the move into steps and put the halfway positions into queue
        delta_x, delta_y = [(x - y) / speed for x,
                            y in zip(position, self._current_pos)]
        self._to_flip = delta_x < 0
        pos_x, pos_y = self._current_pos
        self._queue.extend(
            [(pos_x + delta_x * i, pos_y + delta_y * i)
             for i in range(speed, 0, -1)])

    def __load_frames(self, size, fps):
        ratio = fps // 10
        images = [pygame.transform.scale(pygame.image.load(x), (size, size))
                  for x in (SOURCES.kiri.stand, SOURCES.kiri.run)]
        if ratio > 1:
            images = sum([[i for _ in range(ratio)] for i in images], [])
        self.frames = tuple(images)

    def __update_image(self):
        self.image = self.frames[self._frame_ind]
        if self.rect is None:
            self.rect = self.image.get_rect()
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, *args, **kwargs):
        "update the character image"
        if self.moving:
            self._frame_ind += 1
            self._frame_ind %= len(self.frames)
        else:
            self._frame_ind = 0
        self.__update_image()

    def draw(self, screen):
        "draw the character on screen"
        if self._current_pos is None:
            return None

        if self.moving:
            self._current_pos = self._queue.pop()

        self.update()
        image = self.image
        if self._to_flip:
            image = pygame.transform.flip(image, True, False)
        return screen.blit(image, self._current_pos)


class Button(BaseSprite):
    """
    module to describe a button

    params
    ------
    path : str
        path of the button icon
    size : (int, int)
        the size of the button
    action : func
        the action when the button is pressed

    """

    normal_color = (150, 150, 150)

    pressed_color = (50, 50, 50)

    def __init__(self, path, position, size=(80, 40), margin=5, action=None):
        super().__init__()
        self.size = size
        self.margin = margin
        self._current_pos = position
        self.__current = 0
        self.__load_frames(path)
        if isinstance(action, Callable):
            self.action = action
        else:
            self.action = lambda x: None
        self._pressed = False

    @property
    def image(self):
        "image to show"
        return self.frames[self.__current]

    def __load_frames(self, path):
        if isinstance(path, str):
            path = [path]
        size = min(self.size) - self.margin * 2
        self.frames = [pygame.transform.scale(pygame.image.load(p),
                                              (size, size))
                       for p in path]

        self._img_pos = [x + (dx - size) / 2 for x, dx in zip(self._current_pos,
                                                     self.size)]
        self._img_pos[1] = self._current_pos[1] + self.margin
        self.surface = pygame.Surface(self.size)
        self.rect = self.surface.get_rect()

    def update(self):
        "update the shown color"
        color = self.normal_color
        if self._pressed:
            color = self.pressed_color
            self._pressed = False
        self.surface.fill(color)

    def draw(self, screen):
        "draw the button on screen"
        self.update()
        self.rect = screen.blit(self.surface, self._current_pos)
        screen.blit(self.image, self._img_pos)
        return self.rect

    def on_event(self, event):
        "react if the event happens on the button"
        if in_rect(event.pos, self.rect):
            self._pressed = True
            self.__current += 1
            self.__current %= len(self.frames)
            self.action(event)
            return True
        return False
