import {wholify,irradix} from './index.js';

const RADIX = Math.PI;

console.log(irradix);

for( let i = 0; i < 1024; i ++ ) {
  const [A,B] = [Math.floor(RADIX), Math.ceil(RADIX)];
  const baseA = i.toString(A);
  const baseB = i.toString(B);
  const baseI = irradix(i, Math.PI);
  const back = wholify(baseI, Math.PI);
  console.log(`${i} in base pi. (${baseA}_${A}, ${baseB}_${B})`, baseI, back, back === i);
}
