const { ethers } = require('ethers');

async function checkTokens() {
    try {
        const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
        const targetAddress = "0x433704c40F80cBff02e86FD36Bc8baC5e31eB0c1";

        // Common token contracts on Base (e.g., USDC)
        const tokens = {
            "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "WETH": "0x4200000000000000000000000000000000000006"
        };

        const erc20Abi = ["function balanceOf(address owner) view returns (uint256)", "function decimals() view returns (uint8)"];

        console.log("Scanning token balances for endpoint:", targetAddress);

        for (const [symbol, tokenAddr] of Object.entries(tokens)) {
            const contract = new ethers.Contract(tokenAddr, erc20Abi, provider);
            const balance = await contract.balanceOf(targetAddress);
            const decimals = await contract.decimals();
            const formatted = ethers.formatUnits(balance, decimals);
            console.log(`${symbol} Balance: ${formatted}`);
        }

    } catch (err) {
        console.error("Token check error:", err.message);
    }
}

checkTokens();
