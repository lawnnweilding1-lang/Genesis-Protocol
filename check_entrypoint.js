const { ethers } = require('ethers');

async function checkDeposit() {
    try {
        const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
        // Convert to lowercase to bypass checksum validation errors
        const targetAddress = "0x433704c40F80cBff02e86FD36Bc8baC5e31eB0c1".toLowerCase();
        const entryPointAddress = "0x5FF137D4b0fdCD49Dca30c7CF57E578a026d2789".toLowerCase();
        
        const entryPointAbi = [
            "function balanceOf(address account) view returns (uint256)"
        ];

        const contract = new ethers.Contract(entryPointAddress, entryPointAbi, provider);
        const deposit = await contract.balanceOf(targetAddress);
        
        console.log("EntryPoint Deposit Balance:", ethers.formatEther(deposit), "ETH");
    } catch (err) {
        console.error("Deposit check error:", err.message);
    }
}

checkDeposit();
