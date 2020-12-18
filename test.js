import {derradix,irradix} from './index.js';

const VALS = {
  PI: Math.PI,
  SQRT2: Math.SQRT2,              /* no OEIS */
  PHI: 0.5+Math.sqrt(5)/2,        /* golden mean, as binary is A336231 */
  "2PHI": 2/(0.5+Math.sqrt(5)/2), /* 2-inverse of golden mean, no OEIS */
  DELTA: 1+Math.SQRT2,            /* silver mean */
  BRONZE: (3+Math.sqrt(13))/2,    /* bronze mean */
  SQRT3: Math.sqrt(3),
  SQRT3IPHI: Math.sqrt(3+1/(0.5+Math.sqrt(5)/2)),
  E: Math.E,
  G: Math.E**Math.PI,
  G20: Math.E**Math.PI-Math.PI,
  G20T: (Math.E**Math.PI-Math.PI)/10
};

const RADIX = VALS[process.argv[2] || 'PI'] || parseFloat(process.argv[2]);

const MARK = '+';
const GAP = '-';
const PATTERN_WIDTH = 64;
let pattern = ['+'];
let lastN = 0;
let count = 1;

for( let i = 0; i <= 30; i ++ ) {
  const [A,B] = [Math.max(2,Math.min(36,Math.floor(RADIX))), Math.min(Math.max(2,Math.ceil(RADIX)),36)];
  const baseA = i.toString(A);
  const baseB = i.toString(B);
  const baseI = irradix(i, RADIX);
  const back = derradix(baseI, RADIX);
  const N = parseInt(baseI,B);
  for( let j = lastN; j < N; j++ ) {
    if ( j === lastN ) {
      pattern.push(MARK);
    } else { 
      pattern.push(GAP);
    }
    //console.log("j",j);
    count++;
    if ( (j+1)% PATTERN_WIDTH === 0 ) {
      //console.log("Pattern length", pattern.length);
      //console.log("Break");
      pattern.push('\n');
    }
  }
  //console.log("N",N);
  lastN = N;
  console.log(
    `${i} in base ${RADIX}: ${baseI} ${baseI.length} (${parseInt(baseI,B)}) ${back} ${i === back} (${baseA}_${A}, ${baseB}_${B})`
  );
}

pattern.push('+')

count++;

console.log('');
console.log(pattern.join('') + '\n');
console.log(count);
