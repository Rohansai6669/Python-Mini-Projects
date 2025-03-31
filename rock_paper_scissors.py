import streamlit as st
import cv2
import mediapipe as mp
import random
import time
import numpy as np
import math
from PIL import Image
# Landmark indices
WRIST = 0

INDEX_FINGER_MCP = 5   # Index finger metacarpophalangeal joint
INDEX_FINGER_PIP = 6   # Index finger proximal interphalangeal joint
INDEX_FINGER_TIP = 8   # Index finger tip

MIDDLE_FINGER_MCP = 9  # Middle finger metacarpophalangeal joint
MIDDLE_FINGER_PIP = 10 # Middle finger proximal interphalangeal joint
MIDDLE_FINGER_TIP = 12 # Middle finger tip

RING_FINGER_MCP = 13   # Ring finger metacarpophalangeal joint
RING_FINGER_PIP = 14   # Ring finger proximal interphalangeal joint
RING_FINGER_TIP = 16   # Ring finger tip

PINKY_MCP = 17         # Pinky metacarpophalangeal joint
PINKY_PIP = 18         # Pinky proximal interphalangeal joint
PINKY_TIP = 20         # Pinky tip

THUMB_CMC = 1          # Thumb carpometacarpal joint
THUMB_MCP = 2          # Thumb metacarpophalangeal joint
THUMB_TIP = 4          # Thumb tip

# Constants for angle thresholds
EXTENDED_ANGLE_THRESHOLD = 160
CURLED_ANGLE_THRESHOLD = 45


def main():
    st.set_page_config(page_title="Rock Paper Scissors", page_icon="🤚")
    
    # Initialize session state
    if 'game_initialized' not in st.session_state:
        st.session_state.update({
            'player_score': 0,
            'computer_score': 0,
            'game_state': 'Not Started',
            'current_gesture': 'No Gesture',
            'computer_choice': None,
            'round_message': '',
            'countdown': 3,
            'game_initialized': False,
            'round_start_time': None,
            'status_message': '',
            'status_type': 'info'
        })

    # Mediapipe setup
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # Computer move images
    MOVE_IMAGES = {
    'Rock': 'images/rock.png',
    'Paper': 'images/paper.png',
    'Scissors': 'images/scissor.png',
    'No Gesture': 'images/waiting.png',
    }
    
    # Main layout
    st.title("🤚 MediaPipe Rock Paper Scissors")
    
    # Status container for game state messages
    status_container = st.empty()
    
    # Score and game status
    score_col1, score_col2 = st.columns(2)
    with score_col1:
        player_score_display = st.metric("Player Score", 0, delta_color="normal")
    with score_col2:
        computer_score_display = st.metric("Computer Score", 0, delta_color="normal")


    # Main game columns
    col1, col2 = st.columns(2)

    with col1:
        st.header("Your Camera")
        player_frame = st.empty()
        player_gesture_display = st.empty()
        
    with col2:
        st.header("Computer's Move")
        computer_move_display = st.empty()
        computer_gesture_display = st.empty()
    
    # Game actions container
    game_actions = st.container()

    # Update game state message function
    def update_game_state_message():
        state_messages = {
            'Not Started': ('Welcome to Rock Paper Scissors! Click Start to begin.', 'info'),
            'Waiting for Thumbs Up': ('Raise Thumbs Up to Start Round!', 'warning'),
            'Countdown': (f'Get Ready: {st.session_state.countdown}', 'warning'),
            'Player Move': ('Show Your Move!', 'primary'),
            'Game Over': ('Game completed. Play Again?', 'error')
        }
        
        message, message_type = state_messages.get(
            st.session_state.game_state, 
            ('Invalid Game State', 'error')
        )
        
        # Store message and type in session state
        st.session_state.status_message = message
        st.session_state.status_type = message_type
        
        # Display message based on type
        if message_type == 'info':
            status_container.info(message)
        elif message_type == 'warning':
            status_container.warning(message)
        elif message_type == 'error':
            status_container.error(message)
        else:
            status_container.write(message)
            
            
    def calculate_angle(a, b, c):
        """Calculate the angle between three points using the cosine rule."""
        ba = (a.x - b.x, a.y - b.y)
        bc = (c.x - b.x, c.y - b.y)
        
        dot_product = ba[0] * bc[0] + ba[1] * bc[1]
        magnitude_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
        magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
        
        if magnitude_ba * magnitude_bc == 0:
            return 0  # Prevent division by zero
        
        angle = math.acos(dot_product / (magnitude_ba * magnitude_bc))
        return math.degrees(angle)
    
    
    def detect_gesture(results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                INDEX_ANGLE = calculate_angle(
                    hand_landmarks.landmark[INDEX_FINGER_MCP],
                    hand_landmarks.landmark[INDEX_FINGER_PIP],
                    hand_landmarks.landmark[INDEX_FINGER_TIP],
                )
                MIDDLE_ANGLE = calculate_angle(
                    hand_landmarks.landmark[MIDDLE_FINGER_MCP],
                    hand_landmarks.landmark[MIDDLE_FINGER_PIP],
                    hand_landmarks.landmark[MIDDLE_FINGER_TIP],
                )
                RING_ANGLE = calculate_angle(
                    hand_landmarks.landmark[RING_FINGER_MCP],
                    hand_landmarks.landmark[RING_FINGER_PIP],
                    hand_landmarks.landmark[RING_FINGER_TIP],
                )
                PINKY_ANGLE = calculate_angle(
                    hand_landmarks.landmark[PINKY_MCP],
                    hand_landmarks.landmark[PINKY_PIP],
                    hand_landmarks.landmark[PINKY_TIP],
                )
                THUMB_ANGLE = calculate_angle(
                    hand_landmarks.landmark[THUMB_CMC],
                    hand_landmarks.landmark[THUMB_MCP],
                    hand_landmarks.landmark[THUMB_TIP],
                )
                
                # Thumbs Up: Thumb extended, other fingers curled
                if THUMB_ANGLE > EXTENDED_ANGLE_THRESHOLD and INDEX_ANGLE < CURLED_ANGLE_THRESHOLD and MIDDLE_ANGLE < CURLED_ANGLE_THRESHOLD and RING_ANGLE < CURLED_ANGLE_THRESHOLD and PINKY_ANGLE < CURLED_ANGLE_THRESHOLD:
                    return "Thumbs Up"
                
                # Rock: All fingers curled
                if INDEX_ANGLE < CURLED_ANGLE_THRESHOLD and MIDDLE_ANGLE < CURLED_ANGLE_THRESHOLD and RING_ANGLE < CURLED_ANGLE_THRESHOLD and PINKY_ANGLE < CURLED_ANGLE_THRESHOLD:
                    return "Rock"
                
                # Paper: All fingers extended
                if INDEX_ANGLE > EXTENDED_ANGLE_THRESHOLD and MIDDLE_ANGLE > EXTENDED_ANGLE_THRESHOLD and RING_ANGLE > EXTENDED_ANGLE_THRESHOLD and PINKY_ANGLE > EXTENDED_ANGLE_THRESHOLD:
                    return "Paper"
                
                # Scissors: Index and middle extended, others curled
                if INDEX_ANGLE > EXTENDED_ANGLE_THRESHOLD and MIDDLE_ANGLE > EXTENDED_ANGLE_THRESHOLD and RING_ANGLE < CURLED_ANGLE_THRESHOLD and PINKY_ANGLE < CURLED_ANGLE_THRESHOLD:
                    return "Scissors"
                
        return "No Gesture"

    def determine_winner(player_choice, computer_choice):
        if player_choice == computer_choice:
            return 'Tie'
        elif (
            (player_choice == 'Rock' and computer_choice == 'Scissors') or
            (player_choice == 'Paper' and computer_choice == 'Rock') or
            (player_choice == 'Scissors' and computer_choice == 'Paper')
        ):
            return 'Player'
        else:
            return 'Computer'
    def resize_image(image_path, target_width, target_height):
        """
        Resize image to match camera frame dimensions while maintaining aspect ratio.
        
        Args:
            image_path (str): Path to the image file
            target_width (int): Target width to resize to
            target_height (int): Target height to resize to
        
        Returns:
            PIL.Image: Resized image
        """
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Resize the image while maintaining aspect ratio
            img = img.resize((target_width, target_height), Image.LANCZOS)
            
            return img
        except Exception as e:
            st.error(f"Error loading image {image_path}: {e}")
            return None

    def capture_frames():
        cap = cv2.VideoCapture(0)
        
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        ) as hands:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_height, frame_width = frame.shape[:2]
 
                results = hands.process(frame_rgb)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame, 
                            hand_landmarks, 
                            mp_hands.HAND_CONNECTIONS
                        )
                
                gesture = detect_gesture(results)
                st.session_state.current_gesture = gesture
                
                # Game state logic
                if st.session_state.game_state == 'Waiting for Thumbs Up':
                    if gesture == 'Thumbs Up':
                        st.session_state.game_state = 'Countdown'
                        st.session_state.round_start_time = time.time()
                        st.session_state.countdown = 3
                        update_game_state_message()
                
                elif st.session_state.game_state == 'Countdown':
                    current_time = time.time()
                    elapsed_time = current_time - st.session_state.round_start_time
                    
                    if elapsed_time >= 1:
                        st.session_state.countdown -= 1
                        st.session_state.round_start_time = current_time
                        update_game_state_message()
                    
                    if st.session_state.countdown <= 0:
                        st.session_state.game_state = 'Player Move'
                        update_game_state_message()
                
                elif st.session_state.game_state == 'Player Move':
                    if gesture in ['Rock', 'Paper', 'Scissors']:
                        # Computer chooses
                        st.session_state.computer_choice = random.choice(['Rock', 'Paper', 'Scissors'])
                        
                        # Display computer's move
                        computer_move_img = resize_image(
                            MOVE_IMAGES[st.session_state.computer_choice], 
                            frame_width, 
                            frame_height
                        )
                        
                        # computer_move_display.code(MOVE_IMAGES[st.session_state.computer_choice], language='')
                        computer_move_display.image(computer_move_img, 
                                         caption=f"Computer's {st.session_state.computer_choice}")
                        computer_gesture_display.success(f"Computer chose: {st.session_state.computer_choice}")
                        
                        # Player's move display
                        player_gesture_display.success(f"You chose: {gesture}")
                        
                        # Determine winner
                        winner = determine_winner(gesture, st.session_state.computer_choice)
                        
                        # Update scores
                        if winner == 'Player':
                            st.session_state.player_score += 1
                            st.success("You Won This Round!")
                        elif winner == 'Computer':
                            st.session_state.computer_score += 1
                            st.error("Computer Won This Round!")
                        else:
                            st.warning("It's a Tie!")
                        
                        # Game win condition
                        if st.session_state.player_score == 3:
                            st.balloons()
                            st.session_state.game_state = 'Game Over'
                            update_game_state_message()
                            st.success("Congratulations! You Won the Game!")
                        elif st.session_state.computer_score == 3:
                            st.snow()
                            st.session_state.game_state = 'Game Over'
                            update_game_state_message()
                            st.error("Computer Won the Game! Try again.")
                        else:
                            # Prepare for next round
                            st.session_state.game_state = 'Waiting for Thumbs Up'
                            update_game_state_message()
                
                yield frame

    # Game initialization and restart
    with game_actions:
        if st.session_state.game_state == 'Not Started':
            if st.button("🎮 Start Game", type="primary"):
                st.session_state.game_state = 'Waiting for Thumbs Up'
                st.session_state.game_initialized = True
                update_game_state_message()
        
        if st.session_state.game_state == 'Game Over':
            if st.button("🔁 Play Again", type="primary"):
                st.session_state.update({
                    'player_score': 0,
                    'computer_score': 0,
                    'game_state': 'Waiting for Thumbs Up',
                    'current_gesture': 'No Gesture',
                    'computer_choice': None,
                    'countdown': 3
                })
                update_game_state_message()

    # Main game loop
    if st.session_state.game_state != 'Not Started':
        for frame in capture_frames():
            # Display live camera feed
            player_frame.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 
                               caption="Live Camera Feed")
            
            # Update score displays
            player_score_display.metric("Player Score", st.session_state.player_score)
            computer_score_display.metric("Computer Score", st.session_state.computer_score)

if __name__ == '__main__':
    main()