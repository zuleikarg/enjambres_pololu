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
        
    # create general variables
    max_speed = 10.00
    not_detected = False
    count = 0
    
    #Initial velocity
    DD_speed = 0.0 
    ID_speed = 0.0
    
    # Main loop:
    
    while robot.step(timestep) != -1:
        #Get front distance value
        front_distance = distance_sensors[0].getValue()
        
        #Get line values
        front_line = line_sensors[0].getValue()
        front_left_line = line_sensors[2].getValue()
        front_right_line = line_sensors[3].getValue()
        
        # Line detected in front sensor move forward
        if(front_line>=200):
            not_detected = False
            DD_speed = ((front_distance*max_speed)/1000) -1
            ID_speed = ((front_distance*max_speed)/1000) -1
        # Line detected in left sensor move right
        elif(front_left_line>=200):
            not_detected = False
            DD_speed = -((front_distance*max_speed)/1000)
            ID_speed = ((front_distance*max_speed)/1000)
        # Line detected in right sensor move left
        elif(front_right_line>=200):
            not_detected = False
            DD_speed = ((front_distance*max_speed)/1000)
            ID_speed = -((front_distance*max_speed)/1000)
        # Line not detected in any sensor
        elif(front_line<100 and front_left_line<100 and front_right_line<100):
           count = count +1
           # Move to find the line
           if(count >= 200 or not_detected == True):
                count = 0
                not_detected = True
                DD_speed = (front_distance*max_speed)/1000
                ID_speed = ((front_distance*max_speed)/1000) -3
                
        #Apply velocity       
        DA.setVelocity(DD_speed)
        DD.setVelocity(DD_speed)
        IA.setVelocity(ID_speed)
        ID.setVelocity(ID_speed)