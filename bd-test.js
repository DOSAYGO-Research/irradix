import {Decimal} from 'decimal.js';
import BigNumber from 'bignumber.js';
import Big from 'big.js';


console.log({
  Decimal,
  BigNumber,
  Big,
});

Decimal.set({precision:101});
BigNumber.set({DECIMAL_PLACES:100});
Big.DP = 100;

const PHI = [
  Decimal.sqrt(5).plus(1).div(2).toString(),
  new BigNumber(5).squareRoot().plus(1).div(2).toString(),
  new Big(5).sqrt().plus(1).div(2).toString()
];

console.log({PHI});
