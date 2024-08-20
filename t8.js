import { Decimal } from 'decimal.js';
import API, { VALS, _bi_irradix as irradix, _bi_derradix as derradix, _bi_encode as encode, _bi_decode as decode } from './jindex.js';
const bi = val => {
  if (typeof val == "bigint") {
    return val.toString();
  }
}

// Helper function to add color
function colorize(text, color) {
  const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    reset: '\x1b[0m'
  };
  return `${colors[color] || colors.reset}${text}${colors.reset}`;
}

// Helper function to convert BigInt to binary string
function toBinaryString(num) {
  return num.toString(2);
}

// Randomized Testing with Detailed Progress and Bit Length Analysis
function randomizedTest(iterations = 10000) {
  let passCount = 0;
  let failCount = 0;

  for (let i = 0; i < iterations; i++) {
    // Generate random BigInt integers within the range 1 to 1e9
    const nums = Array.from({ length: 10 }, () => BigInt(Math.floor(Math.random() * 1e9) + 1));
    
    console.log(`Test #${i + 1} - Numbers:`, nums.map(num => num.toString()));

    // Calculate the original bit strings and concatenate them
    const originalBitStrings = nums.map(toBinaryString);
    const originalBitString = originalBitStrings.join('');
    const originalBitLength = originalBitString.length;

    console.log(`Original Bit String: ${originalBitString}`);

    // Encode the numbers
    const encoded = encode(nums);
    console.log(encoded);
    const encodedBitString = encoded.nums.map(x => parseInt(x).toString(2)).join('');
    console.log("Encoded Bit String:", encodedBitString);

    // Decode the numbers
    const decoded = decode(encoded.nums);
    console.log("Decoded Numbers:", decoded.map(num => num.toString()));

    // Calculate the base-phi bit string length
    const basePhiBitLength = encodedBitString.length;

    // Calculate delimiter bit length
    const delimiterBitLength = (nums.length - 1) * 3;  // Each delimiter "101" is 3 bits

    // Total bit length with delimiters
    const totalBitLengthWithDelimiters = basePhiBitLength + delimiterBitLength;

    console.log(`Base-Phi Delimited Bit String: ${encodedBitString.split('').join('101')}`);

    // Verify the decoded numbers match the original
    if (JSON.stringify(nums, bi) !== JSON.stringify(decoded, bi)) {
      failCount++;
      console.error(colorize(`Test #${i + 1} failed!`, "red"), { nums, decoded });
    } else {
      passCount++;
      console.log(colorize(`Test #${i + 1} passed!`, "green"));
    }

    // Display bit length statistics
    console.log(`\nExpansion Statistics:`);
    console.log(`Original Bit Length: ${originalBitLength}`);
    console.log(`Base-Phi Bit Length: ${basePhiBitLength}`);
    console.log(`Expansion Factor: ${(basePhiBitLength / originalBitLength).toFixed(2)}`);
    console.log(`Delimiter Bit Length: ${delimiterBitLength}`);
    console.log(`Total Bit Length (with delimiters): ${totalBitLengthWithDelimiters}`);
    console.log(colorize(`\nRunning Totals: Passes: ${passCount} | Fails: ${failCount} | Pass Rate: ${(passCount / (i + 1) * 100).toFixed(2)}%\n`, "yellow"));
  }

  // Display final statistics
  console.log("\nFinal Test Results:");
  console.log(colorize(`Total Passes: ${passCount}`, "green"));
  console.log(colorize(`Total Fails: ${failCount}`, "red"));
  console.log(colorize(`Final Pass Rate: ${(passCount / iterations * 100).toFixed(2)}%`, "yellow"));
}

// Run the test
randomizedTest();

