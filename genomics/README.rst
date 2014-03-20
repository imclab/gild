Structure of the "Genomics" cube
================================

Introduction
------------

Genomics is a support cube, designed to be used in application( cube)s which deal with genomic data.

The Genomics cube defines several quite general entities, which can be further specialized in cubes using it.

In this document we will explore the entities defined in the schema of the Genomics cube.


Anatomy of the Genomics schema
------------------------------

In the Genomics cube we have three categories of entities:

#. Data -/ result-specific entities
   We have only two data / result -specific entities, 
   ``CghResult`` and ``Mutation``. Each of these entities is related to at 
   most one generic ``GenomicMeasure`` via the optional ``related_measure`` 
   inlined object-composite relation.

   Beyond this relation, these two entities have different relations and attributes.

   Thus, a ``CghResult`` is related to a ``GenomicRegion`` via the optional 
   ``related_region`` inlined object-composite relation; that is, each ``CghResult`` 
   is related to at most one ``GenomicRegion``, and the ``CghResult`` cannot 
   exist anymore if its associated ``GenomicRegion`` ceases to exist.

   On the other hand, a ``Mutation`` object is related to at most one single ``Gene``
   via the optional ``related_gene`` inlined object-composite relation.

   These two entities also have several attributes, some mandatory (required), some
   optional. The mandatory attributes are listed below:

   * For ``CghResult``, there are the floats ``cgh_ratio`` and ``log2_ratio``, the string ``status``,
     and the integer ``numprobes``.

   * For ``Mutation``, there are the strings ``mutation_type``, ``reference_base`` 
     and ``variant_base`` and the integer ``position_in_gene``.

#. Pure genetics entities
   There are four such entities, ``Chromosome``, ``Gene``, ``GenomicRegion`` 
   and ``Snp`` (SNIP). 
   
   The ``Chromosome`` has two required string attributes,
   ``name`` and ``identifier``.

   The ``Gene`` is related to at least one ``Chromosome`` via the mandatory 
   ``chromosomes`` relation. 
   Generally speaking, each ``Gene`` is situated on a single chromosome,
   thus linked to a single ``Chromosome``. However, to accommodate translocated genes,
   provisions are made that ``Genes`` can be linked to several ``Chromosomes``.
   The ``Gene`` also has one required string attribute, ``gene_id``, besides other
   optional attributes.

   The ``GenomicRegion`` is situated on a single chromosome, thus being linked to precisely
   one ``Chromosome`` via the mandatory inlined object-composite ``chromosome`` relation.
   The ``GenomicRegion`` also has some required attributes, the integers ``start``,
   ``stop`` and ``width``, and the strings ``cytoband_start`` and ``cytoband_stop``. The
   last two attributes are represented as strings, in the absence of further information
   regarding their semantics. On the long run, they might get a more meaningful 
   representation.
   The ``GenomicRegion`` normally encompasses several genes, whence the ``genes`` relation
   to several ``Gene`` entities. Please note that only genes that are fully enclosed in the
   genomic region are referenced by the ``genes`` relation.
   Out of all these genes, some are oncogenes (whence the ``oncogenes``
   relation to several ``Gene`` entities), some are atlas genes (whence the ``atlas_genes``
   relation to several ``Gene`` entities), and finally some are census genes (whence 
   the ``census_genes`` relation to several ``Gene`` entities).

   The ``Snp`` (Single-nucleotide polymorphism) is associated to exactly one ``Chromosome``
   via the mandatory ``chromosome`` inlined object-composite relation, and to at most 
   one ``Gene`` via the optional ``gene`` inlined object-composite relation.

#. Measure-specific entities. There are three such entities, ``GenomicMeasure``, 
   ``GenomicPlatform`` and ``ColumnRef``.

   The ``GenomicMeasure`` is performed on a single ``GenomicPlatform`` (when information
   regarding the latter is available), whence the inlined ``platform`` relation linking
   a ``GenomicMeasure`` to a ``GenomicPlatform``.
   The results of a ``GenomicMeasure`` are stored in a (possibly empty) set of files, whence
   the ``results_file`` link to ``File`` entities. Please note that the ``File`` entities mean
   that the said files are managed by CubicWeb, optionally being stored on a CubicWeb-managed
   file system.
   The ``GenomicMeasure`` also has three required string attributes, ``type``, ``format`` and 
   ``filepath``, the latter being constrained to a length of at most 256 characters.

   The ``GenomicPlatform`` is associated to zero, one or several SNIPs, via the 
   ``related_snps`` relation between ``GenomicPlatform`` and ``Snp``.
   The ``GenomicPlatform`` also has an ``identifier``, as a required string attribute.

   The ``ColumnRef`` is mandatorily linked to a single ``GenomicMeasure`` via the ``measure`` inlined
   object-composite relation.
   The ``ColumnRef`` also has a required string attribute, ``type``.
