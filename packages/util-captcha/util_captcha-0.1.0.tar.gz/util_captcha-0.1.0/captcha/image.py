# -*- coding: utf-8 -*-
"""
:author: Punk Lee
:url: https://punk_lee.gitee.io/
:copyright: © 2023 Punk Lee <punklee333@gmail.com>
"""
from io import BytesIO
from base64 import b64encode

from random import randint, randrange, uniform
from PIL import Image, ImageDraw, ImageFont

from captcha.utils import random_color

TABLE = [int(i * 1.97) for i in range(256)]


class ImageCaptcha:
    def __init__(
        self,
        mode: str = "RGBA",
        width: int = 120,
        height: int = 40,
        background: int = (0, 0, 0, 0),
    ):
        self.mode = mode
        self.width = width
        self.height = height
        self.background = background
        self.canvas = Image.new(self.mode, (self.width, self.height), self.background)

    def draw_chars(self, chars: str, font_path: str, font_size: int = 33):
        draw = ImageDraw.Draw(self.canvas)
        font = ImageFont.truetype(font_path, size=font_size)

        def _draw_character(c: str):
            _, _, w, h = draw.textbbox((1, 1), c, font=font)

            dx = randint(0, 4)
            dy = randint(0, 6)
            im = Image.new("RGBA", (w + dx, h + dy))
            ImageDraw.Draw(im).text((dx, dy), c, font=font, fill=random_color())

            # rotate
            im = im.crop(im.getbbox())
            im = im.rotate(uniform(-33, 33), Image.Resampling.BILINEAR, expand=1)

            # warp
            dx = w * uniform(0.1, 0.3)
            dy = h * uniform(0.2, 0.3)
            x1 = int(uniform(-dx, dx))
            y1 = int(uniform(-dy, dy))
            x2 = int(uniform(-dx, dx))
            y2 = int(uniform(-dy, dy))
            w2 = w + abs(x1) + abs(x2)
            h2 = h + abs(y1) + abs(y2)
            data = (
                x1,
                y1,
                -x1,
                h2 - y2,
                w2 + x2,
                h2 + y2,
                w2 - x2,
                -y1,
            )
            im = im.resize((w2, h2))
            im = im.transform((w, h), Image.Transform.QUAD, data)

            return im

        char_image_list = []
        for c in chars:
            char_image_list.append(_draw_character(c))

        text_width = sum([im.size[0] for im in char_image_list])

        width = max(text_width, self.width)
        self.canvas = self.canvas.resize((width, self.height))

        average = int(text_width / len(chars))
        offset = int(average * 0.1)

        # horizontal center & vertical random
        each_w = self.width / len(chars)
        for i in range(len(char_image_list)):
            im = char_image_list[i]
            w, h = im.size
            mask = im.convert("L").point(TABLE)
            x = each_w * i + (each_w - w) / 2
            y = randrange(0, self.height - h)
            xy = int(offset if each_w < w else x), int(y)
            self.canvas.paste(im, xy, mask)
            offset = offset + w

        if width > self.width:
            self.canvas = self.canvas.resize((self.width, self.height))

    def draw_curve(self, number: int = 3):
        w, h = self.width, self.height
        for _ in range(number):
            x1 = randint(0, int(w / 5))
            x2 = randint(w - int(w / 5), w)
            y1 = randint(int(h / 5), h - int(h / 5))
            y2 = randint(y1, h - int(h / 5))
            points = [x1, y1, x2, y2]
            start = randint(0, 20)
            end = randint(100, 200)
            ImageDraw.Draw(self.canvas).arc(points, start, end, fill=random_color())

    def draw_dots(self, width: int = 1, number: int = 90):
        w, h = self.width, self.height
        draw = ImageDraw.Draw(self.canvas)
        while number:
            x1 = randint(0, w)
            y1 = randint(0, h)
            draw.line(((x1, y1), (x1 - 1, y1 - 1)), fill=random_color(), width=width)
            number -= 1
        return

    def generate(self, fmt: str = "png") -> BytesIO:
        out = BytesIO()
        self.canvas.save(out, format=fmt)
        out.seek(0)
        return out

    def generate_base64(self, fmt: str = "png") -> str:
        prefix = f"data:image/{fmt};base64,"
        return f"{prefix}{b64encode(self.generate().read()).decode()}"
