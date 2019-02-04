#ifndef _MINIADOL1CANDPRODUCER_H_
#define _MINIADOL1CANDPRODUCER_H_

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"

#include <DataFormats/Math/interface/deltaR.h>

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"

#include "DataFormats/Math/interface/deltaR.h"

#include <string>
#include <vector>

template <class T>
class MiniAODL1CandProducerV3 : public edm::EDProducer {

  typedef std::vector<T> TCollection;
  typedef edm::Ref<TCollection> TRef;
  typedef edm::RefVector<TCollection> TRefVector;

public:
  MiniAODL1CandProducerV3(const edm::ParameterSet&);
  ~MiniAODL1CandProducerV3();

 private:
  /// compare two l1Extra in et

  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  
  edm::EDGetTokenT<TRefVector> inputs_;
  //std::vector<l1t::EGammaRef> l1ObjectsToken_;
  edm::EDGetTokenT<BXVector<l1t::EGamma> > l1ObjectsToken_;
  float minET_;
  float dRMatch_;
};

template <class T>
MiniAODL1CandProducerV3<T>::MiniAODL1CandProducerV3(const edm::ParameterSet& iConfig ) :
  inputs_(consumes<TRefVector>(iConfig.getParameter<edm::InputTag>("inputs"))),
  l1ObjectsToken_(consumes<BXVector<l1t::EGamma>>(iConfig.getParameter<edm::InputTag>("l1Objects"))),
  minET_(iConfig.getParameter<double>("minET")),		
  dRMatch_(iConfig.getParameter<double>("dRmatch")) {

  produces<TRefVector>();
}

template <class T>
MiniAODL1CandProducerV3<T>::~MiniAODL1CandProducerV3()
{}

template <class T>
void MiniAODL1CandProducerV3<T>::produce(edm::Event &iEvent, const edm::EventSetup &eventSetup) {

  //edm::Handle<std::vector<l1t::EGammaRef>> l1IsoObjectsH;
  edm::Handle<BXVector<l1t::EGamma> > l1Cands;
  edm::Handle<TRefVector> inputs;

  iEvent.getByToken(l1ObjectsToken_, l1Cands);
  iEvent.getByToken(inputs_, inputs);

  // Create the output collection
  std::unique_ptr<TRefVector> outColRef(new TRefVector);

  for (size_t i=0; i<inputs->size(); i++) {
    bool saveObj = false;
    TRef ref = (*inputs)[i];

    for (std::vector<l1t::EGamma>::const_iterator l1Cand = l1Cands->begin(0); l1Cand != l1Cands->end(0); ++l1Cand) {

      float dR = deltaR(l1Cand->eta(), l1Cand->phi() , ref->eta(), ref->phi());
      if (dR < dRMatch_ && l1Cand->et() >= minET_) { // >= since l1 et is stored in 0.5 steps
         saveObj = true;
      }
    }

    if (saveObj)
      outColRef->push_back(ref);
  }

  iEvent.put(std::move(outColRef));
}



#endif
