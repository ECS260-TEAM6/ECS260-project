const fs = require('fs');
const readline = require('readline');
const axios = require('axios');

var args = process.argv.slice(2);
const fPath = args[0];
const outFile = args[1];
const task = args[2];

async function processLineByLine() {
    const rStream = fs.createReadStream(fPath);

    const rl = readline.createInterface({
        input: rStream,
        crlfDelay: Infinity
    });

    for await (const line of rl) {
        if (task == 'poke') {
            await poke(line);
        } else if (task == 'extract') {
            await extract(line);
        }
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function poke(line) {
    await sleep(100);

    console.log(`Line from file: ${line}`);

    // [login, project, language, watchers]
    const items = line.split(',');
    const login = items[0];
    const project = items[1];
    let useTravis = false;
    let moreThanFiftyBuilds = false;

    let res;
    try {
        const req = `https://api.travis-ci.org/repos/${login}/${project}`;
        console.log(`Make request to ${req}`)
        const res = await axios.get(`${req}`);
        const data = res.data;

        // check if 'last_build_number' is valid
        if (typeof data.last_build_number == 'string') {
            items.push(data.last_build_number);
        } else {
            items.push(-1);
        }
        await fs.appendFileSync(outFile, `${items.toString()}\n`);
    } catch (e) {
        console.error(e);
        items.push(-1);
        await fs.appendFileSync(outFile, `${items.toString()}\n`);
    }
}

async function extract(line) {
    console.log(`Line from file: ${line}`);

    // [login, project, language, watchers]
    const items = line.split(',');
    const login = items[0];
    const project = items[1];
    const isEnabled = items[4];

    if (isEnabled == '-1') {
        return;
    }
    await fs.appendFileSync(outFile, `${items.slice(0, 2).join(' ')}\n`);
}


processLineByLine();