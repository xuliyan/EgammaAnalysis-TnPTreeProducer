# EgammaAnalysis-TnPTreeProducer
TnP package for EGM for UL

*Currently this branch does not work with the doPhoIDs options*
Based on the default RunIIfinal branch, but with minor updates to get it running in CMSSW\_10\_6\_X

## To produce new tuples
### 1. Install (CMSSW\_10\_6\_X or higher)

```
cmsrel CMSSW_10_6_10
cd CMSSW_10_6_10/src
cmsenv
git clone -b RunIIfinal_UL https://github.com/tomcornelis/EgammaAnalysis-TnPTreeProducer EgammaAnalysis/TnPTreeProducer
scram b -j8
```

### 2. Try-out 
You can find the cmsRun executable in EgammaAnalysis/TnPTreeProducer/python:
```
cmsRun TnPTreeProducer_cfg.py isMC=True doTrigger=True era=2018
```
Check [TnPTreeProducer\_cfg.py](python/TnPTreeProducer_cfg.py) for all available options. Update the code if you need to implement custom-made recipes.

Test files can be defined in [python/etc/tnpInputTestFiles\_cff.py](python/etc/tnpInputTestFiles_cff.py)
If you update the code, you can use the ./runTests.py script in the test directory to check for new differences in the 2016, 2017 and 2018 test files.

### 3. Submit jobs
Check in EgammaAnalysis/TnPTreeProducer//crab the tnpCrabSubmit.py script to submit your jobs using crab

## To make a pull request to this repository
1. On github fork the package https://github.com/cms-analysis/EgammaAnalysis-TnPTreeProducer 
2. Add the remote 
```
git remote add username-push git@github.com:username/EgammaAnalysis-TnPTreeProducer.git
```
3. push commits to fork and then standard pull request process
```
git push username-push branchname
```

## Adding new workingpoints
You can add new electron workingpoints in [python/egmElectronIDModules\_cff.py](python/egmElectronIDModules_cff.py) and new photon workingpoints
in [python/egmPhotonIDModules\_cff.py](python/egmPhotonIDModules_cff.py). Each new workingpoint added in these python config fragments will
add a new "passing<WP>" boolean in the electron and photon trees respectively. Of course, one can also choose to simply add a variable in
[python/egmTreesContent\_cff.py](python/egmTreesContent\_cff.py), which might be preferred for MVA variables when you want to have the
flexibility to explore different workingpoints: you can simply put a cut on these variable in the egm\_tnp\_analysis package.

## Note about leptonMva
Some leptonMva variables are now included in the TnPTreeProducer trees. Unfortunately, it is very easy to get out of sync for these variables:
even a new global tag could slightly alter the input variables, given some of them are dependent on the jet energy corrections or b-taggers which
were in use when training these leptonMva's. Additionaly, some leptonMva's use (extremely) old effective areas for miniIso or relIso variables.
We therefore strongly recommend leptonMva analyzers to sync with their own analysis code before producing tuples.
The sync can easily be done by setting the debug flag to True in [python/leptonMva\_cff.py](python/leptonMva_cff.py). The leptonMva xml files
are found in [data](data), and implementation of a new leptonMvaType can happen in the produce function in
[plugins/LeptonMvaProducer.cc](plugins/LeptonMvaProducer.cc).
