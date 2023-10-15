from multiprocessing import Process
import Rover_with_controller
import Object_detection_tf

if __name__ == '__main__':
    print("Now starting: Rover Movement")
    rv = Process(target= Rover_with_controller.main)
    rv.start()
    print("Now starting: Camera")
    ca = Process(target= Object_detection_tf.main)
    ca.start()