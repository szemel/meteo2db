import constants


class Masks(object):

    def __init__(self, img):
        self.img = img
        self.r, self.g, self.b = self.return_colors()

    def return_colors(self):
        reds = self.img[:, :, constants.RED]
        greens = self.img[:, :, constants.GREEN]
        blues = self.img[:, :, constants.BLUE]
        return reds, greens, blues

    def plot_grid_mask(self):
        return (self.g == 128) & (self.r == 128) & (self.r == 128)

    def plot_curve_mask(self):
        return (self.r > 200) & (self.b < 200)

    def axis_digits_mask(self):
        return (self.g < 200) & (self.r < 200) & (self.b > 200)

    def black_mask(self):
        return (self.g < 240) & (self.r < 240) & (self.b < 240)

    def pink_mask(self):
        return (self.g == 0) & (self.r == 255) & (self.b == 255)
