// src/lock_a.rs
// Genesis Framework: Lock A 192-byte Consensus Domain & Error Precedence

pub const LOCK_A_SIZE_BYTES: usize = 192;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransitionError {
    Structural = 1,
    ParentLinkage = 2,
    SequenceMonotonicity = 3,
    EpochProgression = 4,
    CommitmentUniqueness = 5,
}

pub struct LockADomain {
    pub payload: [u8; LOCK_A_SIZE_BYTES],
}

impl LockADomain {
    pub fn new(data: &[u8]) -> Result<Self, &'static str> {
        if data.len() > LOCK_A_SIZE_BYTES {
            return Err("Payload exceeds 192-byte Lock A domain limit");
        }
        let mut payload = [0u8; LOCK_A_SIZE_BYTES];
        payload[..data.len()].copy_from_slice(data);
        Ok(Self { payload })
    }

    pub fn compute_digest(&self) -> u64 {
        let mut hash: u64 = 0xcbf29ce484222325;
        for &b in &self.payload {
            hash ^= b as u64;
            hash = hash.wrapping_mul(0x100000001b3);
        }
        hash
    }
}
