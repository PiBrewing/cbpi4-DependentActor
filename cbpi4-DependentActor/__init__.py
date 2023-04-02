
# -*- coding: utf-8 -*-
import logging
import asyncio
from cbpi.api import *
from cbpi.api.dataclasses import NotificationAction, NotificationType

logger = logging.getLogger(__name__)

@parameters([Property.Actor(label="Base",  description="Select the actor you would like to add a dependency to."),
            Property.Select(label="DependencyType", options=["Restriction", "Prerequisite"], description="Select the dependency type. With 'Restriction', the 'Actor Dependency' is required to be OFF in order to switch the 'Base Actor' ON. With 'Prerequisite', the 'Actor Dependency' is required to be ON in order to switch the 'Base Actor' ON."),
            Property.Actor(label="ActorDependency", description="Select the actor that the base actor will depend upon."),
            Property.Select(label="notification", options=["Yes", "No"], description="Will show notifications in case of errors if set to yes")])

class DependentActor(CBPiActor):

    async def on_start(self):
        self.state = False
        self.power=100
        self.base = self.props.get("Base", None)
        if self.base:
            await self.cbpi.actor.off(self.base)
        self.ActorDependency = self.props.get("ActorDependency", None)
        self.dependency_type = self.props.get("DependencyType", "Prerequisite")
        self.notification = self.props.get("notification", "Yes")
        pass

    async def on(self, power=None):
        if power is not None:
            self.power=power

        ActorDependency = self.cbpi.actor.find_by_id(self.ActorDependency)
        try:
            ActorDependencyState = ActorDependency.instance.state
        except:
            ActorDependencyState = False

        if (ActorDependencyState == False) & (self.dependency_type == "Restriction"):
            await self.cbpi.actor.on(self.base, self.power)
            self.state = True
        elif (ActorDependencyState == True) & (self.dependency_type == "Prerequisite"):
            await self.cbpi.actor.on(self.base, self.power)
            self.state = True
        else:
            self.state=False
            await self.off()
            if self.notification == "Yes":
                self.cbpi.notify("Powering of Actor prevented", "This is due to the current power state of it's dependency %s" %(ActorDependency.name) ,NotificationType.ERROR)

    async def off(self):
        logger.info("ACTOR %s OFF " % self.base)
        await self.cbpi.actor.off(self.base)
        self.state = False
        await self.cbpi.actor.ws_actor_update()

    def get_state(self):
        return self.state
    
    async def run(self):
        #if self.init == False:
        #    if self.base is not None:
        #        await self.cbpi.actor.off(self.base)
        #        self.state = False
        #    self.init = True
        while self.running:
            await self.cbpi.actor.ws_actor_update()
            await asyncio.sleep(2)
        pass

    async def set_power(self, power):
        self.power=power
        await self.cbpi.actor.set_power(self.base, self.power)
        pass


@parameters([Property.Actor(label="Actor", description="Select a targetactor which is triggered by this group."),
            Property.Select(label="Action", options=["on","off"], description="Targetactor is switched on or off dependent on other actors in group."),
             Property.Select(label="Logic", options=["OR","AND"], description="Actor is triggered if all (AND) or one actor (OR) of the group is ON."),
            Property.Actor(label="Actor01", description="Select an actor which triggers targetactor."),
            Property.Actor(label="Actor02", description="Select an actor which triggers targetactor."),
            Property.Actor(label="Actor03", description="Select an actor which triggers targetactor."),
            Property.Actor(label="Actor04", description="Select an actor which triggers targetactor."),
            Property.Actor(label="Actor05", description="Select an actor which triggers targetactor."),
            Property.Actor(label="Actor06", description="Select an actor which triggers targetactor."),
            Property.Actor(label="Actor07", description="Select an actor which triggers targetactor."),
            Property.Actor(label="Actor08", description="Select an actor which triggers targetactor.")])
class ConditionalActor(CBPiActor):

    async def on_start(self):
        self.state = False
        self.actors = []
        self.power = 0
        self.actoractivity = True if self.props.get("Action", "on") == "on" else False
        self.grouplogic = True if self.props.get("Logic", "AND") == "AND" else False
        self.switch=self.props.get("Actor")
        try:
            if self.props.get("Actor01", None) is not None:
                self.actors.append(self.props.get("Actor01"))
            if self.props.get("Actor02", None) is not None:
                self.actors.append(self.props.get("Actor02"))
            if self.props.get("Actor03", None) is not None:
                self.actors.append(self.props.get("Actor03"))
            if self.props.get("Actor04", None) is not None:
                self.actors.append(self.props.get("Actor04"))
            if self.props.get("Actor05", None) is not None:
                self.actors.append(self.props.get("Actor05"))
            if self.props.get("Actor06", None) is not None:
                self.actors.append(self.props.get("Actor06"))
            if self.props.get("Actor07", None) is not None:
                self.actors.append(self.props.get("Actor07"))
            if self.props.get("Actor08", None) is not None:
                self.actors.append(self.props.get("Actor08"))
        except Exception as e:
            logging.error(e)
        self.numberactors=len(self.actors)
        
    async def on(self, power=100):      
        self.power=power
        self.state = True
        await self.cbpi.actor.on(self.switch,self.power)

    async def off(self):
        self.state = False
        await self.cbpi.actor.off(self.switch)      

    def get_state(self):
        return self.state

    async def run(self):
        while self.running == True:
            statesum = 0

            targetactor = self.cbpi.actor.find_by_id(self.switch)
            try:
                targetstatus=targetactor.instance.state
            except:
                targetstatus=False            

            for actor in self.actors:
                currentactor=self.cbpi.actor.find_by_id(actor)
                try:
                    status=currentactor.instance.state
                except:
                    status=False
                if status:
                    statesum +=1

            if self.grouplogic:
                logging.info("AND")
                if statesum == self.numberactors:
                    if self.actoractivity:
                        if self.state == False or targetstatus == False:
                            await self.on()
                    else:
                        if self.state == True or targetstatus == True:
                            await self.off()
                else:
                    if self.actoractivity:
                        if self.state == True or targetstatus == True:
                            await self.off()
                    else:
                        if self.state == False or targetstatus == False:
                            await self.on()
            # OR for logic
            if not self.grouplogic:
                logging.info("OR")
                if statesum != 0:
                    if self.actoractivity:
                        if self.state == False or targetstatus == False:
                            await self.on()
                    else:
                        if self.state == True or targetstatus == True:
                            await self.off()
                else:
                    if self.actoractivity:
                        if self.state == True or targetstatus == True:
                            await self.off()
                    else:
                        if self.state == False or targetstatus == False:
                            await self.on()

            await self.cbpi.actor.ws_actor_update()
            await asyncio.sleep(1)
        
    async def set_power(self, power=0):
        self.power=0
        pass


def setup(cbpi):
    cbpi.plugin.register("Dependent Actor", DependentActor)
    cbpi.plugin.register("Conditional Actor", ConditionalActor)
    pass
