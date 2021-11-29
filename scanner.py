import numpy as np
import cv2
import face_recognition
import json
import random
from paho.mqtt import client as mqtt_client
import time

class Scanner:
     
    def scan(self):

        """ # Broker 
        broker = '192.168.10.107'
        port = 1883
        topic = "mqtt"
        # Id for client
        client_id = 'python-mqtt-SecuritySystem7000'


        # Connect mqtt
        def connect_mqtt():
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    print("Connected to MQTT Broker!")
                else:
                    print("Failed to connect, return code %d\n", rc)

            client = mqtt_client.Client(client_id)
            
            client.on_connect = on_connect
            client.connect(broker, port)
            return client

        # Publishing
        def publish(client, message):
                    
            msg = message
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            


        
        client = connect_mqtt()
        client.loop_start() """
       
        # Start capturing video
        video_capture = cv2.VideoCapture(0)


        known_face_encodings = []
        known_face_names = []
       
        
        # Open users.json
        with open('./users.json') as f:
            data = json.load(f)

           
        # Initialize known faces
        for user in data['users']:
            image = face_recognition.load_image_file(user["imageUrl"])
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(user['name'])

       
        
        

        # Send message to broker and save image of intruder locally
        def alert(image):
            msg = "Tunkeilija havaittu"
            cv2.imwrite("intruder.jpg", image)
            publish(client, msg)

            
            
            
        # Loop through frames
        process_this_frame = True
        while True:

            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                      
                    # if not matching face send message to broker
                    else:
                        alert(frame)
                        

                    face_names.append(name) 

            process_this_frame = not process_this_frame


            # Display the results. Not necessary for this project but helps testing

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)
            

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
                
        
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        




    def scan_for_registration(self, user):
        
            
        video_capture = cv2.VideoCapture(0)

        # Sleep a bit that the camera has time to open
        time.sleep(5)
        ret, frame = video_capture.read()
        
        # not necessary
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            
        # Filename    
        imageurl = user + ".jpg"
        # Save file
        cv2.imwrite(imageurl, small_frame)

        filename = '/Users/kallelehikoinen/face_recognition/Secsystem7000/users.json'
        new_user = {"id": random.randint(1, 10000), "name": user, "imageUrl": imageurl}
        # Read file 
        with open(filename, "r") as file:
            data = json.load(file)
        # Update json object
        data['users'].append(new_user)
        # Write json file
        with open(filename, "w") as file:
            json.dump(data, file)


        video_capture.release()
               