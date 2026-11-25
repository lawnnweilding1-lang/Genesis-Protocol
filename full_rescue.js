const fs = require('fs');
const { Coinbase, Wallet } = require('@coinbase/coinbase-sdk');

async function runAll() {
    try {
        console.log("=== GENESIS SECURE RECOVERY PIPELINE ===");
        
        // 1. Check local files directly in current directory
        if (!fs.existsSync('./cdp_api_key (1).json') || !fs.existsSync('./wallet (1).data')) {
            throw new Error("Missing required local files: 'cdp_api_key (1).json' or 'wallet (1).data' not found in current directory.");
        }

        console.log("Local files verified. Configuring Coinbase SDK...");
        Coinbase.configureFromJson({ filePath: './cdp_api_key (1).json' });

        console.log("Importing wallet payload...");
        const encryptedData = fs.readFileSync('./wallet (1).data', 'utf8').trim();
        const importedWallet = await Wallet.import(encryptedData);
        
        const defaultAddress = await importedWallet.getDefaultAddress();
        console.log("Active Controlled Address:", defaultAddress.getId());

        console.log("Pipeline state synchronized. Ready for broadcast execution.");
    } catch (error) {
        console.error("Pipeline execution halted:", error.message);
    }
}

runAll();
