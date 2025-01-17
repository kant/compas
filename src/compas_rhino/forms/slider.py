from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.forms.base import BaseForm

import System
from System.Drawing import Size
from System.Drawing import Point
from System.Drawing import Color
from System.Windows.Forms import TextBox
from System.Windows.Forms import TrackBar

import scriptcontext as sc


__all__ = ['SliderForm']


class SliderForm(BaseForm):
    """A form for sliders.

    Parameters
    ----------
    minval : int
        The lowest value of the sliding range.
    maxval : int
        The highest value of the sliding range.
    step : int
        Size of one increment in the sliding range.
    value : int
        Starting value.

    """

    def __init__(self, minval, maxval, step, value):
        self.minval = minval
        self.maxval = maxval
        self.step = step
        self.value = value
        super(SliderForm, self).__init__()

    def init(self):
        """Initialize the form.

        Returns
        -------
        None

        """
        textbox = TextBox()
        textbox.Text = str(self.value)
        textbox.Location = Point(10, 10)
        textbox.Width = 40
        textbox.TextChanged += System.EventHandler(self.on_textchanged)
        trackbar = TrackBar()
        trackbar.Minimum = self.minval
        trackbar.Maximum = self.maxval
        trackbar.SmallChange = self.step
        trackbar.LargeChange = self.step
        trackbar.TickFrequency = self.step
        trackbar.Value = self.value
        trackbar.Width = 460
        trackbar.Location = Point(60, 10)
        trackbar.Scroll += System.EventHandler(self.on_scroll)
        self.Controls.Add(textbox)
        self.Controls.Add(trackbar)
        self.ClientSize = Size(10 + textbox.Width + 10 + trackbar.Width + 10, trackbar.Height + 10)
        self.textbox = textbox
        self.trackbar = trackbar

    def on_textchanged(self, sender, e):
        """Callback for changes made to the text input field.

        Parameters
        ----------
        sender : System.Object
            The sender object.
        e : System.Object.EventArgs
            The event arguments.

        Returns
        -------
        None

        """
        if sender.Text:
            self.trackbar.Value = int(sender.Text)

    def on_scroll(self, sender, e):
        """Callback for changes made with the slider.

        Parameters
        ----------
        sender : System.Object
            The sender object.
        e : System.Object.EventArgs
            The event arguments.

        Returns
        -------
        None

        """
        self.textbox.Text = str(sender.Value)
        sc.doc.Views.Redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import Rhino
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Plane
    from Rhino.Geometry import Circle
    from Rhino.Geometry import Cylinder

    from Rhino.Display import DisplayMaterial

    class Pipe(Rhino.Display.DisplayConduit):
        """"""

        def __init__(self, slider):
            super(Pipe, self).__init__()
            self.slider = slider
            self.base = Point3d(0, 0, 0)
            self.normal = Point3d(0, 0, 1) - self.base
            self.height = 30
            self.plane = Plane(self.base, self.normal)
            self.color = Color.FromArgb(255, 0, 0)
            self.material = DisplayMaterial(self.color)

        def DrawForeground(self, e):
            radius = self.slider.trackbar.Value
            circle = Circle(self.plane, radius)
            cylinder = Cylinder(circle, self.height)
            brep = cylinder.ToBrep(True, True)
            e.Display.DrawBrepShaded(brep, self.material)

    try:
        slider = SliderForm(0, 10, 1, 3)
        pipe = Pipe(slider)
        pipe.Enabled = True
        sc.doc.Views.Redraw()
        slider.show()

    except Exception as e:
        print(e)

    finally:
        pipe.Enabled = False
        del pipe
