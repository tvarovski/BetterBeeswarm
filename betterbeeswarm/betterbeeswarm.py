from seaborn.categorical import Beeswarm as OriginalBeeswarm
from seaborn.categorical import _get_transform_functions
import warnings
import numpy as np

class Beeswarm(OriginalBeeswarm):
    """Modifies a scatterplot artist to show a beeswarm plot.
    This is a modification of the seaborn beeswarm plot that instead of
    stopping when points overlap and moving them to the gutter, it shrinks
    the points and tries again. This is done until the points no longer
    overlap.
    """
    def __init__(self, orient="x", width=0.8, warn_thresh=.05):

        self.orient = orient
        self.width = width
        self.warn_thresh = warn_thresh
        self.gutters = False #BetterBeeswarm modification
        self.shrink_factor = 0.9 #BetterBeeswarm modification

    def __call__(self, points, center):
        """Swarm `points`, a PathCollection, around the `center` position."""
        # Convert from point size (area) to diameter

        ax = points.axes
        dpi = ax.figure.dpi

        # Get the original positions of the points
        orig_xy_data = points.get_offsets()

        # Reset the categorical positions to the center line
        cat_idx = 1 if self.orient == "y" else 0
        orig_xy_data[:, cat_idx] = center

        # Transform the data coordinates to point coordinates.
        # We'll figure out the swarm positions in the latter
        # and then convert back to data coordinates and replot
        orig_x_data, orig_y_data = orig_xy_data.T
        orig_xy = ax.transData.transform(orig_xy_data)

        # Order the variables so that x is the categorical axis
        if self.orient == "y":
            orig_xy = orig_xy[:, [1, 0]]

        # Add a column with each point's radius
        sizes = points.get_sizes()
        if sizes.size == 1:
            sizes = np.repeat(sizes, orig_xy.shape[0])
        edge = points.get_linewidth().item()
        radii = (np.sqrt(sizes) + edge) / 2 * (dpi / 72)

        #BetterBeeswarm modified added while loop to check for gutters
        checking_gutters = True
        radius_shrink_factor = self.shrink_factor
        original_radius_fraction = 1.0
        orig_xy_copy = orig_xy.copy()

        while checking_gutters:

            orig_xy = np.c_[orig_xy_copy, radii] #BetterBeeswarm modified by changing orig_xy to orig_xy_copy

            # Sort along the value axis to facilitate the beeswarm
            sorter = np.argsort(orig_xy[:, 1])
            orig_xyr = orig_xy[sorter]

            # Adjust points along the categorical axis to prevent overlaps
            new_xyr = np.empty_like(orig_xyr)
            new_xyr[sorter] = self.beeswarm(orig_xyr)

            # Transform the point coordinates back to data coordinates
            if self.orient == "y":
                new_xy = new_xyr[:, [1, 0]]
            else:
                new_xy = new_xyr[:, :2]
            new_x_data, new_y_data = ax.transData.inverted().transform(new_xy).T

            # Add gutters
            t_fwd, t_inv = _get_transform_functions(ax, self.orient)
            if self.orient == "y":
                self.add_gutters(new_y_data, center, t_fwd, t_inv)
            else:
                self.add_gutters(new_x_data, center, t_fwd, t_inv)

            # Reposition the points so they do not overlap
            if self.orient == "y":
                points.set_offsets(np.c_[orig_x_data, new_y_data])
            else:
                points.set_offsets(np.c_[new_x_data, orig_y_data])

            # Check if gutters were added
            if self.gutters:
                # Shrink the radii and try again
                radii = radii * radius_shrink_factor
                original_radius_fraction = original_radius_fraction * radius_shrink_factor
                print(f"Shrinking radii to the {original_radius_fraction * 100}% of the original point size.")
            else:
                checking_gutters = False

    def add_gutters(self, points, center, trans_fwd, trans_inv):
        """Stop points from extending beyond their territory."""
        half_width = self.width / 2
        low_gutter = trans_inv(trans_fwd(center) - half_width)
        off_low = points < low_gutter
        if off_low.any():
            points[off_low] = low_gutter
        high_gutter = trans_inv(trans_fwd(center) + half_width)
        off_high = points > high_gutter
        if off_high.any():
            points[off_high] = high_gutter

        gutter_prop = (off_high + off_low).sum() / len(points)
        if gutter_prop > self.warn_thresh:
            msg = (
                "{:.1%} of the points cannot be placed; you may want "
                "to decrease the size of the markers or use stripplot."
                f"Using BetterBeeswarm to recursively shrink points by {(1 - self.shrink_factor) * 100:.1f}%"
            ).format(gutter_prop)
            warnings.warn(msg, UserWarning)
        
        #BetterBeeswarm modified
            self.gutters = True
        else:
            self.gutters = False
        #end BetterBeeswarm modification

        return points
