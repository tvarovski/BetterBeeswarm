from seaborn.categorical import Beeswarm as OriginalBeeswarm
from seaborn.categorical import _CategoricalPlotter as OriginalCategoricalPlotter
from seaborn.categorical import _get_transform_functions
from seaborn.categorical import _categorical_docs
from seaborn.utils import _draw_figure
from seaborn.utils import _scatter_legend_artist
from seaborn.utils import _default_color
from matplotlib.markers import MarkerStyle
import warnings
import numpy as np
import matplotlib.pyplot as plt
from textwrap import dedent

class Beeswarm(OriginalBeeswarm):
    """Modifies a scatterplot artist to show a beeswarm plot.
    This is a modification of the seaborn beeswarm plot that instead of
    stopping when points overlap and moving them to the gutter, it shrinks
    the points and tries again. This is done until the points no longer
    overlap.
    """
    def __init__(self, orient="x", width=0.8, warn_thresh=.05, overflow="gutters"):

        self.orient = orient
        self.width = width
        self.warn_thresh = warn_thresh

        #BetterBeeswarm modifications
        self.gutters = False
        self.shrink_factor = 0.9
        self.overflow = overflow
        if overflow == "gutters":
            self.keep_gutters = True
        elif overflow in ["shrink", "random"]:
            self.keep_gutters = False
        else:
            raise ValueError("overflow must be 'gutters', 'shrink', or 'random'")

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

            # Add gutters or randomize points if they overflow
            t_fwd, t_inv = _get_transform_functions(ax, self.orient)

            if self.overflow == "random":

                if self.orient == "y":
                    self.add_randomly(new_y_data, center, t_fwd, t_inv)
                else:
                    self.add_randomly(new_x_data, center, t_fwd, t_inv)
                checking_gutters = False

            elif self.overflow in ["gutters", "shrink"]:

                if self.orient == "y":
                    self.add_gutters(new_y_data, center, t_fwd, t_inv)
                else:
                    self.add_gutters(new_x_data, center, t_fwd, t_inv)

                if self.overflow == "gutters":
                    checking_gutters = False

                elif self.overflow == "shrink":
                    # Check if there were gutters added
                    if self.gutters == True:
                        # if so, shrink the radii and try again
                        radii = radii * radius_shrink_factor
                        original_radius_fraction = original_radius_fraction * radius_shrink_factor
                        print(f"Shrinking radii to the {original_radius_fraction * 100}% of the original point size.")
                    else:
                        checking_gutters = False

        # Reposition the points so they do not overlap
        if self.orient == "y":
            points.set_offsets(np.c_[orig_x_data, new_y_data])
        else:
            points.set_offsets(np.c_[new_x_data, orig_y_data])

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
                "{:.1%} of the points cannot be placed as swarm; you may want to decrease"
                " the size of the markers, use stripplot, or set overflow='shrink'."
            ).format(gutter_prop)
            warnings.warn(msg, UserWarning)
        
        #BetterBeeswarm modified
        if gutter_prop > 0:
            self.gutters = True
        else:
            self.gutters = False
        #end BetterBeeswarm modification

        return points
    
    def add_randomly(self, points, center, trans_fwd, trans_inv):
        """Randomly place points within the width of the bounds."""
        half_width = self.width / 2
        low_bound = trans_inv(trans_fwd(center) - half_width)
        high_bound = trans_inv(trans_fwd(center) + half_width)

        off_low = points < low_bound
        off_high = points > high_bound

        if off_low.any() or off_high.any():
            points[off_low] = np.random.uniform(low_bound, high_bound, size=off_low.sum())
            points[off_high] = np.random.uniform(low_bound, high_bound, size=off_high.sum())

        gutter_prop = (off_high + off_low).sum() / len(points)
        if gutter_prop > self.warn_thresh:
            msg = (
                "{:.1%} of the points cannot be placed as swarm; you may want to decrease"
                " the size of the markers, use stripplot, or set overflow='shrink'."
            ).format(gutter_prop)
            warnings.warn(msg, UserWarning)

class _CategoricalPlotter(OriginalCategoricalPlotter):
    def plot_swarms(
        self,
        dodge,
        color,
        warn_thresh,
        plot_kws,
    ):

        width = .8 * self._native_width
        offsets = self._nested_offsets(width, dodge)

        iter_vars = [self.orient]
        if dodge:
            iter_vars.append("hue")

        ax = self.ax
        point_collections = {}
        dodge_move = 0

        if "marker" in plot_kws and not MarkerStyle(plot_kws["marker"]).is_filled():
            plot_kws.pop("edgecolor", None)

        if "overflow" in plot_kws:
            overflow = plot_kws.pop("overflow")
        else:
            overflow = "gutters"

        for sub_vars, sub_data in self.iter_data(iter_vars,
                                                 from_comp_data=True,
                                                 allow_empty=True):

            ax = self._get_axes(sub_vars)

            if offsets is not None:
                dodge_move = offsets[sub_data["hue"].map(self._hue_map.levels.index)]

            if not sub_data.empty:
                sub_data[self.orient] = sub_data[self.orient] + dodge_move

            self._invert_scale(ax, sub_data)

            points = ax.scatter(sub_data["x"], sub_data["y"], color=color, **plot_kws)
            if "hue" in self.variables:
                points.set_facecolors(self._hue_map(sub_data["hue"]))

            if not sub_data.empty:
                point_collections[(ax, sub_data[self.orient].iloc[0])] = points

        beeswarm = Beeswarm(width=width, orient=self.orient, warn_thresh=warn_thresh, overflow=overflow)
        for (ax, center), points in point_collections.items():
            if points.get_offsets().shape[0] > 1:

                def draw(points, renderer, *, center=center):

                    beeswarm(points, center)

                    if self.orient == "y":
                        scalex = False
                        scaley = ax.get_autoscaley_on()
                    else:
                        scalex = ax.get_autoscalex_on()
                        scaley = False

                    # This prevents us from undoing the nice categorical axis limits
                    # set in _adjust_cat_axis, because that method currently leave
                    # the autoscale flag in its original setting. It may be better
                    # to disable autoscaling there to avoid needing to do this.
                    fixed_scale = self.var_types[self.orient] == "categorical"
                    ax.update_datalim(points.get_datalim(ax.transData))
                    if not fixed_scale and (scalex or scaley):
                        ax.autoscale_view(scalex=scalex, scaley=scaley)

                    super(points.__class__, points).draw(renderer)

                points.draw = draw.__get__(points)

        _draw_figure(ax.figure)
        self._configure_legend(ax, _scatter_legend_artist, plot_kws)


def swarmplot(
    data=None, *, x=None, y=None, hue=None, order=None, hue_order=None,
    dodge=False, orient=None, color=None, palette=None,
    size=5, edgecolor=None, linewidth=0, hue_norm=None, log_scale=None,
    native_scale=False, formatter=None, legend="auto", warn_thresh=.05,
    ax=None, **kwargs
):

    p = _CategoricalPlotter(
        data=data,
        variables=dict(x=x, y=y, hue=hue),
        order=order,
        orient=orient,
        color=color,
        legend=legend,
    )

    if ax is None:
        ax = plt.gca()

    if p.plot_data.empty:
        return ax

    if p.var_types.get(p.orient) == "categorical" or not native_scale:
        p.scale_categorical(p.orient, order=order, formatter=formatter)

    p._attach(ax, log_scale=log_scale)

    if not p.has_xy_data:
        return ax

    # Deprecations to remove in v0.14.0.
    hue_order = p._palette_without_hue_backcompat(palette, hue_order)
    palette, hue_order = p._hue_backcompat(color, palette, hue_order)

    p.map_hue(palette=palette, order=hue_order, norm=hue_norm)

    #save overflow kwarg
    overflow = kwargs.pop("overflow", "gutters")

    color = _default_color(ax.scatter, hue, color, kwargs)

    kwargs["overflow"] = overflow

    edgecolor = p._complement_color(edgecolor, color, p._hue_map)

    kwargs.setdefault("zorder", 3)
    size = kwargs.get("s", size)

    if linewidth is None:
        linewidth = size / 10

    kwargs.update(dict(
        s=size ** 2,
        edgecolor=edgecolor,
        linewidth=linewidth,
    ))

    p.plot_swarms(
        dodge=dodge,
        color=color,
        warn_thresh=warn_thresh,
        plot_kws=kwargs,
    )

    p._add_axis_labels(ax)
    p._adjust_cat_axis(ax, axis=p.orient)

    return ax


swarmplot.__doc__ = dedent("""\
    Draw a categorical scatterplot with points adjusted to be non-overlapping.

    This function is similar to :func:`stripplot`, but the points are adjusted
    (only along the categorical axis) so that they don't overlap. This gives a
    better representation of the distribution of values, but it does not scale
    well to large numbers of observations. This style of plot is sometimes
    called a "beeswarm".

    A swarm plot can be drawn on its own, but it is also a good complement
    to a box or violin plot in cases where you want to show all observations
    along with some representation of the underlying distribution.

    {categorical_narrative}

    Parameters
    ----------
    {categorical_data}
    {input_params}
    {order_vars}
    dodge : bool
        When a `hue` variable is assigned, setting this to `True` will
        separate the swaarms for different hue levels along the categorical
        axis and narrow the amount of space allotedto each strip. Otherwise,
        the points for each level will be plotted in the same swarm.
    {orient}
    {color}
    {palette}
    size : float
        Radius of the markers, in points.
    edgecolor : matplotlib color, "gray" is special-cased
        Color of the lines around each point. If you pass `"gray"`, the
        brightness is determined by the color palette used for the body
        of the points.
    {linewidth}
    {log_scale}
    {native_scale}
    {formatter}
    {legend}
    {ax_in}
    kwargs : key, value mappings
        Other keyword arguments are passed through to
        :meth:`matplotlib.axes.Axes.scatter`.

    Returns
    -------
    {ax_out}

    See Also
    --------
    {boxplot}
    {violinplot}
    {stripplot}
    {catplot}

    Examples
    --------
    .. include:: ../docstrings/swarmplot.rst

    """).format(**_categorical_docs)

import seaborn as sns
sns.categorical.Beeswarm = Beeswarm
sns.categorical._CategoricalPlotter = _CategoricalPlotter
sns.swarmplot = swarmplot