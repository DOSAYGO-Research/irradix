import {encode, decode, VALS,derradix,irradix} from './index.js';

const NUM_SIZE = 64;

testCodec();

function testCodec() {
  const bits = 32;
  let X = [1123,1312,1,9,1231312,8,11231312,111231312,211231312,311231312,411231312,511231312,611231312,711231312,811231312,911231312,1011231312,57];
  X = [1,2,3,51,4];
  const packed = toTypedArray(encode(X, bits), bits);
  const unpacked = decode(packed, bits);
  console.log({X,packed,unpacked});
  console.log({packedSize:packed.length*bits/8,unpackedSize:unpacked.length*NUM_SIZE/8});
}

function toTypedArray(stuff, bits) {
  const types = {
    8: Uint8Array,
    16: Uint16Array,
    32: Uint32Array,
    64: BigUint64Array
  }
  let arrayType;
  for( let i = 0; i < Object.keys(types).length; i++ ) {
    const key = parseInt(Object.keys(types)[i]);
    if ( bits > key ) continue;
    arrayType = types[key];
    break;
  }
  return new arrayType(stuff);
}

function testRadix() {
  const RADIX = VALS[process.argv[2] || 'PI'] || parseFloat(process.argv[2]);

  const MARK = '+';
  const GAP = '-';
  const PATTERN_WIDTH = 64;
  let pattern = ['+'];
  let lastN = 0;
  let count = 1;

  for( let i = 0; i <= 20; i ++ ) {
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
}
