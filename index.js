export const VALS = {
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

const ALPHABET = {
  6: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'.split('')
};

export function irradix(num, radic = Math.PI) {
  if ( num === 0 ) {
    return "0";
  }

  if ( ! Number.isInteger(num) ) {
    throw new TypeError(`Sorry cannot convert non-integer numbers.`);
  }

  if ( Math.abs(radic) <= 1 ) {
    throw new TypeError(`Sorry we don't support radices less than or equal to 1`);
  }

  const S = Math.sign(num);

  if ( S == -1 ) {
    num *= S;
  }

  const w = [num, 0];
  const r = []; 
  let lastW = Array.from(w);

  const quanta = radic**-(Math.log(num)/Math.log(radic));
  const epsilon = Number.EPSILON;

  while( Math.abs(w[0]) > epsilon ) {
    w[1] = w[0] % radic;

    if ( w[1] < 0 ) {
      w[1] -= radic;
    }

    w[0] = w[0] - w[1];
    w[0] = w[0] / radic;

    if ( Math.abs(w[0]) >= Math.abs(lastW[0]) ) {
      if ( Math.sign(radic) === -1 ) {
        if ( w[0] === 0 ) {
          break;
        }
      } else {
        break;
      }
    }
    const unit = Math.floor(Math.abs(w[1])).toString(36);
    r.unshift(unit);
    
    lastW = Array.from(w);
  }

  if ( S == -1 ) {
    r.unshift('-');
  } 

  if ( radic > 36 ) {
    return r.join(',');
  } else {
    const OK = r.join('');
    if ( OK.includes('101') ) {
      throw new TypeError('UH OH', OK, num);
    }
    return OK;
  }
}

export function derradix(rep, radic = Math.PI) {
  const S = rep[0] === '-' ? -1 : 1;

  if ( S === -1 ) {
    rep = rep.slice(1);
  }

  rep = rep.split(radic > 36 ? ',' : '').map(u => parseInt(u, 36));
  let num = 0;
  for(let u of rep) {
    num *= radic;
    num = Math.ceil(num + u);
  }

  return S*num;
}

// encode positive javascript integers of any size (not floats, not bigints)
// into a packed array with members of arbitrary bit length
export function encode(nums, bits = 8) {
  nums = Array.from(nums);
  //nums.unshift(nums.length);
  //nums.push(999);
  console.log(nums);

  nums = nums.map(x => irradix(x*2+1, VALS.PHI)); // every number now has no '101' in it

  console.log(nums);

  //console.assert(nums.map(x => x.endsWith('10') ? x + '0' : x ).join('').split('101').length === 1);

  nums = nums.map(x => x.endsWith('10') ? x + '0101' : x); // add extra 0

  console.log('1',nums);


  nums = nums.join('10');                     // now every number is separated by 1-0-1

  console.log('2',nums);

  let maxSize;
  ({chunks:nums,maxSize} = chunk(nums, bits));

  console.log({maxSize,bits});
  if ( maxSize > bits ) {
    bits = maxSize;
  }

  console.log('oo', nums);

  nums = nums.filter(s => s.length).map(s => parseInt(s,2));
  
  console.log(nums);

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

    if ( str[i] === '0' ) {
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
    return n.toString(2);
  });
  console.log(chunks);
  chunks = chunks.join('');
  let realChunks = [];
  console.log('3', chunks);
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
  console.log(realChunks);
  chunks = Array.from(realChunks);
  */
  console.log(chunks);
  for ( let i = 0; i < chunks.length; i++ ) {
    let chunk = chunks[i];
    console.log(chunk);

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
  console.log('rc', realChunks);
  chunks = realChunks.map(c => derradix(c,VALS.PHI));
  chunks = chunks.map(x => (x-1)/2);
  //const len = chunks.shift();
  const len = chunks.length;

  return chunks.slice(0,len);
}
