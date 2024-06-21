
## Equations

The equations outdined are sourced from the [AAFC Technical Report: Holos V4.0 Algorithm Document REVIEW VERSION 22 Jan 2024](https://github.com/holos-aafc/Holos/raw/e33ea632053a7635589c245318bd3ad05939607b/AAFC_Technical_Report_Holos_V4.0_Algorithm_Document_REVIEWVERSION22Jan2024.docx). The numbers in parentheses following each equation indicate the specific equation numbers in the Holos documentation. Each equation includes a reference link to the corresponding line in the Holos code on GitHub.

### Total Crop Residues

$N_{crop\_residues} = (AboveGround_{residue\_N} + BelowGround_{residue\_N}) \times {area} \quad \text{(2.5.6-9)}$

**Variables**:

- $N_{crop\_residues}$: N (nitrogen) inputs from crop residue returned to soil ($kg N$)
- $AboveGround_{residue\_N}$: Aboveground residue nitrogen ($kg N ha^{-1}$)
- $BelowGround_{residue\_N}$: Belowground residue nitrogen $kg N ha^{-1}$)
- $area$: Area of crop ($ha$)

#### AboveGround Residue Nitrogen

$$
AboveGround_{residue\_N} = [{Grain_N} + {Straw_N}] \quad \text{(2.5.6-6)}
$$

**Holos Code Reference**: [Holos GitHub - Equation 2.5.6-6](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L617)

**Variables**:

- $AboveGround_{residue\_N}$: Nitrogen in above-ground crop residues ($kg N$)
- ${Grain_N}$: Nitrogen content of the grain returned to the soil ($kg N ha^{-1}$)
- ${Straw_N}$: Nitrogen content of the straw returned to the soil ($kg N ha^{-1}$)

#### BelowGround Residue Nitrogen

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

- $BelowGround_{residue\_N}$: Belowground residue nitrogen ($kg N ha^{-1}$)
- ${Root_N}$: Nitrogen content of the root returned to the soil ($kg N ha^{-1}$)
- ${Exudate_N}$: Nitrogen content of the exudates returned to the soil ($kg N ha^{-1}$)
- $S_r$: Root turnover fraction

#### Grain_N

$$
{Grain}_N = \frac{C_{p\_to\_soil}}{0.45} \times N_p \quad \text{(2.5.6-2)}
$$

**Holos Code Reference**: [Holos GitHub - Equation 2.5.6-2](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L561)

**Variables**:

- ${Grain}_N$: Nitrogen content of the grain returned to the soil ($kg N ha^{-1}$)
- $C_{p\_to\_soil}$: Carbon input from product ($kg ha^{-1}$)
- $N_p$: N concentration in the product ($kg kg^{-1}$) [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

#### Straw_N

$$
{Straw}_N = \frac{C_s}{0.45} \times N_s \quad \text{(2.5.6-3)}
$$

**Holos Code Reference**: [GitHub - Equation 2.5.6-3](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L575)

**Variables**:

- ${Straw}_N$: Nitrogen content of the straw returned to the soil ($kg N ha^{-1}$)
- $C_s$: Carbon input from straw ($kg ha^{-1}$)
- $N_s$: N concentration in the straw ($kg kg^{-1}$) [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

#### Root_N

$$
{Root}_N = \frac{C_r}{0.45} \times N_r \quad \text{(2.5.6-4)}
$$

**Holos Code Reference**: [GitHub - Equation 2.5.6-4](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L589)

**Variables**:

- ${Root}_N$: Nitrogen content of the root returned to the soil ($kg N ha^{-1}$)
- $C_r$: Carbon input from roots ($kg ha^{-1}$)
- $N_r$: N concentration in the roots ($kg kg^{-1}$) [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

#### Exudate_N

$$
{Exudate}_N = \frac{C_e}{0.45} \times N_e \quad \text{(2.5.6-5)}
$$

**Holos Code Reference**: [GitHub - Equation 2.5.6-5](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L603)

**Variables**:

- $\text{Exudate}_N$: Nitrogen content of the exudates returned to the soil ($kg N ha^{-1}$)
- $C_e$: Carbon input from extra-root material ($kg ha^{-1}$)
- $N_e$: N concentration in the extra root material ($kg kg^{-1}$) [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

#### C_p: Above and Belowground Residue Input

$$
C_p = [(yield + yield \times \frac{S_p}{100}) \times (1 - \frac{{moisture \ content}}{100})] \times {Carbon \ concentration} \quad \text{(2.1.2-6)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-6](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L270)

**Variables**:

- $C_p$: Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $yield$: Crop yield (${kg} \text{ wet weight } ha^{-1}$, default provided, user override)
- $S_p$: Percentage of product yield returned to soil (user override)
- $\text{moisture content}$: Moisture content (%) of crop product [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $\text{Carbon concentration}$: C concentration of all plant parts ($kg kg^{-1}$)

#### C_p_to_soil: Carbon input from product

$$
C_{{p\_to\_soil}} = C_p \times \frac{S_p}{100} \quad \text{(2.1.2-7)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-7](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L307)

**Variables**:

- $C_{p\_to\_soil}$: Carbon input from product ($kg ha^{-1}$)
- $C_p$: Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $S_p$: Percentage of product yield returned to soil (user override)

#### C_s: Carbon Input from Straw

$$
C_s = C_p \times \frac{R_s}{R_p} \times \frac{S_s}{100} \quad \text{(2.1.2-8)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-8](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L344)

**Variables**:

- $C_s$: C (carbon)  input from straw ($kg ha^{-1}$)
- $C_p$: Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $R_s$: Relative biomass allocation coefficient for straw [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $R_p$：Relative biomass allocation coefficient for product [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $S_s$: Percentage of straw returned to soil (user override)

#### C_r: Carbon input from Root

$$
C_r = C_p \times \frac{R_r}{R_p} \times \frac{S_r}{100} \quad \text{(2.1.2-9)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-9](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L398)

**Variables**:

- $C_r$: C (carbon)  input from roots ($kg ha^{-1}$)
- $C_p$:  Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $R_r$:Relative biomass allocation coefficient for roots [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $R_p$：Relative biomass allocation coefficient for product [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $S_r$: Percentage of roots returned to soil (user override)

#### C_e: Carbon Input from Exudate

$$
C_e = C_p \times \frac{R_e}{R_p} \quad \text{(2.1.2-9)}
$$

**Holos Code Reference**: [GitHub - Equation 2.1.2-9](https://github.com/holos-aafc/Holos/blob/21c18d94c871eaa1eaa2ab1d475eca0f0e34b35b/H.Core/Calculators/Carbon/ICBMSoilCarbonCalculator.cs#L398)

**Variables**:

- $C_e$: C (carbon) input from extra-root material ($kg ha^{-1}$)
- $C_p$: Plant C (carbon) in agricultural product ($kg ha^{-1}$)
- $R_e$: Relative biomass allocation coefficient for extra-root material [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)
- $R_p$: Relative biomass allocation coefficient for product [[Holos Table 7]](https://github.com/holos-aafc/Holos/blob/main/H.Content/Resources/Table_7_Relative_Biomass_Information.csv)

### Emission Factor

#### Calculate Base Emission Factor - Ecodistrict-level Emission Factor

$EF\\\_CT_{i,P>PE} = \exp^{0.00558 \times P_{i} - 7.7}$  (2.5.1-1)

$EF\\\_CT_{i,P\leqslant PE} = \exp^{0.00558 \times PE_{i} - 7.7}$  (2.5.1-2)

**Holos Code Reference**: [GitHub - Equation 2.5.1](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L880)

**Variables**:

- $EF\\\_CT_i$: Ecodistrict-level emission factor ($kg \, N_2O\text{-}N \, (kg \, N)^{-1}$)
- $P_i$: Annual growing season precipitation (May – October), in ecodistrict “i” (mm)
- $PE$: Growing season potential evapotranspiration, by ecodistrict (May – October) (mm)

#### Calculate Emission Factor Adjustment Due to Position in Landscape/Topography

For humid environments $P/PE > 1$: $EF\\\_Topo_i = EF\\\_CT_{i,P>PE}$ (2.5.2-1)

For non-irrigated sites and dry environments $P/PE \leqslant 1$: $EF\\\_Topo_i = (EF\\\_CT_{i,P<PE} \times FR\\\_Topo_i) + [EF\\\_CT_{i,P>PE} \times (1 - FR\\\_Topo_i)]$ (2.5.2-2)

For irrigated sites and $P < PE$: $EF\\\_Topo_i = EF\\\_CT_{i,P\leqslant PE}$ (2.5.2-3)

**Holos Code Reference**: [GitHub - Equation 2.5.2](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L381)

**Notes:**

For non-irrigated sites and $P/PE \leqslant 1$, the fraction of low-lying land and depressions is calculated with the actual PE ($EF\\\_CT_{i,P\leqslant PE}$), and the remainder of the land with the standard EF ($EF\\\_CT_{i,P>PE}$).

For irrigated sites, the assumption is that the irrigation amount is equal to PE - P, thus making P = PE.

**Variables**:

- $EF\\\_Topo_i$: N2O emission factor adjusted due to position in landscape and moisture regime ($kg \, N_2O\text{-}N$)
- $FR\\\_Topo_i$: Fraction of land occupied by lower portions of the landscape

#### Calculate Emission Factor Adjustment Due to Soil Texture

$EF\\\_Base_i = (EF\\\_Topo_i \times RF\\\_TX_i) \times \frac{1}{0.645}$ (2.5.3-2)

**Holos Code Reference**: [GitHub - Equation 2.5.3-2](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/Calculators/Nitrogen/N2OEmissionFactorCalculator.cs#L451)

**Variables**:

- $RF\\\_TX_i$: Weighted modifier which provides a correction of the $EF\_Topo$ in ecodistrict “i” based on the soil texture.
- $EF\\\_Base_i$: A function of the three factors that create a base ecodistrict-specific value that accounts for the climatic, topographic, and edaphic characteristics of the spatial unit for lands.
- $\frac{1}{0.645}$: Fraction of growing season emissions of total annual emissions (Pelster et al. 2022, in prep.).

#### Calculate Emission Factor

$EF_{i,k,l,m,n} = EF\_{Base_i} \times RF\_{NS_k} \times RF\_{Till_l} \times RF\_{CS_m} \times RF\_{AM}$ (2.5.4-1)

**Variables**:

- $RF\_{NS_k}$: Reduction factor for N source, $RF\_NS_k$ (SN = Synthetic Nitrogen; ON = Organic Nitrogen; CRN = Crop Residue Nitrogen). For CRN, the value is 0.84. [[Holos Lookup Function]](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/Providers/Soil/Table_13_Soil_N2O_Emission_Factors_Provider.cs#L43)
- $RF\_{Till_l}$: Reduction factor for tillage practice [[Holos Lookup Function]](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/Providers/Soil/Table_13_Soil_N2O_Emission_Factors_Provider.cs#L93)
- $RF\_{CS_m}$: Reduction factor for cropping system. For annual cropping system, the value is 1. For Perennial systems, the value is 0.19 [[Holos Lookup Function]](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/Providers/Soil/Table_13_Soil_N2O_Emission_Factors_Provider.cs#L75)
- $RF\_{AM}$: Reduction factor based on application method, only applicable to calculations of EF specific for SN. For other N source, the value is 1 [[Holos Lookup Function]](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/Providers/Soil/Table_13_Soil_N2O_Emission_Factors_Provider.cs#L189)

### Emission

#### Calculate Direct Nitrous Oxide from Inputs

$N_2O - N_{CRNdirect(t,field,n)} = N_{CropResidues(t,field,n)} \times EF_{i,CRN,l,m,n}$ (2.6.5-2)

**Holos Code Reference**: [GitHub - Equation 2.6.5-2](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/Calculators/Carbon/CarbonCalculatorBase.Nitrogen.cs#L377)

**Variables**:

- $N_2O - N_{CRNdirect(t,field,n)}$: Direct N₂O emissions ($kg \, N_2O\text{-}N \, ha^{-1}$) resulting from crop residues and N mineralization on field n in year t.
- $N_{CropResidues(t,field,n)}$: Amount of crop residues on field n in year t.
- $EF_{i,CRN,l,m,n}$: Emission factor for crop residue nitrogen specific to the conditions i, l, m, and n.

#### Calculate Emission for Each Field, Crop, and Year

$N_2O - N_{direct} = N_2O - N_{SNdirect} + N_2O - N_{CRNdirect} + N_2O - N_{CRNmindirect} + N_2O - N_{ONdirect}$

**Notes:**

Currently, only Nitrogen Direct Emission from crop residues is calculated, as this only accounts for crop-related factors and not livestock, fertilizer, and manure.

**Variables**:

- $N_2O - N_{SNdirect}$: N₂O emissions ($kg \, N_2O\text{-}N \, kg^{-1} \, N \, ha^{-1}$) resulting from fertilizer application
- $N_2O - N_{CRNdirect}$: N₂O emissions ($kg \, N_2O\text{-}N \, kg^{-1} \, N \, ha^{-1}$) resulting from crop residues and N mineralization
- $N_2O - N_{CRNmindirect}$: N₂O emissions ($kg \, N_2O\text{-}N \, kg^{-1} \, N \, ha^{-1}$) resulting from N mineralization
- $N_2O - N_{ONdirect}$: N₂O emissions ($kg \, N_2O\text{-}N \, kg^{-1} \, N \, ha^{-1}$) resulting from organic fertilizers

#### Convert N₂O - N to N₂O

$N_2O = N_2O - N \times \frac{44}{28}$

**Variables**:

- $\frac{44}{28}$: Conversion factor from N₂O-N to N₂O based on molecular mass

#### Calculate CO₂ Equivalent of N₂O Emissions

$CO_2e = N_2O \times 273$

**Notes:**

Holos uses 273 as the Global Warming Potential value for N₂O. [Holos Reference](https://github.com/holos-aafc/Holos/blob/6f24e78c7bd46ae35848906933475f077562cd0d/H.Core/CoreConstants.cs#L135)

**Variables**:

- $273$: Global Warming Potential for N₂O compared to CO₂
