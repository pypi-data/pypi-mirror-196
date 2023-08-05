"""Custom widgets dedicated to the reclassification  table interface."""

from colorsys import rgb_to_hls, rgb_to_hsv
from pathlib import Path
from typing import Optional, Union

import ipyvuetify as v
import pandas as pd
from matplotlib.colors import to_rgb
from traitlets import Int
from typing_extensions import Self

from sepal_ui import sepalwidgets as sw
from sepal_ui.message import ms
from sepal_ui.reclassify import parameters as param
from sepal_ui.scripts import decorator as sd
from sepal_ui.scripts import utils as su

__all__ = ["TableView"]


class ClassTable(sw.DataTable):

    SCHEMA = param.SCHEMA

    def __init__(
        self, out_path: Union[str, Path] = Path.home() / "downloads", **kwargs
    ) -> None:
        """Custom data table to modify, display and save classification.

        From this interface, a user can modify a classification starting from a scratch or by loading a classification file. the display datatable allow all the CRUD fonctionality (create, read, update, delete).

        Args:
            out_path: output path where table will be saved, default to ~/downloads/
        """
        # save the output path
        self.out_path = Path(out_path)

        # create the dialogs
        self.save_dialog = SaveDialog(
            table=self, out_path=self.out_path, transition=False
        )
        self.edit_dialog = EditDialog(table=self)

        # create the 4 CRUD btn
        # and set them in the top slot of the table
        self.edit_btn = sw.Btn(
            msg=ms.rec.table.btn.edit,
            gliph="fa-solid fa-pencil-alt",
            class_="ml-2 mr-2",
            color="secondary",
            small=True,
        )
        self.delete_btn = sw.Btn(
            msg=ms.rec.table.btn.delete,
            gliph="fa-solid fa-trash-alt",
            color="error",
            small=True,
        )
        self.add_btn = sw.Btn(
            msg=ms.rec.table.btn.add,
            gliph="fa-solid fa-plus",
            color="success",
            small=True,
        )
        self.save_btn = sw.Btn(
            msg=ms.rec.table.btn.save, gliph="fa-regular fa-save", small=True
        )

        slot = v.Toolbar(
            class_="d-flex mb-6",
            flat=True,
            children=[
                self.edit_dialog,
                self.save_dialog,
                v.ToolbarTitle(children=["Actions"]),
                v.Divider(class_="mx-4", inset=True, vertical=True),
                v.Flex(
                    class_="ml-auto",
                    children=[self.add_btn, self.edit_btn, self.delete_btn],
                ),
                v.Divider(class_="mx-4", inset=True, vertical=True),
                self.save_btn,
            ],
        )

        self.v_slots = [{"name": "top", "variable": "top", "children": [slot]}]

        # set up default parameters of the datatable
        self.v_model = []
        self.items = []
        self.item_key = "id"
        self.show_select = True
        self.single_select = True
        self.hide_default_footer = True
        self.headers = [
            {"text": v[0].capitalize(), "value": t} for t, v in self.SCHEMA.items()
        ]

        # create the object
        super().__init__(**kwargs)

        # js events
        self.edit_btn.on_event("click", self._edit_event)
        self.delete_btn.on_event("click", self._remove_event)
        self.add_btn.on_event("click", self._add_event)
        self.save_btn.on_event("click", self._save_event)

    def populate_table(self, items_file: Union[Path, str] = "") -> Self:
        """Populate table.

        It will fill the table with the item contained in the items_file parameter. If no file is provided the table is reset.

        Args:
            items: file containing classes and description
        """
        # If there is not any file passed as an argument, populate and empy table
        if not items_file:
            self.items = []
            return self

        # if there is, retrieve the content of the file to populate the table
        df = pd.read_csv(items_file, header=None)

        # TODO: We can check if the input file has header names, and if so, extract the
        # corresponding values with the SCHEMA.

        # small sanity check
        if len(df.columns) not in [2, 3]:
            raise AssertionError(
                f"The file is not a valid classification file as it has {len(df.columns)} columns instead of 2 or 3"
            )

        # add a color column if necessary
        if len(df.columns) == 2:
            df[2] = ["#000000"] * len(df)

        # TODO: Warning, here we are asumming that the values are in the same order as the schema keys
        # set the lines
        self.items = [
            dict(zip(self.SCHEMA.keys(), [i] + row.tolist()))
            for i, row in df.iterrows()
        ]

        return self

    def _save_event(self, *args) -> None:
        """open the save dialog to save the current table in a specific formatted table."""
        if not self.items:
            return

        self.save_dialog.v_model = True

        return

    def _edit_event(self, *args) -> None:
        """Open the edit dialog and fill it with current line information."""
        if not self.v_model:
            return

        self.edit_dialog.update([v for v in self.v_model[0].values()])

        return

    def _add_event(self, *args) -> None:
        """Open the edit dialog to create a new line to the table."""
        self.edit_dialog.update()

        return

    def _remove_event(self, *args) -> None:
        """Remove current selection (self.v_model) element from table."""
        if not self.v_model:
            return

        current_items = self.items.copy()
        current_items.remove(self.v_model[0])

        self.items = current_items

        return


class EditDialog(v.Dialog):

    TITLES = ms.rec.table.edit_dialog.titles

    def __init__(self, table: ClassTable, **kwargs) -> None:
        """Dialog to modify/create new elements from the ClassTable data_table.

        Args:
            table: Table linked with dialog
        """
        # custom attributes
        self.table = table

        # set the title
        self.title = v.CardTitle(children=[self.TITLES[0]])

        # Action buttons
        self.save = sw.Btn(msg=ms.rec.table.edit_dialog.btn.save.name)
        save_tool = sw.Tooltip(
            self.save, ms.rec.table.edit_dialog.btn.save.tooltip, bottom=True
        )

        self.modify = sw.Btn(msg=ms.rec.table.edit_dialog.btn.modify.name)
        self.modify.hide()  # by default modify is hidden
        modify_tool = sw.Tooltip(
            self.modify, ms.rec.table.edit_dialog.btn.modify.tooltip, bottom=True
        )

        self.cancel = sw.Btn(
            msg=ms.rec.table.edit_dialog.btn.cancel.name, outlined=True, class_="ml-2"
        )
        cancel_tool = sw.Tooltip(
            self.cancel, ms.rec.table.edit_dialog.btn.cancel.tooltip, bottom=True
        )

        actions = v.CardActions(children=[save_tool, modify_tool, cancel_tool])

        # create the widgets
        self.widgets = [
            v.TextField(label=val[0], type=val[1], v_model=None, _metadata={"name": k})
            for k, val in param.SCHEMA.items()
            if k in ["id", "code", "desc"]
        ] + [
            v.ColorPicker(
                label=param.SCHEMA["color"][0],
                mode=param.SCHEMA["color"][1],
                _metadata={"name": "color"},
                v_model=None,
            )
        ]

        self.widgets[0].disabled = True  # it's the id

        # some default params
        self.v_model = False
        self.max_width = 500
        self.overlay_opcity = 0.7

        # create the object
        super().__init__(**kwargs)

        # add the widget to the dialog
        self.children = [
            v.Card(class_="pa-4", children=[self.title] + self.widgets + [actions])
        ]

        # Create events
        self.save.on_event("click", self._save)
        self.modify.on_event("click", self._modify)
        self.cancel.on_event("click", self._cancel)

    def update(self, data: list = [None, None, None, None]) -> Self:
        """Upadte the dialog with the provided information and activate it.

        Args:
            data: the text value of the selected line (id, code, description, color). default to 4 None (new line)
        """
        # change the title accodring to the presence of data
        self.title.children = [self.TITLES[not any(data)]]

        # change the btns visiblity
        if not any(data):
            self.save.show()
            self.modify.hide()
        else:
            self.save.hide()
            self.modify.show()

        # change the content
        for i, item in enumerate(zip(self.widgets, data)):

            widget, val = item

            # textfield can be filled directly
            if i != 3:
                widget.v_model = val

            # the color picker need to be set in every color format to work
            else:

                # default to red if no value is provided
                val = val if val else "#FF0000"

                rgb = [int(i * 255) for i in to_rgb(val)]
                hls = rgb_to_hls(*to_rgb(val))
                hsv = rgb_to_hsv(*to_rgb(val))

                # rebuild all the colors from the hex code
                # the full v_model need to provided to see the color in the colorpicker
                widget.v_model = {
                    "alpha": 1,
                    "hex": val,
                    "hexa": f"{val}FF",
                    "hsla": {"h": hls[0], "s": hls[2], "l": hls[1], "a": 1},
                    "hsva": {"h": hsv[0], "s": hsv[1], "v": hsv[2], "a": 1},
                    "hue": hsv[0],
                    "rgba": {"r": rgb[0], "g": rgb[1], "b": rgb[2], "a": 1},
                }

        # if nothing is set I need to specify a new id value
        # this value should not interfere with the currently existing one. I'll thus just take the biggest +1
        if not any(data):
            self.widgets[0].v_model = (
                1
                if not self.table.items
                else max([i["id"] for i in self.table.items]) + 1
            )

        # activate the dialog
        self.v_model = True

        return self

    def _modify(self, *args) -> None:
        """Modify elements in the data_table and close the dialog."""
        # modify a local copy of the items
        # modifying does not trigger the display so a dummy element is also added
        # just to be removed afterward
        current_items = self.table.items.copy()
        for i, item in enumerate(current_items):
            if item["id"] == self.widgets[0].v_model:
                for w in self.widgets:
                    val = (
                        w.v_model
                        if w._metadata["name"] != "color"
                        else w.v_model["hex"]
                    )
                    current_items[i][w._metadata["name"]] = val

        current_items.append([""] * 4)

        # update the table values
        self.table.items = current_items

        # remove the dummy element to trigger the display
        self.table.items = self.table.items.copy()[:-1]

        # hide the dialog
        self.v_model = False

        # deselect the value for next time
        # if not deselected the previous item will remain in the v_model
        self.table.v_model = []

        return

    def _save(self, *args) -> None:
        """Add elements to the table and close the dialog."""
        # modify a local copy of the items
        current_items = self.table.items.copy()

        item_to_add = {}
        for w in self.widgets:
            item_to_add[w._metadata["name"]] = (
                w.v_model if w._metadata["name"] != "color" else w.v_model["hex"]
            )

        current_items.insert(0, item_to_add)

        # update the table values
        self.table.items = current_items

        # hide the dialog
        self.v_model = False

        return

    def _cancel(self, *args) -> None:
        """Close dialog and do nothing."""
        self.v_model = False

        return


class SaveDialog(v.Dialog):

    reload = Int(0).tag(sync=True)
    "a traitlet to inform the rest of the app that saving is complete"

    def __init__(self, table: ClassTable, out_path: Union[str, Path], **kwargs) -> None:
        """Dialog to save as .csv file the content of a ClassTable data table.

        Args:
            table: Table linked with dialog
            out_path: Folder path to store table content
        """
        # gather the table and saving params
        self.table = table
        self.out_path = out_path

        # set some default parameters
        self.max_width = 500
        self.v_model = False

        # create the widget
        super().__init__(**kwargs)

        # build widgets
        self.w_file_name = v.TextField(
            label=ms.rec.table.save_dialog.filename,
            v_model=ms.rec.table.save_dialog.placeholder,
        )

        self.save = sw.Btn(msg=ms.rec.table.save_dialog.btn.save.name)
        save = sw.Tooltip(
            self.save,
            ms.rec.table.save_dialog.btn.save.tooltip,
            bottom=True,
            class_="pr-2",
        )

        self.cancel = sw.Btn(
            msg=ms.rec.table.save_dialog.btn.cancel.name, outlined=True, class_="ml-2"
        )
        cancel = sw.Tooltip(
            self.cancel, ms.rec.table.save_dialog.btn.cancel.tooltip, bottom=True
        )

        self.alert = sw.Alert(children=["Choose a name for the output"]).show()

        # assemlble the layout
        self.children = [
            v.Card(
                class_="pa-4",
                children=[
                    v.CardTitle(children=[ms.rec.table.save_dialog.title]),
                    self.w_file_name,
                    self.alert,
                    save,
                    cancel,
                ],
            )
        ]

        # Create events
        self.save.on_event("click", self._save)
        self.cancel.on_event("click", self._cancel)
        self.w_file_name.on_event("blur", self._normalize_name)
        self.w_file_name.observe(self._store_info, "v_model")

    def _store_info(self, change: dict) -> None:
        """Display where will be the file written."""
        new_val = change["new"]
        out_file = self.out_path / f"{su.normalize_str(new_val)}.csv"

        msg = f"Your file will be saved as: {out_file}"

        if not new_val:
            msg = "Choose a name for the output"

        self.alert.add_msg(msg)

        return

    def show(self) -> Self:
        """Display the dialog and write down the text in the alert."""
        self.v_model = True
        self.w_file_name.v_model = ""

        # the message is display after the show so that it's not cut by the display
        self.alert.add_msg(ms.rec.table.save_dialog.info.format(self.out_path))

        return self

    def _normalize_name(self, widget: v.VuetifyWidget, *args) -> None:
        """Replace the name with it's normalized version."""
        # normalized the name
        widget.v_model = su.normalize_str(widget.v_model)

        return

    def _save(self, *args) -> None:
        """Write current table on a text file."""
        # set the file name
        out_file = self.out_path / su.normalize_str(self.w_file_name.v_model)

        # write each line values but not the id
        lines = [list(item.values())[1:] for item in self.table.items]
        txt = [",".join(str(e) for e in ln) + "\n" for ln in lines]
        out_file.with_suffix(".csv").write_text("".join(txt))

        # Every time a file is saved, we update the current widget state
        # so it can be observed by other objects.
        self.reload += 1

        self.v_model = False

        return

    def _cancel(self, *args) -> None:
        """Hide the widget and do nothing."""
        self.v_model = False

        return


class TableView(sw.Card):

    title: Optional[v.CardTitle] = None
    "v.CardTitle: the title of the card"

    class_path: str = ""
    "str: Folder path containing already existing classes"

    out_path: str = ""
    "str: the folder to save the created classifications"

    w_class_file: Optional[sw.FileInput] = None
    "sw.FileInput: the file input of the existing classification system"

    w_class_table: Optional[ClassTable] = None
    "ClassTable: the classtable (CRUD) to manage the editing of the classification"

    btn: Optional[sw.Btn] = None
    "sw.Btn: the btn to start loading file data into the table"

    alert: Optional[sw.Alert] = None
    "sw.Alert: the alert to display loading information (error and success)"

    def __init__(
        self,
        class_path: Union[str, Path] = Path.home(),
        out_path: Union[str, Path] = Path.home() / "downloads",
        **kwargs,
    ):
        r"""Stand-alone Card object allowing the user to build custom class table.

        The user can start from an existing table or start from scratch. It gives the oportunity to change: the value, the class name and the color. It can be used as a tile in a sepal_ui app. The id\_ of the tile is set to "classification_tile".

        Args:
            class_path: Folder path containing already existing classes. Default to ~/
            out_path: the folder to save the created classifications. default to ~/downloads
        """
        # create metadata to make it compatible with the framwork app system
        self._metadata = {"mount_id": "reclassify_tile"}

        # set some default params
        self.class_ = "pa-5"

        # init the card
        super().__init__(**kwargs)

        # set the folders
        self.class_path = Path(class_path)
        self.out_path = Path(out_path)

        # set a title to the card
        self.title = v.CardTitle(
            children=[v.Html(tag="h2", children=[ms.rec.table.title])]
        )

        # add the widgets
        w_class_title = v.Html(
            tag="h3", children=[ms.rec.table.classif.title], class_="mt-2"
        )
        self.w_class_file = sw.FileInput(
            extentions=[".csv"],
            label=ms.rec.table.classif.file_select,
            folder=self.class_path,
        )
        self.btn = sw.Btn(
            msg=ms.rec.table.classif.btn,
            gliph="far fa-table",
            color="success",
            outlined=True,
        )
        w_panels = v.ExpansionPanels(
            children=[
                v.ExpansionPanel(
                    children=[
                        v.ExpansionPanelHeader(children=[w_class_title]),
                        v.ExpansionPanelContent(children=[self.w_class_file, self.btn]),
                    ]
                )
            ]
        )

        w_table_title = v.Html(tag="h2", children=[ms.rec.table.table], class_="mt-5")
        self.w_class_table = ClassTable(out_path=self.out_path, class_="mt-5")

        # create an alert to display error and outputs
        self.alert = sw.Alert()

        # assemble a layout
        self.children = [
            self.title,
            w_panels,
            self.alert,
            w_table_title,
            self.w_class_table,
        ]

        # Events
        self.btn.on_event("click", self.get_class_table)

    @sd.loading_button(debug=True)
    def get_class_table(self, *args) -> Self:
        """Display class table widget in view."""
        # load the existing file into the table
        self.w_class_table.populate_table(self.w_class_file.v_model)

        return self

    def nest_tile(self) -> Self:
        """Prepare the view to be used as a nested component in a tile.

        The elevation will be set to 0 and the title remove from children.
        The mount_id will also be changed to nested.
        """
        # remove id
        self._metadata["mount_id"] = "nested_tile"

        # remove elevation
        self.elevation = False

        # remove title
        without_title = self.children.copy()
        without_title.remove(self.title)
        self.children = without_title

        return self
