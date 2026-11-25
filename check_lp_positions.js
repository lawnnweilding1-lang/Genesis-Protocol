const { ethers } = require('ethers');

async function checkLP() {
    try {
        const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
        const targetAddress = "0x433704c40F80cBff02e86FD36Bc8baC5e31eB0c1";

        // Uniswap v3/v4 NonfungiblePositionManager on Base
        const positionManagerAddress = "0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1";
        
        const nftAbi = [
            "function balanceOf(address owner) view returns (uint256)",
            "function tokenOfOwnerByIndex(address owner, uint256 index) view returns (uint256)"
        ];

        const contract = new ethers.Contract(positionManagerAddress, nftAbi, provider);
        const nftBalance = await contract.balanceOf(targetAddress);
        
        console.log(`LP Position NFT Balance: ${nftBalance.toString()}`);

        if (nftBalance > 0) {
            for (let i = 0; i < nftBalance; i++) {
                const tokenId = await contract.tokenOfOwnerByIndex(targetAddress, i);
                console.log(`Found Position NFT Token ID: ${tokenId.toString()}`);
            }
        }
    } catch (err) {
        console.error("LP check error:", err.message);
    }
}

checkLP();
