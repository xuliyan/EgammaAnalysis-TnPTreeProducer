#include "MiniAODL1CandProducerV3.h"
  
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

typedef MiniAODL1CandProducerV3<pat::Electron> PatElectronL1CandProducerV3;
DEFINE_FWK_MODULE(PatElectronL1CandProducerV3);

typedef MiniAODL1CandProducerV3<pat::Photon> PatPhotonL1CandProducer;
DEFINE_FWK_MODULE(PatPhotonL1CandProducer);

