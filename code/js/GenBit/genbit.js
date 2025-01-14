// ISO1 or ISO2 or 3 track data generator!


function calculateOddParity(value, nBits) {
    let countOnes = value.toString(2).split('1').length - 1;
    if (countOnes % 2 === 0) {
        value |= (1 << nBits);
    }
    return value;
}

function displayBinary(value, nBits, reverse = false, invert = false) {
    let binary = value.toString(2).padStart(nBits, '0');
    if (reverse) {
        binary = binary.split('').reverse().join('');
    }
    if (invert) {
        binary = binary.split('').map(bit => bit === '0' ? '1' : '0').join('');
    }
    return binary;
}

function getBinStr(valueArray, nBits, reverse = false, invert = false, invertByteOrder = false) {
    let sBin = "";
    valueArray.forEach(byte => {
        const binary = displayBinary(byte, nBits + 1, reverse, invert);
        if (invertByteOrder) {
            sBin = binary + sBin;
        } else {
            sBin += binary;
        }
    });
    return sBin;
}

function getAscBytesFromUser(input) {
    decodedData = "";
    if( input.length === 0 ) {
        decodedData = "1234567890333458899912345678901111111";
    }
    else{
        decodedData = input;
    }

    const ascBytes = new TextEncoder().encode(decodedData);
    document.getElementById("output").innerHTML += `<p>Default decoded data: ${decodedData}</p>`;
    document.getElementById("output").innerHTML += `<p>ASCII (hex): ${Array.from(ascBytes).map(byte => `0x${byte.toString(16).toUpperCase()}`).join(', ')}</p>`;
    return ascBytes;
}

function getDataBitSizeFromUser() {
    let nBit = 4; // Default bit size
    const input = prompt("Select data bit size (4 or 6):", "4");
    if (input) {
        const parsed = parseInt(input, 10);
        if ([4, 6].includes(parsed)) {
            nBit = parsed;
        } else {
            alert("Invalid choice. Using default bit size of 4.");
        }
    }
    document.getElementById("output").innerHTML += `<p>The bit size: ${nBit}</p>`;
    return nBit;
}

function getStxEtx(nBitSize) {
    return nBitSize === 4 ? { stx: 0x0B, etx: 0x0F } : { stx: 0x05, etx: 0x1F };
}

function getIsoData(ascBytes, nBit) {
    const offset = nBit === 4 ? 0x30 : 0x20;
    const isoData = ascBytes.map(byte => byte - offset);
    document.getElementById("output").innerHTML += `<p>ISO (hex, before parity): ${isoData.map(byte => `0x${byte.toString(16).toUpperCase()}`).join(', ')}</p>`;
    return isoData;
}

function addStxEtxLrc(isoData, stx, etx) {
    const isoWithFrame = [stx, ...isoData, etx];
    const lrc = isoWithFrame.reduce((acc, byte) => acc ^ byte, 0);
    isoWithFrame.push(lrc);
    document.getElementById("output").innerHTML += `<p>ISO (hex, added stx, etx, lrc): ${isoWithFrame.map(byte => `0x${byte.toString(16).toUpperCase()}`).join(', ')}</p>`;
    return isoWithFrame;
}

function findSubstringPositions(mainStr, subStr) {
    const positions = [];
    let start = 0;
    while ((start = mainStr.indexOf(subStr, start)) !== -1) {
        positions.push(start);
        start++;
    }
    return positions;
}

function getBinStringEncoderDataFromUser(input) {
    hexStr = "";

    if( input.length === 0 ) {
        hexStr = "FFFFCAFB9B6A90FACF18C6DABBD6318FB9B6A90FACF3DEF7BDEF047FFFFF";
    }
    else{
        hexStr = input;
    }


    // Convert hex string to binary string
    const binStr = hexStr.match(/.{1,2}/g) // Split hex string into byte pairs
        .map(byte => parseInt(byte, 16).toString(2).padStart(8, '0')) // Convert each byte to binary
        .join('');

    document.getElementById("output").innerHTML += `<p>Default encoder data: ${hexStr}</p>`;
    document.getElementById("output").innerHTML += `<p>The number of bits in encoded data: ${binStr.length} bits</p>`;
    return binStr;
}

function genbit() {
    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = ""; // Clear previous output

    const encoderBox = document.getElementById("encoderBox");
    encoderData = encoderBox.value.trim();
    if (!encoderData) {
        encoderData = "";
    }

    const ascBox = document.getElementById("ascBox");
    ascData = ascBox.value.trim();
    if (!ascData) {
        ascData = "";
    }

    const binEncoder = getBinStringEncoderDataFromUser(encoderData);
    const ascBytes = getAscBytesFromUser(ascData);
    const nBit = getDataBitSizeFromUser();
    const isoData = getIsoData(ascBytes, nBit);

    const { stx, etx } = getStxEtx(nBit);
    let isoWithFrame = addStxEtxLrc(isoData, stx, etx);

    isoWithFrame = isoWithFrame.map(byte => calculateOddParity(byte, nBit));
    document.getElementById("output").innerHTML += `<p>ISO (hex, after parity): ${isoWithFrame.map(byte => `0x${byte.toString(16).toUpperCase()}`).join(', ')}</p>`;

    const representations = [
        { desc: "MSB -> LSB", reverse: false, invert: false, byteReverse: false },
        { desc: "Inverted (MSB -> LSB)", reverse: false, invert: true, byteReverse: false },
        { desc: "LSB -> MSB", reverse: true, invert: false, byteReverse: false },
        { desc: "Inverted (LSB -> MSB)", reverse: true, invert: true, byteReverse: false },
        { desc: "Byte-INV-MSB -> LSB", reverse: false, invert: false, byteReverse: true },
        { desc: "Byte-INV-Inverted (MSB -> LSB)", reverse: false, invert: true, byteReverse: true },
        { desc: "Byte-INV-LSB -> MSB", reverse: true, invert: false, byteReverse: true },
        { desc: "Byte-INV-Inverted (LSB -> MSB)", reverse: true, invert: true, byteReverse: true }
    ];

    representations.forEach(rep => {
        const binStr = getBinStr(isoWithFrame, nBit, rep.reverse, rep.invert, rep.byteReverse);
        document.getElementById("output").innerHTML += `<h3>${rep.desc}:</h3>`;
        document.getElementById("output").innerHTML += `<p>Encoded data: ${binStr}</p>`;
        const positions = findSubstringPositions(binEncoder, binStr);
        document.getElementById("output").innerHTML += `<p>The positions: ${positions.join(', ')}</p>`;
    });
}
