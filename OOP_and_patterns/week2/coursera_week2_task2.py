import pygame
import random
import math

SCREEN_DIM = (800, 600)

def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Left mouse button", "Add point to first line"])
    data.append(["Any another mouse button", "Add point to second line"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["Delete", "delete last point"])
    data.append(["Up arrow", "Speed Up"])
    data.append(["Down arrow", "Speed Down"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (50, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (400, 100 + 30 * i))


class Vec2d:
    def __init__(self, vector):
        self.x = vector[0]
        self.y = vector[1]

    def _mul(self, k):
        return (self.x * k, self.y * k)

    def _scal_mul(self, obj):
        return (self.x * obj.x, self.y * obj.y)

    def __add__(self, obj):
        return Vec2d((self.x + obj.x, self.y + obj.y))

    def __sub__(self, obj):
        return Vec2d((self.x - obj.x, self.y - obj.y))

    def __mul__(self, obj):
        if isinstance(obj, Vec2d):
            return Vec2d(self._scal_mul(obj))
        else:
            return Vec2d(self._mul(obj))

    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self, window_size):
        self.points = []
        self.poly_points = []
        self.speeds = []
        self.window_size = window_size
        self.points_color = (random.randint(10, 255),
                             random.randint(10, 255),
                             random.randint(10, 255))

    def add_point(self, point):
        self.points.append(Vec2d(point))
        self.speeds.append(Vec2d((random.random() * 2, random.random() * 2)))
        self.poly_points = self.points

    def delete_point(self):
        if self.points:
            self.points.pop()
            self.speeds.pop()
        self.poly_points = self.points

    def change_speed(self, type="up"):
        for i in range(len(self.speeds)):
            if type=="up":
                self.speeds[i] = self.speeds[i] * 2
            elif type=="down":
                self.speeds[i] = self.speeds[i] * 0.5

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > self.window_size[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d((- self.speeds[p].x, self.speeds[p].y))
            if self.points[p].y > self.window_size[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d((self.speeds[p].x, -self.speeds[p].y))
        self.poly_points = self.points

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.poly_points) - 1):
                pygame.draw.line(gameDisplay, color, self.poly_points[p_n].int_pair(),
                                self.poly_points[p_n + 1].int_pair(), width)

        elif style == "points":
            color = self.points_color
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(), width)


class Knot(Polyline):

    def __init__(self, window_size, steps):
        super().__init__(window_size)
        self.steps = steps


    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)


    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res


    def get_knot(self):
        if len(self.points) < 3:
            self.poly_points = []
            return
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))

        self.poly_points = res

    def add_point(self, point):
        super().add_point(point)
        self.get_knot()

    def delete_point(self):
        super().delete_point()
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()








if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")




    steps = 35
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    first_line = Knot(SCREEN_DIM, steps)
    second_line = Knot(SCREEN_DIM, steps)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    first_line.points = []
                    first_line.speeds = []
                    first_line.poly_points = []
                    second_line.points = []
                    second_line.speeds = []
                    second_line.poly_points = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                    first_line.steps = steps
                    first_line.get_knot()
                    second_line.steps = steps
                    second_line.get_knot()
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                    first_line.steps = steps
                    first_line.get_knot()
                    second_line.steps = steps
                    second_line.get_knot()
                if event.key == pygame.K_DELETE:   #Delete last point that was added
                    first_line.delete_point()
                    second_line.delete_point()
                if event.key == pygame.K_UP:
                    first_line.change_speed("up")
                    second_line.change_speed("up")
                if event.key == pygame.K_DOWN:
                    first_line.change_speed("down")
                    second_line.change_speed("down")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    first_line.add_point(event.pos)
                else:
                    second_line.add_point(event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        first_line.draw_points()
        first_line.draw_points("line", 3, color=color)
        second_line.draw_points()
        second_line.draw_points("line", 3, color=color)
        if not pause:
            first_line.set_points()
            second_line.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
