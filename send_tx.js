const { ethers } = require("ethers");

async function checkBalance() {
    const provider = new ethers.JsonRpcProvider("https://mainnet.base.org");
    const privateKey = process.env.PRIVATE_KEY;
    
    if (!privateKey) {
        console.error("Error: PRIVATE_KEY environment variable is not set.");
        process.exit(1);
    }
    
    const wallet = new ethers.Wallet(privateKey, provider);
    const balance = await provider.getBalance(wallet.address);
    
    console.log(`Connected to: base`);
    console.log(`Wallet Address: ${wallet.address}`);
    console.log(`Current Balance: ${ethers.formatEther(balance)} ETH`);
    
    const amountToSend = ethers.parseEther("1.0");
    if (balance < amountToSend) {
        console.error("Error: Insufficient balance to cover the transaction and gas fees!");
        process.exit(1);
    }
    
    console.log("Balance is sufficient. Proceeding with transaction...");
}

checkBalance().catch((err) => {
    console.error("Error:", err.shortMessage || err.message || err);
    process.exit(1);
});

