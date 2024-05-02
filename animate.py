import arcade as bora


class Animate(bora.Sprite):
    i = 0
    time = 0

    def update_animation(self, delta_time: float = 1 / 60):
        self.time += delta_time
        if self.time >= 0.1:
            self.time = 0
            self.next_texture()

    def next_texture(self):
        if self.i == len(self.textures) - 1:
            self.i = 0
        else:
            self.i += 1
        self.set_texture(self.i)