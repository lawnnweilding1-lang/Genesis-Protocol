import requests

url = "https://api.etherscan.io/v2/api?chainid=1&module=contract&action=verifysourcecode&apikey=YOUR_API_KEY"

payload = {
    "contractaddress": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "sourceCode": "<string>",
    "contractname": "contracts/Verified.sol:Verified",
    "compilerversion": "v0.8.24+commit.e11b9ed9",
    "codeformat": "solidity-standard-json-input",
    "optimizationUsed": "0",
    "runs": "200",
    "constructorArguments": "00000000000000000000000074271f2282ed7ee35c166122a60c9830354be42a",
    "evmVersion": "default",
    "licenseType": "1"
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)

print(response.text)
