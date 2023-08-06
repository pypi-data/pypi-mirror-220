# Splinterglyph

## Problem Statement
Suppose we find ourselves in the following situation:
>   You and four of your friends want to encrypt a file.  You each get one of
   five (different) cryptographic keys.  If any three of you combine your
   keys, you can decrypt the file.

We might imagine the following equivalent problem:
>   You want to encrypt a file, but implement your own (very secure) multifactor
   authentication. You produce multiple cryptographic keys, but keep one on
   your laptop, one on your phone, one in a thumb drive in a bank safe deposit box, one printed on a slip of paper under your bed, etc.  You suspect that you might lose a few of them, but if you combine any three keys, you can decrypt the file.

This repo is designed to solve the preceding sort of problems.  Because the user may need to record or recover some of the keys manually, they are encoded in a (relatively) human-friendly fashion.

## Installation
Assuming you have already installed `pip`:
```
python3 -m pip install --user virtualenv
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
### Encryption
Suppose you have a file called `my_data` that you'd like to encrypt.  You could then run
```
splinterglyph_encrypt my_data
```
This would produce an encrypted output file called `my_data.splinterglyph` and would print out a set of key shares, which might look something like this:
```
1-even,disturb,equipment,cleanups,tomo,biagiotti,favoritos,bl,obtained,komatsu,approachable,mowers,arrange

2-even,athol,lost,aloud,condon,wardrobes,herbs,fishermans,dielectric,cpc,galesburg,withdrew,hercegovina

3-even,tissue,break,oreck,solver,mangas,punishable,mutiny,superoxide,dubbing,crucifix,aaaa,celle

4-even,refractive,protect,pulley,tx,frosted,anthracite,rests,floodplains,liquor,excesses,glowing,emphasises

5-even,dichroic,administrator,beeson,memoria,inconvenience,instructor,backwoods,broadcasts,minton,sprout,convictions,standoff
```
By default, `splinterglyph_encrypt` produces 5 shares and requires 2 to decrypt. If you, e.g., wanted to generate 7 shares but require 3 to decrypt, you would run:
```
splinterglyph_encrypt my_data --N 7 --M 3
```

You can try
```
splinterglyph_encrypt -h
```
to see all command line options.

### Decryption
Continuing the example in the previous section, you could decrypt the file `my_data.splinterglyph` using the 1st and 3rd key shares by running:
```
splinterglyph_decrypt my_data.splinterglyph my_data.recovered --shares "3-even,tissue,break,oreck,solver,mangas,punishable,mutiny,superoxide,dubbing,crucifix,aaaa,celle  1-even,disturb,equipment,cleanups,tomo,biagiotti,favoritos,bl,obtained,komatsu,approachable,mowers,arrange"
```
That command would write the decrypted data to `my_data.recovered`.

Note that in that example, any two (distinct) key shares would have been sufficient to decrypt, and the order of the shares doesn't matter.

You can try
```
splinterglyph_decrypt -h
```
to see all command line options; this includes an option to pass the key shares as a file (as opposed to the command line).

## Details

There's two parts to this process: splitting a secret key and actually encrypting the file.  We split the key using [Shamir's secret sharing protocol](https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing).  The code for this exists entirely within the Splinterglyph repository, but is shamelessly [stolen from Jonathan Queiroz' repo](https://github.com/jqueiroz/python-sslib).  The actual encryption is done using [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard).  By default, the system uses 128-bit AES, but the `--key_bit_length` allows the user to upgrade that to 192 or 256 bit keys.

The perceptive reader may have expected that the cryptographic key shares might look like `0x17a7503ce...`, whereas they actually look like `3-even,tissue,break,oreck,solver,mangas,...`.  What's going on?  Well, we imagine that the user may wish to record some of their key shares physically, e.g., by printing them onto a piece of paper.  In that case, they may need to retype them manually in order to decrypt the file.  It can be difficult to type long random strings perfectly, so we encode the key shares as a list of words chosen from the most common 2<sup>16</sup> English words.  (The "words" are sometimes just common strings, like `aaaa`).

In addition to encryption/decryption, we also perform message authentication on the ciphertext.  Therefore, if somebody monkeys with your encrypted file, you'll see an error message like:
```
###############################
##  FILE TAMPERING DETECTED  ##
###############################
```
followed by a Python traceback.  The tampered file will not be decrypted.

When you encrypt a file, a number of parameters get specified (like the AES encryption strength and the number of shares required to decrypt).  This metadata is stored as part of the encrypted file, so you no longer need to keep track of that.  If, however, you forget how many shares you need, a quick trick for recovering that is by examining the top of the encrypted file.  The first handful of bytes are human readable and look something like this:
```
SPLINTERGLYPH v0001
Made 00005 shares; require 00002
2023-06-17 16:23:07
Key len: 0128
prime_mod length: 000025
<followed by binary nonsense>
```
In this example, you'd need two key shares to decrypt the file.

We also share a general warning about "deleting" files.  The presumptive behavior is that after encrypting a file, the user would destroy the original plaintext file.  On modern computing systems this may be more difficult than it seems because fragments of files may persist in the file system.  On a file system with journaling, this problem may be even worse.  Using an encrypted file partition can address this problem, but only if access to that encrypted system is secure.  In any event, if the user is particularly concerned about security, they should consider this issue.
