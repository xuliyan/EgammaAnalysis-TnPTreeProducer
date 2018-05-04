#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "TMVA/Reader.h"

#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "TMath.h"

namespace{
  template<typename T> void Store(edm::Event &iEvent, const edm::Handle<std::vector<pat::Electron>> &probes,
	                          const std::vector<T> &values, const std::string &name){
      std::unique_ptr<edm::ValueMap<T>> valMap(new edm::ValueMap<T>());
      typename edm::ValueMap<T>::Filler filler(*valMap);
      filler.insert(probes, values.begin(), values.end());
      filler.fill();
      iEvent.put(std::move(valMap), name);
  }

  bool PassIDEmuDoubleEG(const pat::Electron &ele){
    float eInvMinusPInv = (1.0 - ele.eSuperClusterOverP())/ele.ecalEnergy();
    if(ele.full5x5_sigmaIetaIeta()                    >= (ele.isEB() ? 0.011 : 0.030)) return false;
    if(std::abs(ele.deltaPhiSuperClusterTrackAtVtx()) >= (ele.isEB() ? 0.04  : 0.07))  return false;
    if(std::abs(ele.deltaEtaSuperClusterTrackAtVtx()) >= (ele.isEB() ? 0.01  : 0.008)) return false;
    if(ele.hadronicOverEm()                           >= (ele.isEB() ? 0.10  : 0.07))  return false;
    if(eInvMinusPInv                                  <= -0.05)                        return false;
    if(eInvMinusPInv                                  >= (ele.isEB() ? 0.01  : 0.005)) return false;
    return true;
  }

  bool PassTTVLoose(const pat::Electron &ele, float dxy, float dz, float sip3d, double miniIso, int missingHits){
    if(!PassIDEmuDoubleEG(ele))                       return false;
    if(std::abs(dxy) > 0.05)                          return false;
    if(std::abs(dz) > 0.1)                            return false;
    if(std::abs(sip3d) > 8)                           return false;
    if(miniIso > 0.4)                                 return false;
    if(missingHits > 1)                               return false;
    return true;
  }

  bool PassLeptonMva(TString level, double mva, double deepCSV, bool is2016){
    if(deepCSV > (is2016 ? 0.8958 : 0.8001)) return false;
    if(level == "ttZ4l")  return mva > -0.4;
    if(level == "ttZ3l")  return mva >  0.4;
    if(level == "ttW")    return mva >  0.6;
    if(level == "tZq")    return mva >  0.8;
    return false;
  }
}



class TTVElectronVariableHelper : public edm::EDProducer {
public:
  explicit TTVElectronVariableHelper(const edm::ParameterSet & iConfig);
  virtual ~TTVElectronVariableHelper() ;
  
  virtual void beginJob();
  bool combine(std::map<TString, std::vector<bool>>& passWorkingPoints, std::vector<TString> wps);
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup) override;
  
private:
  edm::EDGetTokenT<std::vector<pat::Electron>> probesToken_;
  edm::EDGetTokenT<edm::View<reco::Candidate>> probesViewToken_;
  edm::EDGetTokenT<edm::ValueMap<float>> dxyToken_;
  edm::EDGetTokenT<edm::ValueMap<float>> dzToken_;
  edm::EDGetTokenT<edm::ValueMap<float>> mvaToken_;
  edm::EDGetTokenT<edm::ValueMap<float>> mvaGPToken_;
  edm::EDGetTokenT<double> rhoToken_;

  bool is2016;

  float pt, eta, trackMult, miniIsoCharged, miniIsoNeutral, ptRel, ptRatio, relIso, deepCSV, sip3d, dxyLog, dzLog, eleMva;
  TMVA::Reader *reader;

  std::vector<TString> workingPoints;
};

TTVElectronVariableHelper::TTVElectronVariableHelper(const edm::ParameterSet & iConfig) :
  probesToken_(        consumes<std::vector<pat::Electron>>(iConfig.getParameter<edm::InputTag>("probes"))),
  probesViewToken_(    consumes<edm::View<reco::Candidate>>(iConfig.getParameter<edm::InputTag>("probes"))),
  dxyToken_(           consumes<edm::ValueMap<float>>(      iConfig.getParameter<edm::InputTag>("dxy"))),
  dzToken_(            consumes<edm::ValueMap<float>>(      iConfig.getParameter<edm::InputTag>("dz"))),
  mvaToken_(           consumes<edm::ValueMap<float>>(      iConfig.getParameter<edm::InputTag>("mvas"))),
  is2016(                                                   iConfig.getUntrackedParameter<bool>("is2016")){

    workingPoints = {"TTVLoose","TTVLeptonMvaTTZ3l","TTVLeptonMvaTTZ4l","TTVLeptonMvaTTW","TTVLeptonMvatZq","RTTVLeptonMvaTTZ3l","RTTVLeptonMvaTTZ4l","RTTVLeptonMvaTTW","RTTVLeptonMvatZq","TightCharge"};
    for(TString wp : workingPoints) produces<edm::ValueMap<bool>>(("pass" + wp).Data());
}

TTVElectronVariableHelper::~TTVElectronVariableHelper(){}

void TTVElectronVariableHelper::beginJob(){
  reader  = new TMVA::Reader( "!Color:!Silent" );

  TString eleMvaName = is2016 ? "electronMva" : "electronMvaFall17NoIso";
  reader->AddVariable( "pt",                  &pt);
  reader->AddVariable( "eta",                 &eta);
  reader->AddVariable( "trackMultClosestJet", &trackMult);
  reader->AddVariable( "miniIsoCharged",      &miniIsoCharged);
  reader->AddVariable( "miniIsoNeutral",      &miniIsoNeutral);
  reader->AddVariable( "pTRel",               &ptRel);
  reader->AddVariable( "ptRatio",             &ptRatio);
  reader->AddVariable( "relIso",              &relIso);
  reader->AddVariable( "deepCsvClosestJet",   &deepCSV);
  reader->AddVariable( "sip3d",               &sip3d);
  reader->AddVariable( "dxy",                 &dxyLog);
  reader->AddVariable( "dz",                  &dzLog);
  reader->AddVariable( eleMvaName,            &eleMva);

  edm::FileInPath *fip = new edm::FileInPath(TString("PhysicsTools/NanoAOD/data/el_BDTG_TTV_") + (is2016 ? "2016" : "2017") + ".weights.xml");
  reader->BookMVA("BDTG method", fip->fullPath().c_str());
}

// Combine workingpoints
bool TTVElectronVariableHelper::combine(std::map<TString, std::vector<bool>>& passWorkingPoints, std::vector<TString> wps){
    for(TString wp : wps) if(!passWorkingPoints[wp].back()) return false;
    return true;
}

void TTVElectronVariableHelper::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  // read input
  edm::Handle<std::vector<pat::Electron>> probes;      iEvent.getByToken(probesToken_,         probes);
  edm::Handle<edm::View<reco::Candidate>> probes_view; iEvent.getByToken(probesViewToken_,     probes_view);
  edm::Handle<edm::ValueMap<float>> dxys;              iEvent.getByToken(dxyToken_,            dxys);
  edm::Handle<edm::ValueMap<float>> dzs;               iEvent.getByToken(dzToken_,             dzs);
  edm::Handle<edm::ValueMap<float>> mvas;              iEvent.getByToken(mvaToken_,            mvas);

  std::map<TString, std::vector<bool>> passWorkingPoints;
  for(TString wp : workingPoints) passWorkingPoints[wp] = std::vector<bool>();

  size_t i = 0;
  for(const auto &probe: *probes){
    edm::RefToBase<reco::Candidate> pp = probes_view->refAt(i);

    float dxy      = fabs((*dxys)[pp]);
    float dz       = fabs((*dzs)[pp]);
    pt             = pp->pt();
    eta            = fabs(pp->eta());
    trackMult      = probe.userFloat("jetNDauChargedMVASel");
    miniIsoCharged = probe.userFloat("miniIsoChg")/pt;
    miniIsoNeutral = (probe.userFloat("miniIsoAll")-probe.userFloat("miniIsoChg"))/pt;
    relIso         = probe.userFloat("PFIsoAll")/pt;
    ptRel          = probe.userFloat("ptRel");
    ptRatio        = TMath::Min(probe.userFloat("ptRatio"),(float)1.5);
    deepCSV        = std::max((std::isnan(probe.userFloat("closestJetDeepCsv")) ? 0. : probe.userFloat("closestJetDeepCsv")), 0.);
    sip3d          = fabs(probe.dB(pat::Electron::PV3D)/probe.edB(pat::Electron::PV3D));
    dxyLog         = log(dxy);
    dzLog          = log(dz);
    eleMva         = (*mvas)[pp];

    float leptonMva        = reader->EvaluateMVA("BDTG method");
    float mini_iso         = probe.userFloat("miniIsoAll")/probe.pt();
    int   missingInnerHits = probe.gsfTrack()->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);

   // std::cout << pt << "\t" << eta << "\t" << trackMult << "\t" << miniIsoCharged << "\t" << miniIsoNeutral << "\t" << ptRel << "\t" << ptRatio << "\t" << deepCSV << "\t" << sip3d << "\t" << dxyLog << "\t" << dzLog << "\t" << relIso << "\t" << eleMva << "\t" << leptonMva << std::endl;
    passWorkingPoints["ConvVeto"].push_back(probe.passConversionVeto());
    passWorkingPoints["Charge"].push_back(probe.isGsfCtfScPixChargeConsistent());
    passWorkingPoints["IHit0"].push_back(missingInnerHits == 0);

    bool TTVLoose = PassTTVLoose(probe, dxy, dz, sip3d, mini_iso, missingInnerHits);
    passWorkingPoints["TTVLoose"].push_back(TTVLoose);
    for(TString i : {"TTZ3l","TTZ4l","TTW","tZq"}){
      passWorkingPoints["TTVLeptonMva"+i].push_back(PassLeptonMva(i, leptonMva, deepCSV, is2016));
      passWorkingPoints["RTTVLeptonMva"+i].push_back(combine(passWorkingPoints, {"TTVLoose", "TTVLeptonMva"+i}));
    }
    passWorkingPoints["TightCharge"].push_back(combine(passWorkingPoints, {"Charge", "ConvVeto","IHit0"}));


    ++i;
  }

  for(TString wp : workingPoints){
    Store(iEvent, probes, passWorkingPoints[wp], ("pass" + wp).Data());
  }
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TTVElectronVariableHelper);
