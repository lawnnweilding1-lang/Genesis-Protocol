// src/transition.rs
// Genesis Framework: Strict Error Precedence State Transition Engine

use crate::lock_a::{LockADomain, TransitionError};

pub struct StateTransitionEngine;

impl StateTransitionEngine {
    pub fn validate_transition(
        parent_link_valid: bool,
        sequence_monotonic: bool,
        epoch_progressed: bool,
        commitment_unique: bool,
    ) -> Result<(), TransitionError> {
        // Enforce strict error precedence order:
        // 1. Structural (Assumed valid if deserialized)
        // 2. Parent Linkage
        if !parent_link_valid {
            return Err(TransitionError::ParentLinkage);
        }
        // 3. Sequence Monotonicity
        if !sequence_monotonic {
            return Err(TransitionError::SequenceMonotonicity);
        }
        // 4. Epoch Progression
        if !epoch_progressed {
            return Err(TransitionError::EpochProgression);
        }
        // 5. Commitment Uniqueness
        if !commitment_unique {
            return Err(TransitionError::CommitmentUniqueness);
        }

        Ok(())
    }
}
