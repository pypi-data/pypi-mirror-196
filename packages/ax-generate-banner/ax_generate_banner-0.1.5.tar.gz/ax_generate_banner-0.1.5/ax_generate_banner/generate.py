import pathlib
from typing import Optional

from PIL import Image, ImageFont, ImageDraw, ImageOps

BASE_DIR = pathlib.Path(__file__).parent.parent


class Generate:
    def __init__(self, left_image: Optional[str],
                 right_image: Optional[list],
                 text_header: Optional[tuple],
                 text_data: Optional[tuple],
                 residence_title: Optional[str],
                 font: Optional[str] = BASE_DIR / 'fonts' / 'arial.ttf'):
        self.font = str(BASE_DIR / 'fonts' / str(font))
        self.residence_title = residence_title.upper()
        self.text_header = text_header
        self.text_data = text_data
        self.left_image = left_image
        self.right_image = [img for img in right_image]
        self.image = Image
        self.total_width: Optional[int] = 1354
        self.total_height: Optional = 960
        self.left_image_width = 502
        self.right_image_width = 850
        self.right_image_height = 690

    def make_square_image(self, image_path):
        """
        :param image_path: right image path
        :return: squared new images
        """
        n = len(image_path)
        right_image_height = self.right_image_height // 1 if n <= 2 else self.right_image_height // (n - 1)
        right_image_width = self.right_image_width // n
        new_temp_size = (right_image_width, right_image_height)
        new_size = (self.right_image_width, self.right_image_height)
        images = []
        for item, img in enumerate(image_path):
            with Image.open(img) as image:

                width, height = image.size
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                if n == 4:
                    right_image_height = self.right_image_height // 2
                    right_image_width = self.right_image_width // 2
                    new_temp_size = (right_image_width, right_image_height)
                if height > right_image_height:
                    p = right_image_height / height
                    fit_size = (int(width * p), right_image_height)
                elif width > right_image_width:
                    p = right_image_width / width
                    fit_size = (right_image_width, int(height * p))

            image = image.resize(fit_size)
            new = Image.new("RGBA", new_temp_size, 'WHITE')
            new.paste(image, ((new_temp_size[0] - fit_size[0]) // 2, (new_temp_size[1] - fit_size[1]) // 2), mask=image)
            images.append(new)
        # new_image.paste(image, ((new_size[0] - fit_size[0]) // 2, (new_size[1] - fit_size[1]) // 2), mask=image)
        _new_image = Image.new("RGBA", new_size, 'WHITE')
        n_cols = 2
        for i, img in enumerate(images):
            if n == 4:
                row = i // n_cols
                col = i % n_cols
                x = col * img.width
                y = row * img.height
                _new_image.paste(img, (x, y))
            else:
                _new_image.paste(img, (i * img.width, (new_size[1] - fit_size[1]) // 2))
        return _new_image

    def resize_images(self) -> Optional[tuple]:
        """
        :return: left image and right image
        """
        left_image = self.image.open(self.left_image)
        right_images = []
        for img in self.right_image:
            right_images.append(img)
        right_image = self.make_square_image(right_images)
        right_image.resize((self.right_image_width, self.right_image_height))
        left_image = left_image.resize((self.left_image_width, self.total_height))
        left_image = self.gradient(left_image)
        return left_image, right_image

    def join_images(self):
        """
        :return: joined images in one image
        """
        image_left, image_right = self.resize_images()
        result = self.image.new('RGB', (self.total_width, self.total_height), (255, 255, 255))
        result.paste(image_left, (0, 0))
        right_centered = self.left_image_width + int(
            (self.total_width - self.left_image_width - self.right_image_width) / 2)
        right_side_center = (right_centered, 25)
        result.paste(image_right, right_side_center)
        self.right_side_text(result)
        self.left_side_text(result)
        return result

    def right_side_text(self, result) -> Optional[None]:
        """
        Customize right image text
        :param result: joined result image
        :return: None
        """
        width, font_size, font_size_nums = 700, 35, 84

        font_shrift = str(BASE_DIR / 'fonts' / 'montserrat.ttf')
        font = ImageFont.truetype(font_shrift, font_size)
        font_nums = ImageFont.truetype(self.font, font_size_nums)

        center = self.left_image_width + (self.right_image_width - width) // 2
        header_x, header_y = center, 766
        text_color = (0, 0, 0)
        rows, cols, gap_size = 1, 3, 10
        cell_size = (width - (cols + 1) * 10) // cols

        draw = ImageDraw.Draw(result)
        for row in range(rows):
            for col in range(cols):
                # position of grid stats
                x = col * (cell_size + gap_size) + gap_size + header_x
                y = row * (cell_size + gap_size) + gap_size + header_y

                # stats nums of headers
                number = row * cols + col + 1
                number_size = draw.textsize(self.text_data[number - 1], font=font_nums)
                number_x = x + (cell_size - len(self.text_data[number - 1])) // 2 + 4
                number_y = y + (cell_size - number_size[1]) // 2
                draw.text((number_x, number_y), self.text_data[number - 1], font=font_nums, fill=text_color,
                          anchor="ms")

                # header of stats nums
                title = f"{self.text_header[number - 1]}"
                title_size = draw.textsize(title, font=font)
                title_x = x + (cell_size - title_size[0]) // 2
                title_y = y - title_size[1] - 5
                draw.text((title_x, title_y), title, font=font, fill=text_color)

    def left_side_text(self, result, font_size: Optional[int] = 50) -> Optional[None]:
        """
        Customize left image text
        :param result: joined result image
        :param font_size: size of text
        :return: None
        """
        draw = ImageDraw.Draw(result)
        W, Y = self.left_image_width, self.total_height
        font = ImageFont.truetype(font=self.font, size=font_size)
        text_wrap = self.text_wrap(self.residence_title, font, self.left_image_width - 30)
        text_wrap = "\n".join(text_wrap)
        w, y = draw.textsize(text_wrap, font)
        x, y = (W - w) // 2, (Y - y) // 2
        draw.text((x, 740), text_wrap, font=font, fill=(255, 255, 255), align='center')

    def save(self, file_name) -> Optional[None]:
        """
        :param file_name: generated new file name
        :return: None
        """
        self.join_images().save(file_name)

    def text_wrap(self, text, font, max_width) -> Optional[list]:
        """
        Centralize text
        :param text: input text of right image text
        :param font: font of text
        :param max_width: width of text block
        :return: list
        """
        lines = []

        if font.getsize(text)[0] <= max_width:
            lines.append(text)
        else:
            words = text.split(' ')
            i = 0
            while i < len(words):
                line = ''
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)
        return lines

    def gradient(self, result, gradient_magnitude=1.):
        """
        Gradient of right image
        :param result: joined result image
        :param gradient_magnitude: value of gradient
        :return: joined result image
        """
        if result.mode != 'RGBA':
            result = result.convert('RGBA')
        width, height = result.size
        gradient = Image.new('L', (1, height), color=0xFF)
        for y in range(height):
            gradient.putpixel(
                (0, y), int(255 * (gradient_magnitude * float(y) / height)) - 70
            )
        alpha = gradient.resize(result.size)
        black_im = Image.new('RGBA', (width, height), color=0)
        black_im.putalpha(alpha)
        gradient_im = Image.alpha_composite(result, black_im)
        result.paste(gradient_im)
        return result
