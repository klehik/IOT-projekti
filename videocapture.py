import cv2


class Scanner:


    def open_camera(self):

        cap = cv2.VideoCapture(0)
       
        while True:
            ret, frame = cap.read() #returns ret and the frame
            if ret:
                cv2.imshow('frame',frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()    
           

   
            
           
