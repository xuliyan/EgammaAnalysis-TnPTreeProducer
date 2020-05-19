import FWCore.ParameterSet.Config as cms


filesMiniAOD_Preliminary2018 = {
    'mc' :  cms.untracked.vstring(
#        '/store/mc/RunIISpring18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/100X_upgrade2018_realistic_v10-v2/100000/6815ED2D-7530-E811-90C0-FA163E27991E.root',
#        '/store/mc/RunIISpring18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/100X_upgrade2018_realistic_v10-v2/100000/801BEA3C-9C2F-E811-AFA4-02163E015DB8.root',
#        '/store/mc/RunIISpring18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/100X_upgrade2018_realistic_v10-v2/100000/6815ED2D-7530-E811-90C0-FA163E27991E.root'
#        '/store/relval/CMSSW_10_2_5/RelValZEE_13/MINIAODSIM/PU25ns_102X_upgrade2018_realistic_v12_Can30fb_v1_HS_rsb-v1/10000/12D80735-7226-134A-B33E-DEC1F061C9F5.root'
        '/store/mc/RunIIAutumn18MiniAOD/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/D0F66982-B732-0D4F-BA52-AC8868C57CFE.root'
        ),

    'data' : cms.untracked.vstring(
        #'/store/data/Run2018A/EGamma/MINIAOD/PromptReco-v1/000/315/252/00000/40343760-464B-E811-ACC9-02163E00B0CB.root',
#        '/store/data/Run2018D/EGamma/MINIAOD/PromptReco-v2/000/320/500/00000/0225B398-F895-E811-A82F-FA163EE8C7E8.root',
#        '/store/data/Run2018D/EGamma/MINIAOD/PromptReco-v2/000/324/420/00000/44AB86DD-CF58-4845-9FAC-63D20958C491.root',
        '/store/data/Run2018A/EGamma/MINIAOD/22Jun2018-v1/20000/E4718DAE-847C-E811-95CE-FA163E1746EB.root'
        )
}

filesAOD_Preliminary2018 = {
    'mc' :  cms.untracked.vstring(
        '/store/mc/RunIISpring18DRPremix/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/AODSIM/100X_upgrade2018_realistic_v10-v2/90001/FE8F7D45-133E-E811-891E-FA163EA4957D.root',
        ),
    'data' :  cms.untracked.vstring(
        '/store/data/Run2018B/EGamma/AOD/PromptReco-v1/000/317/864/00000/C269C719-EC71-E811-9C7E-FA163EF55202.root',
        )
}

filesAOD_Preliminary2017 = {
    'mc' :  cms.untracked.vstring(
        '/store/mc/RunIIFall17DRPremix/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/AODSIM/PU2017RECOPF_94X_mc2017_realistic_v11-v1/50000/D42B8057-9F67-E811-9656-549F3525C4EC.root'
        ),
    'data' :  cms.untracked.vstring(
        '/store/data/Run2017F/SingleElectron/AOD/17Nov2017-v1/50000/005B2A56-96E0-E711-B727-0CC47A4D7690.root',
        )
}

 
filesMiniAOD_Preliminary2017 = {
    'mc' :  cms.untracked.vstring(
#        '/store/mc/RunIISummer17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10_ext1-v1/00000/02A09B42-59F1-E711-9E8F-002590DE6E30.root',
#        '/store/mc/RunIISummer17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10_ext1-v1/110000/02CF84A2-6086-E711-A3A1-0CC47A7C3458.root',#92X
        '/store/mc/RunIIFall17MiniAOD/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/20000/001C74A0-B4D6-E711-BD4B-FA163EB4F61D.root',#94X
        ),
    
    'data' : cms.untracked.vstring( 
        #       '/store/data/Run2017B/SingleElectron/MINIAOD/17Nov2017-v1/40000/064D4B85-E9DB-E711-8B34-02163E019D0E.root',
        '/store/data/Run2017B/SingleElectron/MINIAOD/31Mar2018-v1/60000/B2A401AB-3E38-E811-8FE1-008CFAC940DC.root',
        #        '/store/data/Run2017C/SingleElectron/MINIAOD/PromptReco-v1/000/299/368/00000/08588A8B-836D-E711-8ACF-02163E01A3AC.root',
        #        '/store/data/Run2017B/SingleElectron/MINIAOD/PromptReco-v1/000/297/050/00000/166F7BB0-3C56-E711-BD8B-02163E0145C5.root',     
        )
}

# 2016 SAMPLES
filesMiniAOD_ReReco2016 = {
    'mc' :  cms.untracked.vstring(
        '/store/mc/RunIISummer16MiniAODv3/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/110000/FCEAAD4B-4AEA-E811-8B96-001E67DDC0FB.root',
        ),
    
    'data' : cms.untracked.vstring( 
        '/store/data/Run2016B/SingleElectron/MINIAOD/17Jul2018_ver2-v1/00000/00293812-4D8C-E811-B7C5-00266CFFC80C.root',
        )
}

