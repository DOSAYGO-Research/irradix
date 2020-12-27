  import {Decimal} from 'decimal.js';
  Decimal.set({precision:101});

  const VAR_WIDTHS = false;
  const DEBUG = false;

  export const VALS = {
    HILBERT: (new Decimal(2)).pow(Decimal.sqrt(2)),
    BigPHI: Decimal.sqrt(5).plus(1).div(2),
    // note the rest of these have no been converted to Decimal size (maybe you can?)
    C1: Math.log(Math.PI**2),
    C2: Math.log(Math.PI**2) - Math.log(6) + 1, /* not sum of 1 and reciprocals of squares of primes */
    C3: 1.4522474200410654985065, /* correct C2 */
    HBARC: 3.16152649, /* plankc in radians */
    EM1: 1.57721566490153286060651209008240243, /* Euler M constant */
    RZ2: Math.PI**2/6,
    PISOTV3: 1.4432687912703731076,
    PISOTV6: 1.5341577449142669154,
    PISOTV9: 1.5701473121960543629,
    FIB_PSI: 3.35988566624317755317201130291892,
    PSI: 1.465571231876768026656731,
    APERY: 1.2020569031595942853997381,
    P: 1.32471795724474602596,
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
  VALS.P2 = VALS.P**2;

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

  export function irradix(num, radic = Math.PI) {
    num = new Decimal(num);
    if ( num.comparedTo(0) === 0 ) {
      return "0";
    }

    if ( ! num.isInteger() ) {
      throw new TypeError(`Sorry cannot convert non-integer numbers.`);
    }

    radic = new Decimal(radic);
    if ( Decimal.abs(radic).comparedTo(1) <= 0 ) {
      throw new TypeError(`Sorry we don't support radices less than or equal to 1`);
    }

    const S = Decimal.sign(num);

    if ( S == -1 ) {
      num = num.mul(S);
    }

    const w = [num, 0];
    const r = []; 
    let lastW = Array.from(w);

    const quanta = radic.pow(-(Decimal.log(num)/Decimal.log(radic)));
    const epsilon = new Decimal(Number.EPSILON);

    const thresh = Decimal.min(quanta, epsilon);

    DEBUG && console.log({quanta, epsilon, thresh});
    while( true ) {
      DEBUG && console.log("abs", Decimal.abs(w[0]));
      if ( Decimal.abs(w[0]).comparedTo(thresh) <= 0 ) {
        break;
      }

      w[1] = w[0].mod(radic);

      if ( w[1].comparedTo(0) < 0 ) {
        w[1] = w[1].sub(radic);
      }

      DEBUG && console.log({w});
      w[0] = w[0].sub(w[1]);
      DEBUG && console.log({w});
      w[0] = w[0].div(radic);

      DEBUG && console.log({w});

      if ( Decimal.abs(w[0]).comparedTo(Decimal.abs(lastW[0])) >= 0 ) {
        if ( Decimal.sign(radic) === -1 ) {
          if ( w[0].comparedTo(0) === 0 ) {
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

    if ( S == -1 ) {
      r.unshift('-');
    } 

    const errors = [];

    let result;
    if ( radic.comparedTo(36) > 0 ) {
      result = r.join(',');
    } else {
      result = r.join('');
      if ( radic.comparedTo(VALS.BigPHI) === 0 && result.includes('101') ) {
        //DEBUG && console.info(101,result,result.length,num, num.toBinary().length);
        errors.push(new TypeError('UH OH 101'));
      }
    }
    let try1;
    if ( (try1=derradix(result, radic)).comparedTo(num) !== 0 ) {
      DEBUG && console.info('xderradix',result,result.length,num, num.toBinary().length, try1);
      errors.push(new TypeError('UH OH No ret'));
    }

    //DEBUG && console.log(try1,num);

    if ( errors.length ) {
      errors.length > 1 && DEBUG && console.warn(errors[1]);
      throw errors[0];
    }

    return result;
  }

  export function derradix(rep, radic = Math.PI) {
    const S = rep[0] === '-' ? -1 : 1;

    if ( S === -1 ) {
      rep = rep.slice(1);
    }

    radic = new Decimal(radic);

    rep = rep.split(radic > 36 ? ',' : '').map(u => new Decimal(parseInt(u, 36)));
    let num = new Decimal(0);
    for(let u of rep) {
      num = num.mul(radic);
      num = Decimal.ceil(num.plus(u));
      DEBUG && console.log({rep,num});
    }

    return num.mul(S);
  }

  // encode positive javascript integers of any size (not floats, not bigints)
  // into a packed array with members of arbitrary bit length
  export function encode(nums, bits = 8) {
    nums = Array.from(nums);
    if ( ! VAR_WIDTHS ) {
      nums.unshift(nums.length);
      nums.push(0x99, 0x99, 0x99);
    }
    DEBUG && console.log(nums);

    nums = nums.map(x => irradix((x+1)*2, VALS.BigPHI)); // every number now has no '101' in it

    DEBUG && console.log(nums);

    //DEBUG && console.assert(nums.map(x => x.endsWith('10') ? x + '0' : x ).join('').split('101').length === 1);

    nums = nums.map(x => x.endsWith('10') ? x + '0101' : x); // add extra 0

    DEBUG && console.log('1',nums);


    nums = nums.join('10');                     // now every number is separated by 1-0-1

    DEBUG && console.log('2',nums);

    let maxSize;
    ({chunks:nums,maxSize} = chunk(nums, bits));

    DEBUG && console.log({maxSize,bits});
    if ( maxSize > bits ) {
      bits = maxSize;
    }
    DEBUG && console.log(nums);

    DEBUG && console.log('oo', nums);

    nums = nums.filter(s => s.length).map(s => parseInt(s,2));
    
    DEBUG && console.log(nums);

    if ( bits > 6 ) {
      // do nothing
    } else if ( bits === 6 ) {
      nums = nums.map(x => ALPHABET[bits][x]);
    } else {
      nums = nums.map(x => x.toString(2**bits));
    }
    return {nums,bits};
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
    if ( bits === 6 ) {
      chunks = chunks.map(i => ALPHABET_I[bits][i]);
    } else if ( bits < 6 ) {
      chunks = chunks.map(i => parseInt(i, 2**bits));
    }
    chunks = chunks.map((n,i) => {
      let x = n.toString(2)
      if ( !VAR_WIDTHS ) {
        x = x.padStart(bits, '0');
      }
      return x;
    });
    DEBUG && console.log(chunks);
    chunks = chunks.join('');
    let realChunks = [];
    DEBUG && console.log('3', chunks);
    chunks = chunks.split('101');
    /*
    while(chunks.length) {
      if ( chunks.slice(0,3) == '101' ) {
        chunks = chunks.slice(3);
        if ( chunks.slice(0,3) == '101' ) {
          chunks = chunks.slice(3);
          realChunks.push('');
        }
      } else {
        const next = chunks.indexOf('101');
        if ( next == -1 ) {
          realChunks.push(chunks);
          break;
        }
        realChunks.push(chunks.slice(0,next));
        chunks = chunks.slice(next);
      }
    }
    DEBUG && console.log(realChunks);
    chunks = Array.from(realChunks);
    */
    DEBUG && console.log(chunks);
    for ( let i = 0; i < chunks.length; i++ ) {
      let chunk = chunks[i];
      DEBUG && console.log(chunk);

      if ( chunk == '' ) continue;

      if ( i > 0 ) {
        chunk = '1' + chunk; // add extra one lost in 101 split
      }

      if ( i < chunks.length-1 ) {
        if ( chunks[i+1] == '' ) {
          chunk = chunk.slice(0,-1); // remove extra zero added if ended with '10'
        }
      }

      realChunks.push(chunk);
    }
    DEBUG && console.log('rc', realChunks);
    chunks = realChunks.map(c => derradix(c,VALS.BigPHI).toNumber());
    chunks = chunks.map(x => (x/2)-1);
    const len = VAR_WIDTHS ? chunks.length : chunks.shift();

    return chunks.slice(0,len);
  }
