#!/bin/env python
import os

#
# Example script to submit TnPTreeProducer to crab
#
submitVersion = "2020-05-19"
doL1matching  = False

defaultArgs   = ['doEleID=True','doPhoID=True','doTrigger=True']
mainOutputDir = '/store/user/%s/TnP/%s' % (os.environ['USER'], submitVersion)

# Logging the current version of TnpTreeProducer here, such that you can find back what the actual code looked like when you were submitting
os.system('mkdir -p /eos/uscms/%s' % mainOutputDir)
os.system('(git log -n 1;git diff) &> /eos/cms/%s/git.log' % mainOutputDir)


#
# Common CRAB settings
#
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config
config = config()

config.General.requestName             = ''
config.General.transferLogs            = False
config.General.workArea                = 'crab_%s' % submitVersion

config.JobType.pluginName              = 'Analysis'
config.JobType.psetName                = '../python/TnPTreeProducer_cfg.py'
config.JobType.sendExternalFolder      = True
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset               = ''
config.Data.inputDBS                   = 'global'
config.Data.publication                = False
config.Data.allowNonValidInputDataset  = True
config.Site.storageSite                = 'T3_US_FNALLPC'


#
# Certified lumis for the different eras
#
def getLumiMask(era):
  if   era=='2016': return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
  elif era=='2017': return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
  elif era=='2018': return 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'


#
# Submit command
#
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

def submit(config, requestName, sample, era, globalTag, json, extraParam=[]):
  isMC                        = 'SIM' in sample
  config.General.requestName  = '%s_%s' % (era, requestName)
  config.Data.inputDataset    = sample
  config.Data.outLFNDirBase   = '%s/%s/%s/' % (mainOutputDir, era, 'mc' if isMC else 'data')
  config.Data.splitting       = 'FileBased' if isMC else 'LumiBased'
  config.Data.lumiMask        = None if isMC else json
  config.Data.unitsPerJob     = 5 if isMC else 100
  config.JobType.pyCfgParams  = defaultArgs + ['isMC=True' if isMC else 'isMC=False', 'GT=%s' % globalTag, 'era=%s' % era] + extraParam

  print config
  try:                           crabCommand('submit', config = config)
  except HTTPException as hte:   print "Failed submitting task: %s" % (hte.headers)
  except ClientException as cle: print "Failed submitting task: %s" % (cle)
  print
  print

#
# Wrapping the submit command
# In case of doL1matching=True, vary the L1Threshold and use sub-json
#
from multiprocessing import Process
def submitWrapper(requestName, sample, era, globalTag, extraParam=[]):
  if doL1matching:
    from getLeg1ThresholdForDoubleEle import getLeg1ThresholdForDoubleEle
    for leg1Threshold, json in getLeg1ThresholdForDoubleEle(era):
      print 'Submitting for leg 1 threshold %s' % (leg1Threshold)
      p = Process(target=submit, args=(config, '%s_leg1Threshold%s' % (requestName, leg1Threshold), sample, era, globalTag, json, extraParam + ['L1Threshold=%s' % leg1Threshold]))
      p.start()
      p.join()
  else:
    p = Process(target=submit, args=(config, requestName, sample, era, globalTag, getLumiMask(era), extraParam))
    p.start()
    p.join()

# List of samples to submit, with eras and global tags
# If you would switch to AOD, don't forget to add 'isAOD=True' to the defaultArgs!

era       = '2016'
globalTag = '94X_dataRun2_v10'
submitWrapper('Run2016B', '/SingleElectron/Run2016B-17Jul2018_ver2-v1/MINIAOD', era, globalTag)
submitWrapper('Run2016C', '/SingleElectron/Run2016C-17Jul2018-v1/MINIAOD', era, globalTag)
submitWrapper('Run2016D', '/SingleElectron/Run2016D-17Jul2018-v1/MINIAOD', era, globalTag)
submitWrapper('Run2016E', '/SingleElectron/Run2016E-17Jul2018-v1/MINIAOD', era, globalTag)
submitWrapper('Run2016F', '/SingleElectron/Run2016F-17Jul2018-v1/MINIAOD', era, globalTag)
submitWrapper('Run2016G', '/SingleElectron/Run2016G-17Jul2018-v1/MINIAOD', era, globalTag)
submitWrapper('Run2016H', '/SingleElectron/Run2016H-17Jul2018-v1/MINIAOD', era, globalTag)

globalTag = '94X_mcRun2_asymptotic_v3'
submitWrapper('DY16_LO_HT-100to200_ext1'         , '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'     , era , globalTag)
submitWrapper('DY16_LO_HT-100to200'                 , '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'     , era , globalTag)
submitWrapper('DY16_LO_HT-200to400'                , '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'     , era , globalTag)
submitWrapper('DY16_LO_HT-200to400_ext1'        , '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM'     , era , globalTag)
submitWrapper('DY16_LO_HT-400to600'                , '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'     , era , globalTag)
submitWrapper('DY16_LO_HT-600to800'                , '/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'     , era , globalTag)
submitWrapper('DY16_LO_HT-800to1200'               , '/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'     , era , globalTag)
submitWrapper('DY16_LO_HT-1200to2500'             , '/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'     , era , globalTag)
submitWrapper('DY16_LO_HT-2500toInf'                ,'/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'     , era , globalTag)

# era       = '2017'
# globalTag = '94X_dataRun2_v11'
# submitWrapper('Run2017B_Photon', '/SinglePhoton/Run2017B-31Mar2018-v1/MINIAOD', era, globalTag, ['isEarly2017=True'])
# submitWrapper('Run2017C_Photon', '/SinglePhoton/Run2017C-31Mar2018-v1/MINIAOD', era, globalTag)
# submitWrapper('Run2017D_Photon', '/SinglePhoton/Run2017D-31Mar2018-v1/MINIAOD', era, globalTag)
# submitWrapper('Run2017E_Photon', '/SinglePhoton/Run2017E-31Mar2018-v1/MINIAOD', era, globalTag)
# submitWrapper('Run2017F_Photon', '/SinglePhoton/Run2017F-31Mar2018-v1/MINIAOD', era, globalTag)
# exit()
# submitWrapper('Run2017B', '/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD', era, globalTag, ['isEarly2017=True'])
# submitWrapper('Run2017C', '/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD', era, globalTag)
# submitWrapper('Run2017D', '/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD', era, globalTag)
# submitWrapper('Run2017E', '/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD', era, globalTag)
# submitWrapper('Run2017F', '/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD', era, globalTag)

# globalTag = '94X_mc2017_realistic_v17'
# submitWrapper('DY17_LO_HT-100to200'         , '/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM'     , era , globalTag)
# submitWrapper('DY17_LO_HT-100to200_newpmx'  , '/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'  , era , globalTag)
# submitWrapper('DY17_LO_HT-1200to2500'       , '/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'        , era , globalTag)
# submitWrapper('DY17_LO_HT-200to400'         , '/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM'          , era , globalTag)
# submitWrapper('DY17_LO_HT-200to400_ext1'    , '/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM'     , era , globalTag)
# submitWrapper('DY17_LO_HT-2500toInf_newpmx' , '/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM' , era , globalTag)
# submitWrapper('DY17_LO_HT-400to600'         , '/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM'     , era , globalTag)
# submitWrapper('DY17_LO_HT-400to600_newpmx'  , '/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'  , era , globalTag)
# submitWrapper('DY17_LO_HT-600to800_newpmx'  , '/DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'  , era , globalTag)
# submitWrapper('DY17_LO_HT-70to100'          , '/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'           , era , globalTag)
# submitWrapper('DY17_LO_HT-800to1200_newpmx' , '/DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM' , era , globalTag)



# era       = '2018'
# globalTag = '102X_dataRun2_v12'
# submitWrapper('Run2018A', '/EGamma/Run2018A-17Sep2018-v2/MINIAOD', era, globalTag)
# submitWrapper('Run2018B', '/EGamma/Run2018B-17Sep2018-v1/MINIAOD', era, globalTag)
# submitWrapper('Run2018C', '/EGamma/Run2018C-17Sep2018-v1/MINIAOD', era, globalTag)
# submitWrapper('Run2018D', '/EGamma/Run2018D-22Jan2019-v2/MINIAOD', era, globalTag)

# globalTag = '102X_upgrade2018_realistic_v20'
# submitWrapper('DY18_HT-100to200'   , '/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'      , era , globalTag)
# submitWrapper('DY18_HT-1200to2500' , '/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'    , era , globalTag)
# submitWrapper('DY18_HT-200to400'   , '/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'      , era , globalTag)
# submitWrapper('DY18_HT-2500toInf'  , '/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'     , era , globalTag)
# submitWrapper('DY18_HT-400to600'   , '/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v3/MINIAODSIM' , era , globalTag)
# submitWrapper('DY18_HT-600to800'   , '/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'      , era , globalTag)
# submitWrapper('DY18_HT-70to100'    , '/DYJetsToLL_M-50_HT-70to100_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'       , era , globalTag)
# submitWrapper('DY18_HT-800to1200'  , '/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'     , era , globalTag)