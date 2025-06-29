# install pycortex, it supports python3.11, so we can install pycortex in the nilearn conda env.
# remember to install numpy 1.26.1.

import os
import matplotlib.pyplot as plt
import numpy as np
from nilearn import image
import ants

import cortex
############## Method 1
subject = "fsaverage"
xfm = '/home/clancy/miniconda3/envs/nilearn/share/pycortex/db/fsaverage/transforms/atlas_2mm'
file = 'cortisol_brain_zcoef_sub19.nii.gz' # mni2009cAsym
TemplateFlow = '/home/clancy/TemplateFlow'
newmni_fslmni = ants.read_transform(f'{TemplateFlow}/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_from-MNI152NLin2009cAsym_mode-image_xfm.h5')
# ants transform
file_img = ants.image_read(file)
ref_img = ants.image_read(f'{TemplateFlow}/tpl-MNI152NLin6Asym/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz')
file_fsl = newmni_fslmni.apply_to_image(image = file_img, 
                             reference = ref_img, 
                             interpolation='linear')

voxel_vol = cortex.Volume(file_fsl.numpy(), subject, xfm )
#cortex.webgl.show(data=voxel_vol)
# Then we have to get a mapper from voxels to vertices for this transform
mapper = cortex.get_mapper(subject, xfm, 'line_nearest', recache=True)
# Just pass the voxel data through the mapper to get vertex data
vertex_map = mapper(voxel_vol)
# You can plot both as you would normally plot Volume and Vertex data
cortex.quickshow(vertex_map)
plt.show()

############## Method 2
from nilearn.surface import SurfaceImage
from nilearn.datasets import load_fsaverage
fsa = load_fsaverage('fsaverage')
file = 'cortisol_brain_zcoef_sub19.nii.gz' # mni2009cAsym
file_surf = SurfaceImage.from_volume(fsa["pial"], file, inner_mesh=fsa["white_matter"])

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
red_yellow_file = '/usr/local/fsl/fslpython/envs/fslpython/lib/python3.8/site-packages/fsleyes/assets/colourmaps/red-yellow.cmap'
blue_lightblue_file = '/usr/local/fsl/fslpython/envs/fslpython/lib/python3.8/site-packages/fsleyes/assets/colourmaps/blue-lightblue.cmap'
red_yellow_data = np.loadtxt(red_yellow_file)
blue_lightblue_org = np.loadtxt(blue_lightblue_file)
blue_lightblue_data = blue_lightblue_org[::-1]
combined = np.vstack((blue_lightblue_data, red_yellow_data))
cmap_aa = ListedColormap(combined)
vertex_data = cortex.Vertex(np.append(file_surf.data.parts['left'],file_surf.data.parts['right']), 
                              subject, vmax=1, vmin=-1, cmap=cmap_aa)
cortex.quickshow(vertex_data)
plt.show()


####### Add ROI
import os
import nibabel.freesurfer.io as fsio
import numpy as np
import cortex
label_file = '/home/clancy/TemplateFlow/BN_Atlas_freesurfer/fsaverage/label/lh.BN_Atlas.annot'
label_img = fsio.read_annot(label_file)[0]
mask = np.zeros_like(label_img)
mask[mask==22] = 1
V = cortex.dataset.Vertex(mask, 'fsaverage')
cortex.quickshow(V)
plt.show()
####### Add ROI
import os
import nibabel.freesurfer.io as fsio
import numpy as np
import matplotlib.pyplot as plt
import cortex
label_file_lh = '/home/clancy/TemplateFlow/BN_Atlas_freesurfer/fsaverage/label/lh.BN_Atlas.annot'
label_file_rh = '/home/clancy/TemplateFlow/BN_Atlas_freesurfer/fsaverage/label/rh.BN_Atlas.annot'
lh_data = fsio.read_annot(label_file_lh)[0]
rh_data = fsio.read_annot(label_file_rh)[0]
both_data = np.append(lh_data, rh_data)
mask = np.zeros_like(both_data)
mask[(both_data==23) | (both_data==124)] = 1
V = cortex.Vertex(mask, subject="fsaverage", cmap=None)
cortex.add_roi(data=V, name='MFG', open_inkscape=True, add_path=True, overlay_file='rois.svg')

