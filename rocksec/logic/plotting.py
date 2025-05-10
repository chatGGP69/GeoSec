
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

def advanced_plot_section(topography, contacts, rock_layers, rock_colors=None):
    if rock_colors is None:
        rock_colors = {
            "Limestone": "lightblue",
            "Shale": "lightgray",
            "Sandstone": "sandybrown",
            "Basalt": "black",
            "Conglomerate": "peru",
            "Default": "lightyellow"
        }

    if len(topography.points) < 2:
        return

    fig, ax = plt.subplots(figsize=(14, 7))

    # --- Surface Interpolation ---
    distances, elevations = topography.get_profile()
    points = sorted(zip(distances, elevations), key=lambda p: p[0])
    distances_sorted = np.array([p[0] for p in points])
    elevations_sorted = np.array([p[1] for p in points])

    x_surface = np.linspace(distances_sorted.min(), distances_sorted.max(), 1000)
    k_surface = min(3, len(distances_sorted) - 1)
    surface_spline = make_interp_spline(distances_sorted, elevations_sorted, k=k_surface)
    y_surface = surface_spline(x_surface)

    ax.plot(x_surface, y_surface, color="black", linewidth=2, label="Topography")

    # --- Contact Interpolations ---
    contact_curves = {}
    x_range = x_surface

    for contact in contacts:
        pts = contact.sorted_points()
        if len(pts) < 2:
            continue
        cx = np.array([p[0] for p in pts])
        cy = np.array([p[1] for p in pts])
        k = min(2, len(cx) - 1)
        contact_spline = make_interp_spline(cx, cy, k=k)
        contact_y = contact_spline(x_range)
        contact_curves[contact.name] = contact_y
        ax.plot(x_range, contact_y, linewidth=1, color="black")

    # --- Fill Between Layers ---
    for layer in rock_layers:
        top_name = layer.top_contact.name
        bottom_name = layer.bottom_contact.name
        color = rock_colors.get(layer.rock_type, rock_colors["Default"])

        top_y = contact_curves.get(top_name)
        bottom_y = contact_curves.get(bottom_name)

        if top_y is not None and bottom_y is not None:
            ax.fill_between(x_range, top_y, bottom_y, color=color, alpha=0.7)

    # --- Fill from surface to top contact if valid ---
    for layer in rock_layers:
        surface_cut = y_surface
        top_name = layer.top_contact.name
        top_y = contact_curves.get(top_name)
        if top_y is not None:
            color = rock_colors.get(layer.rock_type, rock_colors["Default"])
            ax.fill_between(x_range, surface_cut, top_y, color=color, alpha=0.7)
            break  # Only fill above the uppermost layer once

    # --- Fill below the lowest layer if desired ---
    bottom_contact_y = None
    last_color = None
    for layer in reversed(rock_layers):
        bottom_name = layer.bottom_contact.name
        bottom_y = contact_curves.get(bottom_name)
        if bottom_y is not None:
            bottom_contact_y = bottom_y
            last_color = rock_colors.get(layer.rock_type, rock_colors["Default"])
            break

    if bottom_contact_y is not None:
        y_bottom = np.full_like(x_range, bottom_contact_y.min() - 50)
        ax.fill_between(x_range, bottom_contact_y, y_bottom, color=last_color, alpha=0.5)

    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Elevation (m)")
    ax.legend()
    plt.tight_layout()
    plt.show()
