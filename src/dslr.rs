// src/dslr.rs
// Genesis Framework: DSLR / GLIR Optical & Tensor Coordinate Mapping

pub struct SpectrumCoordinate {
    pub wavelength_nm: f32,
    pub intensity: f32,
    pub phase_angle: f32,
}

pub struct DSLRMapper;

impl DSLRMapper {
    pub fn map_byte_to_spectrum(byte: u8) -> SpectrumCoordinate {
        let base_wavelength = 380.0;
        let range = 400.0;
        let normalized = (byte as f32) / 255.0;
        let wavelength_nm = base_wavelength + (normalized * range);
        let intensity = 1.0;
        let phase_angle = normalized * std::f32::consts::TAU;

        SpectrumCoordinate {
            wavelength_nm,
            intensity,
            phase_angle,
        }
    }

    pub fn canonicalize_payload(payload: &[u8]) -> Vec<SpectrumCoordinate> {
        payload.iter().copied().map(Self::map_byte_to_spectrum).collect()
    }
}
