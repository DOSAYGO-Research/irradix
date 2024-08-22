import { Decimal } from 'decimal.js';
import API, { VALS, irradix, derradix, encode, decode } from './index.js'; // Assuming the library is named `library.js`

// Randomized Testing
function randomizedTest(iterations = 100) {
  for (let i = 0; i < iterations; i++) {
    // Generate random integers
    const nums = Array.from({ length: 10 }, () => Math.floor(Math.random() * 1000));
    
    console.log("Original Numbers:", nums);
    
    // Encode the numbers
    const encoded = encode(nums);
    console.log("Encoded:", encoded.nums.join(''));

    // Decode the numbers
    const decoded = decode(encoded.nums);
    console.log("Decoded Numbers:", decoded);

    // Verify the decoded numbers match the original
    if (JSON.stringify(nums) !== JSON.stringify(decoded)) {
      console.error("Test failed!", { nums, decoded });
      throw new Error("Decoding failed to recover original numbers.");
    } else {
      console.log("Test passed!");
    }
  }
}

// Run the test
randomizedTest();

