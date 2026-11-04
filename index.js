import { createPublicClient, http, getContract } from 'viem';
import { base } from 'viem/chains';
import dotenv from 'dotenv';

dotenv.config();

const STATE_VIEW_ADDRESS = '0xa3c0c9b65bad0b08107aa264b0f3db444b867a71';

const stateViewABI = [
  {
    inputs: [{ internalType: 'PoolId', name: 'poolId', type: 'bytes32' }],
    name: 'getSlot0',
    outputs: [
      { internalType: 'uint160', name: 'sqrtPriceX96', type: 'uint160' },
      { internalType: 'int24', name: 'tick', type: 'int24' },
      { internalType: 'uint8', name: 'protocolFee', type: 'uint8' },
      { internalType: 'uint8', name: 'lpFee', type: 'uint8' }
    ],
    stateMutability: 'view',
    type: 'function'
  },
  {
    inputs: [
      { internalType: 'PoolId', name: 'poolId', type: 'bytes32' },
      { internalType: 'bytes32', name: 'positionId', type: 'bytes32' }
    ],
    name: 'getPositionInfo',
    outputs: [
      { internalType: 'uint128', name: 'liquidity', type: 'uint128' },
      { internalType: 'uint256', name: 'feeGrowthInside0Last', type: 'uint256' },
      { internalType: 'uint256', name: 'feeGrowthInside1Last', type: 'uint256' }
    ],
    stateMutability: 'view',
    type: 'function'
  }
] as const;

const rpcEndpoints = [
  process.env.RPC_URL_PRIMARY,
  process.env.RPC_URL_SECONDARY,
  process.env.RPC_URL_FALLBACK
].filter(Boolean);

if (rpcEndpoints.length === 0) {
  console.error('[Fatal] No RPC endpoints found in environment variables.');
  process.exit(1);
}

let currentRpcIndex = 0;

function getActiveClient() {
  const url = rpcEndpoints[currentRpcIndex];
  const maskedUrl = url ? url.replace(/https?:\/\/([^/]+).*/, '$1/[REDACTED]') : 'undefined';
  console.log(`[Network] Routing through provider index ${currentRpcIndex} (${maskedUrl})`);
  
  return createPublicClient({
    chain: base,
    transport: http(url, {
      retryCount: 1,
      timeout: 4000
    })
  });
}

async function executeWithKeyRotation(taskFunction) {
  let attempts = 0;
  while (attempts < rpcEndpoints.length) {
    const client = getActiveClient();
    try {
      return await taskFunction(client);
    } catch (error) {
      console.warn(`[Warning] Provider ${currentRpcIndex} threw an error: ${error.message}`);
      currentRpcIndex = (currentRpcIndex + 1) % rpcEndpoints.length;
      attempts++;
      console.log(`[Rotation] Switching to alternative provider index ${currentRpcIndex}...`);
    }
  }
  throw new Error('[Fatal] All rotated API keys and RPC endpoints exhausted.');
}

async function mainLoop() {
  console.log('[System] Initializing local execution loop on Base network...');

  const poolId = process.env.UNISWAP_V4_POOL_ID;
  const positionId = process.env.UNISWAP_V4_POSITION_ID;

  if (!poolId) {
    console.error('[Fatal] UNISWAP_V4_POOL_ID is missing from environment variables.');
    process.exit(1);
  }

  await executeWithKeyRotation(async (client) => {
    const blockNumber = await client.getBlockNumber();
    console.log(`[Success] Connected to Base. Current live block: ${blockNumber}`);

    const stateView = getContract({
      address: STATE_VIEW_ADDRESS,
      abi: stateViewABI,
      client
    });

    const [sqrtPriceX96, tick, protocolFee, lpFee] = await stateView.read.getSlot0([poolId]);
    console.log(`[Uniswap v4] Pool State for ${poolId.slice(0, 10)}...`);
    console.log(`  - Active Tick: ${tick}`);
    console.log(`  - SqrtPriceX96: ${sqrtPriceX96.toString()}`);
    console.log(`  - LP Fee Tier: ${lpFee}`);

    if (positionId) {
      const [liquidity, feeGrowthInside0Last, feeGrowthInside1Last] = await stateView.read.getPositionInfo([
        poolId,
        positionId
      ]);
      console.log(`[Uniswap v4] Position Tracking (${positionId.slice(0, 10)}...):`);
      console.log(`  - Position Liquidity: ${liquidity.toString()}`);
      console.log(`  - Fee Growth Inside 0: ${feeGrowthInside0Last.toString()}`);
      console.log(`  - Fee Growth Inside 1: ${feeGrowthInside1Last.toString()}`);
    }
  });
}

mainLoop().catch((err) => {
  console.error(err);
  process.exit(1);
});
