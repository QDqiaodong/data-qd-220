# Mass-spectrometry isotope cluster contract

Mass-spectrometry data processors provide peaks strictly ordered by positive m/z, nonnegative intensity, a maximum integer charge and an absolute m/z tolerance. Numeric strings use exact rational arithmetic. From each unassigned low-mass peak, the service evaluates charge hypotheses whose expected isotope spacing is 1/charge.

A candidate needs at least two consecutive members. The chosen candidate has the most members, then the smallest maximum spacing error, then the lower charge. Assigned peaks cannot be reused in another cluster. The result preserves monoisotopic peak identity, chosen charge, member peaks, intensity total and maximum error; other peaks remain explicitly unassigned.

This bounded baseline does not centroid raw spectra, deconvolve overlapping envelopes, infer molecular formulae or identify compounds. It is a structured peak-evidence product rather than a visualization dashboard. Future retention-time grouping can reuse cluster and source-peak identities.
