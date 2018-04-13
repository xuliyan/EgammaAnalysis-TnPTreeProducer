


import FWCore.ParameterSet.Config as cms
from math import ceil,log

# All workingpoints we need to probe
workingPoints = ["TTVLoose","TTVLeptonMvaL","TTVLeptonMvaM","TTVLeptonMvaT","RTTVLeptonMvaL","RTTVLeptonMvaM","RTTVLeptonMvaT","TightCharge"]

def addTTVIDs(process, options):

    # For some reason importing the NanoAOD configuration breakes VID, so we need to make 
    # sure these lines are called before calling setIDs() in the egmTreesSetup
    from PhysicsTools.NanoAOD.electrons_cff import isoForEle 
    from PhysicsTools.NanoAOD.electrons_cff import ptRatioRelForEle
    from PhysicsTools.NanoAOD.electrons_cff import slimmedElectronsWithUserData
    from PhysicsTools.NanoAOD.electrons_cff import electronMVATTV2016, electronMVATTV2017

    process.isoForEle = isoForEle 
    process.ptRatioRelForEle = ptRatioRelForEle
    process.slimmedElectronsWithUserData = slimmedElectronsWithUserData
    process.electronMVATTV2016 = electronMVATTV2016
    process.electronMVATTV2017 = electronMVATTV2017

    # Make a new electron collection, with additional variables that are used for the LeptonMVA below
    process.slimmedElectronsWithUserData.src = cms.InputTag(options['ELECTRON_COLL'])
    process.slimmedElectronsWithUserData.userIntFromBools = cms.PSet() # Removed
    process.slimmedElectronsWithUserData.userInts = cms.PSet() # Removed

    # Run the ttH MVA, modify src and take MVA directly from VID (VID must run before this producer)
    process.electronMVATTV2016.src = cms.InputTag("slimmedElectronsWithUserData")
    process.electronMVATTV2017.src = cms.InputTag("slimmedElectronsWithUserData")

    # At the end of this, everything we need is either a userfloat or in a producer linked with slimmedElectronsWithUserData

    # Next, we'll call Tom's MyElectronVariableHelper, which will calculate all the needed IDs. Alternatively, we could hack these into the fitter, since all the needed variables exist...
    # ... if the fitter can edit the probe requirements both at the numerator and the denominator, then all the work can be done there, starting from the loosest Tag/Probe combination!

    process.ttvEleVarHelper = cms.EDProducer("TTVElectronVariableHelper",
        probes         = cms.InputTag("slimmedElectronsWithUserData"),
        mvas           = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
        dxy            = cms.InputTag("eleVarHelper:dxy"),
        dz             = cms.InputTag("eleVarHelper:dz"),
        leptonMvas     = cms.InputTag("electronMVATTV2016" if options['is2016'] else "electronMVATTV2017"),
    )

    process.ttv_sequence = cms.Sequence(
        process.isoForEle +
        process.ptRatioRelForEle + 
        process.slimmedElectronsWithUserData 
        )

    process.ttv_sequence_requiresVID = cms.Sequence(
        process.electronMVATTV + 
        process.ttvEleVarHelper
        )


