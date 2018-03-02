import numpy as np

def outgoingks(geometry):
    '''
    generates the outgoing wavevectors for plane waves
    scattered into the detector
    note that here K = k_out, not k_out - k_in
    '''
    det_size_horz = geometry['det_size_horz']
    det_size_vert = geometry['det_size_vert']

    det_pixels_horz = geometry['det_pixels_horz']
    det_pixels_vert = geometry['det_pixels_vert']

    pix_size_horz = det_size_horz * 1. / det_pixels_horz
    pix_size_vert = det_size_vert * 1. / det_pixels_vert

    image_Ny = geometry['imageNy']
    image_Nz = geometry['imageNz']

    beam_center = geometry['beam_center']

    # Local detector coordinate system define the local detector
    # coordinates in image pixels. Origin is at top left pixel
    Y = np.linspace(0, det_size_horz, image_Ny)
    Z = np.linspace(0, det_size_vert, image_Nz)

    # stuff in the XYZ (3D) scattering coordinate system
    D = geometry['det_dist']
    k_0 = 1. / geometry['lambda0'] # Angstroms^-1

    # BEAM CENTER:
    # make sure Z and Y are zero at the beam intersection (i.e. [1 0 0])
    Y = Y - beam_center[0]*pix_size_horz
    Z = Z - beam_center[1]*pix_size_vert

    Ymesh, Zmesh = np.meshgrid(Y,Z)
    Deno = np.sqrt(Zmesh**2 + Ymesh**2 + D**2)

    K = np.zeros((image_Nz, image_Ny, 3))

    K[:,:,0] = k_0 * (D / Deno)
    K[:,:,1] = k_0 * (- Ymesh / Deno)   # RIGHT of image is Y < 0 in the lab frame
    K[:,:,2] = k_0*(- Zmesh / Deno) # positive Z is up, but detector local "Z" increases downwards

    return K
