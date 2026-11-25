const { ethers } = require("ethers");

async function rescueFunds() {
    const provider = new ethers.JsonRpcProvider("https://mainnet.base.org");
    const wallet = new ethers.Wallet("YOUR_PRIVATE_KEY", provider);
    
    console.log("Connected to Base network. Initiating direct recovery bypass...");
    
    // Direct transfer or emergency sweep call to bypass bundler queue
    const tx = await wallet.sendTransaction({
        to: "YOUR_RECEIVER_ADDRESS",
        value: await provider.getBalance(wallet.address) - ethers.parseEther("0.0001") // Leave gas
    });
    
    console.log("Transaction broadcasted:", tx.hash);
    await tx.wait();
    console.log("Funds rescued successfully.");
}

rescueFunds().catch(console.error);
