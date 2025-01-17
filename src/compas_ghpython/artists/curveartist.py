from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import CurveArtist
from .artist import GHArtist


class CurveArtist(GHArtist, CurveArtist):
    """Artist for drawing curves.

    Parameters
    ----------
    curve : :class:`compas.geometry.Curve`
        A COMPAS curve.

    Other Parameters
    ----------------
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`GHArtist` and :class:`~compas.artists.CurveArtist`.

    """

    def __init__(self, curve, **kwargs):
        super(CurveArtist, self).__init__(curve=curve, **kwargs)

    def draw(self):
        """Draw the curve.

        Returns
        -------
        :rhino:`Rhino.Geometry.Curve`

        """
        return self.curve.rhino_curve
