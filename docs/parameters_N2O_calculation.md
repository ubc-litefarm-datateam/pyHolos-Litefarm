## Parameters for Crop Residue Nitrogen Calculation {#Parameters-N2O-Calculation}

|Parameter groups|Parameters|Explanation|Data source|
|---|---|---|---|---|
| Farm | Area | Numerical, total area of the farm (ha)| LiteFarm |
| Farm | Yield | Numerical, the estimated yield ($kg/ha$) | LiteFarm |
| Crop | Moisture | Moisture content of product (%) | Holos default/External information |
| Crop | $N_p$ | N concentration in the product ($kg \ kg^{-1}$) | Holos default/External information |
| Crop | $N_s$ | N concentration in the straw ($kg \ kg^{-1}$) | Holos default/External information |
| Crop | $N_r$ | N concentration in the roots ($kg \ kg^{-1}$) | Holos default/External information |
| Crop | $N_e$ | N concentration in the extra root material ($kg \ kg^{-1}$) | Holos default/External information |
| Crop | $R_s$ | Relative biomass allocation coefficient for straw | Holos default/External information |
| Crop | $R_p$ | Relative biomass allocation coefficient for product | Holos default/External information |
| Crop | $R_r$ | Relative biomass allocation coefficient for roots | Holos default/External information |
| Crop | $R_e$ | Relative biomass allocation coefficient for extra-root material | Holos default/External information |
| Crop group | $C_{concentration}$ | Carbon concentration of all plant parts ($kg \ kg^{-1}$) |Holos default/External information |
| Crop group | $S_p$ | Percentage of product yield returned to soil | Holos default/External information |
| Crop group | $S_s$ | Percentage of straw returned to soils | Holos default/External information |
| Crop group | $S_r$ | Percentage of roots returned to soil | Holos default/External information |
| Climate & soil | $P_i$ | Annual growing season precipitation (May – October), in ecodistrict “i” (mm) | Holos default/NASA POWER |
| Climate & soil | $PE$ | Growing season potential evapotranspiration, by ecodistrict (May – October) | Holos default/NASA POWER |
| Climate & soil | $FR\_Topo_{i}$ | Fraction of land occupied by lower portions of landscape | Holos default |
| Modifiers / soil | $RF\_TX_{i}$ | Weighted modifier which provides a correction of the $EF_Topo$ in ecodistrict ‘‘i’’ based on the soil texture | Holos default/HWSD 2.0 |
| Modifiers | $RF\_CS$ | Reduction factor for Cropping System | Holos default/External information |
| Modifiers | $RF\_NS$ | N source modifier RF_NS (SN = Synthetic Nitrogen; ON = Organic Nitrogen; CRN = Crop Residue Nitrogen) | Holos default/External information |
| Modifiers | $RF\_AM$ | Reduction factor based on application method, only applicable to calculations of EF specific for SN | Holos default/External information |
| Modifiers | $RF\_Till$ | Tillage modifier (Conservation or Conventional Tillage) | Holos default/External information |