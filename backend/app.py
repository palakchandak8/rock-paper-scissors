from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import mediapipe as mp
import numpy as np
import base64
import random

app = Flask(__name__)
CORS(app)  # Allow all origins - simple and works

# MediaPipe setup - Accept BOTH hands (left and right)
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def detect_gesture(landmarks, hand_label):
    """Detect hand gesture from MediaPipe landmarks"""
    tipIds = [4, 8, 12, 16, 20]
    fingers = 0

    # Thumb (check x-coordinate for horizontal direction)
    # MediaPipe labels are from camera perspective (mirrored)
    # So "Right" in MediaPipe means user's left hand, and vice versa
    if hand_label == "Left":  # Camera sees "Left" = user's right hand
        if landmarks[tipIds[0]].x > landmarks[tipIds[0]-1].x:
            fingers += 1
    else:  # hand_label == "Right" - Camera sees "Right" = user's left hand
        if landmarks[tipIds[0]].x < landmarks[tipIds[0]-1].x:
            fingers += 1

    # Other fingers (check y-coordinate for vertical direction)
    for id in range(1, 5):
        if landmarks[tipIds[id]].y < landmarks[tipIds[id]-2].y:
            fingers += 1

    if fingers == 0:
        return "Rock"
    elif fingers == 2:
        return "Scissors"
    elif fingers == 5:
        return "Paper"
    return "Unknown"

@app.route('/api/detect-gesture', methods=['POST'])
def detect_hand_gesture():
    """
    Endpoint to detect hand gesture from base64 image
    Frontend sends camera frame, backend returns detected gesture AND landmarks for BOTH hands
    """
    try:
        data = request.json
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({
                'success': False,
                'gesture': 'None',
                'message': 'No image provided'
            })
        
        # Decode base64 image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({
                'success': False,
                'gesture': 'None',
                'message': 'Invalid image'
            })
        
        # Convert BGR to RGB for MediaPipe
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        result = hands.process(imgRGB)
        
        if result.multi_hand_landmarks and result.multi_handedness:
            # Collect all detected hands
            all_hands = []
            
            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                landmarks = hand_landmarks.landmark
                
                # Get hand label (Left or Right)
                hand_label = result.multi_handedness[idx].classification[0].label
                
                # Detect gesture with hand label
                gesture = detect_gesture(landmarks, hand_label)
                
                # Convert landmarks to JSON format
                landmarks_list = []
                for lm in landmarks:
                    landmarks_list.append({
                        'x': lm.x,
                        'y': lm.y,
                        'z': lm.z
                    })
                
                all_hands.append({
                    'label': hand_label,
                    'gesture': gesture,
                    'landmarks': landmarks_list
                })
            
            # Pick the best gesture (prioritize valid gestures)
            valid_gestures = [h['gesture'] for h in all_hands if h['gesture'] not in ['None', 'Unknown']]
            primary_gesture = valid_gestures[0] if valid_gestures else all_hands[0]['gesture']
            
            return jsonify({
                'success': True,
                'gesture': primary_gesture,
                'hands': all_hands,
                'hand_count': len(all_hands),
                'message': f'Detected {len(all_hands)} hand(s): {primary_gesture}'
            })
        else:
            return jsonify({
                'success': True,
                'gesture': 'None',
                'hands': [],
                'hand_count': 0,
                'message': 'No hand detected'
            })
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'gesture': 'None',
            'error': str(e)
        }), 500

@app.route('/api/play', methods=['POST'])
def play_round():
    """
    Complete round endpoint
    Receives player gesture, generates computer move, determines winner
    """
    try:
        data = request.json
        player_gesture = data.get('playerGesture', 'None')
        
        if player_gesture in ['None', 'Unknown']:
            return jsonify({
                'success': False,
                'message': 'Invalid gesture'
            })
        
        # Computer makes random choice
        computer_gesture = random.choice(['Rock', 'Paper', 'Scissors'])
        
        # Determine winner
        if player_gesture == computer_gesture:
            result = 'draw'
            message = "It's a Draw!"
        elif (player_gesture == 'Rock' and computer_gesture == 'Scissors') or \
             (player_gesture == 'Paper' and computer_gesture == 'Rock') or \
             (player_gesture == 'Scissors' and computer_gesture == 'Paper'):
            result = 'win'
            message = 'You Win!'
        else:
            result = 'lose'
            message = 'Computer Wins!'
        
        return jsonify({
            'success': True,
            'playerGesture': player_gesture,
            'computerGesture': computer_gesture,
            'result': result,
            'message': message
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Backend server is running'
    })

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        'message': 'Rock Paper Scissors Backend API',
        'endpoints': {
            '/api/detect-gesture': 'POST - Detect hand gesture from image (supports both hands)',
            '/api/play': 'POST - Play a round',
            '/api/health': 'GET - Health check'
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Rock Paper Scissors Backend Server...")
    print("📡 Server running on http://localhost:5000")
    print("🎮 Ready to detect hand gestures!")
    print("👐 Now detecting BOTH hands!")
    app.run(debug=True, host='0.0.0.0', port=5000)
