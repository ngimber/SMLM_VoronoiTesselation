Voronoi Tesselation for Single Molecule Localization Microscopy
==========

The included Python script performs Voronoi tesselation on localization tables from from single-molecule localization microscopy.
Localization tables must have the ThunderSTORM [1] oder SD-Mixer [2] file format.

The script was used for the the following publications:



Instructions
-------
- Localization tables must have the ThunderSTORM .csv file format (column headers: 'x [nm]' and 'y [nm]', including quotation marks) or ther SD-Mixer file format (columns headers: 'x short [nm]','y short [nm]', ...).
- Selected files must be stored in the same folder.
- Users will be asked to set the following parameters:
    - Relative Threshold: The value is muliplied with the median 'tesselation area' and serves as a threshold for segmentation.
    - Number of Parallel Jobs: Defines how many files should be processed in parallel.
  
- Two files are exported per input. One full dataset and one 'segmented' dataset, without localizations above 'tesselation area' threshold. Files are exported in the ThunderSTORM file format with an extra column 'tesselation area'. and can be loaded back into ThunderSTORM for further processig.


References
-------
[1] Ovesny, M., et al., ThunderSTORM: a comprehensive ImageJ plug-in for PALM and STORM data analysis and super-resolution imaging. Bioinformatics, 2014. 30(16): p. 2389-90. 
[2] Tadeus, G. (2015) SDmixer2 https://github.com/gtadeus/sdmixer2 GitHub. 
