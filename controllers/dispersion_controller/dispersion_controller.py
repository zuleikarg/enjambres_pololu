# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

if __name__ == "__main__":
    
    # create the Robot instance.
    robot = Robot()
    
    # create motor instances.
    DA = robot.getDevice('motor4')
    DD = robot.getDevice('motor3')
    IA = robot.getDevice('motor2')
    ID = robot.getDevice('motor1')
    
    DA.setPosition(float('inf'))
    DA.setVelocity(0.0)
    DD.setPosition(float('inf'))
    DD.setVelocity(0.0)
    IA.setPosition(float('inf'))
    IA.setVelocity(0.0)
    ID.setPosition(float('inf'))
    ID.setVelocity(0.0)
    
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())

    # create sensor instances.
    distance_sensors=[]
    names_distance=["front_distance","left_distance","right_distance"]
    panel_distance=[0,0,0]
    
    for i in range(0,3):
        distance_sensors.append(robot.getDevice(names_distance[i]))
        distance_sensors[i].enable(timestep)
    
    imu = robot.getDevice('IMU')
    imu.enable(timestep)
    
    # create general variables
    max_speed = 4.00  
    max_distance = 700

    # Main loop:
    
    while robot.step(timestep) != -1:
        #Get distance values
        front_distance = distance_sensors[0].getValue()
        left_distance = distance_sensors[1].getValue()
        right_distance = distance_sensors[2].getValue()
        
        #Initial velocity
        DD_speed = 0*max_speed
        ID_speed = 0*max_speed
        
        # Distance too small
        if(front_distance<= max_distance or left_distance<= max_distance+300 or right_distance<= max_distance+300):
            # Move backwards if front distance too small
            if(front_distance < left_distance and front_distance < right_distance and front_distance >0):
                DD_speed = -(((max_distance)/front_distance)/max_speed)  
                ID_speed = -(((max_distance)/front_distance)/max_speed) 
            # Move backwards and right if left distance too small
            elif(left_distance < front_distance and left_distance < right_distance and left_distance > 0):
                DD_speed = -(((max_distance+300)/left_distance)/max_speed) +3
                ID_speed = -(((max_distance+300)/left_distance)/max_speed) 
            # Move backwards and left if right distance too small
            elif(right_distance < front_distance and right_distance < left_distance and right_distance >0):
                DD_speed = -(((max_distance+300)/right_distance)/max_speed) 
                ID_speed = -(((max_distance+300)/right_distance)/max_speed) +3

        #Apply velocity       
        DA.setVelocity(DD_speed)
        DD.setVelocity(DD_speed)
        IA.setVelocity(ID_speed)
        ID.setVelocity(ID_speed)

     