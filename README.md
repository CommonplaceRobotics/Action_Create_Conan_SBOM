# Create Conan SBOM action
Github Action for creating incomplete CycloneDX SBOMs for dependencies defined by Conan 2

This action is intended to be used for CPR internal purposes. Use by anyone else is at your own risk, consider this repository not stable.

Use it as follows:

```
- name: Create incomplete SBOM
  uses: CommonplaceRobotics/SW_Create_Conan_SBOM@v1
  with:
    lockfile: conan_linux.lock
    sbom: sbom_temp1.cdx.json
```

With the following parameters:
* lockfile: Conan 2 lockfile to read
* sbom: name of the SBOM file to create

This creates a CycloneDX v1.6 SBOM that should be completed using further tools.
