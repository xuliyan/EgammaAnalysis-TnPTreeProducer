


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

    if options['is2016']: effAreas = 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt'
    else:                 effAreas = 'RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt'

    process.isoForEle = isoForEle
    process.isoForEle.rho_MiniIso    = cms.InputTag("fixedGridRhoFastjetAll")
    process.isoForEle.EAFile_MiniIso = cms.FileInPath(effAreas)
    process.isoForEle.EAFile_PFIso   = cms.FileInPath(effAreas)

    process.ptRatioRelForEle = ptRatioRelForEle
    process.slimmedElectronsWithUserData = slimmedElectronsWithUserData

    process.electronMVATTV = electronMVATTV2016 if options['is2016'] else electronMVATTV2017

    # Make a new electron collection, with additional variables that are used for the LeptonMVA below
    process.slimmedElectronsWithUserData.src = cms.InputTag(options['ELECTRON_COLL'])
    process.slimmedElectronsWithUserData.userFloats = cms.PSet(
        miniIsoChg = cms.InputTag("isoForEle:miniIsoChg"),
        miniIsoAll = cms.InputTag("isoForEle:miniIsoAll"),
        PFIsoChg = cms.InputTag("isoForEle:PFIsoChg"),
        PFIsoAll = cms.InputTag("isoForEle:PFIsoAll"),
        ptRatio = cms.InputTag("ptRatioRelForEle:ptRatio"),
        ptRel = cms.InputTag("ptRatioRelForEle:ptRel"),
        jetNDauChargedMVASel = cms.InputTag("ptRatioRelForEle:jetNDauChargedMVASel"),
        )
    process.slimmedElectronsWithUserData.userIntFromBools = cms.PSet() # Removed
    process.slimmedElectronsWithUserData.userInts = cms.PSet() # Removed

    # Run the ttH MVA, modify src and take MVA directly from VID (VID must run before this producer)
    process.electronMVATTV.src = cms.InputTag("slimmedElectronsWithUserData")

    # At the end of this, everything we need is either a userfloat or in a producer linked with slimmedElectronsWithUserData
    process.ttvEleVarHelper = cms.EDProducer("TTVElectronVariableHelper",
        probes         = cms.InputTag("slimmedElectronsWithUserData"),
        mvas           = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
        dxy            = cms.InputTag("eleVarHelper:dxy"),
        dz             = cms.InputTag("eleVarHelper:dz"),
        leptonMvas     = cms.InputTag("electronMVATTV"),
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


