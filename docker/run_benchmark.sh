#!/bin/sh

#ModelPlex Simplification proofs
echo "ModelPlex Simplification proofs"
java -jar keymaerax-webui-5.1.1.jar prove --tool WolframEngine /proofs/ModelPlex_Versaille.kyx

#Model Safety proofs
echo "Model Safety proofs"
java -jar keymaerax-webui-5.1.1.jar prove --tool WolframEngine /proofs/ABZ_final.kyx

#Model Refinement proofs (and consequent safety)
echo "Model Refinement proofs (and consequent safety)"
java -jar keymaerax-webui-5.1.1.jar prove --tool WolframEngine /proofs/refinementCtrl.kyx
