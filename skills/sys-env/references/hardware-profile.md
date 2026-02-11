# Hardware Profile

## CPU
- **Model:** AMD Ryzen 5 5500U (Lucienne, Zen 2 architecture)
- **Cores/Threads:** 6 cores / 12 threads
- **Base/Boost:** 2.1 GHz / 4.0 GHz
- **TDP:** 15W (configurable 10-25W)
- **Instruction sets:** SSE4.2, AVX2, AES-NI (no AVX-512)

## GPU
- **Model:** AMD Radeon Graphics (Vega 7, integrated in APU)
- **Driver:** amdgpu (kernel module)
- **Userspace:** Mesa (OpenGL, Vulkan via RADV)
- **Video acceleration:** VA-API via `libva-mesa-driver`
- **Vulkan ICD:** radeon (`radv`)
- **OpenCL:** via `mesa` (ROCm not supported on this APU)
- **No discrete GPU** — all GPU workloads run on integrated Vega 7

### GPU Driver Stack (do NOT modify individually)
```
Kernel:    amdgpu (loaded automatically)
Mesa:      mesa (OpenGL 4.6, Vulkan 1.3)
Vulkan:    vulkan-radeon (RADV driver)
VA-API:    libva-mesa-driver
VDPAU:     mesa-vdpau
```
These packages are interdependent. Upgrading mesa requires matching vulkan-radeon and libva-mesa-driver versions. Always upgrade together via `pacman -Syu`.

## RAM
- **Total:** 7.1 GiB physical
- **Swap:** 7.6 GiB zram (compressed in-memory swap)
- **Type:** DDR4 (soldered, not upgradeable)

## Display
- **Panel:** 1920x1080 @ 60Hz (eDP-1, laptop built-in)
- **Compositor:** Hyprland (Wayland, no X11)
- **Multi-monitor:** Supported via Hyprland config (`monitor=` rules)

## Storage
- **Type:** NVMe SSD
- **Filesystem:** ext4

## Kernel
- **Version:** 6.12.x-lts (Arch Linux LTS kernel)
- **Package:** `linux-lts` + `linux-lts-headers`
- **Key modules:** amdgpu, snd_hda_intel, btusb, iwlwifi/ath11k (wifi)
- **Rationale:** LTS kernel chosen for stability on rolling release

## Power Management
- AMD-specific: `amd_pstate` driver (or `acpi-cpufreq`)
- TLP or power-profiles-daemon may be installed for battery management
- GPU power managed by amdgpu kernel driver (DPM)

## Limitations
- No discrete GPU — CUDA not available locally (use remote Jetson/ZedBox for CUDA)
- No AVX-512 — some ML workloads may be slower
- 7 GiB RAM — large models or datasets should use remote machines or swap
- Soldered RAM — cannot upgrade beyond 8 GiB physical
