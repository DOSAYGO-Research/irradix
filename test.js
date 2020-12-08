import {derradix,irradix} from './index.js';

const VALS = {
  PI: Math.PI,
  SQRT2: Math.SQRT2,
  PHI: 0.5+Math.sqrt(5)/2,
  DELTA: 1+Math.SQRT2,
  E: Math.E,
  G: Math.E**Math.PI,
  G20: Math.E**Math.PI-Math.PI
};

const RADIX = VALS[process.argv[2] || 'PI'] || parseFloat(process.argv[2]);
//(1 + Math.sqrt(5))/2;

for( let i = -1000; i <= 1000; i ++ ) {
  const [A,B] = [Math.max(2,Math.min(36,Math.floor(RADIX))), Math.min(Math.max(2,Math.ceil(RADIX)),36)];
  const baseA = i.toString(A);
  const baseB = i.toString(B);
  const baseI = irradix(i, RADIX);
  const back = derradix(baseI, RADIX);
  console.log(
    `${i} in base ${RADIX}: ${baseI} ${back} ${i === back} (${baseA}_${A}, ${baseB}_${B})`
  );
}
