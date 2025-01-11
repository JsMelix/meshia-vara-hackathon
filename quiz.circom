pragma circom 2.0.0;

template Quiz() {
    signal input answer;
    signal input correct_answer;
    signal output is_correct;

    is_correct <== answer === correct_answer;
}

component main = Quiz();

circom quiz.circom --r1cs --wasm --sym
snarkjs groth16 setup quiz.r1cs pot12_final.ptau quiz_0000.zkey
snarkjs zkey contribute quiz_0000.zkey quiz_final.zkey --name="First contribution" -v
snarkjs zkey export verificationkey quiz_final.zkey verification_key.json
snarkjs zkey export solidityverifier quiz_final.zkey verifier.sol