import { Decimal } from 'decimal.js';
Decimal.set({ precision: 101 });

const VAR_WIDTHS = false;
const DEBUG = false;

const API = {
  encode,
  decode,
  irradix,
  derradix,
  encodeString,
  decodeString,
  _bi_encode,
  _bi_decode,
  _bi_irradix,
  _bi_derradix,
  _bi_encodeString,
  _bi_decodeString,
};
export default API;

export const VALS = {
  HILBERT: (new Decimal(2)).pow(Decimal.sqrt(2)),
  BigPHI: Decimal.sqrt(5).plus(1).div(2),
  BigPHI7: Decimal.sqrt(7).plus(1).div(2),
  BigDELTA: Decimal.sqrt(2).plus(1),
  BigBRONZE: Decimal.sqrt(13).plus(3).div(2),
  C1: Math.log(Math.PI ** 2),
  C2: Math.log(Math.PI ** 2) - Math.log(6) + 1, 
  C3: 1.4522474200410654985065, 
  HBARC: 3.16152649, 
  EM1: 1.57721566490153286060651209008240243, 
  RZ2: Math.PI ** 2 / 6,
  PISOTV3: 1.4432687912703731076,
  PISOTV6: 1.5341577449142669154,
  PISOTV9: 1.5701473121960543629,
  FIB_PSI: 3.35988566624317755317201130291892,
  PSI: 1.465571231876768026656731,
  APERY: 1.2020569031595942853997381,
  P: 1.32471795724474602596,
  PI: Math.PI,
  SQRT2: Math.SQRT2, 
  PHI: 0.5 + Math.sqrt(5) / 2, 
  "2PHI": 2 / (0.5 + Math.sqrt(5) / 2), 
  DELTA: 1 + Math.SQRT2, 
  BRONZE: (3 + Math.sqrt(13)) / 2, 
  SQRT3: Math.sqrt(3),
  SQRT3IPHI: Math.sqrt(3 + 1 / (0.5 + Math.sqrt(5) / 2)),
  E: Math.E,
  G: Math.E ** Math.PI,
  G20: Math.E ** Math.PI - Math.PI,
  G20T: (Math.E ** Math.PI - Math.PI) / 10
};
VALS.P2 = VALS.P ** 2;

const ALPHABET = {
  6: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'.split('')
};

const ALPHABET_I = {
  6: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    .split('')
    .reduce((dict, letter, index) => {
      dict[letter] = index; 
      return dict;
    }, {})
};

// Original functions (without BigInt)

export function encode(nums, bits = 8) {
  DEBUG && console.log(nums, bits);
  nums = Array.from(nums);

  // Adding length and markers if VAR_WIDTHS is false
  if (!VAR_WIDTHS) {
    nums.unshift(nums.length);
    nums.push(0x99, 0x99, 0x99);
  }

  DEBUG && console.log(nums);

  // Convert each number to a base-phi representation
  nums = nums.map(x => irradix((x + 1) * 2, VALS.BigPHI));

  DEBUG && console.log(nums);

  // Add extra 0 if the number ends with '10'
  nums = nums.map(x => x.endsWith('10') ? x + '0101' : x);

  DEBUG && console.log('1', nums);

  // Join numbers with '101' as a delimiter
  nums = nums.join('10');

  DEBUG && console.log('2', nums);

  // Chunking the string into parts based on bit size
  let maxSize;
  ({ chunks: nums, maxSize } = chunk(nums, bits));

  DEBUG && console.log({ maxSize, bits });

  if (maxSize > bits) {
    bits = maxSize;
  }

  DEBUG && console.log(nums);

  // Convert each chunk to a number
  nums = nums.filter(s => s.length).map(s => parseInt(s, 2));

  DEBUG && console.log(nums);

  // Encoding numbers as base-64 or base-2**bits based on bit size
  if (bits > 6) {
    // Do nothing
  } else if (bits === 6) {
    nums = nums.map(x => ALPHABET[bits][x]);
  } else {
    nums = nums.map(x => x.toString(2 ** bits));
  }

  return { nums, bits };
}

  /* probably need to handle last chunk somehow */
  function chunk(str, size) {
    const chunks = []; 
    let nextChunk = '';
    let maxSize = 0;

    let i = 0;

    while(i < str.length) {
      nextChunk += str[i];
      i++;
      if ( nextChunk.length < size ) continue;

      if ( VAR_WIDTHS && str[i] === '0' ) {
        const last1Index = nextChunk.lastIndexOf('1');
        const suffix = nextChunk.slice(last1Index);
        const chunk = nextChunk.slice(0,last1Index);
        if ( chunk.length > maxSize ) {
          maxSize = chunk.length;
        }
        chunks.push(chunk);
        nextChunk = suffix;
      } else {
        if ( nextChunk.length > maxSize ) {
          maxSize = nextChunk.length;
        }
        chunks.push(nextChunk);
        nextChunk = '';
      }
    }

    if ( nextChunk.length ) {
      if ( nextChunk.length > maxSize ) {
        maxSize = nextChunk.length;
      }
      chunks.push(nextChunk);
    }

    return {chunks, maxSize};
  }
export function decode(chunks, bits = 8) {
  chunks = Array.from(chunks);

  // Decode base-64 or base-2**bits based on bit size
  if (bits === 6) {
    chunks = chunks.map(i => ALPHABET_I[bits][i]);
  } else if (bits < 6) {
    chunks = chunks.map(i => parseInt(i, 2 ** bits));
  }

  // Convert numbers to binary strings and pad if needed
  chunks = chunks.map((n, i) => {
    let x = n.toString(2);
    if (!VAR_WIDTHS) {
      x = x.padStart(bits, '0');
    }
    return x;
  });

  DEBUG && console.log(chunks);

  // Recombine the chunks and split by '101' delimiter
  chunks = chunks.join('');
  let realChunks = [];
  chunks = chunks.split('101');

  // Process the split chunks
  for (let i = 0; i < chunks.length; i++) {
    let chunk = chunks[i];

    if (chunk == '') continue;

    if (i > 0) {
      chunk = '1' + chunk; // Add back a '1' lost during split
    }

    if (i < chunks.length - 1 && chunks[i + 1] == '') {
      chunk = chunk.slice(0, -1); // Remove the extra '0' added earlier
    }

    realChunks.push(chunk);
  }

  DEBUG && console.log('rc', realChunks);

  // Convert the chunks back to numbers
  chunks = realChunks.map(c => derradix(c, VALS.BigPHI).toNumber());
  chunks = chunks.map(x => (x / 2) - 1);

  const len = VAR_WIDTHS ? chunks.length : chunks.shift();

  return chunks.slice(0, len);
}

export function _bi_encode(nums, bits = 8) {
  DEBUG && console.log(nums, bits);
  nums = Array.from(nums, BigInt);

  if (!VAR_WIDTHS) {
    nums.unshift(BigInt(nums.length));
    nums.push(BigInt(0x99), BigInt(0x99), BigInt(0x99));
  }

  DEBUG && console.log(nums);

  nums = nums.map(x => irradix(x * BigInt(2), VALS.BigPHI));

  DEBUG && console.log(nums);

  nums = nums.map(x => x.endsWith('10') ? x + '0101' : x);

  DEBUG && console.log('1', nums);

  nums = nums.join('10');

  DEBUG && console.log('2', nums);

  let maxSize;
  ({ chunks: nums, maxSize } = chunk(nums, bits));

  DEBUG && console.log({ maxSize, bits });

  if (maxSize > bits) {
    bits = maxSize;
  }

  DEBUG && console.log(nums);

  nums = nums.filter(s => s.length).map(s => BigInt(parseInt(s, 2)));

  DEBUG && console.log(nums);

  if (bits > 6) {
    // Do nothing
  } else if (bits === 6) {
    nums = nums.map(x => ALPHABET[bits][Number(x)]);
  } else {
    nums = nums.map(x => x.toString(2 ** bits));
  }

  return { nums, bits };
}

export function _bi_decode(chunks, bits = 8n) {
  chunks = Array.from(chunks);
  if (bits === 6n) {
    chunks = chunks.map(i => ALPHABET_I[bits][i]);
  } else if (bits < 6n) {
    chunks = chunks.map(i => BigInt(parseInt(i, 2 ** Number(bits))));
  }
  chunks = chunks.map((n, i) => {
    let x = n.toString(2);
    if (!VAR_WIDTHS) {
      x = x.padStart(Number(bits), '0');
    }
    return x;
  });
  DEBUG && console.log(chunks);
  chunks = chunks.join('');
  let realChunks = [];
  DEBUG && console.log('3', chunks);
  chunks = chunks.split('101');
  DEBUG && console.log(chunks);
  for (let i = 0; i < chunks.length; i++) {
    let chunk = chunks[i];
    DEBUG && console.log(chunk);

    if (chunk == '') continue;

    if (i > 0) {
      chunk = '1' + chunk; // add extra one lost in 101 split
    }

    if (i < chunks.length - 1) {
      if (chunks[i + 1] == '') {
        chunk = chunk.slice(0, -1); // remove extra zero added if ended with '10'
      }
    }

    realChunks.push(chunk);
  }
  DEBUG && console.log('rc', realChunks);

  // Convert Decimal to BigInt
  chunks = realChunks.map(c => BigInt(derradix(c, VALS.BigPHI).toString()));

  chunks = chunks.map(x => (x / 2n) - 1n);
  const len = VAR_WIDTHS ? chunks.length : chunks.shift();

  return chunks.slice(0, Number(len));
}

export function irradix(num, radic = Math.PI) {
  num = new Decimal(num.toString());
  if (num.comparedTo(0) === 0) {
    return "0";
  }

  if (!num.isInteger()) {
    throw new TypeError(`Sorry cannot convert non-integer numbers.`);
  }

  radic = new Decimal(radic);
  if (Decimal.abs(radic).comparedTo(1) <= 0) {
    throw new TypeError(`Sorry we don't support radices less than or equal to 1`);
  }

  const S = Decimal.sign(num);

  if (S == -1) {
    num = num.mul(S);
  }

  const w = [num, 0];
  const r = []; 
  let lastW = Array.from(w);

  const quanta = radic.pow(-(Decimal.log(num) / Decimal.log(radic)));
  const epsilon = new Decimal(Number.EPSILON);

  const thresh = Decimal.min(quanta, epsilon);

  DEBUG && console.log({ quanta, epsilon, thresh });
  while (true) {
    DEBUG && console.log("abs", Decimal.abs(w[0]));
    if (Decimal.abs(w[0]).comparedTo(thresh) <= 0) {
      break;
    }

    w[1] = w[0].mod(radic);

    if (w[1].comparedTo(0) < 0) {
      w[1] = w[1].sub(radic);
    }

    DEBUG && console.log({ w });
    w[0] = w[0].sub(w[1]);
    DEBUG && console.log({ w });
    w[0] = w[0].div(radic);

    DEBUG && console.log({ w });

    if (Decimal.abs(w[0]).comparedTo(Decimal.abs(lastW[0])) >= 0) {
      if (Decimal.sign(radic) === -1) {
        if (w[0].comparedTo(0) === 0) {
          break;
        }
      } else {
        break;
      }
    }
    let unit = Decimal.floor(Decimal.abs(w[1]));
    DEBUG && console.log(unit.toString());
    unit = unit.toNumber().toString(36);
    r.unshift(unit);

    lastW = Array.from(w);
  }

  if (S == -1) {
    r.unshift('-');
  } 

  const errors = [];

  let result;
  if (radic.comparedTo(36) > 0) {
    result = r.join(',');
  } else {
    result = r.join('');
    if (radic.comparedTo(VALS.BigPHI) === 0 && result.includes('101')) {
      errors.push(new TypeError('UH OH 101'));
    }
  }
  let try1;
  if ((try1 = derradix(result, radic)).comparedTo(num) !== 0) {
    DEBUG && console.info('xderradix', result, result.length, num, num.toBinary().length, try1);
    errors.push(new TypeError('UH OH No ret'));
  }

  if (errors.length) {
    errors.length > 1 && DEBUG && console.warn(errors[1]);
    throw errors[0];
  }

  return result;
}

export function derradix(rep, radic = Math.PI) {
  const S = rep[0] === '-' ? -1 : 1;

  if (S === -1) {
    rep = rep.slice(1);
  }

  radic = new Decimal(radic);

  rep = rep.split(radic > 36 ? ',' : '').map(u => new Decimal(parseInt(u, 36)));
  let num = new Decimal(0);
  for (let u of rep) {
    num = num.mul(radic);
    num = Decimal.ceil(num.plus(u));
    DEBUG && console.log({ rep, num });
  }

  return num.mul(S);
}

export function encodeString(str, bits = 6) {
  return Array.from(encode(str.split('').map(c => c.codePointAt(0)), bits).nums).join('');
}

export function decodeString(str, bits = 6) {
  return decode(str, bits).map(p => String.fromCodePoint(p)).join('');  
}

// BigInt versions of the key functions (_bi_ prefixed)

// Convert BigInt to Decimal for internal processing
function bigintToDecimal(bigint) {
  return new Decimal(bigint.toString());
}

// Convert Decimal back to BigInt
function decimalToBigInt(decimal) {
  return BigInt(decimal.toFixed(0));
}

export function _bi_irradix(num, radic = Math.PI) {
  // Convert BigInt to Decimal
  const decimalNum = bigintToDecimal(num);
  const decimalRadic = new Decimal(radic);

  const result = irradix(decimalNum, decimalRadic);

  // The result will be a string, no need to convert back
  return result;
}

export function _bi_derradix(rep, radic = Math.PI) {
  const decimalRadic = new Decimal(radic);
  const result = derradix(rep, decimalRadic);

  // Convert Decimal back to BigInt
  return decimalToBigInt(result);
}

export function _bi_encodeString(str, bits = 6) {
  return Array.from(_bi_encode(str.split('').map(c => BigInt(c.codePointAt(0))), bits).nums).join('');
}

export function _bi_decodeString(str, bits = 6) {
  return _bi_decode(str, bits).map(p => String.fromCodePoint(Number(p))).join('');
}


