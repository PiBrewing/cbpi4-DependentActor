
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from cbpi.api.dataclasses import NotificationAction, NotificationType

logger = logging.getLogger(__name__)

@parameters([Property.Actor(label="Base",  description="Select the actor you would like to add a dependency to."),
            Property.Select(label="DependencyType", options=["Restriction", "Prerequisite"], description="Select the dependency type. With 'Restriction', the 'Actor Dependency' is required to be OFF in order to switch the 'Base Actor' ON. With 'Prerequisite', the 'Actor Dependency' is required to be ON in order to switch the 'Base Actor' ON."),
            Property.Actor(label="ActorDependency", description="Select the actor that the base actor will depend upon."),
            Property.Select(label="notification", options=["Yes", "No"], description="Will show notifications in case of errors if set to yes")])

class DependentActor(CBPiActor):

    def on_start(self):
        self.state = False
        self.base = self.props.get("Base", None)
        self.ActorDependency = self.props.get("ActorDependency", None)
        self.dependency_type = self.props.get("DependencyType", "Prerequisite")
        self.notification = self.props.get("notification", "Yes")
        self.init = False
        pass

    async def on(self, power=0):
        ActorDependency = self.cbpi.actor.find_by_id(self.ActorDependency)
        try:
            ActorDependencyState = ActorDependency.instance.state
        except:
            ActorDependencyState = False

        if (ActorDependencyState == False) & (self.dependency_type == "Restriction"):
            await self.cbpi.actor.on(self.base)
            self.state = True
        elif (ActorDependencyState == True) & (self.dependency_type == "Prerequisite"):
            await self.cbpi.actor.on(self.base)
            self.state = True
        else:
            await self.cbpi.actor.off(self.base)
            self.state = False
            if self.notification == "Yes":
                self.cbpi.notify("Powering of Actor prevented", "This is due to the current power state of it's dependency %s" %(ActorDependency.name) ,NotificationType.ERROR)


    async def off(self):
        logger.info("ACTOR %s OFF " % self.base)
        await self.cbpi.actor.off(self.base)
        self.state = False

    def get_state(self):
        return self.state
    
    async def run(self):
        if self.init == False:
            if self.base is not None:
                await self.cbpi.actor.off(self.base)
                self.state = False
            self.init = True
        pass


def setup(cbpi):
    cbpi.plugin.register("Dependent Actor", DependentActor)
    pass
