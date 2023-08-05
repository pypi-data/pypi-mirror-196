import pyCGM2
import numpy as np
import copy
from pyCGM2.Model import frame

LOGGER = pyCGM2.LOGGER

class AbstractModelCorrectionProcedure(object):
    def __init__(self):
        pass


class Naim2019ThighMisaligmentCorrectionProcedure(AbstractModelCorrectionProcedure):
    """ This function corrects the thigh anatomical frame in respect with the method detailed in Naim et al, 2019.

    Args:
        iMod (pyCGM2.Model.CGM2.model.Model): a model instance
        side (str): body side
        threshold (double,Optional[20]): only consider frames with a flexion angle above the given threshold

        **Reference:**

        Naaim, A., Bonnefoy-Mazure, A., Armand, S., & Dumas, R. (2019).
        Correcting lower limb segment axis misalignment in gait analysis: A simple geometrical method.
        Gait and Posture, 72(May), 34–39
    """

    def __init__(self,model,side,threshold=20):
        super(Naim2019ThighMisaligmentCorrectionProcedure,self).__init__()
        self.m_model =  model
        self.m_side = side

        self.m_threshold = threshold
        # self.m_virtual=dict()

        LOGGER.logger.info("[pyCGM2] threshold of the Naim's correction method : %s"%(threshold))

    def correct(self):

        side = self.m_side

        if self.m_side == "Both":
            sides = ["Left","Right"]
        else:
            sides = [self.m_side]

        for side in sides:
            if side== "Left":
                sequence = "ZXiY"
                letter = "L"
            elif side == "Right":
                sequence = "ZXY"
                letter = "R"
            else:
                raise Exception("[pyCGM2] : side not recognized ( Left or Right only)")

            LOGGER.logger.warning("Naim knee Correction on the %s side "%(side))
            seg = self.m_model.getSegment(side+" Thigh")

            hjc = self.m_model.getSegment(side+" Thigh").anatomicalFrame.getNodeTrajectory(letter+"HJC")
            kjc = self.m_model.getSegment(side+" Thigh").anatomicalFrame.getNodeTrajectory(letter+"KJC")
            ajc = self.m_model.getSegment(side+" Shank").anatomicalFrame.getNodeTrajectory(letter+"AJC")

            v = np.cross(hjc-kjc,ajc-kjc)

            # 3d angle
            va = kjc-ajc
            vb = hjc-kjc

            angle = np.zeros((va.shape[0],1))

            for i in range(0,va.shape[0]):
                angle[i] = np.rad2deg(np.arctan2(np.linalg.norm(np.cross(va[i,:],vb[i,:])), np.dot(va[i,:],vb[i,:])))


            # extract v> threshold
            v_sup = list()
            for i in range(0,va.shape[0]):
                if angle[i]>self.m_threshold:
                    v_sup.append(v[i,:])
            v_sup = np.asarray(v_sup)

            vmean = v_sup.mean(axis=0)

            # normalized axis
            v = np.nan_to_num(np.divide(vmean,np.linalg.norm(vmean)))

            # virtual point along the mean axis
            virtual = np.zeros((len(ajc),3))
            for i in range(0,len(ajc)):
                virtual[i,:]= kjc[i,:] + -100 * v if side == "Left" else kjc[i,:] + 100 * v

            # self.m_virtual[side] = virtual

            #alteration of the segmental motion
            seg.anatomicalFrame.motion=[] # erase all previous motion

            csFrame=frame.Frame()
            for i in range(0,len(ajc)):
                pt1=kjc[i,:]
                pt2=hjc[i,:]
                pt3=virtual[i,:]
                ptOrigin=hjc[i,:]

                a1=(pt2-pt1)
                a1=np.nan_to_num(np.divide(a1,np.linalg.norm(a1)))

                v=(pt3-pt1)
                v=np.nan_to_num(np.divide(v,np.linalg.norm(v)))

                a2=np.cross(a1,v)
                a2=np.nan_to_num(np.divide(a2,np.linalg.norm(a2)))

                x,y,z,R=frame.setFrameData(a1,a2,sequence)

                csFrame.m_axisX=x
                csFrame.m_axisY=y
                csFrame.m_axisZ=z
                csFrame.setRotation(R)
                csFrame.setTranslation(ptOrigin)

                seg.anatomicalFrame.addMotionFrame(copy.deepcopy(csFrame))


            LOGGER.logger.warning("[pyCGM2] : %s thigh anatomical frame motion corrected according Naim et al, 2019"%(side))
