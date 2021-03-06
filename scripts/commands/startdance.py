from services.sui import SUIWindow
from services.sui import SUIService
from services.sui.SUIWindow import Trigger
from services.sui.SUIService import ListBoxType
from java.util import Vector
from java.util import HashMap
import sys

def setup():
    return

def run(core, actor, target, commandString):
    
    entSvc = core.entertainmentService
    global actorObject
    global coreObject
    global availableDances
    global suiWindow
    actorObject = actor
    coreObject = core

    if len(commandString) > 0:
        params = commandString.split(" ")
        startDance(core, actor, params[0], 0)
        return
    else:

        availableDances = entSvc.getAvailableDances(actor)
        print availableDances

        suiSvc = core.suiService
        suiWindow = suiSvc.createListBox(ListBoxType.LIST_BOX_OK_CANCEL, "@performance:select_dance", "@performance:available_dances", availableDances, actor, None, 10)

        returnList = Vector()
        returnList.add("List.lstList:SelectedRow")
        suiWindow.addHandler(0, '', Trigger.TRIGGER_OK, returnList, handleStartdance)
        
        suiSvc.openSUIWindow(suiWindow)
        return
    return


def handleStartdance(core, owner, eventType, returnList):

    item = suiWindow.getMenuItems().get(int(returnList.get(0)))

    if not item:
      return
        
    #if eventType == 0:
    startDance(coreObject, actorObject, '', int(item.getObjectId()))
    return

def startDance(core, actor, danceName, visual):

    entSvc = core.entertainmentService

    if visual <= 0:
      visual = entSvc.getDanceVisualId(danceName)

    if visual <= 0:
      return

    if not entSvc.isDance(visual):
      actor.sendSystemMessage('@performance:dance_unknown_self',0)
      return

    if not entSvc.canDance(actor, visual):
      actor.sendSystemMessage('@performance:dance_lack_skill_self',0)
      return

    if actor.getPerformanceId() > 0:
      actor.sendSystemMessage('@performance:already_performing_self',0)
      return

    #TODO: check costume, posture, etc?

    actor.sendSystemMessage('@performance:dance_start_self',0);
    actor.notifyAudience('@performance:dance_start_other');

    danceVisual = 'dance_' + str(visual)

    if not actor.getPerformanceWatchee():
      #this also notifies the client with a delta4
      actor.setPerformanceWatchee(actor)
  
    #this should send a CREO3 
    actor.setPosture(0x09);

    dance = entSvc.getDance(visual)

    # send CREO6 here
    # second param is some sort of counter or start tick
    actor.startPerformance(dance.getLineNumber(), -842249156 , danceVisual, 1)

    return
