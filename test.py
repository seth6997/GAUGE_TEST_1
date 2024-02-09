import pygame

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# SET VALUES FOR COLORS USED, ADD NAME TO ASSIGN TO HEX VALUES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class CustomGauge:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Custom Gauge")
        self.clock = pygame.time.Clock()

        # Load custom gauge background image
        self.background_image = pygame.image.load("images/GAUGE_BG.png").convert_alpha()

        # Load rectangle images into a list
        self.rectangle_images = []
        for i in range(1, 31):
            filename = f"images/RECTANGLE_{i}.png"
            image = pygame.image.load(filename).convert_alpha()
            self.rectangle_images.append(image)

        # Set initial value
        self.current_value = 0

        # Index of last displayed rectangle
        self.last_displayed_index = -1

        # Initialize key press flags
        self.up_pressed = False
        self.down_pressed = False

        # Load font
        self.font = pygame.font.Font(None, 68)

    def increase_value(self):
        # Increase the value
        self.current_value = min(self.current_value + 216, 8000)

    def decrease_value(self):
        # Decrease the value
        self.current_value = max(self.current_value - 150, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.up_pressed = True
                elif event.key == pygame.K_DOWN:
                    self.down_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.up_pressed = False
                elif event.key == pygame.K_DOWN:
                    self.down_pressed = False
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()

            # INCREASE / DECREASE VALUE FOR RPM READING EMULATION
            if self.up_pressed:
                self.increase_value()
            elif self.down_pressed:
                self.decrease_value()

            # BG COLOR
            self.screen.fill(BLACK)

            # SHOW CUSTOM GAUGE
            self.screen.blit(self.background_image, (0, 0))

            # RENDER EACH CUSTOM RECTANGLE LAYER
            num_rectangles = min(self.current_value // 266 + 1, len(self.rectangle_images))

            # Display the appropriate number of rectangle layers
            for i in range(len(self.rectangle_images)):
                if i < num_rectangles:
                    self.screen.blit(self.rectangle_images[i], (0, 0))
                else:
                    break

            # RPM VALUE
            value_text = self.font.render(f" {self.current_value}", True, BLACK)
            self.screen.blit(value_text, (222, 196))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    app = CustomGauge()
    app.run()
