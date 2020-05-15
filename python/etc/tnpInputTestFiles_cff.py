import FWCore.ParameterSet.Config as cms

# Some miniAOD testfiles, which are available now and hopefully don't get deleted too soon
filesMiniAOD_UL2018 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL18MiniAOD/DYJetsToEE_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/NoPUECALGT1_106X_upgrade2018_realistic_v11_L1v1-v3/50000/0DC236F0-792D-4749-A920-00B3DBE98BF0.root'),
    'data' : cms.untracked.vstring('/eos/cms//store/data/Run2018D/EGamma/MINIAOD/12Nov2019_UL2018-v1/40000/1769B854-08A2-D441-B7B2-1D1646BBF99A.root'),
}

filesMiniAOD_UL2017 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/100001/454B5511-3427-834C-A598-AA42475EFC94.root'),
    'data' : cms.untracked.vstring('/store/data/Run2017F/SingleElectron/MINIAOD/09Aug2019_UL2017_rsb-v2/00000/D6FA4039-620B-C74E-B9E3-CC9BBA38A929.root'),
}


# AOD testfiles
filesAOD_UL2018 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL18RECO/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/230000/696A0205-2900-054F-A4D8-8528E5EA34A9.root'),
    'data' : cms.untracked.vstring('/store/data/Run2018D/EGamma/AOD/ForValUL2018-v2/60002/C1BC446B-0B7E-D74E-9FD0-E9506552EFB8.root'),
}

filesAOD_UL2017 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL17RECO/DYJetsToEE_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/AODSIM/106X_mc2017_realistic_v6-v2/30000/FFCA4B4F-6AFD-D644-8CA6-C9264C6C0C68.root'),
    'data' : cms.untracked.vstring('/store/data/Run2017F/SingleElectron/AOD/09Aug2019_UL2017_rsb-v2/110000/20034F69-8143-8946-8F26-17954FEFDFF7.root'),
}
