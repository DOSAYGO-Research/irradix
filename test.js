import {encode, decode, VALS,derradix,irradix} from './index.js';

const NUM_SIZE = 64;

//testOne(149950108427);
//randomTest();
//testCodec();
testRadix();

function testOne(num) {
  encode([(num-1)/2], 8);
}

function randomTest() {
  const X = newRandomArray(newRandomLength());
  let bits = newRandomBitSize();
  let packed;
  ({nums:packed,bits} = encode(X, bits));
  console.log('ok', packed, bits);
  let key;
  if ( bits >= 7 ) {
    ({key,packed} = toTypedArray(packed, bits));
  }
  console.log(packed);
  const unpacked = decode(packed, bits);
  console.log({X,packed,unpacked});
  console.log({packedSize:packed.length*(key||bits)/8,unpackedSize:unpacked.length*NUM_SIZE/8});
  const A = JSON.stringify(X);
  const B = JSON.stringify(Array.from(unpacked));
  console.assert(A === B);
}

function testCodec() {
  let bits = 5;
  let X = [1123,1312,1,9,1231312,8,11231312,111231312,211231312,311231312,411231312,511231312,611231312,711231312,811231312,911231312,1011231312,57];
  X = [0,1,1,1,2,3,99,51,4,8,9,81,781,81];
  X = [0,1,1,99,51,4,8,9,81,781,81];
  X = [1,2,3,4,5,10111];
  let packed;
  ({nums:packed,bits} = encode(X, bits));
  console.log('ok', packed, bits);
  let key;
  if ( bits >= 7 ) {
    ({key,packed} = toTypedArray(packed, bits));
  }
  console.log(packed);
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
    if ( bits > Key ) continue;
    arrayType = types[Key];
    key = Key;
    break;
  }
  return {packed:new arrayType(stuff), key};
}

function testRadix() {
  const RADIX = VALS[process.argv[2] || 'BigPHI'] || parseFloat(process.argv[2]);

  const MARK = '+';
  const GAP = '-';
  const PATTERN_WIDTH = 64;
  let pattern = ['+'];
  let lastN = 0;
  let count = 1;

  for( let i = 24; i <= 24; i ++ ) {
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
    /*
    console.log(
      `${i} in base ${RADIX}: ${baseI} ${baseI.length} (${parseInt(baseI,B)}) ${back} ${i === back} (${baseA}_${A}, ${baseB}_${B})`
    );
    */

    console.log({baseI, back});
  }

  pattern.push('+')

  count++;

  console.log('');
  //console.log(pattern.join('') + '\n');
  //console.log(count);
}

function newRandomArray(len) {
  const arr = new Array(len); 
  for( let i = 0; i < len; i++ ) {
    arr[i] = newRandomValue();
  }

  return arr;
}

function newRandomLength() {
  const lowEnd = 1;
  const highEnd = 10000000;
  const logLowEnd = Math.log(lowEnd);
  const logHighEnd = Math.log(highEnd);
  const range = logHighEnd - logLowEnd;
  const ranLogLen = Math.random() * range + logLowEnd;
  const ranLen = Math.exp(ranLogLen);
  return Math.round(ranLen);
}

function newRandomBitSize() {
  return Math.round((Math.random()*28) + 4);
}

function newRandomValue() {
  const TOP = 2**40;
  const topLog = Math.log(TOP);
  const bottomLog = Math.log(1);
  const range = topLog - bottomLog;
  const logRan = Math.random()*range;
  const val = Math.expm1(logRan);
                                  // can use expm1 since our bottomLog is on 1 
                                  // rather than 0 but our values can go from zero 
  const realVal = Math.round(val);
  return realVal;
}
