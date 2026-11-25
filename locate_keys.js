const fs = require('fs');
const { execSync } = require('child_process');

console.log("Searching device storage for CDP keys and wallet data...");

try {
    // Search common directories across internal storage and Termux home
    const findCmd = "find ~ /sdcard /storage -name 'cdp_api_key*.json' -o -name 'wallet*.data' 2>/dev/null";
    const result = execSync(findCmd, { encoding: 'utf8' }).trim();
    
    if (!result) {
        console.log("Files not found via automated search. Please check file placement.");
        process.exit(1);
    }

    const paths = result.split('\n');
    console.log("Found files:\n", paths);

    paths.forEach(filePath => {
        if (filePath) {
            const fileName = filePath.split('/').pop();
            execSync(`cp "${filePath}" ./`);
            console.log(`Copied ${fileName} to current directory.`);
        }
    });

    console.log("Setup complete. Local key files are ready.");
} catch (err) {
    console.error("Error during file search/copy:", err.message);
}
