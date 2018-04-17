


import FWCore.ParameterSet.Config as cms
from math import ceil,log

# All workingpoints we need to probe
workingPoints = ["TTVLoose","TTVLeptonMvaL","TTVLeptonMvaM","TTVLeptonMvaT","RTTVLeptonMvaL","RTTVLeptonMvaM","RTTVLeptonMvaT","TightCharge"]

#
# Sequence to add userfloats
#
def ttvUserFloatsSeq(process, options):
    from PhysicsTools.NanoAOD.electrons_cff import isoForEle, ptRatioRelForEle, slimmedElectronsWithUserData 

    if options['is2016']: effAreas = 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt'
    else:                 effAreas = 'RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt'

    process.isoForEle                = isoForEle
    process.isoForEle.rho_MiniIso    = cms.InputTag("fixedGridRhoFastjetAll")
    process.isoForEle.EAFile_MiniIso = cms.FileInPath(effAreas)
    process.isoForEle.EAFile_PFIso   = cms.FileInPath(effAreas)

    process.ptRatioRelForEle             = ptRatioRelForEle
    process.slimmedElectronsWithUserData = slimmedElectronsWithUserData

    # Make a new electron collection, with additional variables that are used for the LeptonMVA below
    process.slimmedElectronsWithUserData.src = cms.InputTag(options['ELECTRON_COLL'])
    process.slimmedElectronsWithUserData.userFloats = cms.PSet(
      miniIsoChg           = cms.InputTag("isoForEle:miniIsoChg"),
      miniIsoAll           = cms.InputTag("isoForEle:miniIsoAll"),
      PFIsoChg             = cms.InputTag("isoForEle:PFIsoChg"),
      PFIsoAll             = cms.InputTag("isoForEle:PFIsoAll"),
      ptRatio              = cms.InputTag("ptRatioRelForEle:ptRatio"),
      ptRel                = cms.InputTag("ptRatioRelForEle:ptRel"),
      jetNDauChargedMVASel = cms.InputTag("ptRatioRelForEle:jetNDauChargedMVASel"),
      closestJetDeepCsv    = cms.InputTag("ptRatioRelForEle:closestJetDeepCsv"),
    )
    process.slimmedElectronsWithUserData.userIntFromBools = cms.PSet() # Removed
    process.slimmedElectronsWithUserData.userInts         = cms.PSet() # Removed

    options['ELECTRON_COLL'] = "slimmedElectronsWithUserData"
    process.userFloatsSeq = cms.Sequence(
      process.isoForEle +
      process.ptRatioRelForEle + 
      process.slimmedElectronsWithUserData 
    )
    return process.userFloatsSeq

#
# Helper to create TTV id's
#
def ttvVarHelper(process, options):
    process.ttvEleVarHelper = cms.EDProducer("TTVElectronVariableHelper",
      probes = cms.InputTag("slimmedElectronsWithUserData"),
      mvasGP = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
      mvas   = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values"),
      is2016 = cms.untracked.bool((True if options['is2016'] else False)),
    )
    return process.ttvEleVarHelper

#
# Add probes
#
def ttvTagProbes(process):
  pass


def temp(process):
    process.ttv_ele_sequence = cms.Sequence()
    def getProbes(name):
      temp = cms.EDProducer("PatElectronSelectorByValueMap",
        input     = cms.InputTag("goodElectrons"),
        cut       = cms.string(options['ELECTRON_CUTS']),
        selection = cms.InputTag('ttvEleVarHelper:pass' + name),
        id_cut    = cms.bool(True)
      )
      setattr(process, 'probes' + name, temp)
      process.ttv_ele_sequence += temp

    for wp in workingPoints: getProbes(wp)

    # Applies trigger matching (denominators need to be listed here)
    def getAllProbes(name):
      temp = process.goodElectronsTagHLT.clone()
      temp.isAND = cms.bool(False)
      temp.selection = cms.InputTag('probes' + name)
      setattr(process, 'goodElectronsProbe' + name, temp)
      process.ttv_ele_sequence += temp

    referenceWp = ['Feb2018Loose','RFeb2018LeptonMvaL','RFeb2018LeptonMvaM','RFeb2018LeptonMvaT']
    for wp in referenceWp:
      getAllProbes(wp)

def getTreeSeqTTV(process):
    tree_sequence = cms.Sequence()

    def addProducer(name, allProbes, ref, workingPointsForRef):
      probeEle = process.probeEle.clone()
      probeEle.inputs = cms.InputTag('goodElectrons' + ref) # this should be like goodElectrons
      setattr(process, 'probe' + ref, probeEle)
      process.ele_sequence += probeEle

      tnpPairing       = process.tnpPairingEleIDs.clone()
      tnpPairing.decay = cms.string('tagEle probe' + ref)
      setattr(process, 'tnpPairing' + ref, tnpPairing)
      process.tnpPairs_sequence *= tnpPairing

      producer = process.tnpEleIDs.clone()
#      producer.jetCollection = cms.InputTag("slimmedJets")
#      producer.jet_pt_cut    = cms.double(30.)
#      producer.jet_eta_cut   = cms.double(2.5)
#      producer.match_delta_r = cms.double(0.3)
      producer.tagProbePairs = cms.InputTag('tnpPairing' + ref)
      producer.allProbes     = cms.InputTag('probe' + ref)
      producer.flags         = cms.PSet()
      for wp in workingPointsForRef: setattr(producer.flags, 'passing' + wp, cms.InputTag('probe' + wp))

      setattr(process, name, producer)
      tree_sequence *= producer

    addProducer('EleToId',                        'Ele',                ['Feb2018Loose'])
    addProducer('Feb2018LooseToLeptonMva',        'Feb2018Loose',       ['Feb2018LeptonMvaL','Feb2018LeptonMvaM','Feb2018LeptonMvaT'])
    addProducer('Feb2018LeptonMvaLToTightCharge', 'RFeb2018LeptonMvaL', ['TightCharge'])
    addProducer('Feb2018LeptonMvaMToTightCharge', 'RFeb2018LeptonMvaM', ['TightCharge'])
    addProducer('Feb2018LeptonMvaTToTightCharge', 'RFeb2018LeptonMvaT', ['TightCharge'])
    return tree_sequence
