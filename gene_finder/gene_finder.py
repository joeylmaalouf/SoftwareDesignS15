"""
Joey L. Maalouf
Software Design, Spring 2015
Franklin W. Olin College of Engineering
"""
from amino_acids import aa, codons, aa_table
from load import load_seq
import random


def shuffle_string(s):
	""" Shuffles the characters in the input string
		NOTE: this is a helper function, you do not have to modify this in any way
	"""
	return "".join(random.sample(s, len(s)))


def get_complement(nucleotide):
	""" Returns the complementary nucleotide

		nucleotide: a nucleotide (A, C, G, or T) represented as a string
		returns: the complementary nucleotide
	>>> get_complement('A')
	'T'
	>>> get_complement('C')
	'G'
	"""
	return { "A": "T", "C": "G", "G": "C", "T": "A" }[nucleotide]


def get_reverse_complement(dna):
	""" Computes the reverse complementary sequence of DNA for the specfied DNA
		sequence
	
		dna: a DNA sequence represented as a string
		returns: the reverse complementary DNA sequence represented as a string
	>>> get_reverse_complement("ATGCCCGCTTT")
	'AAAGCGGGCAT'
	>>> get_reverse_complement("CCGCGTTCA")
	'TGAACGCGG'
	"""
	return "".join(get_complement(c) for c in dna)[::-1]


def rest_of_ORF(dna):
	""" Takes a DNA sequence that is assumed to begin with a start codon and returns
		the sequence up to but not including the first in frame stop codon.  If there
		is no in frame stop codon, returns the whole string.
		
		dna: a DNA sequence
		returns: the open reading frame represented as a string
	>>> rest_of_ORF("ATGTGAA")
	'ATG'
	>>> rest_of_ORF("ATGAGATAGG")
	'ATGAGA'
	"""
	for c in range(0, len(dna[:-2]), 3):
		if dna[c:c+3] in ["TAA", "TAG", "TGA"]:
			dna = dna[:c]
	return dna


def find_all_ORFs_oneframe(dna):
	""" Finds all non-nested open reading frames in the given DNA sequence and returns
		them as a list.  This function should only find ORFs that are in the default
		frame of the sequence (i.e. they start on indices that are multiples of 3).
		By non-nested we mean that if an ORF occurs entirely within
		another ORF, it should not be included in the returned list of ORFs.
		
		dna: a DNA sequence
		returns: a list of non-nested ORFs
	>>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
	['ATGCATGAATGTAGA', 'ATGTGCCC']
	"""
	i, l = 0, []
	while i < len(dna)-2:
		if dna[i:i+3] == "ATG":
			l.append(rest_of_ORF(dna[i:]))
			i += len(l[-1])
		else:
			i += 3
	return l


def find_all_ORFs(dna):
	""" Finds all non-nested open reading frames in the given DNA sequence in all 3
		possible frames and returns them as a list.  By non-nested we mean that if an
		ORF occurs entirely within another ORF and they are both in the same frame,
		it should not be included in the returned list of ORFs.
		
		dna: a DNA sequence
		returns: a list of non-nested ORFs

	>>> find_all_ORFs("ATGCATGAATGTAG")
	['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
	"""
	l = []
	for frame in range(3):
		l.extend(find_all_ORFs_oneframe(dna[frame:]))
	return l


def find_all_ORFs_both_strands(dna):
	""" Finds all non-nested open reading frames in the given DNA sequence on both
		strands.
		
		dna: a DNA sequence
		returns: a list of non-nested ORFs
	>>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
	['ATGCGAATG', 'ATGCTACATTCGCAT']
	"""
	return find_all_ORFs(dna)+find_all_ORFs(get_reverse_complement(dna))


def longest_ORF(dna):
	""" Finds the longest ORF on both strands of the specified DNA and returns it
		as a string
	>>> longest_ORF("ATGCGAATGTAGCATCAAA")
	'ATGCTACATTCGCAT'
	"""
	return max(find_all_ORFs_both_strands(dna), key=len)


def longest_ORF_noncoding(dna, num_trials):
	""" Computes the maximum length of the longest ORF over num_trials shuffles
		of the specfied DNA sequence
		
		dna: a DNA sequence
		num_trials: the number of random shuffles
		returns: the maximum length longest ORF
	
	I added these unit tests because none existed for this function,
	and they test different values for both dna and num_trials.
	>>> longest_ORF_noncoding("ATGCGAATGTAGCATCAAA", 400)
	15
	>>> longest_ORF_noncoding("ATGCATGAATGTAG", 200)
	14
	"""
	length = len(longest_ORF(dna))
	for i in range(num_trials):
		shuffle_string(dna)
		length = max(length, len(longest_ORF(dna)))
	return length


def coding_strand_to_AA(dna):
	""" Computes the Protein encoded by a sequence of DNA.  This function
		does not check for start and stop codons (it assumes that the input
		DNA sequence represents an protein coding region).
		
		dna: a DNA sequence represented as a string
		returns: a string containing the sequence of amino acids encoded by the
				 the input DNA fragment

		>>> coding_strand_to_AA("ATGCGA")
		'MR'
		>>> coding_strand_to_AA("ATGCCCGCTTT")
		'MPA'
	"""
	return "".join(aa_table[dna[c:c+3]] for c in range(0, len(dna[:-2]), 3))


def gene_finder(dna):
	""" Returns the amino acid sequences that are likely coded by the specified dna.
		
		dna: a DNA sequence
		returns: a list of all amino acid sequences coded by the sequence dna.

		I added these unit tests because none existed for this function,
		and they test different values.
		>>> gene_finder("ATGCCCGCTTT")
		['MPA']
		>>> gene_finder("ATGCGAATGTAGCATCAAA")
		['MLHSH']
	"""
	threshold = longest_ORF_noncoding(dna, 1500)
	return [coding_strand_to_AA(i) for i in find_all_ORFs_both_strands(dna) if len(i) >= threshold]


if __name__ == "__main__":
	import doctest
	doctest.testmod()
	print(gene_finder(load_seq("./data/X73525.fa")))
