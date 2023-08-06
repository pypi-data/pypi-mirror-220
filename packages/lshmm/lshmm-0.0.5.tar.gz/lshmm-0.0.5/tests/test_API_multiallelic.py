# Simulation
import itertools

# Python libraries
import msprime
import numpy as np
import pytest
import tskit

import lshmm as ls
import lshmm.forward_backward.fb_diploid as fbd
import lshmm.forward_backward.fb_haploid as fbh
import lshmm.vit_diploid as vd
import lshmm.vit_haploid as vh

EQUAL_BOTH_HOM = 4
UNEQUAL_BOTH_HOM = 0
BOTH_HET = 7
REF_HOM_OBS_HET = 1
REF_HET_OBS_HOM = 2

MISSING = -1
MISSING_INDEX = 3


class LSBase:
    """Superclass of Li and Stephens tests."""

    def example_haplotypes(self, ts, num_random=10, seed=42):

        H = ts.genotype_matrix()
        s = H[:, 0].reshape(1, H.shape[0])
        H = H[:, 1:]

        haplotypes = [s, H[:, -1].reshape(1, H.shape[0])]
        s_tmp = s.copy()
        s_tmp[0, -1] = MISSING
        haplotypes.append(s_tmp)
        s_tmp = s.copy()
        s_tmp[0, ts.num_sites // 2] = MISSING
        haplotypes.append(s_tmp)
        s_tmp = s.copy()
        s_tmp[0, :] = MISSING
        haplotypes.append(s_tmp)

        return H, haplotypes

    def haplotype_emission(self, mu, m, n_alleles, scale_mutation_based_on_n_alleles):
        # Define the emission probability matrix
        e = np.zeros((m, 2))
        if isinstance(mu, float):
            mu = mu * np.ones(m)

        if scale_mutation_based_on_n_alleles:
            e[:, 0] = mu - mu * np.equal(
                n_alleles, np.ones(m)
            )  # Added boolean in case we're at an invariant site
            e[:, 1] = 1 - (n_alleles - 1) * mu
        else:
            for j in range(m):
                if n_alleles[j] == 1:  # In case we're at an invariant site
                    e[j, 0] = 0
                    e[j, 1] = 1
                else:
                    e[j, 0] = mu[j] / (n_alleles[j] - 1)
                    e[j, 1] = 1 - mu[j]
        return e

    def example_parameters_haplotypes(self, ts, seed=42, scale_mutation=True):
        """Returns an iterator over combinations of haplotype, recombination and
        mutation probabilities."""
        np.random.seed(seed)
        H, haplotypes = self.example_haplotypes(ts)
        n = H.shape[1]
        m = ts.get_num_sites()

        # Here we have equal mutation and recombination
        r = np.zeros(m) + 0.01
        mu = np.zeros(m) + 0.01
        r[0] = 0

        for s in haplotypes:
            # Must be calculated from the genotype matrix because we can now get back mutations that
            # result in the number of alleles being higher than the number of alleles in the reference panel.
            n_alleles = np.int8(
                [len(np.unique(np.append(H[j, :], s[:, j]))) for j in range(m)]
            )
            e = self.haplotype_emission(
                mu, m, n_alleles, scale_mutation_based_on_n_alleles=scale_mutation
            )
            yield n, m, H, s, e, r, mu

        # Mixture of random and extremes
        rs = [np.zeros(m) + 0.999, np.zeros(m) + 1e-6, np.random.rand(m)]
        mus = [np.zeros(m) + 0.2, np.zeros(m) + 1e-6, np.random.rand(m) * 0.2]

        e = self.haplotype_emission(
            mu, m, n_alleles, scale_mutation_based_on_n_alleles=scale_mutation
        )

        for s, r, mu in itertools.product(haplotypes, rs, mus):
            r[0] = 0
            n_alleles = np.int8(
                [len(np.unique(np.append(H[j, :], s[:, j]))) for j in range(H.shape[0])]
            )
            e = self.haplotype_emission(
                mu, m, n_alleles, scale_mutation_based_on_n_alleles=scale_mutation
            )
            yield n, m, H, s, e, r, mu

    def assertAllClose(self, A, B):
        """Assert that all entries of two matrices are 'close'"""
        assert np.allclose(A, B, rtol=1e-9, atol=0.0)

    # Define a bunch of very small tree-sequences for testing a collection of parameters on
    def test_simple_n_10_no_recombination(self):
        ts = msprime.sim_ancestry(
            samples=10,
            recombination_rate=0,
            random_seed=42,
            sequence_length=10,
            population_size=10000,
        )
        ts = msprime.sim_mutations(ts, rate=1e-5, random_seed=42)
        assert ts.num_sites > 3
        self.verify(ts)

    def test_simple_n_6(self):
        ts = msprime.sim_ancestry(
            samples=6,
            recombination_rate=1e-4,
            random_seed=42,
            sequence_length=40,
            population_size=10000,
        )
        ts = msprime.sim_mutations(ts, rate=1e-3, random_seed=42)
        assert ts.num_sites > 5
        self.verify(ts)

    def test_simple_n_8(self):
        ts = msprime.sim_ancestry(
            samples=8,
            recombination_rate=1e-4,
            random_seed=42,
            sequence_length=20,
            population_size=10000,
        )
        ts = msprime.sim_mutations(ts, rate=1e-4, random_seed=42)
        assert ts.num_sites > 5
        assert ts.num_trees > 15
        self.verify(ts)

    def test_simple_n_16(self):
        ts = msprime.sim_ancestry(
            samples=16,
            recombination_rate=1e-2,
            random_seed=42,
            sequence_length=20,
            population_size=10000,
        )
        ts = msprime.sim_mutations(ts, rate=1e-4, random_seed=42)
        assert ts.num_sites > 5
        self.verify(ts)

    def verify(self, ts):
        raise NotImplementedError()


class FBAlgorithmBase(LSBase):
    """Base for forwards backwards algorithm tests."""


class TestMethodsHap(FBAlgorithmBase):
    """Test that we compute the sample likelihoods across all implementations."""

    def verify(self, ts):
        for n, m, H_vs, s, e_vs, r, mu in self.example_parameters_haplotypes(ts):
            F_vs, c_vs, ll_vs = fbh.forwards_ls_hap(n, m, H_vs, s, e_vs, r)
            B_vs = fbh.backwards_ls_hap(n, m, H_vs, s, e_vs, c_vs, r)
            F, c, ll = ls.forwards(H_vs, s, r, p_mutation=mu)
            B = ls.backwards(H_vs, s, c, r, p_mutation=mu)
            self.assertAllClose(F, F_vs)
            self.assertAllClose(B, B_vs)
            # print(e_vs)
            self.assertAllClose(ll_vs, ll)

        for n, m, H_vs, s, e_vs, r, mu in self.example_parameters_haplotypes(
            ts, scale_mutation=False
        ):
            F_vs, c_vs, ll_vs = fbh.forwards_ls_hap(n, m, H_vs, s, e_vs, r)
            B_vs = fbh.backwards_ls_hap(n, m, H_vs, s, e_vs, c_vs, r)
            F, c, ll = ls.forwards(
                H_vs, s, r, p_mutation=mu, scale_mutation_based_on_n_alleles=False
            )
            B = ls.backwards(
                H_vs, s, c, r, p_mutation=mu, scale_mutation_based_on_n_alleles=False
            )
            self.assertAllClose(F, F_vs)
            self.assertAllClose(B, B_vs)
            self.assertAllClose(ll_vs, ll)


class VitAlgorithmBase(LSBase):
    """Base for viterbi algoritm tests."""


class TestViterbiHap(VitAlgorithmBase):
    """Test that we have the same log-likelihood across all implementations"""

    def verify(self, ts):
        for n, m, H_vs, s, e_vs, r, mu in self.example_parameters_haplotypes(ts):

            V_vs, P_vs, ll_vs = vh.forwards_viterbi_hap_lower_mem_rescaling(
                n, m, H_vs, s, e_vs, r
            )
            path_vs = vh.backwards_viterbi_hap(m, V_vs, P_vs)
            path_ll_hap = vh.path_ll_hap(n, m, H_vs, path_vs, s, e_vs, r)
            path, ll = ls.viterbi(H_vs, s, r, p_mutation=mu)

            self.assertAllClose(ll_vs, ll)
            self.assertAllClose(ll_vs, path_ll_hap)
            self.assertAllClose(path_vs, path)
