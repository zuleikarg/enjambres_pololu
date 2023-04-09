"""zumito_controller controller."""

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
    max_speed = 10.00
    rotation = False
    distance = 500
    left = True
    count = 0
    current_angle = 0.0
    not_found = True

    # Main loop:
    
    while robot.step(timestep) != -1:
        #Get front distance value
        front_distance = distance_sensors[0].getValue()
        #Get IMU values
        imu_values=imu.getRollPitchYaw()
        
        # Adjust angle
        angle = imu_values[2]*180/3.14
        if(angle < 0):
            angle = angle + 360
        
        # Robot not found, move around
        if(not_found == True):
            # First, move forward and to the left
            if(left == True):
                count = count +1
                
                DD_speed = 0.6*max_speed
                ID_speed = 0.6*max_speed-2
                
                if(count >= 300):
                    count = 0
                    left = False
            # Second, move forward and to the left
            if(left == False):
                count = count +1
                
                DD_speed = 0.6*max_speed -2
                ID_speed = 0.6*max_speed
                
                if(count >= 150):
                    count = 0
                    left = True
            # If a robot is detected in front, follow it
            if(front_distance<1000):
                not_found = False 
                count = 0
                left = True
                current_angle = angle
                
        # Robot found 
        else:
            # Robot lose in front
            if(front_distance >= 900):
                count = count +1
                
                # First, look to the left to find the robot
                if(left == True):
                    DD_speed = (front_distance*max_speed/1000)
                    ID_speed = (front_distance*max_speed/1000)-8
                    
                    if(current_angle >=345 and angle <=15):
                        current_angle = 360- current_angle
                        
                    dif = current_angle - angle
                    
                    if(dif < 0):
                        dif = dif *(-1)
                        
                    if(dif >= 15):
                        left = False
                        dif = 0
                # Second, look to the right to find the robot   
                else:
                    DD_speed = (front_distance*max_speed/1000)-8
                    ID_speed = (front_distance*max_speed/1000)
                    
                    if(current_angle <=40 and angle >=320):
                        angle = 360- angle
                        
                    dif = angle - current_angle
                    
                    if(dif < 0):
                        dif = dif *(-1)
                        
                    if(dif >= 40):
                        print(current_angle)
                        left = True
                        dif = 0
                
                # Robot finally not found, start moving around
                if( count >500):
                    count = 0
                    not_found = True
                    dif = 0
            # Robot detected in front, move forward
            else:
                left = True
                count = 0
                current_angle = angle
                
                DD_speed = front_distance*max_speed/1000
                ID_speed = front_distance*max_speed/1000
             
        #Apply velocity       
        DA.setVelocity(DD_speed)
        DD.setVelocity(DD_speed)
        IA.setVelocity(ID_speed)
        ID.setVelocity(ID_speed)