const DEBUG = false;

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

  let index, j = 0, minDif = Infinity, minIndex = undefined;

  for( let i = low; i <= high; i++ ) {
    const resi = i % radic; 
    Res.push(resi);
    if ( index === undefined ) {
      if ( resi === residue ) {
        index = j;
      } else if ( Math.abs(resi-residue) < minDif ) {
        minDif = Math.abs(resi-residue);
        minIndex = j;
      }
    }
    j++;
  }

  if ( index === undefined ) {
    DEBUG && console.log({minDif, minIndex});
    index = minIndex;
    DEBUG && console.log({Res,low,high,num,radic,residue,index});
  }

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

  const unit = Order[index];
  if ( unit > (Math.floor(radic)-1) ) {
    DEBUG && console.log({minDif, minIndex, unit});
    DEBUG && console.log({Order,Res,low,high,num,radic,residue,index});
  } 
  return unit;
}

export function wholify(rep, radic = Math.PI) {
  rep = rep.split('').reverse().map(u => parseInt(u));
  let num = 1;
  for(let u of rep) {
    u = u + 1;
    // count up to the uth whole number above num
    while(u--) {
      num = Math.floor(num + 1);
    }
    num *= radic;
  }

  return num;
}

