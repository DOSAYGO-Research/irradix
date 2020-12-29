import {encodeString, decodeString, encode, decode, VALS,derradix,irradix} from './index.js';

const NUM_SIZE = 64;

//testOne(149950108427);
//testOne(133799491136);
//randomTestLong();
//randomTestShorts();
//testCodec();
testRadix();
//testStrings();

function testStrings() {
 const hi= "💉💎 or 👦🏻👓⚡嗨，我唔係Gpt - 3寫嘅。 你叫咩名呀?"
 console.log(hi);
 const result = encodeString(hi);
 console.log({result});
 const hey = decodeString(result);
 console.log(hey);
}

function testOne(num) {
  const {nums,bits} = encode([(num-1)/2], 8);
  console.log({nums,bits});
  const unpacked = (decode(nums, bits)*2)+1;
  console.log(num,unpacked);
}

function randomTestLong() {
  return randomTest();
}

function randomTestShorts() {
  let i= 0;
  let PS = 0, UPS = 0, PC = 0;
  while(i++ < 100) {
    const {packedSize, unpackedSize} = randomTest(100);
    PS += packedSize;
    UPS += unpackedSize;
    const pc = parseFloat(((packedSize/unpackedSize)*100).toFixed(2));
    console.log({pc:pc+'%'});
    PC += pc;
  }

  const PPC = ((PS/UPS)*100).toFixed(2);
  i--;
  PS /= i;
  UPS /= i;
  PC /= i;
  console.log({
    avgPacked: PS.toFixed(2),
    avgUnpacked: UPS.toFixed(2),
    avgPackPC: PC.toFixed(2),
    avgPackedTotalPC: PPC
  });
}

function randomTest(len) {
  const X = newRandomArray(newRandomLength(len));
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
  const packedSize = packed.length*(key||bits)/8;
  const unpackedSize = unpacked.length*NUM_SIZE/8;
  if ( ! len ) {
    console.log({packedSize,unpackedSize});
  }
  const A = JSON.stringify(X);
  const B = JSON.stringify(Array.from(unpacked));
  console.assert(A === B);
  if ( A !== B ) {
    console.log(A,B);
    throw new TypeError("Packing failed");
  }
  return {packedSize,unpackedSize};
}

function testCodec() {
  let bits = 5;
  let X = [1123,1312,1,9,1231312,8,11231312,111231312,211231312,311231312,411231312,511231312,611231312,711231312,811231312,911231312,1011231312,57];
  X = [0,1,1,1,2,3,99,51,4,8,9,81,781,81];
  //X = [0,1,1,99,51,4,8,9,81,781,81];
  //X = [1,2,3,4,5,10111];
  let packed;
  ({nums:packed,bits} = encode(X, bits));
  console.log('ok', packed, bits);
  let key;
  if ( bits >= 7 ) {
    ({key,packed} = toTypedArray(packed, bits));
  }
  console.log(packed, key, bits);
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

  for( let i = 0; i <= 64; i ++ ) {
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

    console.log({based:baseI, back, i});
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

function newRandomLength(len) {
  const lowEnd = 1;
  const highEnd = len || 10000;
  const logLowEnd = Math.log(lowEnd);
  const logHighEnd = Math.log(highEnd);
  const range = logHighEnd - logLowEnd;
  const ranLogLen = Math.random() * range + logLowEnd;
  const ranLen = Math.exp(ranLogLen);
  return Math.round(ranLen);
}

function newRandomBitSize() {
  const x = Math.log(32-4);
  const y = Math.log(4);
  const range = x - y;
  const val = Math.random()*range + y;
  return Math.floor(Math.exp(val));
}

function newRandomValue() {
  const TOP = 2**20;
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
