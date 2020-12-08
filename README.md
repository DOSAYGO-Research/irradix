# irradix

Irrational radices 

## Usage

```js
import {irradix, derradix} from 'irradix';

const rep = irradix(1001, Math.PI);
const num = derradix(rep, Math.PI);
```

## Supports

- Any radix (above 10, units represented as a-z, above 36, representation has units separted by commas)
- Any irrational radix (PI, E, PHI, Math.sqrt(163), etc), also regular radices (like 4, or 9991)
- Negative radix
- Negative integers

## Does not support

- Radices of 1 or smaller
- Encoding non-integers

## Why?

I had the idea. I thought it was cool. Nuff said. 

## ~But I like more detail...please explain~ But I like to know more so I can find something to criticize because I love telling people how wrong I think they are

OK, I literally just had the idea pop into my head. I went searching about it and found a couple of web pages saying "there are problems" using irratonal radixes, suggesting it was impossible. Or coming up with bizarre schemes that did not look radix-like to me (such as purely positional notation without powers, similar to the "Fibonacci" or "Prime" radix). 

I checked out the Wikipedia page, and honestly did not really understand it. I basically understand what they do now, but I dislike it. I think there's a better representation. To my mind, the radix in an integer base is like this:

```math

N = kb + r

N - integer
k - divisor
r - remainder
b - base

So N can be written has a multiple of b plus the remainder.

Now, iterate with k.

k = k_2b + r_2

And so on, as every number can be written like this.

You end up with a polynomial in b

N = b^j.r_j + b^(j-1).r_{j-1} + ... + b.r_1 + r_0

Which is represented as a "numeral" by its coefficients (r_j..r_0)

```

And the "algorithm" for radix conversion (in the arrogant langauge of math papers) "emerges immediately" from the equation: you subtract remainders, and divide through by b, and repeat.

But it seems Wikipedia is talking about something different with irrational radices, that has the appearance (to me) of p-adic numbers. I don't know why they don't simply use the above remainder based representation. They say the scheme "reduces to regular integer" radix schemes when integer bases are used, but I don't see it. It seems like they are finding "bracketing powers" around an integer, and outputting I don't know what, and it seems like they ignore the remainder completely.  I don't know how to use their scheme, and I don't like their scheme. If I really wanted to understand it I would go back to the original papers they quote from the 50s, and read them. Original (and old) papers are usually pretty clear. 

Anyway, I'm pretty sure it's different to my (simpler) scheme, because the representations they quote are different to the ones I get. My "key insight" was that you can simply convert the irrational remainders you get to an integer that represents, how many integers past the product you need to go to your number.

So for example, if you divide 100 by PI you get a remainder of about 2.6

Which means that if you have something that you multiply by PI, then go up to the next integer (ceil) then 2 more (floor of the remainder), you get back to your number. So the "radix units" can simply be the floor values of the irrational remainders, and you can reconstruct your integers. And you can do that for every step in the algorithm. 

I was pretty happy to have a scheme where I can take any integer and convert it to any irrational base, and I get a sequence of "radix units" (called "digits" in base 10), that show how to represent that integer in that base. I just think that's pretty cool. 

Basically a radix is just representing a polynomial equation that shows the relationship between some number, and some base. I like that now you can get polynomial equations in some irrational number that show the relationship between that irrational and some integer. 

And "hiding the complexity" by reducing the irrational remainders to simple integers, that "stand in for" that coefficient being the rth integer above the product you are constructing, is a nice step.

I just think it's cool to have a sequence of units like that, that shows the relationship between an integer, and something so unwieldy as an irrational number.

## Caveats

- Obviously this is only good up to the precision you are calculating with. So Math.PI is not really PI it is just a representation of PI up to some number of bits. If JS had BigDecimals and constants that on-the-fly computed their bits to the required precision for any calculation, then I would be confident in saying that this scheme could really convert any integer, whatever the size, to any irrational number base, and be totally accurate. But if you push the integers high enough, probably two inaccuracies will happen: 1) the rep will differ from the "true rep" for that base, because you escaped the precision of the constant for that irrational, and 2) the rep might actually not be convertible back because you escape the precision of the numeric calculations. Those are both fairly "general" caveats, but worth mentioning for anything to do with numerical methods. 
- This scheme might be wrong in some way and have some overlooked corner cases. I've tried to cover the ones important to me (+ve and -ve integer magnitudes, and +ve and -ve real radices), but I've only tested up to 20,000 or so, and while that probably means it's solid, it might not be. Something erroneous could have slipped through.


