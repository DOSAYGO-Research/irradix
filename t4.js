import { Decimal } from 'decimal.js';
import API, { VALS, irradix, derradix, encode, decode } from './index.js'; // Assuming the library is named `library.js`

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

// Randomized Testing with Statistics and Coloration
function randomizedTest(iterations = 10000) {
  let passCount = 0;
  let failCount = 0;

  for (let i = 0; i < iterations; i++) {
    // Generate random integers
    const nums = Array.from({ length: 10 }, () => Math.floor(Math.random() * 1000));
    
    // Encode the numbers
    const encoded = encode(nums);
    
    // Decode the numbers
    const decoded = decode(encoded.nums);

    // Verify the decoded numbers match the original
    if (JSON.stringify(nums) !== JSON.stringify(decoded)) {
      failCount++;
      console.error(colorize("Test failed!", "red"), { nums, decoded });
    } else {
      passCount++;
      console.log(colorize("Test passed!", "green"));
    }
  }

  // Display final statistics
  console.log("\nTest Results:");
  console.log(colorize(`Total Passes: ${passCount}`, "green"));
  console.log(colorize(`Total Fails: ${failCount}`, "red"));
  console.log(colorize(`Pass Rate: ${(passCount / iterations * 100).toFixed(2)}%`, "yellow"));
}

// Run the test
randomizedTest();

