use fibertools_rs::extract::FiberseqData;
use pyo3::iter::IterNextOutput;
use pyo3::prelude::*;
use rust_htslib::{bam, bam::ext::BamRecordExtensions, bam::record::Aux, bam::Read};
//use rust_htslib::bam::Read;
//use std::io::Result;

#[pyclass]
/// Record class for fiberseq data, corresponding to a single bam record
pub struct Fiberdata {
    /// Number of ccs passes
    #[pyo3(get, set)]
    pub ec: i64,
    /// Name of the read
    #[pyo3(get, set)]
    pub qname: String,
    /// SAM flag
    #[pyo3(get, set)]
    pub sam_flag: u16,
    /// Read quality
    #[pyo3(get, set)]
    pub rq: String,
    /// Haplotype tag
    #[pyo3(get, set)]
    pub hp: String,
    /// Read sequence
    #[pyo3(get, set)]
    pub seq: String,
    /// Chromosome
    #[pyo3(get, set)]
    pub chrom: String,
    /// Chromosome start
    #[pyo3(get, set)]
    pub start: i64,
    /// Chromosome end
    #[pyo3(get, set)]
    pub end: i64,
    /// Strand
    #[pyo3(get, set)]
    pub strand: char,
    #[pyo3(get, set)]
    /// Read group
    pub rg: String,
    /// m6a :class:`~pyft.Basemods` object
    #[pyo3(get, set)]
    pub m6a: Basemods,
    /// cpg :class:`~pyft.Basemods` object
    #[pyo3(get, set)]
    pub cpg: Basemods,
    /// :class:`~pyft.Ranges` object for msp features
    #[pyo3(get, set)]
    pub msp: Ranges,
    /// :class:`~pyft.Ranges` object for nuc features
    #[pyo3(get, set)]
    pub nuc: Ranges,
}
#[pymethods]
impl Fiberdata {
    pub fn __str__(&self) -> String {
        format!(
            "{}\t{}\t{}\t{}\n{:?}",
            self.qname, self.chrom, self.start, self.end, self.m6a.starts,
        )
    }

    /// return the length of the sequence
    pub fn get_seq_length(&self) -> usize {
        self.seq.len()
    }
}

fn new_py_fiberdata(fiber: &FiberseqData) -> Fiberdata {
    // PB features
    let ec = fiber.ec.round() as i64;

    // record features
    let qname = std::str::from_utf8(fiber.record.qname()).unwrap();
    let sam_flag = fiber.record.flags();
    let rq = match fiber.get_rq() {
        Some(x) => format!("{}", x),
        None => ".".to_string(),
    };
    let hp = fiber.get_hp();
    let seq = String::from_utf8_lossy(&fiber.record.seq().as_bytes()).to_string();
    let (chrom, start, end, strand): (&str, i64, i64, char) = if fiber.record.is_unmapped() {
        (".", 0, 0, '.')
    } else {
        let strand = if fiber.record.is_reverse() { '-' } else { '+' };
        (
            &fiber.target_name,
            fiber.record.reference_start(),
            fiber.record.reference_end(),
            strand,
        )
    };
    let rg = if let Ok(Aux::String(f)) = fiber.record.aux(b"RG") {
        log::trace!("{f}");
        f
    } else {
        "."
    };

    // fiberseq features
    let m6a = fiber.base_mods.m6a();
    let m6a = Basemods::new(m6a.0, m6a.1, m6a.2);
    let cpg = fiber.base_mods.cpg();
    let cpg = Basemods::new(cpg.0, cpg.1, cpg.2);
    let msp_starts = fiber.get_msp(false, true);
    let msp_lengths = fiber.get_msp(false, false);
    let ref_msp_starts = fiber.get_msp(true, true);
    let ref_msp_lengths = fiber.get_msp(true, false);
    let msp = Ranges::new(msp_starts, msp_lengths, ref_msp_starts, ref_msp_lengths);

    let nuc_starts = fiber.get_nuc(false, true);
    let nuc_lengths = fiber.get_nuc(false, false);
    let ref_nuc_starts = fiber.get_nuc(true, true);
    let ref_nuc_lengths = fiber.get_nuc(true, false);
    let nuc = Ranges::new(nuc_starts, nuc_lengths, ref_nuc_starts, ref_nuc_lengths);

    Fiberdata {
        ec,
        qname: qname.to_string(),
        sam_flag,
        rq,
        hp,
        seq,
        chrom: chrom.to_string(),
        start,
        end,
        strand,
        rg: rg.to_string(),
        m6a,
        cpg,
        msp,
        nuc,
    }
}

#[pyclass]
/// Create a fibertools iterator from an indexed bam file.
/// Must provide a valid chrom, start, and end.
/// Returns an iterator over :class:`~pyft.Fiberdata` objects.
pub struct FiberdataIter {
    count: usize,
    fiberdata: Vec<FiberseqData>,
}

#[pymethods]
impl FiberdataIter {
    #[new]
    pub fn new(f: &str, chrom: &str, start: i64, end: i64) -> Self {
        let mut bam = bam::IndexedReader::from_path(f).expect("unable to open indexed bam file");
        let header = bam::Header::from_template(bam.header());
        let head_view = bam::HeaderView::from_header(&header);
        bam.fetch((chrom, start, end))
            .expect("unable to fetch region");
        let records: Vec<bam::Record> = bam.records().map(|r| r.unwrap()).collect();
        let fiberdata = FiberseqData::from_records(&records, &head_view, 0);
        FiberdataIter {
            count: 0,
            fiberdata,
        }
    }

    fn __next__(&mut self) -> IterNextOutput<Fiberdata, &'static str> {
        if self.count < self.fiberdata.len() {
            self.count += 1;
            // Given an instance `counter`, First five `next(counter)` calls yield 1, 2, 3, 4, 5.
            IterNextOutput::Yield(new_py_fiberdata(&self.fiberdata[self.count - 1]))
        } else {
            IterNextOutput::Return("Ended")
        }
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }
}

/// Class for describing base modifications within fiberseq data.
/// For example, m6a and 5mC (cpg) features.
#[pyclass]
#[derive(Clone)]
pub struct Basemods {
    /// Basemod starts
    #[pyo3(get, set)]
    pub starts: Vec<i64>,
    /// Basemod reference starts
    #[pyo3(get, set)]
    pub reference_starts: Vec<i64>,
    /// Basemod ML
    #[pyo3(get, set)]
    pub ml: Vec<u8>,
}

#[pymethods]
impl Basemods {
    #[new]
    pub fn new(starts: Vec<i64>, reference_starts: Vec<i64>, ml: Vec<u8>) -> Self {
        Self {
            starts,
            reference_starts,
            ml,
        }
    }
}

/// Class for describing ranges within fiberseq data.
/// For example, nucleosomes and msp features.
#[pyclass]
#[derive(Clone)]
pub struct Ranges {
    /// Range starts
    #[pyo3(get, set)]
    pub starts: Vec<i64>,
    /// Range ends
    #[pyo3(get, set)]
    pub ends: Vec<i64>,
    /// Range lengths
    #[pyo3(get, set)]
    pub lengths: Vec<i64>,
    /// Reference starts
    #[pyo3(get, set)]
    pub reference_starts: Vec<i64>,
    /// Reference ends
    #[pyo3(get, set)]
    pub reference_ends: Vec<i64>,
    /// Reference lengths
    #[pyo3(get, set)]
    pub reference_lengths: Vec<i64>,
}

#[pymethods]
impl Ranges {
    #[new]
    pub fn new(
        starts: Vec<i64>,
        lengths: Vec<i64>,
        reference_starts: Vec<i64>,
        reference_lengths: Vec<i64>,
    ) -> Self {
        let ends = starts
            .iter()
            .zip(lengths.iter())
            .map(|(s, l)| s + l)
            .collect();
        let reference_ends = reference_starts
            .iter()
            .zip(reference_lengths.iter())
            .map(|(s, l)| s + l)
            .collect();
        Self {
            starts,
            ends,
            lengths,
            reference_starts,
            reference_ends,
            reference_lengths,
        }
    }
}
