import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from ...plots import assert_shape, generate_mask_colors, plot_contour, plot_image
from ...utils import image_path_to_data_ax, mask_path_to_data_ax, path_in


def image_masks_path(
    image_path,
    masks_path,
    mask_colors=None,
    title_image="Image",
    titles=[],
    cmap="gray",
    origin="upper",
):
    image_path = path_in(image_path)
    image_data = image_path_to_data_ax(image_path)

    if len(masks_path) == 0:
        raise ValueError("masks_path must be a list of paths")
    masks_path = [path_in(path) for path in masks_path]
    masks_data = [mask_path_to_data_ax(path) for path in masks_path]

    image_masks_array(
        image_data,
        masks_data,
        mask_colors=mask_colors,
        title_image=title_image,
        titles=titles,
        cmap=cmap,
        origin=origin,
    )


def image_masks_array(
    image_data,
    masks_data,
    mask_colors=None,
    title_image="Image",
    titles=[],
    cmap="gray",
    origin="upper",
):
    print("Loading images...")

    if len(masks_data) == 0:
        raise ValueError("masks_data must be a list of arrays")

    num_masks = len(masks_data)

    init_slice, last_slice = assert_shape(image_data + masks_data)

    mask_colors = generate_mask_colors(num_masks, mask_colors)

    _, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    plot_image(ax, image_data[:, :, init_slice], cmap=cmap)

    for i in range(num_masks):
        plot_contour(
            ax,
            masks_data[i][:, :, init_slice],
            color=mask_colors[i],
            # origin=origin,
            levels=[0.5],
        )

    ax.set_xlabel(f"Slice Number: {init_slice}")
    ax.set_title("title")

    slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])

    slider = Slider(
        slider_ax,
        "Slice",
        0,
        last_slice,
        valinit=init_slice,
        valstep=1,
    )

    def update(val):
        slice_num = int(slider.val)
        ax.clear()

        plot_image(ax, image_data[:, :, slice_num], cmap="gray")
        for i in range(num_masks):
            plot_contour(ax, masks_data[i][:, :, slice_num], color=mask_colors[i])

        ax.set_xlabel(f"Slice Number: {slice_num}")
        ax.set_title("title")

    slider.on_changed(update)

    plt.show()
