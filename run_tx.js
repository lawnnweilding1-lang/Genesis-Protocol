const { ethers } = require("ethers");

const PHRASE = "salon health lottery raven pill flat soul sentence female long field amateur";
const RPC_URL = "https://mainnet.base.org";
const RECIPIENT = "0x043dF71E507C69A43e1443e3805210fE1445E964";
const AMOUNT = "0.001";

async function main() {
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const wallet = ethers.Wallet.fromPhrase(PHRASE).connect(provider);

    console.log(`Sending from wallet address: ${wallet.address}`);
    console.log(`Sending to recipient: ${RECIPIENT}`);

    const balance = await provider.getBalance(wallet.address);
    console.log(`Current Base ETH Balance: ${ethers.formatEther(balance)} ETH`);

    const amountWei = ethers.parseEther(AMOUNT);

    if (balance === 0n) {
        console.error("Error: This wallet currently has 0 ETH on Base.");
        process.exit(1);
    }

    if (balance < amountWei) {
        console.error(`Error: Insufficient funds. You have ${ethers.formatEther(balance)} ETH, but trying to send ${AMOUNT} ETH (plus gas).`);
        process.exit(1);
    }

    console.log(`Broadcasting transaction for ${AMOUNT} ETH...`);
    
    const tx = await wallet.sendTransaction({
        to: RECIPIENT,
        value: amountWei
    });

    console.log(`Transaction sent! Hash: ${tx.hash}`);
    console.log("Waiting for block confirmation...");
    
    const receipt = await tx.wait();
    console.log(`Confirmed in block: ${receipt.blockNumber}`);
}

main().catch((err) => {
    console.error("Error executing transaction:", err.shortMessage || err.message || err);
    process.exit(1);
});
