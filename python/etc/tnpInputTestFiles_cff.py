import FWCore.ParameterSet.Config as cms

# Some miniAOD testfiles, which are available now and hopefully don't get deleted too soon
filesMiniAOD_2018 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/90000/17D5FDFE-C156-FE47-9202-F819E74881D3.root'),
    'data' : cms.untracked.vstring('/store/data/Run2018A/EGamma/MINIAOD/17Sep2018-v2/100000/0004A5E9-9F18-6B42-B31D-4206406CE423.root'),
}

filesMiniAOD_2017 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14_ext3-v1/30000/84A5C6DA-1EDF-E911-B22B-FA163E1A63BB.root'),
    'data' : cms.untracked.vstring('/store/data/Run2017B/SingleElectron/MINIAOD/31Mar2018-v1/90000/021B46D3-C537-E811-9064-008CFAE452E0.root')
}

filesMiniAOD_2016 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer16MiniAODv3/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/100000/005FEC6C-D6C2-E811-A83B-A0369FC5E094.root'),
    'data' : cms.untracked.vstring('/store/data/Run2016B/SingleElectron/MINIAOD/17Jul2018_ver2-v1/00000/00293812-4D8C-E811-B7C5-00266CFFC80C.root')
}

# Ultralegacy miniAOD
filesMiniAOD_UL2018 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v11_L1v1-v2/70000/00C34BB0-FB09-C54E-9F86-E9640A366B5F.root'),
    'data' : cms.untracked.vstring('/store/data/Run2018D/EGamma/MINIAOD/12Nov2019_UL2018-v4/120000/F0574B49-1CA1-484A-9A3A-698B1903796D.root'),
}

filesMiniAOD_UL2017 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL17MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/100001/454B5511-3427-834C-A598-AA42475EFC94.root'),
    'data' : cms.untracked.vstring('/store/data/Run2017F/SingleElectron/MINIAOD/09Aug2019_UL2017_rsb-v2/00000/D6FA4039-620B-C74E-B9E3-CC9BBA38A929.root'),
}



# No AOD tests files accessible on lxplus!

# Ultralegacy AOD
filesAOD_UL2018 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL18RECO/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/230000/696A0205-2900-054F-A4D8-8528E5EA34A9.root'),
    'data' : cms.untracked.vstring('/store/data/Run2018D/EGamma/AOD/ForValUL2018-v2/60002/C1BC446B-0B7E-D74E-9FD0-E9506552EFB8.root'),
}

filesAOD_UL2017 = {
    'mc' :   cms.untracked.vstring('/store/mc/RunIISummer19UL17RECO/DYJetsToEE_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/AODSIM/106X_mc2017_realistic_v6-v2/30000/FFCA4B4F-6AFD-D644-8CA6-C9264C6C0C68.root'),
    'data' : cms.untracked.vstring('/store/data/Run2017F/SingleElectron/AOD/09Aug2019_UL2017_rsb-v2/110000/20034F69-8143-8946-8F26-17954FEFDFF7.root'),
}
