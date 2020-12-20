import {encode, decode, VALS,derradix,irradix} from './index.js';

const NUM_SIZE = 64;

testCodec();


function testCodec() {
  let bits = 8;
  let X = [1123,1312,1,9,1231312,8,11231312,111231312,211231312,311231312,411231312,511231312,611231312,711231312,811231312,911231312,1011231312,57];
  X = [0,1,1,1,2,3,99,51,4,8,9,81,781,81];
  let packed;
  ({nums:packed,bits} = encode(X, bits));
  console.log('ok', packed);
  let key;
  if ( bits >= 7 ) {
    ({key,packed} = toTypedArray(packed, bits));
  }
  const unpacked = decode(packed, bits);
  console.log({X,packed,unpacked});
  console.log({packedSize:packed.length*(key||bits)/8,unpackedSize:unpacked.length*NUM_SIZE/8});
}

function toTypedArray(stuff, bits) {
  const types = {
    8: Uint8Array,
    16: Uint16Array,
    32: Uint32Array,
    64: BigUint64Array
  }
  let arrayType, key;
  for( let i = 0; i < Object.keys(types).length; i++ ) {
    const Key = parseInt(Object.keys(types)[i]);
    if ( bits > key ) continue;
    arrayType = types[Key];
    key = Key;
    break;
  }
  return {packed:new arrayType(stuff), key};
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
