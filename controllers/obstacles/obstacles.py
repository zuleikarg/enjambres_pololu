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
    max_speed = 12.00
    
    # create sensor instances.
    distance_sensors=[]
    names_distance=["front_distance","left_distance","right_distance"]
    panel_distance=[0,0,0]
    
    for i in range(0,3):
        distance_sensors.append(robot.getDevice(names_distance[i]))
        distance_sensors[i].enable(timestep)
   
    # create general variables
    rotation = False
    distance = 500

    # Main loop:

    while robot.step(timestep) != -1:
        #Initial velocity
        DD_speed = 0.6*max_speed
        ID_speed = 0.6*max_speed
        
        # Obstacle in front of the robot
        if(distance_sensors[0].getValue() <= distance or rotation == True):
            rotation = True
            # Choose the side with more distance
            if(distance_sensors[1].getValue()>distance_sensors[2].getValue()):
                DD_speed = 0.6*max_speed
                ID_speed = -0.6*max_speed
                
                # When obstacle detected in the side finish rotation
                if(distance_sensors[2].getValue() < 1000):
                    rotation = False
            else:
                DD_speed = -0.6*max_speed
                ID_speed = 0.6*max_speed
                
                # When obstacle detected in the side finish rotation
                if(distance_sensors[1].getValue() < 1000):
                    rotation = False
        # Obstacle in the side
        else:
            # Obstacle in the left side 
            if(distance_sensors[1].getValue()<200):
                DD_speed = -0.5*max_speed
                ID_speed = 0.5*max_speed
        
            # Ostacle in the right side
            if(distance_sensors[2].getValue()<200):
                DD_speed = 0.5*max_speed
                ID_speed = -0.5*max_speed
                
        #Apply velocity
        DA.setVelocity(DD_speed)
        DD.setVelocity(DD_speed)
        IA.setVelocity(ID_speed)
        ID.setVelocity(ID_speed)