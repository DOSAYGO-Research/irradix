export function irradix(num, radic = Math.PI, subtractOrderOnly = false, wholeDivisorOnly = false) {
  const rep = []; 

  const epsilon = radic**-(Math.log(num)/Math.log(radic));

  const rem = num % radic;
  const unit = Math.ceil(rem) - 1;

  rep.unshift(unit);

  num -= rem;

  while( Math.abs(num) > epsilon ) {
    num /= radic; 
    const newRem = num % radic;
    const newUnit = Math.round(newRem);

    rep.unshift(unit);

    num -= newRem;
  }

  return rep.join('');
}

function findOrder(residue, num, radic) {
  const low = Math.max(radic,Math.floor(num - radic));
  const high = Math.ceil(num + radic);

  const Res = [ ];

  let index, j = 0;

  for( let i = low; i <= high; i++ ) {
    const resi = i % radic; 
    Res.push(resi);
    if ( index === undefined && resi === residue ) {
      index = j;
    }
    j++;
  }

  //console.log({low,high,num,radic, Res, residue});
  const Order = [];
  let order, lastRes = -Infinity, run = 0, maxRun = -Infinity;
  let first0;

  for( let i = 0; i < Res.length; i++ ) {
    const res = Res[i];
    if ( res === 0 ) {
      first0 = i;
      order = -1;
    }
    if ( res > lastRes ) {
      run += 1;
      if ( order !== undefined ) {
        order++;
      }
    } else {
      if ( run > maxRun ) {
        maxRun = run;
      }
      if ( order === undefined ) {
        first0 = i;
      }
      run = 0;
      order = 0;
    }
    //console.log({order, num, maxRun, res, lastRes, first0, i})
    Order.push(order); 
    lastRes = res;
  }

  for( let i = 0; i < first0; i++ ) {
    Order[i] = maxRun - (first0 - i - 1);
  }

  //console.log({Order, Res});

  return Order[index];
}
