# Module holding WPG beamlines at European XFEL.

import os
from wpg import Beamline
from wpg.optical_elements import (Aperture, Drift, Mirror_elliptical,
                                  Mirror_plane, Use_PP)


def get_beamline():
    """ Setup and return the WPG.Beamline object representing the SPB/SFX nanofocus beamline (KB mirrors).

    :return: beamline
    :rtype: wpg.Beamline
    """

    # Distances
    distance0 = 246.5
    distance1 = 683.5
    distance = distance0 + distance1

    # Focal lengths.
    f_hfm = 3.0          # nominal focal length for HFM KB
    f_vfm = 1.9          # nominal focal length for VFM KB
    distance_hfm_vfm = f_hfm - f_vfm
    distance_foc = 1. / (1. / f_vfm + 1. / (distance + distance_hfm_vfm))

    # Mirror incidence angles
    theta_om = 3.5e-3       # offset mirrors incidence angle
    theta_kb = 3.5e-3       # KB mirrors incidence angle

    # Mirror lengths
    om_mirror_length = 0.8
    om_clear_ap = om_mirror_length * theta_om
    kb_mirror_length = 0.9
    kb_clear_ap = kb_mirror_length * theta_kb

    # Drifts.
    drift0 = Drift(distance0)
    drift1 = Drift(distance1)
    drift_in_kb = Drift(distance_hfm_vfm)
    drift_to_foc = Drift(distance_foc)

    # Mirror apertures.
    ap0 = Aperture('r', 'a', 120.e-6, 120.e-6)
    ap1 = Aperture('r', 'a', om_clear_ap, 2 * om_clear_ap)
    ap_kb = Aperture('r', 'a', kb_clear_ap, kb_clear_ap)

    # Mirror definitions.
    hfm = Mirror_elliptical(
        orient='x',
        p=distance,
        q=(distance_hfm_vfm + distance_foc),
        thetaE=theta_kb,
        theta0=theta_kb,
        length=0.9
    )
    vfm = Mirror_elliptical(
        orient='y',
        p=(distance + distance_hfm_vfm),
        q=distance_foc,
        thetaE=theta_kb,
        theta0=theta_kb,
        length=0.9
    )

    mirrors_path = 'data_common'
    # Wavefront distortions due to mirror profile.
    wf_dist_om = Mirror_plane(orient='x',
                              theta=theta_om,
                              length=om_mirror_length,
                              range_xy=2 * om_clear_ap,
                              filename=os.path.join(
                                  mirrors_path, 'mirror2.dat'),
                              scale=2.,
                              bPlot=True)

    wf_dist_hfm = Mirror_plane(orient='x',
                               theta=theta_kb,
                               length=kb_mirror_length,
                               range_xy=kb_clear_ap,
                               filename=os.path.join(
                                   mirrors_path, 'mirror1.dat'),
                               scale=2.,
                               bPlot=True)

    wf_dist_vfm = Mirror_plane(orient='y',
                               theta=theta_kb,
                               length=kb_mirror_length,
                               range_xy=kb_clear_ap,
                               filename=os.path.join(
                                   mirrors_path, 'mirror2.dat'),
                               scale=2.,
                               bPlot=True)

    # Assemble the beamline with PP parameters.
    bl0 = Beamline()

    zoom = 2.0
    bl0.append(
        ap0, Use_PP(semi_analytical_treatment=0, zoom=zoom, sampling=zoom / 1.2))
    bl0.append(drift0, Use_PP(semi_analytical_treatment=1))

    zoom = 1.4
    # bl0.append(ap1, Use_PP(zoom=1.2)) #bl0.append(ap1, Use_PP(zoom=0.8))
    bl0.append(ap1, Use_PP(zoom=zoom, sampling=zoom / 0.6))
    bl0.append(wf_dist_om, Use_PP())
    bl0.append(drift1, Use_PP(semi_analytical_treatment=1))
    bl0.append(ap_kb, Use_PP(sampling=1. / 0.6))
    bl0.append(hfm, Use_PP())
    bl0.append(wf_dist_hfm, Use_PP())
    bl0.append(drift_in_kb, Use_PP(semi_analytical_treatment=1))
    bl0.append(vfm, Use_PP())
    bl0.append(wf_dist_vfm, Use_PP())
    bl0.append(drift_to_foc, Use_PP(semi_analytical_treatment=1))

    # All done, return.
    return bl0
