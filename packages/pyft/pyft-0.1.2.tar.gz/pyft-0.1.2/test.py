import pyft

print(pyft.__all__)
fiberdata = pyft.FiberdataFetch("../tests/data/center.bam", "chr1", 0, 10_000_000)
for fiber in fiberdata:
    print(fiber)
