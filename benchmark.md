# Results

## Line1-UnSync-Back-Versaille_STEP*.kyx

PROVED ABZ/Versaille/UnSync TT - Back - Versaille_STEP0: tactic=Proofscript,tacticsize=53,budget=Duration.Inf,duration=2902[ms],qe=863[ms],rcf=0,steps=158
PROVED ABZ/Versaille/UnSync TT - Back - Versaille_STEP1: tactic=Proofscript,tacticsize=39,budget=Duration.Inf,duration=27361[ms],qe=22032[ms],rcf=0,steps=4003
PROVED ABZ/Versaille/UnSync TT - Back - Versaille_STEP2: tactic=Proofscript,tacticsize=159,budget=Duration.Inf,duration=60570[ms],qe=47383[ms],rcf=0,steps=7204
PROVED ABZ/Versaille/UnSync TT - Back - Versaille_STEP3: tactic=Proofscript,tacticsize=75,budget=Duration.Inf,duration=13803[ms],qe=255[ms],rcf=0,steps=537

Cumulative: tacticsize=326,duration=104634[ms],qe=70533[ms],steps=11902

## ABZ_final.kyx

PROVED ABZ/safeBackT invariant: tactic=Proof,tacticsize=48,budget=Duration.Inf,duration=21362[ms],qe=10648[ms],rcf=0,steps=15378
PROVED ABZ/safeFrontT invariant: tactic=New proof,tacticsize=97,budget=Duration.Inf,duration=14471[ms],qe=9858[ms],rcf=0,steps=17456
PROVED ABZ/Safety - Back: tactic=Proof,tacticsize=84,budget=Duration.Inf,duration=14701[ms],qe=8241[ms],rcf=0,steps=21068
PROVED ABZ/Safety - Front: tactic=Proof,tacticsize=110,budget=Duration.Inf,duration=16407[ms],qe=6865[ms],rcf=0,steps=25689

## refinementCtrl.kyx

PROVED Simple random merge: tactic=Simple_random_merge_2025-02-12_18-13-51,tacticsize=9,budget=Duration.Inf,duration=45[ms],qe=0[ms],rcf=0,steps=35
PROVED ABZ/Refinement Controller: tactic=New Proof,tacticsize=143,budget=Duration.Inf,duration=4093[ms],qe=1875[ms],rcf=0,steps=2446
PROVED ABZ/Refinement NN variables: tactic=Refinement NN variables: Proof,tacticsize=78,budget=Duration.Inf,duration=1709[ms],qe=0[ms],rcf=0,steps=1007
PROVED ABZ/Refinement modelNN: tactic=ABZ/Refinement modelNN: Proof,tacticsize=10,budget=Duration.Inf,duration=1167[ms],qe=0[ms],rcf=0,steps=3716
PROVED ABZ/Safety Back - NN: tactic=Safety Back - NN: Proof,tacticsize=8,budget=Duration.Inf,duration=1249[ms],qe=0[ms],rcf=0,steps=3874
                                                                                                                              steps=24942 (when adding ABZ/Safety - Back)

