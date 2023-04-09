"""zumito_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

def obstacles(max_speed):

    rotation = True

    DD_speed = 0.6*max_speed
    ID_speed = 0.6*max_speed
    
    # Obstacle in front
    if(distance_sensors[0].getValue() <= 500):
        if(distance_sensors[1].getValue()>distance_sensors[2].getValue()):
            DD_speed = 0.6*max_speed
            ID_speed = -0.6*max_speed
                    
            if(distance_sensors[2].getValue() < 1000):
                rotation = False
        else:
            DD_speed = -0.6*max_speed
            ID_speed = 0.6*max_speed
                    
            if(distance_sensors[1].getValue() < 1000):
                rotation = False 
    # Obstacle in the side
    else:
        if(distance_sensors[1].getValue()<100):
            DD_speed = -0.7*max_speed
            ID_speed = 0.7*max_speed
        else:
            rotation = False
        
        if(distance_sensors[2].getValue()<100):
            DD_speed = 0.7*max_speed
            ID_speed = -0.7*max_speed
        else:
            rotation = False
               
    # Send update
    return rotation, ID_speed, DD_speed

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
    line_sensors=[]
    names_line=["front_line","left_line","right_line", "front_left_line", "front_right_line"]
    panel_line=[0,0,0,0,0]
    
    for i in range(0,5):
        line_sensors.append(robot.getDevice(names_line[i]))
        line_sensors[i].enable(timestep)

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
    angle = 0.0   
    
    food_time = True
    house_time = False
    avoiding_time = False
    
    # Main loop:

    while robot.step(timestep) != -1:
    
        #Get front distance value
        front_distance = distance_sensors[0].getValue()
        
        #Get line values
        front_line = line_sensors[0].getValue()
        left_line = line_sensors[1].getValue()
        right_line = line_sensors[2].getValue() 
        #Get IMU values
        imu_values=imu.getRollPitchYaw()
        
        # Adjust angle
        angle = imu_values[2]*180/3.14
        if(angle < 0):
            angle = angle + 360
        
        # When is avoiding an obstacle
        if(avoiding_time == True):
            [avoiding_time, ID_speed, DD_speed] = obstacles(max_speed)
            
        # When is not avoiding and obstacle
        else:
            # Look for food
            if(food_time == True):
                # Move to the angle of the food
                if(angle>179 and angle<181):
                    DD_speed = 0.7*max_speed
                    ID_speed = 0.7*max_speed

                elif(angle>181):
                    DD_speed = -0.7*max_speed
                    ID_speed = 0.7*max_speed
                elif(angle<179):
                    DD_speed = 0.7*max_speed
                    ID_speed = -0.7*max_speed
                # When arrive to the food, go home
                if(front_line>180 and left_line>180 and right_line>180):
                    food_time = False
                    house_time = True
                    
            # Look for home
            elif(house_time == True):
                # Move to the angle of home
                if(angle<1 or (360-angle)<1):
                    DD_speed = 0.7*max_speed
                    ID_speed = 0.7*max_speed

                elif((360-angle)>1):
                    DD_speed = 0.7*max_speed
                    ID_speed = -0.7*max_speed
                elif(angle>1):
                    DD_speed = -0.7*max_speed
                    ID_speed = 0.7*max_speed
                # When arrive to home, go find food
                if(front_line>140 and front_line<160 and left_line>140 and left_line<160 and right_line>140 and right_line<160):
                    food_time = True
                    house_time = False
        
        # If a obstacle is detected start to avoid it
        if(distance_sensors[0].getValue() <= 500 or distance_sensors[1].getValue()<200 or distance_sensors[2].getValue()<200):
            avoiding_time= True
            
        #Apply velocity       
        DA.setVelocity(DD_speed)
        DD.setVelocity(DD_speed)
        IA.setVelocity(ID_speed)
        ID.setVelocity(ID_speed)