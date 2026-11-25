const { ethers } = require('ethers');

async function resolveBundler() {
    try {
        // Connect to public Base network RPC provider
        const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
        const bundlerAddress = "0x433704c40F80cBff02e86FD36Bc8baC5e31eB0c1";

        console.log("Querying ERC-4337 Bundler state at:", bundlerAddress);
        
        // Fetch code / state at the endpoint
        const code = await provider.getCode(bundlerAddress);
        console.log("Bundler Bytecode Length:", code.length);

        // Fetch balance held at the bundler endpoint
        const balance = await provider.getBalance(bundlerAddress);
        console.log("Locked Asset Balance (ETH/ETH-equiv):", ethers.formatEther(balance));

        console.log("Relay resolution scan complete.");
    } catch (err) {
        console.error("Resolver error:", err.message);
    }
}

resolveBundler();
