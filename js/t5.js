import { Decimal } from 'decimal.js';
import API, { VALS, _bi_irradix as irradix, _bi_derradix as derradix, _bi_encode as encode, _bi_decode as decode } from './jindex.js';
const bi = val => {
  if ( typeof val == "bigint" ) {
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

// Randomized Testing with Detailed Progress and Larger Random Range
function randomizedTest(iterations = 10000) {
  let passCount = 0;
  let failCount = 0;

  for (let i = 0; i < iterations; i++) {
    // Generate random BigInt integers within the range 1 to 1e9
    const nums = Array.from({ length: 10 }, () => BigInt(Math.floor(Math.random() * 1e9) + 1));
    
    console.log(`Test #${i + 1} - Numbers:`, nums.map(num => num.toString()));

    // Encode the numbers
    const encoded = encode(nums);
    console.log("Encoded:", encoded.nums.join(''));

    // Decode the numbers
    const decoded = decode(encoded.nums);
    console.log("Decoded Numbers:", decoded.map(num => num.toString()));

    // Verify the decoded numbers match the original
    if (JSON.stringify(nums, bi) !== JSON.stringify(decoded, bi)) {
      failCount++;
      console.error(colorize(`Test #${i + 1} failed!`, "red"), { nums, decoded });
    } else {
      passCount++;
      console.log(colorize(`Test #${i + 1} passed!`, "green"));
    }

    // Display running totals
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

