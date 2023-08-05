# -*- coding: utf-8 -*-
#APIDOC["Path"]=/Core/Events
#APIDOC["Draft"]=False
#--end--
"""
The module contains filter for detecting foot contact events.

check out the script : *\Tests\test_events.py* for examples
"""
import pyCGM2; LOGGER = pyCGM2.LOGGER

try:
    from pyCGM2 import btk
except:
    LOGGER.logger.info("[pyCGM2] pyCGM2-embedded btk not imported")
    try:
        import btk
    except:
        LOGGER.logger.error("[pyCGM2] btk not found on your system. install it for working with the API")


class EventFilter(object):
    """
    Event filter to handle an event procedure
    """
    def __init__(self,procedure,acq):
        """Constructor

        Args:
            procedure (pyCGM2.Events.eventProcedures.EventProcedure):an event procedure instance
            acq (Btk.Acquisition): a btk acquisition

        """


        self.m_aqui = acq
        self.m_procedure = procedure
        self.m_state = None

    def getState(self):
        return self.m_state

    def detect(self):
        """
            Run the motion filter
        """
        pf = self.m_aqui.GetPointFrequency()

        eventDescriptor = self.m_procedure.description

        if self.m_procedure.detect(self.m_aqui) == 0:
            self.m_state = False
        else:
            indexes_fs_left, indexes_fo_left, indexes_fs_right, indexes_fo_right =  self.m_procedure.detect(self.m_aqui)
            self.m_state = True
            for ind in indexes_fs_left:
                ev = btk.btkEvent('Foot Strike', (ind-1)/pf, 'Left', btk.btkEvent.Manual, '', eventDescriptor)
                ev.SetId(1)
                self.m_aqui.AppendEvent(ev)

            for ind in indexes_fo_left:
                ev = btk.btkEvent('Foot Off', (ind-1)/pf, 'Left', btk.btkEvent.Manual, '', eventDescriptor)
                ev.SetId(2)
                self.m_aqui.AppendEvent(ev)

            for ind in indexes_fs_right:
                ev = btk.btkEvent('Foot Strike', (ind-1)/pf, 'Right', btk.btkEvent.Manual, '', eventDescriptor)
                ev.SetId(1)
                self.m_aqui.AppendEvent(ev)

            for ind in indexes_fo_right:
                ev = btk.btkEvent('Foot Off', (ind-1)/pf, 'Right', btk.btkEvent.Manual, '', eventDescriptor)
                ev.SetId(2)
                self.m_aqui.AppendEvent(ev)
