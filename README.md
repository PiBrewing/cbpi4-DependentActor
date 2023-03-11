# Craftbeerpi4 Actor Plugin

## Target Actor can be triggered based on conditions of other actors.

The packages contains two plugins.

1. Dependent Actor (Ported from CraftbeerPi 3 Version)
    - An actor with a restriction may be used in the case of wishing to prevent multiple heating elements from being on at the same time.
    - An actor with a prerequisite may be used if you wish to only have a heating element on if a recirculating pump is on at the same time.
2. Conditional Actor to trigger on target actor automatically based on status of an actor group.
    - Can be used to trigger for instance a bypass valve for a cooling system if other valves in the loop are closed.

### Installation:

You can install it directly via pypi.org:	
- sudo pip3 install cbpi4-DependentActor

Alternativeley you can install (or clone) it from the GIT Repo. In case of updates, you will find them here first:
- sudo pip3 install https://github.com/PiBrewing/cbpi4-DependentActor/archive/main.zip


### Conditional Actor

![Conditional Actor Settings](https://github.com/PiBrewing/cbpi4-Dependentactor/blob/main/conditional_settings.jpg?raw=true)

- Targetactor - Actor that should be triggered (e.g. Bypass valve)
- Action - 'off' or 'on'. Targetactor will be switched to setting if group is on
- Logic - 'AND': all actors in defined group have to be on to trigger targetactor. 'OR' one of the actors in the group have to be on to trigger targetaxctor
- Actor 1-8 - Up to 8 actors can be defined in the group

Image shows example for settings above. Both actors in defined group are off, Actor is on and triggers the target Bypass actor.  
![Bypass on](https://github.com/PiBrewing/cbpi4-Dependentactor/blob/main/bypass_on.jpg?raw=true)

The following images show the bypass is of as soon as one or more actors in the group are 'on'.
![Bypass first](https://github.com/PiBrewing/cbpi4-Dependentactor/blob/main/bypass_off_1.jpg?raw=true)
![Bypass second](https://github.com/PiBrewing/cbpi4-Dependentactor/blob/main/bypass_off_2.jpg?raw=true)
![Bypass both](https://github.com/PiBrewing/cbpi4-Dependentactor/blob/main/bypass_off_both.jpg?raw=true)

### Dependent Actor

The plugin provides an actor type called DependentActor. DependentActors are containers for existing Base Actors, which will only power ON if their Actor Dependency is in the correct state. The Actor Dependency must be ON if it is set as a prerequisite, and OFF if it is set as a restriction.

A DependentActor, can even use some other DependentActor as a base or dependency.

When configuring kettles and fermentors, make sure to select your new DependentActor, as the Base Actor is not currently automatically replaced in these.

This plugin is not a substitute for properly rated hardware components and safety features.

![Dependent Actor Settings](https://github.com/PiBrewing/cbpi4-Dependentactor/blob/main/dependent_settings.jpg?raw=true)

- Base Actor - Actor you want to add a dependency to.
- ActorDepoendency - Actor that the base actor will depend upon.
- Dependency Type - With 'Restriction', the 'Actor Dependency' is required to be OFF in order to switch the 'Base Actor' ON. With 'Prerequisite', the 'Actor Dependency' is required to be ON in order to switch the 'Base Actor' ON.
- Notification - 'Yes' will show Notifications in case actor can't be switched based on dependency



### Changelog

- 11.03.23: (0.0.4) Fixed Bugs in dependent actor and added conditional actor
- (0.0.1) Initial commit, Testing of port
