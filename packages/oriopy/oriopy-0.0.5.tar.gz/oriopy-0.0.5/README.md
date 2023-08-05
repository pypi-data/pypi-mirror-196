<p align="center">
  <img src="https://github.com/jewelsbla/oriopy/blob/main/images/oriopy_logo.png?raw=true">
</p>

<sub><sub>Image source "OREO": https://news.mit.edu/2022/oreometer-cream-0419 \
The trademarks, logos, photography, brand names, design and service marks of "OREO" are owned by the company Nabisco. No copyright infringement intended. <sub><sub>

Graphic by Blarr

***
[![PyPI version](https://badge.fury.io/py/oriopy.svg)](https://badge.fury.io/py/oriopy)
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

*Interpolation of tensors of second and fourth order via decomposition approach*

## Disclaimer 
The paper describing the scientific background and the methods underlying this repository is: Blarr, J., Sabiston, T., Krauß, C. et al. Implementation and comparison of algebraic and machine learning based tensor interpolation methods applied to fiber orientation tensor fields obtained from CT images. Computational Materials Science, 2023.

This code was published alongside the raw data of the CT scans and the evaluated tensor data first as research data set here: https://doi.org/10.5445/IR/1000153725.

If you use the code in this repository, please cite both DOIs.

## Content

OrioPy is a Python package to interpolate fiber orientation tensors (or tensors of any kind for that matter) of second or fourth order. Both methods make use of the fact that symmetric positive definite tensors can be decomposed into eigenvalues and eigenvectors in spectral decomposition. In terms of the visualization of tensors in the form of tensor glyphs, the eigenvalues are responsible for the shape, while the eigenvectors are responsible for the orientation of the tensor in space.

In case of the tensors of fourth order, these eigenvalues and eigenvectors (in the form of the rotation matrix R) are directly weighted according to Shepard's inverse distance weighting, interpolated separately and then recomposed into a tensor.

In case of the orientation tensors of second order, instead of the eigenvalues another group of invariants, so-called orthogonal invariants, are used. The eigenvectors are also recalculated to quaternions and then interpolated. The reasons for this 
detour is explained in the paper mentioned above. The approach is additionally visualized in the following graphic:

<p align="center">
  <img src="https://github.com/jewelsbla/oriopy/blob/main/images/graphic_decomposition_2.png?raw=true">
</p>

## Usage

In the folder "oriopy" there are three Python scripts. The "component_averaging_interpolation.py" and the "decomposition_interpolation.py" work the same: The script needs an input .txt-file with coordinates and the corresponding fiber orientation tensors (the example used in the publication is given in the folder "example" (file "input_file_FOT.txt")). After running the code you are asked in the console for the name of the output file and for lower and upper x and y limit, which are 1 and 13, respectively, in the given case. The scripts then calculate the fiber orientation tensors at all missing positions with the respective method, which are then written into a MATLAB file (which is named the way you input in the console). This MATLAB file is structured in a way that the fiber orientation tensors can be plotted directly with the tensor glyph visualization function of Barmpoutis ("plotDTI"): https://de.mathworks.com/matlabcentral/fileexchange/27462-diffusion-tensor-field-dti-visualization.
The third file "4th_order_decomposition_interpolation.py" works basically the same way, aside from the fact that it needs fourth order tensors as an input and outputs fourth order tensors. In the "example"-folder, there is another input file named "input_file_FOT_4th_order.txt", which can be used for this purpose. Please be aware that there is the possibility for the visualization of fourth order tensors within the mentioned Matlab methods, however, this takes up quite some time to plot the entire field of fourth order tensors. Be free to only use the methods of the oriopy package for interpolation and write your own visualization function instead of using this Matlab visualization or the proposed main of the authors.

An example of a fiber orientation tensor field generated with the decomposition method for tensors of second order can be seen below.

<p align="center">
  <img src="https://github.com/jewelsbla/oriopy/blob/main/images/decomposition_complete_cut_dark_mode.png?raw=true">
</p>


## Details and background

The authors originally determined fiber orientation tensors (FOT) of second and fourth order from µCT scans of carbon fiber reinforced polyamide 6 specimen. The C++ code for the FOT determination works with a structure tensor approach, is explained in this paper and can be found here: Pinter P, Dietrich S, Bertram B, Kehrer L, Elsner P, Weidenmann KA. Comparison and error estimation of 3D fibre orientation analysis of computed tomography image data for fibre reinforced composites. NDT & E International 2018; 95:26–35. https://doi.org/10.1016/j.ndteint.2018.01.001.
https://sourceforge.net/p/composight/code/HEAD/tree/trunk/SiOTo/StructureTensorOrientation/FibreOrientation/StructureTensorOrientationFilter.cxx#l186

The specimens were cut from a 400 mm x 400 mm x 4 mm plate to 10 mm x 10 mm x 4 mm in order to be able to have a high enough resolution to detect fibers in the CT in general. That resulted in very local information of the fiber orientation in the plate. Hence, the idea was to generate a full field of FOT across the plate in order to gain a more holistic idea of the flow behavior in the process and of the mechanical properties of the plate. In the paper of Blarr et al., three tensor interpolation methods for tensors of second order were compared, of which the decomposition method showed the most reliable results and was therefore evolved into the oriopy package. The component averaging method can be found as well. Only the code for the ANN is not available here, but the Jupyter notebook can also be accessed through the data set mentioned above.

The method for the interpolation of tensors of fourth order was implemented later and is described in a following paper, where the results are also assessed in terms of their mechanical meaningfulness. Hence, the results are used for both the Mori Tanaka and the Halpin Tsai homogenization to predict stiffnesses, which are then compared to tensile test based results of Young's moduli.

For further questions, please consider the documentation in the paper Blarr et al. (2023).

## Version

The current version will be further developed into classes soon. 

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg