import cv2
import mediapipe as mp
import numpy as np
import time
import json
from pygame import mixer

global z

def Faces():

    global time1
    man=0
    end=0
    start =0
    str5 = 'Time in minutes : '
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    mp_drawing = mp.solutions.drawing_utils

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    left, right, up,down =0,0,0,0
    leftState, rightState, upState,downState =1,1,1,1

    cap = cv2.VideoCapture(0)
    a = []
    # a[0]=time.time()%60
    m=0
    min=0
    rik=0
    rik1=0
    z1=0
    z2=0
    preval=0
    starttime = time.perf_counter()
    while cap.isOpened():
        success, image = cap.read()

        # start = time.time()
        # jecrc = time.perf_counter()
        # print(int(jecrc))
        # Flip the image horizontally for a later selfie-view display
        # Also convert the color space from BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance
        image.flags.writeable = False
        
        # Get the result
        results = face_mesh.process(image)
    
        # To improve performance
        image.flags.writeable = True
        
        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            # start = (time.time())%60 
            
            time1= time.perf_counter() - starttime
            
        
            if(int(man)==1):
                time1= time1 - ( end - m) +1 
            
            
        
            

            print("start :" , start)
            print("z :", man)
            print("end :" , end)
            print("min",rik)

        
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])       
                
                # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                        [0, focal_length, img_w / 2],
                                        [0, 0, 1]])

                # The distortion parameters
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360
            

                # See where the user's head tilting
                if y < -10:
                    v1 = time.perf_counter()
                    #cv2.putText(image, str(v1 - v5), (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)
                    if (v1 -v5) >20:
                        mixer.init()
                        mixer.music.load('x.mpeg')
                        mixer.music.play()
                        cv2.putText(image, 'beep', (100,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)

                    if leftState:
                        left = left+1
                        leftState = 0
                        rightState = 1

                    text = "Looking Left"
                elif y > 10:
                    v2 = time.perf_counter()
                        #cv2.putText(image, str(v2 - v5), (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)
                    if (v2 -v5) >20:
                        mixer.init()
                        mixer.music.load('x.mpeg')
                        mixer.music.play()
                        cv2.putText(image, 'beep', (100,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)

                    if rightState:
                        leftState = 1
                        upState = 1
                        downState =1
                        rightState = 0
                        right = right+1
                    text = "Looking Right"
                elif x < -10:
                    v3 = time.perf_counter()
                    #cv2.putText(image, str(v3 - v5), (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)
                    if (v3 -v5) >20:
                        mixer.init()
                        mixer.music.load('x.mpeg')
                        mixer.music.play()
                        cv2.putText(image, 'beep', (100,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)
                    if downState:
                        downState =0
                        leftState = 1
                        rightState = 1
                        upState = 1                
                        down = down+1
                    text = "Looking Down"
                elif x > 10:
                    v4 = time.perf_counter()
                    #cv2.putText(image, str(v4 - v5), (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)
                    if (v4 -v5) >20:
                        mixer.init()
                        mixer.music.load('x.mpeg')
                        mixer.music.play()
                        cv2.putText(image, 'beep', (100,200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)
                    if upState:
                        leftState = 1
                        rightState = 1
                        downState =1
                        upState = 0
                        up = up+1
                    text = "Looking Up"
                else:
                    v5 = time.perf_counter()
                    #cv2.putText(image, str(v5 - starttime), (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,0,5), 2)
                    leftState = 1
                    rightState = 1
                    upState = 1
                    downState =1
                    text = "Forward"

                # Display the nose direction
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y * 10) , int(nose_2d[1] - x * 10))
                
                cv2.line(image, p1, p2, (255, 0, 0), 3)

                # Add the text on the image
                #cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                #cv2.putText(image, "x: " + str(np.round(x,2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                #cv2.putText(image, "y: " + str(np.round(y,2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                #cv2.putText(image, "z: " + str(np.round(z,2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                

                cv2.putText(image, "Left: " + str(np.round(left,2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "Right: " + str(np.round(right,2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "Up: " + str(np.round(up,2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "Down: " + str(np.round(down,2)), (500, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


            # end = time.time()
            # totalTime = end - start
            # t=  mid % 60
            # fps = 1 / totalTime
            #print("FPS: ", fps)
            # print(mid)
            # cv2.putText(image, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            # cv2.putText(image, f'time: {int(rik)} : {int(start)}', (300,450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            with open("face.json","w")as tas:
                json.dump(str5,tas)
                json.dump(time1,tas )
            cv2.putText(image, f'time: {int(time1)} sec', (300,450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            # cv2.putText(image, f'time: {int(t)} : {int(start)}', (300,450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)
        else:
            end= time.perf_counter() - starttime
            # end1=time.time()/60
            # min=start1
            # end= time.time()
            
            man=1
            # m=start
            #m= time1
            # t.stop()
        
        cv2.imshow('Head Pose Estimation', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break


    cap.release()

Faces()