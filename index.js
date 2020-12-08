export function irradix(num, radic = Math.PI) {
  if ( ! Number.isInteger(num) ) {
    throw new TypeError(`Sorry cannot convert non-integer numbers.`)
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

  while( w[0] > epsilon ) {
    w[1] = w[0] % radic;
    w[0] = w[0] - w[1];
    w[0] = w[0] / radic;

    if ( w[0] >= lastW[0] ) {
      break;
    }

    const unit = Math.floor(w[1]).toString(36);
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

