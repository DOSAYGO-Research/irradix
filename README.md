# irradix

Irrational radices and integer packing into the Golden Ratio base. 

Did you know 1000 in base *e* is `2010102`? Now you do.

Did you also know that base phi (Golden Ratio) creates binary representations that have no "101" sequence?

At least, that's the hypothesis: Every sequence of 0 bits between any two 1 bits is always even-numbered. I discovered this fact while writing this library, and I realized it could be used to pack integers into a contiguous bit sequence (and then say, "chop" it up into discrete x-bit sized chunks). This packing, like the radix encoding, is reversible. I put the numbers I was getting into [OEIS](http://oeis.org/), and found this sequence](http://oeis.org/A336231), then supposed it was true for every integer, and tests up to some high values (million) then randomly tested multiple times across the space in 0 -- 2**53 (JS integer range). There might be a counter example somewhere!

# Math

Sorry this is not a proof, more of a discussion of my intuition about this. I only acquired this intutiont after noticing the fact, not before. Before creating this irrational radix, I had no idea, the golden ratio base would behave in this way. After investigation a range of other irrational radices, I noticed no other patterns (but surely there must be some). 

I think the "only even zero sequence between 1s" property of base PHI is related to the fact that phi represents a ratio of ratios, as in a:b ~ b:a+b, and because phi**2 = phi + 1, and any sequence of zeroes in the base-phi representation will correspond to an sequence of multiplications via phi, but phi**3 (or any odd-sequence of multiplications) will not have this identity. 

But that's about as far as I got. It would be great to see a proof of this, I think it should be pretty simple.

# Background

I experimented with this and found that for certain source number size distributions related to the chunks size (for example for x bit sized numbers, with x <=32 and for chunks up to 32 bit (matching regular JS type arrary sized slots)), this packing saves some space compared to the naive JS storage of 8 bytes per integer. 

This packing is not rocket science, nor do I think it's any special nor "highly compressed" bit packing. It's logical you should be able to save space when the naive slot is 8 bytes, but your integers only occupy a range of less than that. 

# Hypothesis

Because phi is involved, and because the packing is so simple, I have a feeling that this packing will (in the limit) approach some Shannon entropy limit relative to these distributions. In addition I don't think it's any sort of "fast converging" or "highly efficient" packing, but I do think it might be "among the simplest" sorts of packings of integers. 

Note that by "packing" I don't mean "compressing" an individual bit sequence, I only mean, joining numbers together into a continuous bit sequence while maintaining the boundary ('101') information for each individual number.

# Limitations

There is no support for "negative" numbers, but concievably you could add your own encoding for that (such as adding MAX_NEG_RANGE to all integers prior to packing).

There is no support (neither in the bit packing encoding, nor in the irrational radix representations) for non-integer numbers (only, non integer, even irrational radices).

# Development history

I started out using native JS number implementations. This was incredible fast (coding and packing millions of numbers in a second or two on an average VPS core), but I noticed that some numbers were not reverting to their originals on de-radificiation, and the packing was often broken. I surmised there were probably multiple issues, but that precision  could be one of them. I investigated and found the "non-revertible" numbers were those with long (~20 and above) sequences of zeroes (equating to long sequences of multiplication by phi), which seemed to indicate to me that precision was an issue, as errors would be compounded in these long sequences of multiplications. The precision of phi in JS was limited to the precision of the regular number types which (as is commonly known) have some precision issues relating to floating point.

So I then endeavoured (after I break) to reimplement this in a suitable "BigDecimal" library for JS, to allow arbitrary precision calculations. 

Once I did that, I discovered there were no more issues in the radifications. Hooray!

But there were still issues in the encodings (packings). I discovered a simple arithmetic issue in the encodings and fixed it, leading to fault free implementation. Yeah, I'm awesome! :p ;) xx

## Usage

```js
import {irradix, derradix, VALS, encode, decode} from 'irradix';

const rep = irradix('234232142312342342314213123321', VALS.BigPHI);
const num = derradix(rep, VALS.BigPHI);

const {packed,bits} = encode([123,3,54,45782348,48,1231,0,23]);
const unpacked = decode(packed, bits);
```

## `Decimal` return type

`derradix` returns a Decimal type. You need to call `.toFixed()` on that to get a string value of the base 10 representation. For more `Decimal` APIs [see its documentation](http://mikemcl.github.io/decimal.js/#toFixed)

## `bits` parameter

For encoding you can pass a bits parameters, which gives your indeded chunk size. 
But if you have a number which has a contiguous sequence of zeroes in its base-phi rep, and that bits size you passed in is smaller than what would be required to cut that number into a decodable chunk (not losing leading zeroes), then we will pass back a bits value indicating the number bit size of chunks actually created.

## Supports

- Any radix (above 10, units represented as a-z, above 36, representation has units separted by commas)
- Any irrational radix (PI, E, PHI, Math.sqrt(163), etc), also regular radices (like 4, or 9991)
- Negative radix
- Negative integers

## Does not support

- Radices of 1 or smaller
- Encoding non-integers
- BigInts (sorry, you can't mix BigInt and regular Numbers and so there's not much point, since BigInts can't be fractional)

## Why?

I had the idea. I thought it was cool. Nuff said. 

## ~But I like more detail...please explain~ But I like to know more so I can find something to criticize because I love telling people how wrong I think they are

OK, I literally just had the idea pop into my head. I went searching about it and found a couple of web pages saying "there are problems" using irratonal radixes, suggesting it was impossible. Or coming up with bizarre schemes that did not look radix-like to me (such as purely positional notation without powers, similar to the "Fibonacci" or "Prime" radix). 

I checked out the Wikipedia page, and honestly did not really understand it, and thought there has got to be a better way to do irrational (or fractional) radices. I basically understand what they do now, but I dislike it. I think there's a better representation. To my mind, the radix in an integer base is like this:

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

## Get it

```console
npm i --save irradix
```

## Other interesting stuff

I conjecture this thing might be universal isomorphism over integer bit sequences, and sequences of integers, in the sense that, any bit sequence you can pass in can represent two things: either itself, or its "unpacked" "seqeunce of integers" self, and similarly any "sequence of integers" can represent either itself, or its "compressed" packed into a single bit sequence self. 

I like this. That there is a symmetry across these things, and it's particularly satisfying that it involves phi, the Golden Ratio. However, this may not be the case! It has not been proven and it still might turn out this thing is "not universal". But if so , the structure of those gappy regions might be interesting. 

## Contributions

I'm not a mathematician, this is just a hobby investigation for me, so I would really love if some people good at maths want to contribute some more cool maths stuff on this like proofs, or some way to get nice math formulae into the README. I would love that! So please join in if this interests you. Perhaps we can joint publish a paper on this "Golden Ratio base" (I have not seen anything referring to this in the literature).
