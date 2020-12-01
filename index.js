export function irradix(num, radic = Math.PI, subtractOrderOnly = true, wholeDivisorOnly = true) {
  const rep = []; 

  const epsilon = radic**-(Math.log(num)/Math.log(radic));

  let rem = num;

  while(rem > epsilon) {
    const res = rem % radic; 
    const order = findOrder(res, rem, radic);
    rep.push(order);
    if ( subtractOrderOnly ) {
      rem -= order;
    } else {
      rem -= res; 
    }

    if ( wholeDivisorOnly ) {
      rem /= Math.ceil(radic);
    } else {
      rem /= radic; 
    }
  }

  return rep;
}

function findOrder(residue, num, radic) {
  const low = Math.floor(num - radic);
  const high = Math.ceil(num + radic);

  const Res = [ ];

  let index, j = 0;

  for( let i = low; i <= high; i++ ) {
    const resi = i % radic; 
    if ( index === undefined && resi === residue ) {
      index = j;
    }
    j++;
  }

  const Order = [];
  let order, lastRes = -Infinity, run = 0, maxRun = -Infinity;
  let first0;

  for( let i = 0; i < Res.length; i++ ) {
    const res = Res[i];
    if ( res > lastRes ) {
      run += 1;
      order++;
    } else {
      if ( num > maxRun ) {
        maxRun = run;
      }
      if ( order === undefined ) {
        first0 = i;
      }
      order = 0;
    }
    Order.push(order); 
    lastRes = res;
  }

  for( let i = 0; i < first0; i++ ) {
    Order[i] = maxRun - first0 - i - 1;
  }

  console.log({Order, Res});

  return Order[index];
}
