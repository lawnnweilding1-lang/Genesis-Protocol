const { createPublicClient, http, formatEther } = require('viem');
const { base } = require('viem/chains');

const client = createPublicClient({
  chain: base,
  transport: http('https://mainnet.base.org'),
});

async function checkBalance() {
  const address = '0xcca4aD595C62027e6587EE4763E849D2B71f74e8';
  console.log(`Checking balance for: ${address}\n`);

  try {
    const balance = await client.getBalance({ address });
    console.log(`Native ETH Balance: ${formatEther(balance)} ETH`);
  } catch (err) {
    console.error("Error fetching balance:", err.message);
  }
}

checkBalance();
