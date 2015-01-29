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
		NOTE: this is a helper function, you do not have to modify this in any way """
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
	stop_codons = ["TAA", "TAG", "TGA"]
	for s in stop_codons:
		for c in range(len(dna[:-2])):
			if c%3 == 0 and dna[c:c+3] in s:
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
	starts = [c for c in range(len(dna[:-2])) if (c%3 == 0 and dna[c:c+3] == "ATG")]
	return [rest_of_ORF(dna[s:]) for s in starts]


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
	# TODO: implement this
	pass


def find_all_ORFs_both_strands(dna):
	""" Finds all non-nested open reading frames in the given DNA sequence on both
		strands.
		
		dna: a DNA sequence
		returns: a list of non-nested ORFs
	>>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
	['ATGCGAATG', 'ATGCTACATTCGCAT']
	"""
	# TODO: implement this
	pass


def longest_ORF(dna):
	""" Finds the longest ORF on both strands of the specified DNA and returns it
		as a string
	>>> longest_ORF("ATGCGAATGTAGCATCAAA")
	'ATGCTACATTCGCAT'
	"""
	# TODO: implement this
	pass


def longest_ORF_noncoding(dna, num_trials):
	""" Computes the maximum length of the longest ORF over num_trials shuffles
		of the specfied DNA sequence
		
		dna: a DNA sequence
		num_trials: the number of random shuffles
		returns: the maximum length longest ORF """
	# TODO: implement this
	pass


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
	# TODO: implement this
	pass


def gene_finder(dna, threshold):
	""" Returns the amino acid sequences coded by all genes that have an ORF
		larger than the specified threshold.
		
		dna: a DNA sequence
		threshold: the minimum length of the ORF for it to be considered a valid
				   gene.
		returns: a list of all amino acid sequences whose ORFs meet the minimum
				 length specified.
	"""
	# TODO: implement this
	pass


if __name__ == "__main__":
	import doctest
	doctest.testmod()
