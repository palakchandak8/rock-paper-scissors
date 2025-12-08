import cv2
import mediapipe as mp
import random
import time

class RockPaperScissorsGame:
    def __init__(self):
        # Webcam
        self.cap = cv2.VideoCapture(0)
        
        # MediaPipe Hands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils
        
        # Game state
        self.score_player = 0
        self.score_computer = 0
        self.game_state = "waiting"  # waiting, countdown, result
        self.player_gesture = "None"
        self.computer_move = "None"
        self.result_text = ""
        
        # Countdown timer
        self.countdown_value = 3  # 3, 2, 1
        self.countdown_start_time = None
        self.result_display_time = None
        
    def detect_gesture(self, lmList):
        """Detect hand gesture from landmarks"""
        tipIds = [4, 8, 12, 16, 20]
        fingers = 0

        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
            fingers += 1

        # Other fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers += 1

        if fingers == 0:
            return "Rock"
        elif fingers == 2:
            return "Scissors"
        elif fingers == 5:
            return "Paper"
        return "Unknown"
    
    def determine_winner(self, player, computer):
        """Determine the winner"""
        if player == computer:
            return "Draw"
        elif (player == "Rock" and computer == "Scissors") or \
             (player == "Paper" and computer == "Rock") or \
             (player == "Scissors" and computer == "Paper"):
            self.score_player += 1
            return "You Win!"
        else:
            self.score_computer += 1
            return "Computer Wins!"
    
    def start_countdown(self):
        """Start the countdown timer"""
        self.game_state = "countdown"
        self.countdown_value = 3
        self.countdown_start_time = time.time()
        self.player_gesture = "None"
        self.computer_move = "None"
        self.result_text = ""
    
    def update_countdown(self):
        """Update countdown during game"""
        elapsed = time.time() - self.countdown_start_time
        self.countdown_value = 3 - int(elapsed)
        
        if self.countdown_value < 0:
            # Countdown finished, lock the gesture
            if self.player_gesture != "None" and self.player_gesture != "Unknown":
                self.computer_move = random.choice(["Rock", "Paper", "Scissors"])
                self.result_text = self.determine_winner(self.player_gesture, self.computer_move)
                self.game_state = "result"
                self.result_display_time = time.time()
            else:
                # No valid gesture detected, restart
                self.start_countdown()
    
    def run(self):
        """Main game loop"""
        print("Rock Paper Scissors Game Started!")
        print("Press SPACE to start a round")
        print("Press ESC to exit")
        
        while True:
            success, frame = self.cap.read()
            if not success:
                continue
                
            frame = cv2.flip(frame, 1)  # Mirror
            h, w, c = frame.shape
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(imgRGB)

            # Process hand detection
            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)

                lmList = []
                for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
                    lmList.append([id, int(lm.x*w), int(lm.y*h)])

                self.player_gesture = self.detect_gesture(lmList)

            # Game state machine
            if self.game_state == "countdown":
                self.update_countdown()
            elif self.game_state == "result":
                # Display result for 3 seconds
                if time.time() - self.result_display_time > 3:
                    self.game_state = "waiting"

            # ===== DISPLAY UI =====
            
            # Background
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, 150), (50, 50, 50), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            
            # Title
            cv2.putText(frame, "ROCK PAPER SCISSORS", (w//2 - 200, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
            
            # Scoreboard
            cv2.putText(frame, f"YOU: {self.score_player}", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"COMPUTER: {self.score_computer}", (w - 250, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
            
            # Game state display
            if self.game_state == "waiting":
                cv2.putText(frame, "Press SPACE to Start", (w//2 - 180, h//2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)
                cv2.putText(frame, f"Your Gesture: {self.player_gesture}", (20, h - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                
            elif self.game_state == "countdown":
                # Big countdown number in center
                if self.countdown_value > 0:
                    cv2.putText(frame, str(self.countdown_value), (w//2 - 50, h//2 + 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 255), 10)
                    cv2.putText(frame, "Show your gesture!", (w//2 - 150, h//2 - 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(frame, "SHOOT!", (w//2 - 100, h//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
                
                cv2.putText(frame, f"Your Gesture: {self.player_gesture}", (20, h - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                
            elif self.game_state == "result":
                # Display result
                cv2.putText(frame, f"You: {self.player_gesture}", (50, h//2 - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                cv2.putText(frame, f"Computer: {self.computer_move}", (50, h//2 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 100, 255), 3)
                
                # Result text with color
                result_color = (0, 255, 0) if "Win" in self.result_text else (0, 0, 255) if "Computer" in self.result_text else (255, 255, 0)
                cv2.putText(frame, self.result_text, (w//2 - 150, h//2 + 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, result_color, 4)

            cv2.imshow("Rock Paper Scissors - Backend", frame)

            # Keyboard controls
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32 and self.game_state == "waiting":  # SPACE
                self.start_countdown()

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()