from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys, os

# this will use CRAB client API
from CRABAPI.RawCommand import crabCommand

# talk to DBS to get list of files in this dataset
from dbs.apis.dbsClient import DbsApi
dbs = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

# this now standard CRAB configuration

from WMCore.Configuration import Configuration

config = config()

doEleTree = 'doEleID=False'
doPhoTree = 'doPhoID=False'
doHLTTree = 'doTrigger=True'

submitVersion = "HLT_2018_v2"
if os.environ["USER"] in ['tomc']:
  mainOutputDir           = os.path.join('/store/user/tomc/tnp/electrons', submitVersion)
  config.Site.storageSite = 'T2_BE_IIHE'
else:
  raise Exception('User settings not known')


config.General.requestName = ''
config.General.transferLogs = False
config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = '../../python/TnPTreeProducer_cfg.py'
config.JobType.sendExternalFolder     = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'global'
config.Data.publication = False
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
        if inputDataset: config.Data.inputDataset = inputDataset
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)


    ##### submit DATA
    config.Data.splitting      = 'LumiBased'
    config.Data.unitsPerJob    = 100
    config.Data.outLFNDirBase  = os.path.join(mainOutputDir, 'data')
    config.Data.lumiMask       = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
    config.JobType.pyCfgParams = ['isMC=False', doEleTree, doPhoTree, doHLTTree, 'GT=102X_dataRun2_Sep2018Rereco_v1']
 
    submit(config, 'Run2018A-17Sep2018-v2', '/EGamma/Run2018A-17Sep2018-v2/MINIAOD')
    submit(config, 'Run2018B-17Sep2018-v1', '/EGamma/Run2018B-17Sep2018-v1/MINIAOD')
    submit(config, 'Run2018C-17Sep2018-v1', '/EGamma/Run2018C-17Sep2018-v1/MINIAOD')

    config.JobType.pyCfgParams = ['isMC=False', doEleTree, doPhoTree, doHLTTree, 'GT=102X_dataRun2_Prompt_v11']

    submit(config, 'Run2018D_prompt_v1', '/EGamma/Run2018D-PromptReco-v1/MINIAOD')
    submit(config, 'Run2018D_prompt_v2', '/EGamma/Run2018D-PromptReco-v2/MINIAOD')

    ##### submit MC
    config.Data.splitting      = 'FileBased'
    config.Data.unitsPerJob    = 8
    config.Data.outLFNDirBase  = os.path.join(mainOutputDir, 'mc')
    config.JobType.pyCfgParams = ['isMC=True', doEleTree, doPhoTree, doHLTTree, 'GT=102X_upgrade2018_realistic_v12']

    config.Data.runRange = ''
    config.Data.lumiMask  = ''
    submit(config, 'DY', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM')
