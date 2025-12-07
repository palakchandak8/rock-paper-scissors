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
        self.game_state = "waiting"  # waiting, countdown, playing, result
        self.player_gesture = "None"
        self.computer_move = "None"
        self.result_text = ""
        
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
            return "Player Wins"
        else:
            return "Computer Wins"
    
    def run(self):
        """Main game loop"""
        print("Rock Paper Scissors Game Started!")
        print("Press ESC to exit")
        
        while True:
            success, frame = self.cap.read()
            frame = cv2.flip(frame, 1)  # Mirror
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(imgRGB)

            # Process hand detection
            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)

                lmList = []
                h, w, c = frame.shape
                for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
                    lmList.append([id, int(lm.x*w), int(lm.y*h)])

                self.player_gesture = self.detect_gesture(lmList)

            # Display UI
            cv2.putText(frame, f"Your Move: {self.player_gesture}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.putText(frame, f"Score - You: {self.score_player} | PC: {self.score_computer}", 
                        (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

            cv2.imshow("Rock Paper Scissors - Backend", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()