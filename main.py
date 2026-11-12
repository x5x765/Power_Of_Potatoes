import pygame
import socket
import json
import sys
import random
from helpers import Level, PhysicsController

# Game Settings & Network Targeting
WIDTH, HEIGHT = 1920, 1080
FPS = 20  # 50ms intervals
SERVER_IP = "192.168.4.1"
SERVER_PORT = 5005
PLAYER_ID = f"Player_{random.randint(1000, 9999)}" # Unique identifier

# Initialize Network Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False) # Non-blocking so networking doesn't freeze frame updates

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"ESP32 Multi-Player Game - {PLAYER_ID}")
clock = pygame.time.Clock()

# Local Player State
player_x, player_y = 100, 100
current_frame = 0
all_players_data = {}

running = True
while running:
    # 1. Handle Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  player_x -= 5
    if keys[pygame.K_RIGHT]: player_x += 5
    if keys[pygame.K_UP]:    player_y -= 5
    if keys[pygame.K_DOWN]:  player_y += 5
    if keys[pygame.K_ESCAPE]: running = False

    # Cycle animation frame index dummy tracker
    #current_frame = (current_frame+1)%4

    # 2. Transmit Local State to ESP32
    local_data = {
        "id": PLAYER_ID,
        "x": player_x,
        "y": player_y,
        "frame": current_frame
    }
    try:
        payload = json.dumps(local_data).encode('utf-8')
        client_socket.sendto(payload, (SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(f"Send Error: {e}")

    # 3. Receive Global State Update from ESP32
    try:
        # Drain the network buffer to get the absolute newest packet
        while True:
            data, addr = client_socket.recvfrom(2048)
            all_players_data = json.loads(data.decode('utf-8'))
    except BlockingIOError:
        # Thrown when buffer becomes empty. This is expected.
        pass
    except Exception as e:
        print(f"Receive Error: {e}")

    # 4. Render Scene
    screen.fill((30, 30, 30)) # Dark gray background
    screen.blit(level.levelImage)

    # Draw all players received from server network states
    for pid, data in all_players_data.items():
        x = data.get("x", 0)
        y = data.get("y", 0)
        frame = data.get("frame", 0)

        # Distinguish local player from opponents visually
        color = (0, 255, 0) if pid == PLAYER_ID else (0, 100, 255)
        pygame.draw.circle(screen, color, (x, y), 20)
        
        # Display Text Info overhead
        font = pygame.font.SysFont(None, 20)
        img = font.render(f"{pid} (F:{frame})", True, (255, 255, 255))
        screen.blit(img, (x - 30, y - 40))

    pygame.display.flip()
    clock.tick(FPS) # Locks the Pygame loop securely at 20 frames per second

pygame.quit()
sys.exit()
