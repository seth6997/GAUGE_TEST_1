import pygame
import time  # Import the time module

# DISPLAY SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# COLORS USED
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class speed_gauge:
    def __init__(self, custom_gauge):
        self.value = 0
        self.target_value = 0
        self.up_pressed = False
        self.decrement_step = 1  # DECREMENT STEP SIZE FOR "SLOWING DOWN"
        self.custom_gauge = custom_gauge
        self.max_speeds = [30, 62, 97, 120, 160]  # MAX SPEED IN EACH GEAR

    def update(self):
        if self.up_pressed:
            self.target_value = min(self.target_value + 2, self.max_speeds[self.custom_gauge.current_gear - 1])
        else:
            self.target_value = max(self.target_value - self.decrement_step, 0)  # DECREMENT STEP VALUE

        if self.value < self.target_value:
            self.value = min(self.value + 2, self.target_value)
        elif self.value > self.target_value:
            self.value = max(self.value - 1, self.target_value)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.up_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.up_pressed = False


class CustomGauge:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Custom Gauge")
        self.clock = pygame.time.Clock()

        # STATIC CUSTOM GAUGE BACKGROUND
        self.background_image = pygame.image.load("images/GAUGE_BG.png").convert_alpha()

        # BRING ALL CUSTOM RPM IMAGE LAYERS INTO A CALLABLE LIST
        self.rectangle_images = []
        for i in range(1, 31):
            filename = f"images/RECTANGLE_{i}.png"
            image = pygame.image.load(filename).convert_alpha()
            self.rectangle_images.append(image)

        # INIT VALUE
        self.current_value = 0

        # INDEXING THE LAST RENDERED RECTANGLE FROM THE CUSTOM IMAGES FOLDER
        self.last_displayed_index = -1

        # KEY BIND INIT
        self.up_pressed = False
        self.down_pressed = False

        # FONT SETTINGS
        self.font = pygame.font.Font(None, 68)

        # RENDER SPEED GAUGE
        self.number_gauge = speed_gauge(self)

        # GEAR INIT TO 1ST GEAR
        self.current_gear = 1

        # Variable to track time when speed is 160
        self.timer_start = None

    def increase_value(self):
        # INCREASE RPM
        if self.current_value < 4000:
            self.current_value = min(self.current_value + 266, 8000)
        else:
            # WHEN RPM IS GREATER THAN 4000, INCREASE EXPONENTIALLY TO THE LIMIT OF 8000
            increment = 266 + (self.current_value - 4000) // 20
            self.current_value = min(self.current_value + increment, 8000)

    def decrease_value(self):
        # DECREASE THE RPM
        self.current_value = max(self.current_value - 150, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # PASS EVENTS (UP KEY FOR SPEED/RPM AND U/J FOR SHIFTING)
            self.number_gauge.handle_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.up_pressed = True
                elif event.key == pygame.K_u:  # SHIFT UP WITH U
                    self.shift_up()
                elif event.key == pygame.K_j:  # SHIFT DOWN WITH J
                    self.shift_down()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.up_pressed = False
        return True

    def shift_up(self):
        if self.current_gear < 5:
            self.current_gear += 1
            # SIMULATE AN UP SHIFT
            self.current_value = 2000

    def shift_down(self):
        if self.current_gear > 1:
            self.current_gear -= 1
            # SIMULATE A DOWN SHIFT
            self.current_value = 4000

    def run(self):
        running = True
        show_warning = False  # Variable to track if warning should be displayed
        while running:
            running = self.handle_events()

            # IF SPEED IS 160 FOR 3 SECONDS, START TIMER
            if self.number_gauge.value == 160:
                if self.timer_start is None:
                    self.timer_start = time.time()
                else:
                    # CHECK FOR THREE SECOND TRIGGER
                    elapsed_time = time.time() - self.timer_start
                    if elapsed_time >= 3:
                        # Set the flag to display the warning message
                        show_warning = True
            else:
                # Reset the timer and hide the warning message
                self.timer_start = None
                show_warning = False

            # KEEP UPDATING RPM
            if self.up_pressed:
                self.increase_value()
            else:
                self.current_value = max(self.current_value - 50, 0)

            # KEEP UPDATING SPEED
            self.number_gauge.update()

            # BG COLOR
            self.screen.fill(BLACK)

            # SHOW CUSTOM GAUGE
            self.screen.blit(self.background_image, (0, 0))

            # RENDER EACH CUSTOM RECTANGLE LAYER
            num_rectangles = min(self.current_value // 266 + 1, len(self.rectangle_images))

            # SHOW TOTAL RECTANGLES FOR VALUE OF RPM
            for i in range(len(self.rectangle_images)):
                if i < num_rectangles:
                    self.screen.blit(self.rectangle_images[i], (0, 0))
                else:
                    break

            # RPM VALUE
            if self.current_value >= 0:
                value_text = self.font.render(f" {self.current_value}", True, BLACK)
            else:
                value_text = self.font.render(" 0", True, BLACK)  # SET TO 0 IF NEGATIVE
            self.screen.blit(value_text, (222, 196))

            # SHOW SPEED VALUE
            number_text = self.font.render(f" {self.number_gauge.value}", True, BLACK)
            self.screen.blit(number_text, (200, 320))  # SPEED TEXT LOCATION

            # SHOW CURRENT GEAR
            gear_text = self.font.render(f"Gear: {self.current_gear}", True, WHITE)
            self.screen.blit(gear_text, (30, 10))

            # Render the warning message if the flag is set
            if show_warning:
                warning_text = self.font.render("WARNING!! DANGER TO MANIFOLD!", True, RED)
                warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(warning_text, warning_rect)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    app = CustomGauge()
    app.run()
