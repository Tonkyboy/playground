# Pygame Tetris - Fancy Edition (v2 - Mac Fix Attempt)
# Built for Pyodide compatibility (no external files for sounds/fonts initially)

import pygame
import random
import math
import time
import sys

# Try importing numpy for sound generation, handle potential ImportError
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Warning: Numpy not found. Sound effects will be disabled.")

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # 10 blocks wide
PLAY_HEIGHT = 600 # 20 blocks high
BLOCK_SIZE = 30

GRID_TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
GRID_TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50 # Position grid lower

GRID_LINE_COLOR = (40, 40, 60)
GRID_BG_COLOR = (10, 10, 20)
BACKGROUND_COLOR = (20, 20, 30)
UI_AREA_COLOR = (30, 30, 45) # Area around playfield

# Tetromino Shapes (Standard SRS)
S = [[(0, 1), (0, 2), (1, 0), (1, 1)], [(0, 1), (1, 1), (1, 2), (2, 2)], [(2, 0), (2, 1), (1, 1), (1, 2)], [(0, 0), (1, 0), (1, 1), (2, 1)]] # Added 2 rotations for SRS
Z = [[(0, 0), (0, 1), (1, 1), (1, 2)], [(0, 2), (1, 1), (1, 2), (2, 1)], [(2, 1), (2, 2), (1, 0), (1, 1)], [(0, 1), (1, 0), (1, 1), (2, 0)]] # Added 2 rotations for SRS
I = [[(1, 0), (1, 1), (1, 2), (1, 3)], [(0, 2), (1, 2), (2, 2), (3, 2)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(0, 1), (1, 1), (2, 1), (3, 1)]] # Added 2 rotations for SRS
O = [[(0, 1), (0, 2), (1, 1), (1, 2)]] # O only has 1 rotation state
T = [[(0, 1), (1, 0), (1, 1), (1, 2)], # 0
     [(0, 1), (1, 1), (1, 2), (2, 1)], # R
     [(1, 0), (1, 1), (1, 2), (2, 1)], # 2
     [(0, 1), (1, 0), (1, 1), (2, 1)]] # L
L = [[(0, 2), (1, 0), (1, 1), (1, 2)], # 0
     [(0, 1), (1, 1), (2, 1), (2, 2)], # R
     [(1, 0), (1, 1), (1, 2), (2, 0)], # 2
     [(0, 0), (0, 1), (1, 1), (2, 1)]] # L
J = [[(0, 0), (1, 0), (1, 1), (1, 2)], # 0
     [(0, 1), (0, 2), (1, 1), (2, 1)], # R
     [(1, 0), (1, 1), (1, 2), (2, 2)], # 2
     [(0, 1), (1, 1), (2, 0), (2, 1)]] # L

# List of shapes and their base colors + glow colors
SHAPES = [S, Z, I, O, T, L, J]
SHAPE_COLORS = [
    ((0, 255, 255), (180, 255, 255)), # I - Cyan / Light Cyan
    ((255, 255, 0), (255, 255, 180)), # O - Yellow / Light Yellow
    ((160, 0, 255), (220, 150, 255)), # T - Purple / Light Purple
    ((0, 255, 0), (180, 255, 180)), # S - Green / Light Green
    ((255, 0, 0), (255, 150, 150)), # Z - Red / Light Red
    ((0, 0, 255), (150, 150, 255)), # J - Blue / Light Blue
    ((255, 165, 0), (255, 210, 150)), # L - Orange / Light Orange
]

# Other game settings
FALL_SPEED_INITIAL = 0.4 # seconds per grid step
FALL_SPEED_FAST = 0.05
FALL_SPEED_LEVEL_MULTIPLIER = 0.85 # Speed increases by this factor per level
LINES_PER_LEVEL = 10
SCORE_PER_LINE = [0, 100, 300, 500, 800] # Score for 0, 1, 2, 3, 4 lines cleared
SCORE_SOFT_DROP_BONUS = 1 # Points per grid cell soft-dropped
SCORE_HARD_DROP_BONUS = 2 # Points per grid cell hard-dropped

# Animation timings
LOCK_DELAY = 0.5 # seconds before locking after landing
SCORE_ANIMATION_DURATION = 0.5 # seconds
GAME_OVER_FADE_DURATION = 1.5 # seconds

# Movement handling delays
DAS_DELAY = 0.16 # Delayed Auto Shift - seconds before continuous horizontal move
ARR_DELAY = 0.03 # Auto Repeat Rate - seconds between moves during DAS

# Sound Frequencies (simple tones)
FREQ_LAND = 100
FREQ_CLEAR = 440
FREQ_MULTI_CLEAR = 660
FREQ_LEVEL_UP = 880
FREQ_GAME_OVER = [200, 150, 100, 50]
FREQ_ROTATE = 300
FREQ_HARD_DROP = 150

# --- Pygame Initialization ---
pygame.init()
# Attempt initializing mixer, handle potential failure
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512) # Smaller buffer for less latency
    MIXER_INITIATED = True
except pygame.error as e:
    print(f"Warning: Pygame mixer could not be initiated: {e}. Sound disabled.")
    MIXER_INITIATED = False


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Tetris - Fancy Edition")
clock = pygame.time.Clock()

# --- Font ---
# Fallback included directly in SysFont call
main_font = pygame.font.SysFont("consolas, mono,arial", 35, bold=True)
score_font = pygame.font.SysFont("consolas, mono, arial", 50, bold=True)
small_font = pygame.font.SysFont("consolas, mono, arial", 25)
game_over_font = pygame.font.SysFont("consolas, mono, arial", 70, bold=True)


# --- Sound Generation ---
SOUND_ENABLED = NUMPY_AVAILABLE and MIXER_INITIATED
sound_cache = {}

def generate_tone(frequency, duration_ms, vol=0.1):
    if not SOUND_ENABLED:
        # Create a dummy sound object if sound is disabled
        return pygame.mixer.Sound(buffer=np.array([[0,0]], dtype=np.int16)) # Minimal valid buffer

    sound_key = (frequency, duration_ms)
    if sound_key in sound_cache:
        return sound_cache[sound_key]

    try:
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * duration_ms / 1000.0)

        buf = np.zeros((num_samples, 2), dtype=np.int16) # Stereo
        max_sample = 2**(16 - 1) - 1

        # Simple sine wave
        t = np.linspace(0., duration_ms / 1000.0, num_samples)
        wave = (vol * max_sample * np.sin(2. * np.pi * frequency * t)).astype(np.int16)
        
        # Basic fade in/out to reduce clicks
        fade_len = min(num_samples // 10, sample_rate // 100) # ~10ms fade max
        if fade_len > 1:
            fade_in = np.linspace(0., 1., fade_len)
            fade_out = np.linspace(1., 0., fade_len)
            wave[:fade_len] = (wave[:fade_len] * fade_in).astype(np.int16)
            wave[-fade_len:] = (wave[-fade_len:] * fade_out).astype(np.int16)

        buf[:, 0] = wave
        buf[:, 1] = wave # Copy to right channel for stereo

        sound = pygame.sndarray.make_sound(buf)
        sound_cache[sound_key] = sound
        return sound
    except Exception as e:
        print(f"Error generating tone {frequency}Hz: {e}")
        # Return dummy sound on error during generation
        return pygame.mixer.Sound(buffer=np.array([[0,0]], dtype=np.int16))

def generate_sequence(freq_list, duration_ms_per_note, vol=0.1):
    if not SOUND_ENABLED:
        return pygame.mixer.Sound(buffer=np.array([[0,0]], dtype=np.int16))

    sound_key = (tuple(freq_list), duration_ms_per_note)
    if sound_key in sound_cache:
        return sound_cache[sound_key]

    try:
        sample_rate = pygame.mixer.get_init()[0]
        num_samples_per_note = int(sample_rate * duration_ms_per_note / 1000.0)
        total_samples = num_samples_per_note * len(freq_list)

        if total_samples == 0: # Avoid creating zero-length buffer
             return pygame.mixer.Sound(buffer=np.array([[0,0]], dtype=np.int16))

        buf = np.zeros((total_samples, 2), dtype=np.int16)
        max_sample = 2**(16 - 1) - 1
        current_sample = 0

        for frequency in freq_list:
            if frequency <= 0: # Pause
                chunk_mono = np.zeros(num_samples_per_note, dtype = np.int16)
            else:
                t = np.linspace(0., duration_ms_per_note / 1000.0, num_samples_per_note, endpoint=False)
                chunk_mono = (vol * max_sample * np.sin(2. * np.pi * frequency * t)).astype(np.int16)

            # Apply fade in/out to each note chunk
            fade_len = min(num_samples_per_note // 10, sample_rate // 100)
            if fade_len > 1 and frequency > 0: # Only fade actual notes
                fade_in = np.linspace(0., 1., fade_len)
                fade_out = np.linspace(1., 0., fade_len)
                chunk_mono[:fade_len] = (chunk_mono[:fade_len] * fade_in).astype(np.int16)
                chunk_mono[-fade_len:] = (chunk_mono[-fade_len:] * fade_out).astype(np.int16)

            chunk = np.column_stack((chunk_mono, chunk_mono)) # Stereo
            if current_sample + num_samples_per_note <= total_samples:
                 buf[current_sample:current_sample + num_samples_per_note] = chunk
            current_sample += num_samples_per_note


        sound = pygame.sndarray.make_sound(buf)
        sound_cache[sound_key] = sound
        return sound

    except Exception as e:
        print(f"Error generating sequence starting {freq_list[0]}Hz: {e}")
        return pygame.mixer.Sound(buffer=np.array([[0,0]], dtype=np.int16))

# Pre-generate sounds if possible
sound_land = None
sound_clear = None
sound_multi_clear = None
sound_game_over = None
sound_rotate = None
sound_hard_drop = None

if SOUND_ENABLED:
    print("Attempting to generate sound effects...")
    sound_land = generate_tone(FREQ_LAND, 75, vol=0.08)
    sound_clear = generate_tone(FREQ_CLEAR, 150, vol=0.1)
    sound_multi_clear = generate_tone(FREQ_MULTI_CLEAR, 250, vol=0.12)
    sound_game_over = generate_sequence(FREQ_GAME_OVER, 300, vol=0.15)
    sound_rotate = generate_tone(FREQ_ROTATE, 50, vol=0.06)
    sound_hard_drop = generate_tone(FREQ_HARD_DROP, 100, vol=0.09)
    print("Sound effects generated.")
else:
     print("Sound disabled (Numpy missing or Mixer init failed).")


# --- Game State Variables ---
grid = None
locked_blocks = {} # Initialize as empty dict
current_piece = None
next_piece = None
score = 0
level = 1
lines_cleared_total = 0
fall_time = 0
fall_speed = FALL_SPEED_INITIAL
current_piece_y_float = 0.0 # For smooth falling animation
last_fall_time = 0
last_lock_time = 0
landed = False # Is the current piece touching down?

game_state = "start" # "start", "playing", "paused", "game_over"
game_over_start_time = 0
last_score = 0
score_update_time = 0

# Movement control timers
last_move_time = {"left": 0, "right": 0, "down": 0}
move_key_held = {"left": False, "right": False, "down": False}
das_triggered = {"left": False, "right": False}

# Bag randomizer for pieces
piece_bag = []

# --- Helper Functions ---

def create_grid(locked_pos={}):
    g = [[GRID_BG_COLOR for _ in range(10)] for _ in range(20)]
    for r in range(len(g)):
        for c in range(len(g[r])):
            if (r, c) in locked_pos:
                g[r][c] = locked_pos[(r, c)][0] # Store base color
    return g

def get_shape():
    global piece_bag
    if not piece_bag:
        piece_bag = list(range(len(SHAPES)))
        random.shuffle(piece_bag)

    shape_index = piece_bag.pop()
    shape = SHAPES[shape_index]
    color, glow_color = SHAPE_COLORS[shape_index]
    start_col = 10 // 2 - 2

    return {
        'x': start_col,
        'y': 0, # Start at row 0 (top)
        'shape': shape,
        'color': color,
        'glow_color': glow_color,
        'rotation': 0
    }

def draw_block(surface, color, glow_color, x, y, size, shadow=False):
    border_thickness = max(1, int(size * 0.08)) # Thinner border
    inner_size = size - border_thickness * 2

    # 1. Subtle shadow
    if shadow:
        shadow_offset = max(1, int(size * 0.1))
        shadow_color = (0, 0, 0, 70) # Less opaque shadow
        shadow_rect = pygame.Rect(x + shadow_offset, y + shadow_offset, size, size)
        shadow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, shadow_color, (0, 0, size, size), border_radius=int(border_thickness * 1.5))
        surface.blit(shadow_surf, shadow_rect.topleft)

    # 2. Glow border (drawn slightly larger)
    glow_radius = border_thickness + 1
    glow_rect = pygame.Rect(x - glow_radius // 2, y - glow_radius // 2 , size + glow_radius, size + glow_radius)
    glow_surf = pygame.Surface((size + glow_radius, size+glow_radius), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, glow_color + (100,), (0,0,size+glow_radius, size+glow_radius), border_radius=int(border_thickness * 1.8)) # More alpha for glow, rounder corners
    surface.blit(glow_surf, glow_rect.topleft)

    # 3. Main block base color
    base_rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surface, tuple(c//2 for c in color), base_rect, border_radius=border_thickness) # Slightly darker base

    # 4. Inner color with gradient effect
    inner_rect = pygame.Rect(x + border_thickness, y + border_thickness, inner_size, inner_size)
    # Simple top-to-bottom gradient illusion
    top_color = tuple(min(255, c + 50) for c in color)
    bottom_color = color
    pygame.draw.rect(surface, top_color, inner_rect, border_radius=border_thickness//2)
    highlight_rect = pygame.Rect(inner_rect.left, inner_rect.top + inner_rect.height*0.4, inner_rect.width, inner_rect.height*0.6)
    pygame.draw.rect(surface, bottom_color, highlight_rect, border_radius=border_thickness//2)

def get_formatted_shape(piece):
    positions = []
    if not piece or not piece.get('shape'): # Safety check
         return positions
    shape_format = piece['shape'][piece['rotation'] % len(piece['shape'])]
    for (r_off, c_off) in shape_format:
        positions.append((piece['y'] + r_off, piece['x'] + c_off))
    return positions

def is_valid_position(piece, grid_data, adj_x=0, adj_y=0, adj_rot=0):
    if piece is None: return False # Safety check
    
    potential_piece = piece.copy()
    potential_piece['x'] += adj_x
    potential_piece['y'] += adj_y
    # Ensure 'shape' key exists before accessing length
    if 'shape' in piece:
        potential_piece['rotation'] = (piece.get('rotation', 0) + adj_rot) % len(piece['shape'])
    else:
        return False # Cannot validate if shape is missing

    formatted = get_formatted_shape(potential_piece)
    if not formatted: return False # If shape was invalid

    for r, c in formatted:
        # Check bounds strictly
        if not (0 <= c < 10): return False
        if not (0 <= r < 20): # Check if below grid first
             if r >= 20 : return False # Strictly cannot be below line 20
             if r < 0: # Allow pieces partially above the screen during rotation/spawn? Yes.
                 pass # Valid to be temporarily above grid

        # Check collision with locked blocks (only for rows >= 0)
        if r >= 0:
             try:
                # Check if cell exists before accessing
                 if grid_data[r][c] != GRID_BG_COLOR:
                    return False # Collision
             except IndexError:
                 print(f"Warning: Grid index out of range access: r={r}, c={c}")
                 return False # Treat index error as invalid

    return True

def check_lost(locked_pos):
    for r, c in locked_pos:
        if r < 0: # Check if any part locked above visible area
            return True # Standard Tetris loses if piece locks and overlaps spawn area (usually r=0 or 1)
    return False

def clear_lines(grid_data, locked_pos):
    lines_to_clear = []
    for r in range(19, -1, -1):
        is_full = all(grid_data[r][c] != GRID_BG_COLOR for c in range(10))
        if is_full:
            lines_to_clear.append(r)

    num_cleared = len(lines_to_clear)

    if num_cleared > 0:
        if SOUND_ENABLED:
            try:
                if num_cleared >= 4: sound_multi_clear.play()
                else: sound_clear.play()
            except AttributeError: pass # Ignore if sound obj is None

        lines_to_clear_set = set(lines_to_clear)
        cleared_rows_sorted = sorted(list(lines_to_clear_set), reverse=True)

        # More robust way to create new locked_pos by shifting down
        new_locked = {}
        for r, c in sorted(locked_pos.keys()): # Iterate sorted by row
             if r not in lines_to_clear_set:
                 shift_amount = sum(1 for cleared_r in cleared_rows_sorted if r < cleared_r)
                 new_locked[(r + shift_amount, c)] = locked_pos[(r, c)]

        return num_cleared, new_locked
    else:
        return 0, locked_pos

def draw_text(surface, text, font, color, x, y, center=True):
    label = font.render(text, True, color)
    if center:
        pos = label.get_rect(center=(x, y))
    else:
        pos = label.get_rect(topleft=(x, y))
    surface.blit(label, pos)

def draw_grid(surface, grid_data):
    for r in range(20):
        pygame.draw.line(surface, GRID_LINE_COLOR,
                         (GRID_TOP_LEFT_X, GRID_TOP_LEFT_Y + r * BLOCK_SIZE),
                         (GRID_TOP_LEFT_X + PLAY_WIDTH, GRID_TOP_LEFT_Y + r * BLOCK_SIZE), 1) # Thinner lines
    for c in range(11):
        pygame.draw.line(surface, GRID_LINE_COLOR,
                         (GRID_TOP_LEFT_X + c * BLOCK_SIZE, GRID_TOP_LEFT_Y),
                         (GRID_TOP_LEFT_X + c * BLOCK_SIZE, GRID_TOP_LEFT_Y + PLAY_HEIGHT), 1) # Thinner lines

def draw_next_piece(surface, piece):
    if piece is None: return # Safety check
    draw_text(surface, "NEXT", small_font, (200, 200, 220), GRID_TOP_LEFT_X + PLAY_WIDTH + 80, GRID_TOP_LEFT_Y + 30, center=True)
    sx = GRID_TOP_LEFT_X + PLAY_WIDTH + 80 # Center in the side panel area more accurately
    sy = GRID_TOP_LEFT_Y + 100

    shape_format = piece['shape'][0]
    min_r = min(r for r, c in shape_format)
    max_r = max(r for r, c in shape_format)
    min_c = min(c for r, c in shape_format)
    max_c = max(c for r, c in shape_format)
    shape_h = (max_r - min_r + 1) * BLOCK_SIZE
    shape_w = (max_c - min_c + 1) * BLOCK_SIZE

    start_draw_x = sx - shape_w // 2
    start_draw_y = sy - shape_h // 2

    for r_off, c_off in shape_format:
         draw_block(surface, piece['color'], piece['glow_color'],
                    start_draw_x + (c_off - min_c) * BLOCK_SIZE,
                    start_draw_y + (r_off - min_r) * BLOCK_SIZE, BLOCK_SIZE * 0.8) # Draw slightly smaller in preview


def draw_score_level(surface, score_val, level_val, lines_val, animated=False):
    score_label_y = GRID_TOP_LEFT_Y + PLAY_HEIGHT // 2 - 80 # Move up
    score_text = f"{score_val:07d}"
    score_color = (220, 220, 255)
    current_font = score_font

    if animated: # Fancy score animation
        anim_progress = min(1, (time.time() - score_update_time) / SCORE_ANIMATION_DURATION)
        # Lerp color from yellow back to white
        flash_color = (255, 255, 0)
        score_color = tuple(int(flash + (normal - flash) * anim_progress) for flash, normal in zip(flash_color, score_color))
        # Scale font size (requires rendering a new font object potentially, or pre-rendering sizes)
        # Simple: Just use color flash
        
    ui_side_x = GRID_TOP_LEFT_X // 2 # Position in left panel

    draw_text(surface, "SCORE", small_font, (200, 200, 220), ui_side_x, score_label_y - 40, center=True)
    draw_text(surface, score_text, current_font, score_color, ui_side_x, score_label_y, center=True)

    level_label_y = score_label_y + 100
    draw_text(surface, "LEVEL", small_font, (200, 200, 220), ui_side_x, level_label_y - 30, center=True)
    draw_text(surface, str(level_val), main_font, (220, 220, 255), ui_side_x, level_label_y, center=True)

    lines_label_y = level_label_y + 100
    draw_text(surface, "LINES", small_font, (200, 200, 220), ui_side_x, lines_label_y - 30, center=True)
    draw_text(surface, str(lines_val), main_font, (220, 220, 255), ui_side_x, lines_label_y, center=True)


def draw_game_over(surface, alpha):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, int(alpha)))
    surface.blit(overlay, (0, 0))

    if alpha > 150:
        draw_text(surface, "GAME OVER", game_over_font, (255, 50, 50), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        draw_text(surface, "Press ENTER to Play Again", main_font, (200, 200, 220), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)

def draw_window(surface, grid_data, locked_data, current_p, next_p, score_val, level_val, lines_val, game_state, game_over_alpha, score_anim_active):
    # 1. Backgrounds
    surface.fill(BACKGROUND_COLOR)
    # Draw a subtle gradient for the UI background?
    bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    # pygame.draw.rect(surface, UI_AREA_COLOR, bg_rect) # Simple fill

    # Fancy gradient background attempt
    top_color = (15, 15, 25)
    bottom_color = (35, 35, 55)
    for y in range(SCREEN_HEIGHT):
         ratio = y / SCREEN_HEIGHT
         color = tuple(int(top + (bottom - top) * ratio) for top, bottom in zip(top_color, bottom_color))
         pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))


    play_area_rect = pygame.Rect(GRID_TOP_LEFT_X, GRID_TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT)
    pygame.draw.rect(surface, GRID_BG_COLOR, play_area_rect) # Playfield background

    # 2. Locked Blocks
    for (r, c), (color, glow_color) in locked_data.items():
        if 0 <= r < 20: # Only draw visible locked blocks
             draw_block(surface, color, glow_color,
                        GRID_TOP_LEFT_X + c * BLOCK_SIZE,
                        GRID_TOP_LEFT_Y + r * BLOCK_SIZE, BLOCK_SIZE)

    # 3. Grid Lines (on top of locked blocks)
    draw_grid(surface, grid_data)
    pygame.draw.rect(surface, GRID_LINE_COLOR, play_area_rect, 3) # Border

    # 4. Falling Piece Ghost (Drop Shadow)
    if game_state == "playing" and current_p:
        ghost_p = current_p.copy()
        ghost_valid = True
        while ghost_valid:
            if not is_valid_position(ghost_p, grid_data, adj_y=1):
                ghost_valid = False # Found the final valid spot above obstacle/floor
            else:
                ghost_p['y'] +=1
        
        ghost_shape_pos = get_formatted_shape(ghost_p)
        ghost_color = (80, 80, 80, 100) # Semi-transparent gray
        
        for r, c in ghost_shape_pos:
             if r >= 0: # Only draw ghost within grid bounds
                ghost_rect = pygame.Rect(GRID_TOP_LEFT_X + c * BLOCK_SIZE,
                                      GRID_TOP_LEFT_Y + r * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE)
                # Draw simpler rectangle for ghost
                ghost_surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(ghost_surf, ghost_color, (0,0, BLOCK_SIZE, BLOCK_SIZE), border_radius=2)
                pygame.draw.rect(ghost_surf, (200,200,200, 120), (1,1, BLOCK_SIZE-2, BLOCK_SIZE-2), 1, border_radius=2) # Thin border
                surface.blit(ghost_surf, ghost_rect.topleft)


    # 5. Falling Piece (Actual)
    if game_state == "playing" and current_p:
        render_y_pixel = GRID_TOP_LEFT_Y + current_piece_y_float * BLOCK_SIZE
        shape_pos = get_formatted_shape(current_p)

        for r, c in shape_pos:
            block_pixel_y = render_y_pixel + (r - current_p['y']) * BLOCK_SIZE # Calculate individual block y pixel
            # Only draw blocks vertically within visible playfield or slightly above
            if block_pixel_y > GRID_TOP_LEFT_Y - BLOCK_SIZE:
                draw_block(surface, current_p['color'], current_p['glow_color'],
                           GRID_TOP_LEFT_X + c * BLOCK_SIZE,
                           block_pixel_y,
                           BLOCK_SIZE,
                           shadow=True) # Add shadow effect to falling piece


    # 6. UI Elements
    draw_next_piece(surface, next_p)
    draw_score_level(surface, score_val, level_val, lines_val, score_anim_active)
    draw_text(surface, "FANCY TETRIS", main_font, (180, 180, 220), SCREEN_WIDTH // 2, 35, center=True) # Adjusted Y pos

    # 7. Game Over Screen / Pause Screen
    if game_state == "game_over":
        draw_game_over(surface, game_over_alpha)
    elif game_state == "paused":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # Dark overlay for pause
        surface.blit(overlay, (0,0))
        draw_text(surface, "PAUSED", game_over_font, (220, 220, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)


    # --- Update display ---
    pygame.display.flip()

# --- Game Logic Functions ---

def handle_input(current_p, grid_data):
    global current_piece_y_float, score, game_state, fall_time, landed, last_lock_time, fall_speed
    current_time = time.time()
    modified = False # Track if piece position/rotation changed by input

    # Check for quit events first
    for event in pygame.event.get(eventtype=[pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP]):
        if event.type == pygame.QUIT:
             pygame.event.post(event) # Put it back for the main loop to handle exit
             return fall_speed # Return current speed, don't process further inputs if quitting

        if event.type == pygame.KEYDOWN:
            key = event.key
            if key in (pygame.K_UP, pygame.K_x): # Rotate Clockwise
                 if is_valid_position(current_p, grid_data, adj_rot=1):
                     current_p['rotation'] = (current_p['rotation'] + 1) % len(current_p['shape'])
                     if SOUND_ENABLED: safe_play(sound_rotate)
                     modified = True
                     # Wall kick logic could go here if implemented
            elif key == pygame.K_SPACE: # Hard Drop
                drop_amount = 0
                temp_p = current_p.copy()
                while is_valid_position(temp_p, grid_data, adj_y=1):
                    temp_p['y'] += 1
                    drop_amount += 1
                if drop_amount > 0:
                    current_p['y'] = temp_p['y']
                    current_piece_y_float = float(current_p['y']) # Snap float pos
                    score += drop_amount * SCORE_HARD_DROP_BONUS
                    modified = True # Movement occurred
                    # Force immediate lock check on next logic update:
                    landed = True # Consider it landed for logic
                    fall_time = fall_speed + LOCK_DELAY + 0.1 # Force fall check & lock check to pass immediately
                    if SOUND_ENABLED: safe_play(sound_hard_drop)
            elif key == pygame.K_p: # Pause
                 if game_state == "playing": game_state = "paused"
                 elif game_state == "paused": game_state = "playing"
                 # Need to reset time anchors after unpausing - handled in main loop potentially
                 last_fall_time = current_time # Reset timer anchor on pause/unpause
            elif key == pygame.K_LEFT:
                 move_key_held["left"] = True
                 das_triggered["left"] = False
                 last_move_time["left"] = current_time # Record initial press time
                 if is_valid_position(current_p, grid_data, adj_x=-1):
                     current_p['x'] -= 1
                     modified = True
            elif key == pygame.K_RIGHT:
                 move_key_held["right"] = True
                 das_triggered["right"] = False
                 last_move_time["right"] = current_time
                 if is_valid_position(current_p, grid_data, adj_x=1):
                     current_p['x'] += 1
                     modified = True
            elif key == pygame.K_DOWN:
                 move_key_held["down"] = True
                 last_move_time["down"] = current_time
                 # Faster falling speed handled below, process one step immediately?
                 if is_valid_position(current_p, grid_data, adj_y=1):
                     # Move down one step immediately on press for responsiveness
                     current_p['y'] += 1
                     current_piece_y_float = float(current_p['y'])
                     score += SCORE_SOFT_DROP_BONUS
                     fall_time = 0 # Reset fall timer after manual move
                     modified = True


        elif event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_LEFT: move_key_held["left"] = False
            elif key == pygame.K_RIGHT: move_key_held["right"] = False
            elif key == pygame.K_DOWN: move_key_held["down"] = False


    # Continuous movement handling (DAS/ARR) - run even if KEYDOWN didn't fire this exact frame
    current_fall_speed_used = FALL_SPEED_FAST if move_key_held["down"] else fall_speed

    # Horizontal Movement
    for direction, key_code in [("left", -1), ("right", 1)]:
        if move_key_held[direction]:
            elapsed_since_last = current_time - last_move_time[direction]
            
            # Check DAS first (only trigger DAS movement after delay)
            if not das_triggered[direction] and elapsed_since_last >= DAS_DELAY:
                 das_triggered[direction] = True
                 last_move_time[direction] = current_time # Reset timer for first ARR check
                 if is_valid_position(current_p, grid_data, adj_x=key_code):
                     current_p['x'] += key_code
                     modified = True

            # Then check ARR (only trigger repeats if DAS is active and ARR time passed)
            elif das_triggered[direction] and elapsed_since_last >= ARR_DELAY:
                 last_move_time[direction] = current_time # Reset timer for next repeat
                 if is_valid_position(current_p, grid_data, adj_x=key_code):
                     current_p['x'] += key_code
                     modified = True

    # If any movement/rotation happened, potentially reset the lock timer if piece is now touching down
    if modified:
         reset_lock_delay(current_p, grid_data)

    return current_fall_speed_used

def safe_play(sound):
     """Utility to safely play a sound object that might be None."""
     if SOUND_ENABLED and sound is not None:
        try:
            sound.play()
        except AttributeError:
            pass # Ignore if sound is not a valid sound object
        except Exception as e:
             print(f"Error playing sound: {e}")


def reset_lock_delay(current_p, grid_data):
    """Resets the lock delay timer ONLY if the piece is touching down AFTER a move."""
    global last_lock_time, landed
    # Check if currently landed (cannot move down further)
    if not is_valid_position(current_p, grid_data, adj_y=1):
        last_lock_time = time.time() # Reset timer
        # 'landed' flag itself is set/unset during the main fall logic (update_game_state)
    # If piece is moved horizontally while landed, reset lock timer.


def update_game_state(current_p, next_p, grid_data, locked_pos, current_fall_spd):
    """Updates piece falling, locking, line clearing, spawning."""
    global fall_time, current_piece_y_float, score, level, lines_cleared_total, fall_speed
    global last_lock_time, landed, game_state, game_over_start_time
    global current_piece # Allow modification

    current_time = time.time()
    delta_time = current_time - last_fall_time
    # Clamp delta_time to prevent huge jumps after pause/lag
    delta_time = min(delta_time, 0.2) # Limit to 200ms max jump

    # DEBUG: Uncomment to watch timings
    # print(f"Delta: {delta_time:.4f}, Fall Time: {fall_time:.4f}, FloatY: {current_piece_y_float:.4f}, IntY: {current_p['y']}, Landed: {landed}, Speed: {current_fall_spd:.4f}")

    # Check if currently touching down
    is_touching_down = not is_valid_position(current_p, grid_data, adj_y=1)

    # --- Handle Locking ---
    if landed: # If the piece was flagged as landed previously...
        if is_touching_down: # ...and it's still touching down...
             # Check lock delay timer
             if current_time - last_lock_time >= LOCK_DELAY:
                 # --- LOCK THE PIECE ---
                 shape_pos = get_formatted_shape(current_p)
                 newly_locked = False
                 for r, c in shape_pos:
                     # Only lock blocks fully within the grid's bounds or at the top row
                     if 0 <= r < 20 and 0 <= c < 10:
                          locked_pos[(r, c)] = (current_p['color'], current_p['glow_color'])
                          newly_locked = True
                     elif r < 0 and 0 <= c < 10: # Locked piece partially above screen?
                          # Could signify game over depending on exact rules
                          locked_pos[(r, c)] = (current_p['color'], current_p['glow_color'])
                          newly_locked = True # Or maybe check_lost handles this later? Let's allow locking for now.


                 if not newly_locked: # Piece might have been moved/rotated off floor just before timer ended
                     landed = False # It's not actually locked
                     fall_time = 0 # Restart fall timer
                     # Keep going to falling logic...
                 else:
                    # --- POST-LOCK ACTIONS ---
                    grid_data = create_grid(locked_pos) # Update logical grid immediately
                    num_cleared, locked_pos = clear_lines(grid_data, locked_pos) # Check and clear lines

                    # Update score/level AFTER line clear
                    if num_cleared > 0:
                        score_bonus = SCORE_PER_LINE[min(num_cleared, len(SCORE_PER_LINE)-1)] * level
                        score += score_bonus
                        lines_cleared_total += num_cleared
                        new_level = (lines_cleared_total // LINES_PER_LEVEL) + 1
                        if new_level > level:
                            level = new_level
                            fall_speed = max(0.03, FALL_SPEED_INITIAL * (FALL_SPEED_LEVEL_MULTIPLIER ** (level - 1)))
                            # Play level up sound?
                            # safe_play(sound_level_up)


                    # --- CHECK GAME OVER CONDITION ---
                    if check_lost(locked_pos): # Check if locked pieces are too high
                         game_state = "game_over"
                         game_over_start_time = time.time()
                         safe_play(sound_game_over)
                         return current_p, next_p, create_grid(locked_pos), locked_pos # Exit state update


                    # --- SPAWN NEW PIECE ---
                    current_p = next_p # current becomes the previous next
                    next_p = get_shape() # Get a new next piece
                    current_piece_y_float = 0.0 # Reset float pos
                    fall_time = 0
                    landed = False
                    
                    # Check if new piece spawns in an invalid spot (immediate Game Over)
                    if not is_valid_position(current_p, create_grid(locked_pos)): # Check against updated grid
                         game_state = "game_over"
                         game_over_start_time = time.time()
                         safe_play(sound_game_over)
                         # Ensure the invalid piece is still assigned for drawing the final state? Yes.

                    # Return the new state after locking and spawning
                    return current_p, next_p, create_grid(locked_pos), locked_pos

        else: # Was landed, but now isn't touching down (moved/rotated off ledge)
             landed = False
             fall_time = 0 # Restart fall timer as it's now falling again

    # --- Handle Falling ---
    # If not locked or just became unlanded
    if not landed:
        fall_time += delta_time # Accumulate time based on frame delta

        # Calculate target Y position based purely on accumulated time
        # Add a tiny epsilon to handle float precision near integers
        potential_grid_steps = (fall_time / current_fall_spd)
        
        if potential_grid_steps >= 1.0: # Try to move down integer steps
            steps_to_try = int(potential_grid_steps)
            moved_steps = 0
            can_move_further = True

            for i in range(steps_to_try):
                if is_valid_position(current_p, grid_data, adj_y=1):
                    current_p['y'] += 1 # Move down one step
                    moved_steps += 1
                    # If soft dropping, add score
                    if move_key_held["down"] and current_fall_spd == FALL_SPEED_FAST:
                        score += SCORE_SOFT_DROP_BONUS
                else:
                    can_move_further = False # Hit something
                    break
            
            # Adjust accumulated fall time based on steps actually taken
            fall_time -= moved_steps * current_fall_spd
            fall_time = max(0, fall_time) # Prevent negative time

            # Now check if the piece has become landed *after* moving
            if not can_move_further:
                landed = True
                last_lock_time = time.time() # Start lock timer
                safe_play(sound_land)

            # Always sync float Y to integer Y after grid step movements
            current_piece_y_float = float(current_p['y'])

        else:
             # No full grid step occurred, just update smooth Y position
             # Interpolate based on remaining fall_time within the current step
             sub_step_progress = fall_time / current_fall_spd
             current_piece_y_float = float(current_p['y']) + sub_step_progress
        
        # Final check: Even if we didn't process steps this frame, re-check if now landed
        if not landed and not is_valid_position(current_p, grid_data, adj_y=1):
             landed = True
             last_lock_time = time.time() # Start timer
             # Play land sound only if wasn't already playing/triggered
             # (sound might have played if steps were processed above)
             # safe_play(sound_land) # Maybe redundant?


    # Update last fall time for the next frame's delta calculation
    # This needs careful placement. Do it outside the landed logic.
    # Should be updated every frame the playing state runs. Done in main loop now.

    return current_p, next_p, grid_data, locked_pos # Return state


def reset_game():
    """Resets all game variables to start a new game."""
    global grid, locked_blocks, current_piece, next_piece, score, level, lines_cleared_total
    global fall_time, fall_speed, current_piece_y_float, last_fall_time, last_lock_time, landed
    global game_state, last_score, score_update_time, piece_bag
    global move_key_held, das_triggered, last_move_time

    # print("--- RESETTING GAME ---") # DEBUG
    
    locked_blocks.clear() # Use clear() for existing dict
    grid = create_grid(locked_blocks)
    piece_bag.clear() # Clear and refill the bag
    current_piece = get_shape()
    next_piece = get_shape()
    current_piece_y_float = 0.0
    score = 0
    last_score = 0
    score_update_time = 0
    level = 1
    lines_cleared_total = 0
    fall_time = 0
    fall_speed = FALL_SPEED_INITIAL
    last_fall_time = time.time() # *** Crucial: Initialize time anchor ***
    last_lock_time = 0
    landed = False

    move_key_held = {"left": False, "right": False, "down": False}
    das_triggered = {"left": False, "right": False}
    last_move_time = {"left": 0, "right": 0, "down": 0}

    game_state = "playing"


# --- Main Game Loop ---
def main():
    global grid, locked_blocks, current_piece, next_piece, score, level, lines_cleared_total
    global fall_time, fall_speed, current_piece_y_float, last_fall_time, landed
    global game_state, game_over_start_time, last_score, score_update_time

    running = True
    reset_game() # Initialize variables FIRST
    game_state = "start" # THEN set to start screen state

    while running:
        current_time = time.time()

        # --- Event Pump (Important for responsiveness, call early) ---
        pygame.event.pump()

        # Get QUIT events separately to handle immediate exit
        for event in pygame.event.get(eventtype=pygame.QUIT):
            running = False
            break # Exit inner event loop
        if not running: continue # Go to next iteration of outer loop to exit

        # Create logical grid (needed for drawing & logic checks)
        # Could potentially optimize to only update when locked_blocks changes
        grid = create_grid(locked_blocks)

        # --- State Handling ---
        if game_state == "start":
             # Draw Start Screen (content is the same as before)
             screen.fill(BACKGROUND_COLOR)
             draw_text(screen, "FANCY TETRIS", game_over_font, (180, 180, 220), SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150, center=True)
             draw_text(screen, "Press ENTER to Start", main_font, (200, 200, 220), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, center=True)
             controls_y = SCREEN_HEIGHT // 2 + 40
             draw_text(screen, "Controls:", small_font, (180, 180, 220), SCREEN_WIDTH // 2, controls_y, center=True)
             draw_text(screen, "Left/Right: Move", small_font, (160, 160, 180), SCREEN_WIDTH // 2, controls_y + 30, center=True)
             draw_text(screen, "Up / X: Rotate", small_font, (160, 160, 180), SCREEN_WIDTH // 2, controls_y + 55, center=True)
             draw_text(screen, "Down: Soft Drop", small_font, (160, 160, 180), SCREEN_WIDTH // 2, controls_y + 80, center=True)
             draw_text(screen, "Space: Hard Drop", small_font, (160, 160, 180), SCREEN_WIDTH // 2, controls_y + 105, center=True)
             draw_text(screen, "P: Pause", small_font, (160, 160, 180), SCREEN_WIDTH // 2, controls_y + 130, center=True)
             pygame.display.flip()

             # Event handling ONLY for start screen keys
             for event in pygame.event.get(eventtype=pygame.KEYDOWN):
                 if event.key == pygame.K_RETURN:
                     # print("ENTER pressed, resetting game...") # DEBUG
                     reset_game() # This sets game_state = "playing"
                     # print(f"Game state is now: {game_state}") # DEBUG
                 if event.key == pygame.K_q:
                     running = False


        elif game_state == "playing":
            # DEBUG: Confirm entering this state
            # print(f"Playing frame start: time={current_time:.2f}, last_fall={last_fall_time:.2f}")

            # Store time anchor *before* logic/input for this frame
            current_frame_start_time = time.time()

            # --- Input ---
            # handle_input now manages its own event queue processing internally
            effective_fall_speed = handle_input(current_piece, grid)

            # Check if paused state was triggered by input handler
            if game_state == "paused":
                 # Skip game logic updates if paused
                 pass
            else:
                # --- Game Logic Update ---
                if current_piece: # Only update if there is a piece
                    # update_game_state can change game_state to 'game_over'
                    current_piece, next_piece, grid, locked_blocks = update_game_state(
                        current_piece, next_piece, grid, locked_blocks, effective_fall_speed
                    )
                else: # Safety: if somehow current_piece is None, get a new one
                    current_piece = next_piece
                    next_piece = get_shape()
                    if not is_valid_position(current_piece, grid): # Check if instantly lost
                         game_state = "game_over"
                         game_over_start_time = time.time()
                         safe_play(sound_game_over)


                # Update score animation state
                score_anim_active = False
                if score != last_score:
                     # Don't trigger animation for score == 0 at start
                     if score > 0 or last_score != 0 : 
                        score_update_time = current_time
                        score_anim_active = True
                     last_score = score # Update last_score regardless

                if score_anim_active and (current_time - score_update_time > SCORE_ANIMATION_DURATION):
                     score_anim_active = False # Turn off animation


            # --- Drawing ---
            # Draw regardless of paused state, draw_window handles paused overlay
            draw_window(screen, grid, locked_blocks, current_piece, next_piece, score, level, lines_cleared_total, game_state, 0, score_anim_active)

            # Update last_fall_time *after* all logic/drawing for this frame is done
            last_fall_time = current_frame_start_time

        elif game_state == "paused":
            # Drawing is handled by draw_window called from "playing" state check
            # Handle only unpause/quit events here
            for event in pygame.event.get(eventtype=pygame.KEYDOWN):
                if event.key == pygame.K_p:
                    game_state = "playing"
                    # IMPORTANT: Reset time anchor when unpausing to prevent huge delta_time jump
                    last_fall_time = time.time()
                if event.key == pygame.K_q:
                    running = False

        elif game_state == "game_over":
            elapsed = current_time - game_over_start_time
            game_over_alpha = min(180, (elapsed / GAME_OVER_FADE_DURATION) * 180)

            # Draw the final state + Game Over overlay
            draw_window(screen, grid, locked_blocks, current_piece, next_piece, score, level, lines_cleared_total, game_state, game_over_alpha, False)

            # Handle restart / quit events
            for event in pygame.event.get(eventtype=pygame.KEYDOWN):
                 if event.key == pygame.K_RETURN:
                     reset_game()
                 if event.key == pygame.K_q:
                     running = False

        # --- Frame Rate Control ---
        clock.tick(60) # Aim for 60 FPS

    # --- Clean Up ---
    print("Exiting Pygame Tetris.")
    pygame.quit()

# --- Run the Game ---
if __name__ == "__main__":
     main()
