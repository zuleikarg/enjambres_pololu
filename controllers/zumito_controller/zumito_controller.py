"""zumito_controller controller."""

# You may need to import some classes of the controller module. Ex:
 # from controller import Robot, Motor, DistanceSensor
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
    
    line_sensors=[]
    names_line=["front_line","left_line","right_line"]
    panel_line=[0,0,0]
    
    for i in range(0,3):
        line_sensors.append(robot.getDevice(names_line[i]))
        line_sensors[i].enable(timestep)
  
    distance_sensors=[]
    names_distance=["front_distance","left_distance","right_distance"]
    panel_distance=[0,0,0]
    
    for i in range(0,3):
        distance_sensors.append(robot.getDevice(names_distance[i]))
        distance_sensors[i].enable(timestep)

    gyro = robot.getDevice('gyro')
    gyro.enable(timestep)
    
    acce = robot.getDevice('accelerometer')
    acce.enable(timestep)
    
    compass = robot.getDevice('compass')
    compass.enable(timestep)
    
    # Main loop:
    
    while robot.step(timestep) != -1:
        # DA_speed = 0.5*max_speed
        DD_speed = 0.5*max_speed
        # IA_speed = 0.5*max_speed
        ID_speed = 0.5*max_speed
        
        DA.setVelocity(DD_speed)
        DD.setVelocity(DD_speed)
        IA.setVelocity(ID_speed)
        ID.setVelocity(ID_speed)
        
        print("Line Values")
        for i in range(0,3):
            panel_line=line_sensors[i].getValue()
            print(panel_line)
         
        print(" ")

        print("Distance Values")
        for j in range(0,3):
            panel_distance=distance_sensors[j].getValue()
            print(panel_distance)
             
        print(" ")
        
        print("Gyroscope Values")
        gyro_values=gyro.getValues()
        print(gyro_values)
       
        print(" ")
       
        print("Accelerometer Values")
        acce_values=acce.getValues()
        print(acce_values)
       
        print(" ")
        
        print("Compass Values")
        compass_values=compass.getValues()
        print(compass_values)
       
        print(" ")
    # Enter here exit cleanup code.
    