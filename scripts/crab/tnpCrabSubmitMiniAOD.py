#!/usr/bin/env python
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys,os,time
os.system("eval `scramv1 runtime -sh`")

# Always first copy the latest version of the makeTree.py
import shutil
shutil.copyfile('../../python/TnPTreeProducer_cfg.py', 'TnPTreeProducer_cfg.py')

config = config()

submitVersion = "Moriond18_v4"

if os.environ["USER"] in ['tomc']:
  mainOutputDir           = os.path.join('/store/user/tomc/tnp/electrons', submitVersion)
  config.Site.storageSite = 'T2_BE_IIHE'
else:
  raise Exception('User settings not known')

config.General.transferLogs = False

config.JobType.pluginName         = 'Analysis'
config.JobType.psetName           = 'TnPTreeProducer_cfg.py'
config.JobType.sendExternalFolder = True

config.Data.inputDBS                  = 'global'
config.Data.publication               = False
config.Data.allowNonValidInputDataset = True


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_%s' % submitVersion

    def submit(config, requestName, inputDataset):
        config.General.requestName = requestName
        config.Data.inputDataset   = inputDataset
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)
        time.sleep(15)


    ##### submit MC
    config.Data.splitting      = 'FileBased'
    config.Data.unitsPerJob    = 8
    config.Data.outLFNDirBase  = os.path.join(mainOutputDir,'mc17')
    config.JobType.pyCfgParams = ['isMC=True', 'GT=94X_mc2017_realistic_v13']

    submit(config, 'DYToLL_madgraph',     '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1/MINIAODSIM')
    submit(config, 'DYToLL_madgraph_ext', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10_ext1-v1/MINIAODSIM')
    submit(config, 'DYToLL_amcatnlo',     '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM')
    submit(config, 'DYToLL_amcatnlo_ext', '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10_ext1-v1/MINIAODSIM')

    config.Data.outLFNDirBase  = os.path.join(mainOutputDir, 'mc2016')
    config.JobType.pyCfgParams = ['isMC=True', 'GT=80X_mcRun2_asymptotic_2016_TrancheIV_v8','is2016=True']
    
    submit(config, 'DYToLL_mcatnlo16',    '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM')
    submit(config, 'DYToLL_madgraph16',   '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM')


    ##### submit DATA
    config.Data.splitting      = 'LumiBased'
    config.Data.unitsPerJob    = 100
    config.Data.outLFNDirBase  = os.path.join(mainOutputDir,'data2017')
    config.Data.lumiMask       = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
    config.JobType.pyCfgParams = ['isMC=False', 'GT=94X_dataRun2_v6']
 
    submit(config, '17Nov2017_RunB', '/SingleElectron/Run2017B-17Nov2017-v1/MINIAOD')    
    submit(config, '17Nov2017_RunC', '/SingleElectron/Run2017C-17Nov2017-v1/MINIAOD')    
    submit(config, '17Nov2017_RunD', '/SingleElectron/Run2017D-17Nov2017-v1/MINIAOD')    
    submit(config, '17Nov2017_RunE', '/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD')
    submit(config, '17Nov2017_RunF', '/SingleElectron/Run2017F-17Nov2017-v1/MINIAOD')

    config.Data.outLFNDirBase  = os.path.join(mainOutputDir,'data2016')
    config.Data.lumiMask       = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    config.JobType.pyCfgParams = ['isMC=False', 'GT=80X_dataRun2_2016SeptRepro_v7','is2016=True']

    submit(config, 'Run2016B-v2', '/SingleElectron/Run2016B-03Feb2017_ver2-v2/MINIAOD')
    submit(config, 'Run2016C',    '/SingleElectron/Run2016C-03Feb2017-v1/MINIAOD')
    submit(config, 'Run2016D',    '/SingleElectron/Run2016D-03Feb2017-v1/MINIAOD')
    submit(config, 'Run2016E',    '/SingleElectron/Run2016E-03Feb2017-v1/MINIAOD')
    submit(config, 'Run2016F',    '/SingleElectron/Run2016F-03Feb2017-v1/MINIAOD')
    submit(config, 'Run2016G',    '/SingleElectron/Run2016G-03Feb2017-v1/MINIAOD')
    submit(config, 'Run2016H-v2', '/SingleElectron/Run2016H-03Feb2017_ver2-v1/MINIAOD')
    submit(config, 'Run2016H-v3', '/SingleElectron/Run2016H-03Feb2017_ver3-v1/MINIAOD')
