const fs = require('fs');
const { Coinbase, Wallet } = require('@coinbase/coinbase-sdk');

// Initialize locally using your saved project key file without exposing private keys
Coinbase.configureFromJson({ filePath: './cdp_api_key (1).json' });

async function executeLocalRecovery() {
    try {
        console.log("Reading local encrypted wallet block...");
        const encryptedData = fs.readFileSync('wallet (1).data', 'utf8').trim();
        
        console.log("Importing wallet locally...");
        const importedWallet = await Wallet.import(encryptedData);
        
        const defaultAddress = await importedWallet.getDefaultAddress();
        console.log("Derived Default Address:", defaultAddress.getId());

        // Perform emergency sweep or state serialization
        console.log("Local derivation complete. Ready for broadcast.");
    } catch (error) {
        console.error("Local recovery execution failed:", error.message);
    }
}

executeLocalRecovery();
