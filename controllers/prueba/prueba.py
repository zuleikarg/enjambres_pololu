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
  
        

    # Enter here exit cleanup code.
    