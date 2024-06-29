import pygame
import numpy
import cv2

# Набор из символов, для формирования изображения
MAIN_CHAR_STRING = ' ixzao№#AMW&8%B@$'
# Коэффициент расстояния между символами (для каждой фотографии подбирается свой)
SPACE_BETWEEN_CHARS_COEF = 0.6


def get_image_data(image, color=cv2.COLOR_BGR2GRAY):
    transposed_image = cv2.transpose(image)
    rgb_format_image = cv2.cvtColor(transposed_image, color)
    return rgb_format_image


def get_image(path):
    return cv2.imread(path)


def show_image_cv2(image):
    cv2.imshow('img', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_pygame(path, font_size, save_way='', chars=MAIN_CHAR_STRING, ascii=False, color_lvl=16):
    def create_colors():
        colors, color_coef = numpy.linspace(0, 255, num=color_lvl, dtype=int, retstep=True)
        color_palette = [numpy.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(chars, None)
        color_coef = int(color_coef)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coef)
                char_palette[color_key] = font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coef

    bw_img = get_image_data(get_image(path))
    img = get_image_data(get_image(path), color=cv2.COLOR_BGR2RGB)
    pygame.init()
    font = pygame.font.SysFont('Arial', font_size, bold=True)
    coef = 255 // (len(chars) - 2)
    step = int(font_size * SPACE_BETWEEN_CHARS_COEF)
    _colors, _color_coef = create_colors()

    # def draw_image_pygame():
    #     pygame.surfarray.blit_array(surface, image_data)

    def draw_image_pygame_ASCII():
        bw_ides = bw_img // coef
        cl_ides = img // _color_coef
        for x in range(0, width, step):
            for y in range(0, height, step):
                index = bw_ides[x, y]
                if index:
                    try:
                        char = chars[index]
                        color = tuple(cl_ides[x, y])
                        surface.blit(_colors[char][color], (x, y))
                    except pygame.error:
                        exit()
                    except KeyError as error:
                        print(error)
                        pass

    def screenshot():
        if save_way:
            cv2.imwrite(save_way, cv2.cvtColor(cv2.transpose(pygame.surfarray.array3d(surface)), cv2.COLOR_RGB2BGR))

    screen = width, height = bw_img.shape[0], bw_img.shape[1]
    surface = pygame.display.set_mode(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    screenshot()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        # if not ascii:
        #     draw_image_pygame()
        # else:
        #     draw_image_pygame_ASCII()
        draw_image_pygame_ASCII()
        pygame.display.flip()


if __name__ == '__main__':
    while True:
        try:
            show_pygame(input('> file path: '), 14, save_way='saved.jpg', ascii=True)
        except cv2.error:
            print("Wrong file way")
