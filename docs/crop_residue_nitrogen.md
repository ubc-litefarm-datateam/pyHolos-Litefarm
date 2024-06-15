# Documentation for Crop Residue Nitrogen Calculation

## Introduction

This document outlines the calculation of nitrogen inputs from crop residues returned to the soil. The equations used are sourced from the [AAFC Technical Report: Holos V4.0 Algorithm Document REVIEW VERSION 22 Jan 2024](https://github.com/holos-aafc/Holos/raw/e33ea632053a7635589c245318bd3ad05939607b/AAFC_Technical_Report_Holos_V4.0_Algorithm_Document_REVIEWVERSION22Jan2024.docx). The numbers in parentheses following each equation indicate the specific equation numbers in the Holos documentation. Each equation includes a reference link to the corresponding line in the Holos code on GitHub.

## Calculation

### Total Crop Residues

$N_{crop\_residues} = (AboveGround_{residue\_N} + BelowGround_{residue\_N}) \times {area} \quad (2.5.6-9)$

**Variables**:

- $N_{crop\_residues}$: N (nitrogen) inputs from crop residue returned to soil ($kg N$)
- [$AboveGround_{residue\_N}$](#1-aboveground-residue-nitrogen): Aboveground residue nitrogen ($kg N ha^{-1}$)
- [$BelowGround_{residue\_N}$](#2-belowground-residue-nitrogen): Belowground residue nitrogen $kg N ha^{-1}$)
- $area$: Area of crop ($ha$)

## Components

### 1. AboveGround Residue Nitrogen

$$
AboveGround_{residue\_N} = [{Grain_N} + {Straw_N}] \quad \text{(2.5.6-6)}
$$

**Holos Code Reference**: [Holos GitHub - Equation 2.5.6-6](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L617)

**Variables**:

- [$AboveGround_{residue\_N}$](#1-aboveground-residue-nitrogen): Nitrogen in above-ground crop residues ($kg N$)
- [${Grain_N}$](#3-grain_n): Nitrogen content of the grain returned to the soil ($kg N ha^{-1}$)
- [${Straw_N}$](#4-straw_n): Nitrogen content of the straw returned to the soil ($kg N ha^{-1}$)

### 2. BelowGround Residue Nitrogen

For annual plants:

$$
BelowGround_{{residue_N}} = [{Root_N} + {Exudate_N}] \quad \text{(2.5.6-7)}
$$

**Holos Code Reference**: [Holos GitHub - Equation 2.5.6-7](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L679)

For perennial plants:

$$
BelowGround_{residue_N} = [S_r \times {Root}_N] + {Exudate_N} \quad \text{(2.5.6-8)}
$$

**Holos Code Reference**: [Holos GitHub - Equation 2.5.6-8](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L685)

**Variables**:

- [$BelowGround_{residue\_N}$](#2-belowground-residue-nitrogen): Belowground residue nitrogen ($kg N ha^{-1}$)
- [${Root_N}$](#5-root_n): Nitrogen content of the root returned to the soil ($kg N ha^{-1}$)
- [${Exudate_N}$](#6-exudate_n): Nitrogen content of the exudates returned to the soil ($kg N ha^{-1}$)
- $S_r$: Root turnover fraction

### 3. Grain_N

$$
{Grain}_N = \frac{C_{p\_to\_soil}}{0.45} \times N_p \quad \text{(2.5.6-2)}
$$

**Holos Code Reference**: [Holos GitHub - Equation 2.5.6-2](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L561)

**Variables**:

- [${Grain}_N$](#3-grain_n): Nitrogen content of the grain returned to the soil ($kg N ha^{-1}$)
- [$C_{p\_to\_soil}$](#8-carbon-input-from-product): Carbon input from product ($kg ha^{-1}$)
- $N_p$: N concentration in the product ($kg kg^{-1}$) [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

### 4. Straw_N

$$
{Straw}_N = \frac{C_s}{0.45} \times N_s \quad \text{(2.5.6-3)}
$$

**Holos Code Reference**: [GitHub - Equation 2.5.6-3](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L575)

**Variables**:

- [${Straw}_N$](#4-straw_n): Nitrogen content of the straw returned to the soil ($kg N ha^{-1}$)
- [$C_s$](#9-c_s-carbon-input-from-straw): Carbon input from straw ($kg ha^{-1}$)
- $N_s$: N concentration in the straw ($kg kg^{-1}$) [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

### 5. Root_N

$$
{Root}_N = \frac{C_r}{0.45} \times N_r \quad \text{(2.5.6-4)}
$$

**Holos Code Reference**: [GitHub - Equation 2.5.6-4](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L589)

**Variables**:

- [${Root}_N$](#5-root_n): Nitrogen content of the root returned to the soil ($kg N ha^{-1}$)
- [$C_r$](#10-c_r-carbon-input-from-root): Carbon input from roots ($kg ha^{-1}$)
- $N_r$: N concentration in the roots ($kg kg^{-1}$) [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

### 6. Exudate_N

$$
{Exudate}_N = \frac{C_e}{0.45} \times N_e \quad \text{(2.5.6-5)}
$$

**Holos Code Reference**: [GitHub - Equation 2.5.6-5](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L603)

**Variables**:

- [$\text{Exudate}_N$](#6-exudate_n): Nitrogen content of the exudates returned to the soil ($kg N ha^{-1}$)
- [$C_e$](#11-c_e-carbon-input-from-exudate): Carbon input from extra-root material ($kg ha^{-1}$)
- $N_e$: N concentration in the extra root material ($kg kg^{-1}$) [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

### 7. C_p: Above and Belowground Residue Input

$$
C_p = [(yield + yield \times \frac{S_p}{100}) \times (1 - \frac{{moisture \ content}}{100})] \times {Carbon \ concentration} \quad \text{(2.1.2-6)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-6](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L270)

**Variables**:

- [$C_p$](#7-c_p-above-and-belowground-residue-input): Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $yield$: Crop yield (${kg} \text{ wet weight } ha^{-1}$, default provided, user override)
- $S_p$: Percentage of product yield returned to soil (user override)
- $\text{moisture content}$: Moisture content (%) of crop product [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $\text{Carbon concentration}$: C concentration of all plant parts ($kg kg^{-1}$)

### 8. C_p_to_soil: Carbon input from product

$$
C_{{p\_to\_soil}} = C_p \times \frac{S_p}{100} \quad \text{(2.1.2-7)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-7](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L307)

**Variables**:

- [$C_{p\_to\_soil}$](#8-c_p_to_soil-carbon-input-from-product): Carbon input from product ($kg ha^{-1}$)
- [$C_p$](#7-c_p-above-and-belowground-residue-input): Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $S_p$: Percentage of product yield returned to soil (user override)

### 9. C_s: Carbon Input from Straw

$$
C_s = C_p \times \frac{R_s}{R_p} \times \frac{S_s}{100} \quad \text{(2.1.2-8)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-8](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L344)

**Variables**:

- [$C_s$](#9-c_s-carbon-input-from-straw): C (carbon)  input from straw ($kg ha^{-1}$)
- [$C_p$](#7-c_p-above-and-belowground-residue-input): Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $R_s$: Relative biomass allocation coefficient for straw [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $R_p$：Relative biomass allocation coefficient for product [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $S_s$: Percentage of straw returned to soil (user override)

### 10. C_r: Carbon input from Root

$$
C_r = C_p \times \frac{R_r}{R_p} \times \frac{S_r}{100} \quad \text{(2.1.2-9)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-9](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L398)

**Variables**:

- [$C_r$](#10-c_r-carbon-input-from-root): C (carbon)  input from roots ($kg ha^{-1}$)
- [$C_p$](#7-c_p-above-and-belowground-residue-input):  Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $R_r$:Relative biomass allocation coefficient for roots [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $R_p$：Relative biomass allocation coefficient for product [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $S_r$: Percentage of roots returned to soil (user override)

### 11. C_e: Carbon Input from Exudate

$$
C_e = C_p \times \frac{R_e}{R_p} \quad \text{(2.1.2-9)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-9](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L398)

**Variables**:

- [$C_e$](#11-c_e-carbon-input-from-exudate): C (carbon) input from extra-root material ($kg ha^{-1}$)
- [$C_p$](#7-c_p-above-and-belowground-residue-input): Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $R_e$: Relative biomass allocation coefficient for extra-root material [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $R_p$: Relative biomass allocation coefficient for product [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
