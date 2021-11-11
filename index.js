const fs = require('fs');
const readline = require('readline');
const axios = require('axios');

async function processLineByLine() {
    const fileStream = fs.createReadStream('gh-active-projects.csv');

    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    for await (const line of rl) {
        console.log(`Line from file: ${line}`);
        const items = line.split(',');
        console.log(items[0]);
        let res;
        try {
            const res = await axios.get(`https://api.travis-ci.org/repos/${items[0]}/${items[1]}`);
            const data = res.data;
        } catch (e) {
            console.error(e);
        }
    }
}

processLineByLine();