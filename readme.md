#AKEA

These are some short notes on how to use the AKEA package and some background on the project.

##What is AKEA

The name AKEA origins from the name of our home super cluster Laniakea, which agein was named by words from the Hawaiian language. There lani stands for heaven (which is obviously not our business) and akea for spacious, immeasurable, which ist more what we are goping for. I came up with an acronym which might work as well: AKEA actually konws 'em all. Why this might not be an exxaggeration will be explained later.

AKEA konsists of several tools, which are all centered arround the usage of the AKEA database. The tools I will go into detail are called:
- QRAKEA
- DBAKEA
- ...

##So let's start with the AKEA concept
A classical file system uses adresses to identify the position of a file. Just two examples are NTFS and ZFS, while the latter already offers an 128 bit address space, which is virtually infinite, if you consider a computer fitted onto earth of any size.
AKEA goes down a different road, which allows to identify any file by a hash of itself. In short this is some kind of "fingerprint" which can be generated from a file and does not change as long as the file does not change. Hashing a file with a "good" hash algorithm to generate such a "fingerprint" has some properties which are quite interesting for data handling. 
The hash ("fingerprint") is potentially unique. Uniqueness is enshured by the pseudo random behaviour of the algorithm. Nevertheless, there is the slightest chance, that two different datasets get the same fingerprint which is called collision. This is the reason why AKEA does not only use 128 bit hash keys. Mathematically we are talking about the birthday problem (read about it on [wikipedia](https://en.wikipedia.org/wiki/Birthday_problem)).
Which allows us to calculate the probability of a collions for a given hash length l, and amount of files n:
$$
p(n)\approx 1-e^{{-n^2}/{2\cdot l}}
$$
So let us assume we are using 42 byte hashes (336 bit) which gives us 

$l=2^{336}\approx 1.4\cdot 10^{101}$ 

and have 

$n = 2^{128} \approx 3.4 \cdot 10^{38}$ 

files, we get:

$p(3.4 \cdot 10^{38})\approx 1-e^{{-(3.4 \cdot 10^{38})^2}/{(2\cdot 1.4\cdot 10^{101})}}\approx 4.13 \cdot 10^{-25}$

as the probability that a collision will occure for one (two) of these files.

When you do the math for [all atoms on this planet](https://education.jlab.org/qa/mathatom_05.html) 

$n \approx 1.33 \cdot 10^{50}$

you will get away with a remaingin probability of 

$p(1.33 \cdot 10^{50})\approx 6 \%$

which is still worth a bet that AKEA could actually know 'em all. Or at least would need all of earth's atoms to be able to store enough hashes to reach considerable collision chances.

##Why use QRAKEA?

QRAKEA is a fairly simple tool or rather script. It takes a file calculates the SHA512 hash of it and converts the first 42 bytes of it into a QR code. But why bother generating QR codes of files which you already have? Well in my case I was looking for a possibility to document and later find files I generate while e.g. doing a measurement or running a simulation script. These files typically do not change any more and are perfectly idetentifiable by their hash "fingerprint". The QR code than can be printed and placed in your labbook, analog or digital, to get you to your file later on. You even may transfer and rename all folders and filenames, without having to worry how to find them again.

##What is DBAKEA for?
When you now have the AKEA hashes it is desireable to find your files again. QRAKEA is only able to help you to verify that this is actually the file you once created. But what happens if you do not have a clou which file it is or were it went? Well then grab DBAKEA give your best bet were to find the file and hash a complete folder and its sub folders. If you then "show" the QR-code to DBAKE it will tell you if and were to find the file(s).