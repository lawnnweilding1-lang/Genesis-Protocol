const fs = require('fs');
const { Coinbase, Wallet } = require('@coinbase/coinbase-sdk');

Coinbase.configureFromJson({ filePath: './cdp_api_key (1).json' });

async function interactWithTarget() {
  try {
    const targetContract = "0x433704c40F80cBff02e86FD36Bc8baC5e31eB0c1";
    console.log("Target Contract Endpoint:", targetContract);

    const encryptedData = fs.readFileSync('wallet (1).data', 'utf8').trim();
    const importedWallet = await Wallet.import(encryptedData);
    const address = await importedWallet.getDefaultAddress();
    
    console.log("Local Signing Address:", address.getId());
    console.log("Ready to construct direct call to router.");
  } catch (err) {
    console.error("Error:", err.message);
  }
}

interactWithTarget();
