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
    return r.join('');
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
  nums = nums.map(x => irradix(x, VALS.PHI)); // every number now has no '101' in it
  console.log(nums);
  nums = nums.map(x => x.endsWith('10') ? x + '0101' : x); // add extra 0
  nums = nums.join('10');                     // now every number is separated by 1-0-1

  console.log(nums);
  nums = chunk(nums, bits);

  nums = nums.map(s => parseInt(s,2));
  
  if ( bits > 6 ) {
    return nums;
  } else {
    nums = nums.map(x => ALPHABET[bits][x]);
  }
}

/* probably need to handle last chunk somehow */
function chunk(str, size) {
  const chunks = []; 
  let nextChunk = '';

  let i = 0;

  while(i < str.length) {
    nextChunk += str[i];
    i++;
    if ( nextChunk.length < size ) continue;

    chunks.push(nextChunk);
    nextChunk = '';
  }

  return chunks;
}

export function decode(chunks) {
  chunks = chunks.map(n => n.toString(2)); 
  chunks = chunks.join('');
  let realChunks = [];
  console.log(chunks);
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
  console.log(realChunks);
  chunks = realChunks.map(c => parseInt(c,2));
  return chunks;
}
