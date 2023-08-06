import pygame

class AspectWindow():
    def __init__(self, screen_size: tuple, aspect_ratio: tuple, min_scale: int = 16) -> None:
        self.screen_size = screen_size
        self.aspect_ratio = aspect_ratio
        self.min_scale = min_scale

        # target area
        self.target_area = self.calc_target_area(screen_size)
        self.og_target_area = self.target_area
        self.center_target()

        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.drawing_surface = pygame.Surface(screen_size)
    @property
    def scale(self):
        """
        returns the pixel scale of the window relative to the original screen size
        """
        return self.target_area[0]/self.og_target_area[0]
    def calc_target_area(self, size: tuple) -> tuple:
        self.screen_size = size
        scale = 1
        if size[0]/16 > size[1]/9:
            scale = size[1]/9
        else:
            scale = size[0]/16
        return (scale*self.aspect_ratio[0], scale*self.aspect_ratio[1])

    def center_target(self):
        x_offset = (self.screen_size[0] - self.target_area[0])/2
        y_offset = (self.screen_size[1] - self.target_area[1])/2
        self.target_position = (x_offset, y_offset)
    def modify_window(self, event_size: tuple):
        """
        update the window size and target area
        """
        new_size = [event_size[0], event_size[1]]

        if new_size[0] < self.min_scale*16:
            new_size[0] = self.min_scale*16
        if new_size[1] < self.min_scale*9:
            new_size[1] = self.min_scale*9

        self.target_area = self.calc_target_area((new_size[0], new_size[1]))
        self.center_target()
        self.screen = pygame.display.set_mode((new_size[0], new_size[1]), pygame.RESIZABLE)
    def debug(self):
        """
        displays a frame of the target area
        """
        pygame.draw.rect(self.screen, "red", pygame.Rect(self.target_position[0], self.target_position[1],self.target_area[0], self.target_area[1]), 1)
    # calc utils
    def get_target_coord(self, coord: tuple) -> tuple:
        """
        returns the converted coordinates relative to the target area
        """
        return (coord[0] + self.target_position[0], coord[1] + self.target_position[1])
    def get_target_x(self, num):
        """
        returns the converted X value relative to the target area
        """
        return num + self.target_position[0]
    def get_target_y(self, num):
        """
        returns the converted Y value relative to the target area
        """
        return num + self.target_position[1]
    # drawing utils
    def fill(self, color: pygame.Color):
        """
        fills the target area with a color via pygame.draw.rect
        """
        pygame.draw.rect(self.screen, color, pygame.Rect(self.target_position[0], self.target_position[1], self.target_area[0], self.target_area[1]))